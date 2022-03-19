import time
import threading
import os, sys, glob
from xml.etree.ElementTree import PI
from android import *
from stm import *
from config import *
from pc import *
import cv2

from watchdog.observers import Observer
#from ultrasonic import *
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ObjectDetection.onnx_predictor import *
from Image import *
import Algorithm 

order = []


class Multithreading():

    def __init__(self):
        # Time Limit
        self.timeLimit = 6*60 #time limit of 6 minutes

        # Instantiate all classes
        self.androidThread = AndroidInterface()
        self.stmThread = STMInterface()
        #self.pcThread = PCinterface()
        self.imageThread = Observer()
        #self.handlers = { 'imageHandler': ImageHandler(self) }
        self.handlers = ImageHandler()
        self.events = {}
        self.sent = 0
        self.finished = 0

        # Initialise connections to all interfaces
        self.androidThread.androidConnection(UUID)
        self.stmThread.stmConnection()
        #self.pcThread.pcConnection()
        print("Connected to STM and Android and PC")

        # Delay for buffer set
        time.sleep(0.5)
        print("Beginning Transmission...")


    #function to update elapsed time and check if time limit is met
    def updateTime(self):
        self.elapsedTime = time.time() - self.startTime
        #print(str(elapsedTime))
        return (1 if self.elapsedTime >= self.timeLimit else 0)

    # Function to read from Android via Bluetooth
    def readAndroid(self):
        while True:
            androidMsg = self.androidThread.readFromAndroid()
            androidMsg = str(androidMsg)
            try:
                # Split the string using delimiter ":"
                # Using first index as header to differentiate user input for interface
                self.msgFromBT = androidMsg.split(":")
                header = (self.msgFromBT[0])

                # If Android Connection is Established and Message is present
                if self.androidThread.checkConnection() and androidMsg != "None":
                    # Sending Message from Android to STM
                    if header == 'STM':
                        self.writeSTM(self.msgFromBT[1].strip())
                    # Sending Message from Android to RPI
                    elif header == 'RPI':
                        self.algo = Algorithm.Algorithm([1,18],0) 
                        self.readAlgo(self.msgFromBT[1])                 
                    else:
                        print("(main.py) - Android - Incorrect Device Selected: %s" % (self.msgFromBT))
            except Exception:
                pass

    
    # Function to write to Android via Bluetooth
    def writeAndroid(self, msg):
        if msg != "":
            self.androidThread.writeToAndroid(msg)
            print("Msg sent to android")
    
    def writeResult(self):
        while True:
            if self.handlers.occured==True and self.handlers.pred_class!="" and self.handlers.pred_class!=0:
                self.androidThread.writeToAndroid("TARGET,"+str(order[len(all_results)-1])+","+str(self.handlers.pred_class))
                print("Results sent to android")
                self.handlers.occured = False

            elif self.handlers.occured==True and self.handlers.pred_class==0:
                self.writeAndroid('TARGET,'+str(order[len(all_results)-1])+",43")
                self.handlers.occured = False                

            # if self.sent == 1:
            #     self.finished = 1
            #     self.writeAndroid("STOP,0")
            #     print("finished", self.finished)
                    
    '''
    def writePC(self):
        while True:
            if (self.finished==1):
                print("Stitching Images...")
                images = []
                
                # Stitch Image Horizontally

                imgpath = '/home/pi/output/'
                myList = os.listdir(imgpath)
                for imgN in myList:
                    print("appending")
                    curImg = cv2.imread(f'{imgpath}/{imgN}')
                    images.append(curImg)
                
                # Stitch images starting with "combined"
                # for imgN in glob.iglob('/home/pi/output/combined*'):
                #     print("appending")
                #     curImg = cv2.imread(f'{imgpath}/{imgN}')
                #     images.append(curImg)

                stitcher = cv2.hconcat(images)
                cv2.imwrite('stitched.jpg', stitcher)
                print("Successfully Stitched Image")
                print("Sending IMG to pc")
                time.sleep(0.1)
                self.PCThread = PCinterface()
                while self.PCThread.checkConnection==False:
                    self.PCThread.pcConnection()
                    if self.PCThread.address=="192.168.29.3":
                        self.PCThread.sender()
                time.sleep(0.1)
                print("IMG sent to pc")
                self.finished = 0
    '''
    # Function to read from Algo
    def readAlgo(self, msg):
        
        self.path = self.algo.findPath(msg.strip())
        self.startTime = time.time()
        self.path.pop(0)

        # For Each Obstacle
        for j in self.path:
            order.append(j)
            print("Going to Obstacle " + str(j))
            self.instr, self.coord = self.algo.getMvmtList()
            if self.instr != None:
                for i in range(len(self.instr)):
                    print(self.instr[i].lower())
                    print(self.coord[i])
                    if(self.updateTime() == 1): #update and check if times up, if times up:
                        print("Time Exceeded!")
                        return
                    self.writeSTM(self.instr[i].lower())
                    # Check that STM has reached obstacle
                    self.readSTM()
                    self.writeAndroid(self.coord[i])
                
                # Take Photo
                print("STM is ready, RPI taking image...")
                os.system("libcamera-still\
                    -o /home/pi/images/image_{}.jpg --immediate -n\
                    --camera 0 --verbose 0 \
                    --width 1280 --height 1280 \
                    --ev 2\
                ".format(j))
                self.writeAndroid("TARGET,"+str(j)+",42")
        self.writeAndroid("STOP,0")
        time.sleep(30)
        self.sent = 1

        print("Stitching Images...")
        images = []
    
        # Stitch Image Horizontally
        
        # Stitch images starting with "combined"
        for imgN in glob.iglob('/home/pi/output/combined*'):
            print("appending")
            curImg = cv2.imread(f'{imgN}')
            images.append(curImg)

        stitcher = cv2.hconcat(images)
        cv2.imwrite('stitched.jpg', stitcher)

        

           
    # Function to read from STM via serial connection
    def readSTM(self):
        while True:
            serialMsg = self.stmThread.readFromSTM()
            # If STM Connection is Established and Message is present
            if serialMsg != '':
                print('STM Message Received')
                return 1

    # Function to write to STM via serial connection
    def writeSTM(self, msg):
        if msg != "":
            self.stmThread.writeToSTM(msg)
            print("Msg sent to stm")

    
    # # Function to write Image to PC via Wifi
    # def write_ImgPC(self, img):
    #     # If PC Connection is Established and Image is present
    #     if self.pcThread.checkConnection() and img:
    #         self.pcThread.sender()
    #         return True
    #     return False
    
    def startup(self):
        # Initialise connections to all interfaces
        self.androidThread.androidConnection(UUID)
        self.stmThread.stmConnection()

        print("Connected to STM and Android")

    def disconnectAll(self):
        self.androidThread.androidDisconnection()
        self.stmThread.stmDisconnection()
        print('Multithread process has ended')

    # Function to read and write threads for Multithreading
    def multithread(self):
        # Android read and write thread
        readAndroidThread = threading.Thread(target = self.readAndroid, args = (), name = "read_android_thread")
        writeAndroidThread = threading.Thread(target = self.writeAndroid, args = ("", ), name = "write_android_thread")
        writeResultsToAndroid = threading.Thread(target = self.writeResult, args = (), name = "write_results_thread")

        # STM read and write thread
        writeSTMThread = threading.Thread(target = self.writeSTM, args = ("", ), name = "write_STM_thread")
        readSTMThread = threading.Thread(target = self.readSTM, args = (), name = "read_STM_thread")

        # PC read and write thread
        #writePCthread = threading.Thread(target=self.writePC, args=(), name="write_pc_thread")

        # Object Detection thread
        self.imageThread.schedule(self.handlers, path = '/home/pi/images', recursive = True)
        
        # Set Daemon for all threads
        readAndroidThread.daemon = True
        writeAndroidThread.daemon = True
        writeSTMThread.daemon = True
        readSTMThread.daemon = True
        #readPCthread.daemon = True
        #writePCthread.daemon = True 
        #writeResultsToAndroid.daemon = True
        
        # Start All Threads
        readAndroidThread.start()
        writeAndroidThread.start()
        writeResultsToAndroid.start()
        writeSTMThread.start()
        readSTMThread.start()
        self.imageThread.start()
        #writePCthread.start()
        
    
    def keep_main_alive(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.imageThread.unschedule_all()
            self.imageThread.stop()
            self.readAndroidThread.stop()
            self.writeAndroidThread.stop()
            self.writeSTMThread.stop()
            self.readSTMThread.stop()
        self.imageThread.join()
        self.readAndroidThread.join()
        self.writeAndroidThread.join()
        self.writeSTMThread.join()
        self.readSTMThread.join()

    def close_all_sockets(self):
        #androidThread.androidDisconnection()
        #stmThread.stmDisconnection()
        print("end threads")


########################### to be deleted after fixing 

if __name__ == "__main__":

    # Starting main program
    print("Remove existing images")
    for img in glob.iglob("/home/pi/images/*.jpg"):
        os.remove(img)
    for img in glob.iglob("/home/pi/output/*.jpg"):
        os.remove(img)
    print("Starting Program...")
    rpi = Multithreading()

    try:
        print("Starting threads")
        
        rpi.multithread()       
        rpi.keep_main_alive()

    except KeyboardInterrupt:
        print("Exiting the program")
        rpi.disconnectAll()
