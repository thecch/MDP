import os, time, sys
import threading
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from android import *
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ObjectDetection.onnx_predictor import *

all_results = []

class ImageHandler(watchdog.events.PatternMatchingEventHandler):
  def __init__(self):
    watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg'],
                                                             ignore_directories=True, case_sensitive=False)
    #self.obstacle_id = obstacle_id
    #self.thread = thread
    self.occured = False
    self.pred_class = ""

  def on_created(self, event):
    print("Image Rec in process...")
    self.occured = False
    # event_type, src_path, is_dir = event.key

    # if not is_dir:
    #   size = os.path.getsize(event.src_path)
    #   while True:
    #     size_prev, size = size, os.path.getsize(event.src_path)
    #     if size == size_prev:
    #         break

    try:
      self.pred_class = detect_image(image_path = event.src_path)
      self.occured = True
      all_results.append(self.pred_class)
      print("Predicted Class:", self.pred_class)

    except Exception as e:
      print("Image not detected")
      print("Error:", e)


# class ImageHandler(FileSystemEventHandler):
#   def __init__(self, thread, config = None, log = None):
#     self.thread = thread
#     self.log, self.config = log, config

#   def on_created(self, event):
#     file = os.path.basename(event.src_path)
#     print(event)
#     ext = os.path.splitext(event.src_path)[1]
#     event_type, src_path, is_dir = event.key

#     if not is_dir and ext in ['.jpg', '.JPG']:
#       size = os.path.getsize(event.src_path)
#       while True:
#         size_prev, size = size, os.path.getsize(event.src_path)
#         if size == size_prev:
#             break

#       results = detect_image(image_path = event.src_path)
#       print(results)
#       try:
#         obstacle_id = os.path.splitext(src_path)[0].split('/')[-1][-1]
#         pred_class = results[0].class_name
#         print("Predicted Class:", pred_class)
#         print("TARGET, {}, {}".format(str(obstacle_id), str(pred_class)))

#         # self.thread.writeAndroid("TARGET,{},{}".format(str(obstacle_id), str(pred_class)))
#         print("TARGET,{},{}".format(str(obstacle_id), str(pred_class)))
#       except Exception as e:
#         print("Image not detected")
#         print("Error:", e)