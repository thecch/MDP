import os, sys
import glob
import time
import numpy as np
import pandas as pd
import cv2
import onnxruntime
from cvu.detector.yolov5 import Yolov5 as Yolov5Onnx
from pathlib import Path
from shapely.geometry import Polygon

COLAB_MODE = False
THRESHOLD = 0.5
_file_ = '/content/MDP/ObjectDetection/onnx_predictor.py' if COLAB_MODE else '/home/pi/ObjectDetection/onnx_predictor.py'
BASE_PATH = os.path.split(os.path.realpath(_file_))[0]

class_map = pd.read_csv(BASE_PATH + '/class_map.csv')
#class_list = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
class_list = [16, 18, 21, 22, 23, 28]

models = []
MODEL_DICT = dict()
for model_path in glob.glob(BASE_PATH + '/models/*.onnx'):
  model_name = model_path.split('/')[-1][8:12]
  models.append(model_name)
  MODEL_DICT[model_name] = Yolov5Onnx(
    classes = class_map[model_name].sort_values().astype('str').to_list(), backend = "onnx",
    weight = '{}/models/{}'.format(BASE_PATH, model_path.split('/')[-1]), device = 'cpu'
  )

def get_preds(image_path):
  
  preds_list = []
  for (model_name, model) in MODEL_DICT.items():
    image = cv2.imread(image_path)
    image = cv2.resize(image, (640, 640))
    cur_output_path = image_path.split(os.sep)
    cur_output_path[-2] = 'output'
    cur_output_path[-1] = model_name + '_' + cur_output_path[-1]
    cur_output_path = '/'.join(cur_output_path)

    preds = model(image)
    preds.draw(image)
    cv2.imwrite(cur_output_path, image)
    preds_list.append([model_name, preds])
  
  orignal_image = cv2.imread(image_path)
  orignal_image = cv2.resize(orignal_image, (640, 640))
  output_path = image_path.split(os.sep)
  output_path[-2] = 'output'
  output_path[-1] = 'combined_' + output_path[-1]
  output_path = '/'.join(output_path)

  for model_preds in preds_list:
    model_preds[1].draw(orignal_image)
  cv2.imwrite(output_path, orignal_image)

  return preds_list

def process_pred(model_name, pred):
  return {
    'model': model_name,
    'bbox': pred.bbox,
    'conf': pred.confidence,
    'id': class_map[class_map[model_name].astype('str') == str(pred.class_name)].iloc[0].id
  }
  
def process_rows(df_row):
  df_row['model1'], df_row['model2'] = sorted([str(df_row.model_x), str(df_row.model_y)])
  df_row['conf1'], df_row['conf2'] = sorted([float(df_row.conf_x), float(df_row.conf_y)])
  df_row['bbox1'], df_row['bbox2'] = df_row.bbox_x, df_row.bbox_y
  df_row['weight1'] = 1 if df_row.model_x == 'main' else 0.75
  df_row['weight2'] = 1 if df_row.model_y == 'main' else 0.75
  return df_row[['id', 'model1', 'model2', 'conf1', 'conf2', 'bbox1', 'bbox2', 'weight1', 'weight2']]

def calc_score(df_row):
  x1, y1, x2, y2 = df_row.bbox1
  box1 = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
  x1, y1, x2, y2 = df_row.bbox2
  box2 = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
  df_row['score'] = (float(df_row.conf1) * df_row.weight1 * box1.intersection(box2).area / box1.area) + (float(df_row.conf2) * df_row.weight2 * box1.intersection(box2).area / box2.area)
  df_row['score'] += (float(df_row.conf1) * df_row.weight1) + (float(df_row.conf2) * df_row.weight2)
  return df_row[['id', 'model1', 'model2', 'score']]
  
def detect_image(image_path):
  preds_list = [[process_pred(model_name, pred) for pred in preds] for (model_name, preds) in get_preds(image_path)]
  df = pd.DataFrame([item for sublist in preds_list for item in sublist])
  print(df)

  if len(df) == 0:
    return 0
  else:
    df = df[df['id'].astype('int').isin(class_list)]
    df = df[['model', 'bbox', 'conf', 'id']]
    if len(df) == 0:
      return 0
    crossed_df = pd.concat([df[df.model == model_name].merge(df[df.model != model_name], how = 'outer', on = "id") for model_name in models])
    crossed_df = crossed_df.apply(lambda x: process_rows(x), axis = 1).reset_index(drop = True)
    crossed_df = crossed_df.iloc[crossed_df[['id', 'model1', 'model2', 'conf1', 'conf2']].drop_duplicates().index.to_list()].dropna()
    print(crossed_df)
    if len(crossed_df) == 0:
      df = df[df.conf > 0.6]
      return df.sort_values('conf', ascending = False)['id'].iloc[0]
    else:
      crossed_df = crossed_df.apply(lambda x: calc_score(x), axis = 1)
      crossed_df = crossed_df.sort_values(['id', 'model1', 'model2', 'score'], ascending = False).groupby(['id', 'model1', 'model2']).head(1).reset_index(drop = True)
      print(crossed_df)
      return crossed_df.groupby('id').sum().reset_index(drop = False).sort_values('score', ascending = False)['id'].iloc[0]

# detect_image('/content/yolov5/MDPv2-1/test/images/Alpha-S---0034_jpg.rf.592ecad7ee2089f1076cd37c8ad676f0.jpg')
# detect_image('/content/yolov5/MDPv2-1/test/images/AlphabetT_light0012_jpg.rf.564c96525f878c1a68c836d1d2b53757.jpg')