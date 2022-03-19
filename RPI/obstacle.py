import time
import threading
import sys


import requests
import base64

from android import *
from stm import *
from config import *
from ultrasonic import *
from sendtopc import *

#sys.path.insert(0, '../Algorithm/simulator_py')
import Algorithm 

class Multithreading():

    def __init__(self):
        # Time Limit
        self.timeLimit = 6*60 #time limit of 6 minutes

        # Instantiate all classes
        #self.androidThread = AndroidInterface()
        self.stmThread = STMInterface()

        #starting car position and facing direction 0 = up, 2 = right, 4 = down, 6 = left
        self.algo = Algorithm.Algorithm([1,18],0) 
        
        # Initialise connections to all interfaces

        self.stmThread.stmConnection()
        #self.androidThread.androidConnection(UUID)
        print("Connected to STM and Android")

        # Delay for buffer set
        time.sleep(0.5)

        print("Beginning Transmission...")

    # Function to read ultrasonic distance
    def read_ultra(self):
        ultrasonic = Ultrasonic()
        values = [] 
        while True:
            try:
                dist = ultrasonic.find_distance()
                values.append(dist)
                time.sleep(1)
            except KeyboardInterrupt:
                ultrasonic.cleanup()
            except Exception as e:
                print("Error with Ultra: %s" %str(e))

    # Function to read from Android via Bluetooth
    def readAndroid(self):
        while True:
            androidMsg = self.androidThread.readFromAndroid()
            androidMsg = str(androidMsg)

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
                    return self.msgFromBT[1].strip()
                    #self.readAlgo(self.msgFromBT[1])                    
                else:
                    print("(main.py) - Android - Incorrect Device Selected: %s" % (msgFromBT))
    
    
    # Function to write to Android via Bluetooth
    def writeAndroid(self, msg):
        self.androidThread.writeToAndroid(msg)
        print("Msg sent to android")
    
    # Function to read from Algo
    def readAlgo(self, msg):
        self.path = self.algo.findPath(msg.strip())
        self.startTime = time.time()
        for j in self.path:
            self.instr, self.coord = self.algo.getMvmtList()
            if self.instr!=None:
                for i in range(len(self.instr)):
                    print(self.instr[i])
                    print(self.coord[i])
                    if(self.updateTime() == 1): #update and check if times up, if times up:
                        print("Time Exceeded!")
                        return;
                    self.writeSTM(self.instr[i])
                    self.writeAndroid(self.coord[i])
            print("IMAGE REC PART!!!!!")  # tbc check if correct
            time.sleep(2)
    

    # Function to read from STM via serial connection
    def readSTM(self):
        while True:
            serialMsg = self.stmThread.readFromSTM()

            # If STM Connection is Established and Message is present
            if serialMsg!= '':
                print('STM Message Received')
                return 1

    # Function to write to STM via serial connection
    def writeSTM(self, msg):
        self.stmThread.writeToSTM(msg)
        print("msg sent to stm")
        # If STM connection is up and there is message to be sent
        # if self.stmThread.checkConnection() and msg:
        #     self.stmThread.writeToSTM(msg)
        #     return True
        # return False
    
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
        # STM read and write thread
        writeSTMThread = threading.Thread(target=self.writeSTM, args=("",), name="write_STM_thread")
        readSTMThread = threading.Thread(target=self.readSTM, args=(), name="read_STM_thread")

        # Set Daemon for all threads
        writeSTMThread.daemon = True
        readSTMThread.daemon = True
        
        # Start All Threads
        writeSTMThread.start()
        readSTMThread.start()
        
    
    def keep_main_alive(self):
        while True:
            time.sleep(1)

    def close_all_sockets(self):
        #androidThread.androidDisconnection()
        #stmThread.stmDisconnection()
        print ("end threads")

    def sendImgToPC(self):
    
        def sender(s):
            
            f = open(f'/home/pi/Desktop/image.jpg','rb')
            data = f.read(1024)

            s.sendall(data)
            print('Sending...')
            
            while data != bytes(''.encode()):
                data = f.read(1024)
                s.sendall(data)

            print("IMG sent")

            #time.sleep(3)
            #print('[sendtopc.py] close socket')
            #s.close()
        try:
            # --- create socket ---
            
            print('[sendtopc.py] create socket')
            s = socket.socket()         
            print('[sendtopc.py] connecting:', (HOST, PORT))
            s.connect((HOST, PORT))
            print('[sendtopc.py] connected')
            
            # --- send data ---
            # sendData = threading.Thread(target=sender, args=(s,))
            # sendData.start()
            sender(s)
        except Exception as e:
            print(e)
        except KeyboardInterrupt as e:
            print(e)
        except:
            print(sys.exc_info())


