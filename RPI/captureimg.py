import time
import os
from xml.etree.ElementTree import PI

# for i in range(10):
#     print("Taking photo")
#     os.system("libcamera-still -o /home/pi/images/AlphabetT{0:04d}.jpg --width 640 \
#                     --height 640 --immediate -n \
#                     --camera 0 --verbose 0".format(i))
#     time.sleep(2)

for i in range(100):
    inp = input()
    if inp ==" ":
        os.system("libcamera-still -o /home/pi/images/AlphabetT{0:04d}.jpg --width 640 \
                            --height 640 --immediate -n \
                            --camera 0 --verbose 0".format(i))