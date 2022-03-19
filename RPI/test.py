import sys, os
from xml.etree.ElementTree import PI
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ObjectDetection.onnx_predictor import *

os.system("libcamera-still -o /home/pi/image.jpg --width 640 \
                    --height 640 --brightness -0.05 --immediate -n \
                    --camera 0 --verbose 0")
print("Image Rec taking place...")
results = detect_image("/home/pi/image.jpg")
print(results)