if __name__ == "__main__":
    rpi = Multithreading()
    try:
        print("(obstacles.py) Starting Threads")
        camera = PiCamera()
                            
        obstacle  = True
        face_count = 0

        # time.sleep(5)
        # with open(f'/home/pi/Desktop/image.jpg','rb') as img:
        #     encoded = base64.b64encode(img.read())

        # rpi.writeAndroid(encoded)
        # result = rpi.readAndroid()

        while obstacle and (face_count<4):
            # Take photo
            img = camera.capture('/home/pi/Desktop/image.jpg')
            #rpi.sendImgToPC()
            # f = open(f'/home/pi/Desktop/image.jpg','rb')
            # data = f.read(1024)

            # with open(f'/home/pi/Desktop/image.jpg','rb') as img:
            #     encoded = base64.b64encode(img.read())

            # rpi.writeAndroid(encoded)
            # result = rpi.readAndroid()
            import json
            sendImgToPC()
            time.sleep(20)
            f = open("results.json")
            results = f.readlines()[0]
            #print(results) 
            #print(type(results))
            results = results.replace("[", "")\
                .replace("]", "")\
                .replace("'", '"')
            #print(results)
            results = json.loads(results)
            #print(type(results))
            #print(results['pred_classes'])
           
            try:
                # s = socket.socket()
                # host = '192.168.29.3'  # Get local machine name (PC)
                # port = 5001   # Reserve port for service
                # results = s.recv(1024)
                # print(results)

                if results['pred_classes'] == 'target':
                    # Robot continue rotating while image is obstacle
                    rpi.writeSTM("f045055") # some msg to continue rotating
                    stm_msg = rpi.readSTM()
                    if stm_msg!="":
                        print("STM is ready")
                    face_count+=1
                else:
                    print("Target found")
                    #rpi.writeSTM("s") # Robot stop moving
                    obstacle = False 
            except Exception as e:
                print(e)
                break
            

    except KeyboardInterrupt:
        print("END")



'''
if __name__ == "__main__":
    rpi = Multithreading()
    try:
        print("(obstacles.py) Starting Threads")
        rpi.multithread()
        rpi.keep_main_alive()
        camera = PiCamera()
        try:
            no_start = True
            while no_start:

                # run once
                print("Finding distance..")
                est_distance = rpi.read_ultra()
                print("Estimated distance:", est_distance)
                
                if est_distance<=20:
                    # Stop moving forward
                    rpi.writeSTM("s")
                    
                    obstacle  = True
                    stm_ready = True #tbc do we need ready msg frm stm
                    face_count = 0
                    while obstacle and (face_count<4):
                        # Take photo
                        img = camera.capture('/home/pi/Desktop/image.jpg')

                        # Image Rec Part

                        if img == obstacle_img:
                            # Robot continue rotating while image is obstacle
                            rpi.writeSTM() # some msg to continue rotating
                            face_count+=1
                        else:
                            print("Target found")
                            rpi.writeSTM("s") # Robot stop moving
                            obstacle = False 

                    no_start = False    
                else:
                    # STM move forward
                    rpi.writeSTM("w")
                
                break
                #force stop script
                sys.exit()


        except Exception as e:
            print("Something went wrong in ultrasonic code")

    except KeyboardInterrupt:
        print("END")
'''
