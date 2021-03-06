import sys, os
import glob
from datetime import datetime
from multithreading2 import *


if __name__ == "__main__":

    # Starting main program
    # print("Remove existing images")
    # dt = datetime.strftime(datetime.now(), '%H%M')
    # os.system("mkdir /home/pi/{}".format(dt))
    # os.system("mv /home/pi/output/*jpg /home/pi/{}".format(dt))
    # os.system("mv /home/pi/images/*jpg /home/pi/{}".format(dt))
    print("Starting Program...")
    rpi = Multithreading()

    try:
        print("Starting threads")
        
        rpi.multithread()       
        rpi.keep_main_alive()

    except KeyboardInterrupt:
        print("Exiting the program")
        rpi.disconnectAll()