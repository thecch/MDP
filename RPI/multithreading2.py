import time
import threading
import os, sys, glob
from android import *
from stm import *
from config import *


class Multithreading():

    def __init__(self):
        # Time Limit
        self.timeLimit = 6*60 #time limit of 6 minutes

        # Instantiate all classes
        self.androidThread = AndroidInterface()
        self.stmThread = STMInterface()


        # Initialise connections to all interfaces
        self.androidThread.androidConnection(UUID)
        self.stmThread.stmConnection()
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
                        continue          
                    else:
                        print("(main.py) - Android - Incorrect Device Selected: %s" % (self.msgFromBT))
            except Exception:
                pass

    
    # Function to write to Android via Bluetooth
    def writeAndroid(self, msg):
        if msg != "":
            self.androidThread.writeToAndroid(msg)
            print("Msg sent to android")  

           
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

        # STM read and write thread
        writeSTMThread = threading.Thread(target = self.writeSTM, args = ("", ), name = "write_STM_thread")
        readSTMThread = threading.Thread(target = self.readSTM, args = (), name = "read_STM_thread")

        # Set Daemon for all threads
        readAndroidThread.daemon = True
        writeAndroidThread.daemon = True
        writeSTMThread.daemon = True
        readSTMThread.daemon = True
        
        # Start All Threads
        readAndroidThread.start()
        writeAndroidThread.start()
        writeSTMThread.start()
        readSTMThread.start()

    
    def keep_main_alive(self):
        while True:
            time.sleep(1)

    def close_all_sockets(self):
        #androidThread.androidDisconnection()
        #stmThread.stmDisconnection()
        print("end threads")
