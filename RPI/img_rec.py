from picamera import PiCamera
from sendtopc import *

camera = PiCamera()
print("Taking photo...")
camera.capture('/home/pi/Desktop/image.jpg')

sendImgToPC()