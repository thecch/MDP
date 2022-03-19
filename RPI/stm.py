import os, sys
import traceback
import serial
import time

from config import *


class STMInterface():

    def __init__(self):
        # Initialize variables
        self.port = ""
        self.baudRate = BAUDRATE
        self.ser = 0
        self.isConnected = False

    def checkConnection(self):
        return self.isConnected

    # Establishing STM Connection
    def stmConnection(self):
        # Connect to serial port
        attemptingConnection = True

        try:
            while attemptingConnection:
                print("Connecting to STM robot...")
                try:
                    print("Connecting to USB0")
                    self.ser = serial.Serial(
                        port = USB_PORT,
                        baudrate = self.baudRate, 
                        timeout=3)
                except Exception as e:
                    print("Failed to connect to USB0, connecting to USB1")
                    self.ser = serial.Serial(
                        port = USB_PORT2, 
                        baudrate = self.baudRate, 
                        timeout=3)
                time.sleep(1)

                if self.ser != 0:
                    #print("Connected to STM")
                    self.isConnected = True
                    attemptingConnection = False
                    break

        except Exception as e:
            print("(stm.py) STM - Failed Connection")
            print("Error: %s" %str(e))
            traceback.print_exc(limit=10, file=sys.stdout)

    # Disconnect from STM
    def stmDisconnection(self):
        self.ser.close()
        self.isConnected = False
        print("Disconnected from STM")

    # Read from STM
    def readFromSTM(self):
        try:
            # Decode and Print Message String from STM
            msg = self.ser.readline()
            receivedMsg = str(msg.decode('utf-8'))
            return receivedMsg

        except Exception as e:
            print("(stm.py) STM - Failed to receive message from STM")
            print("Error: %s" % str(e))
            self.stmConnection()

    # Write to STM
    def writeToSTM(self, msg):
        try:
            # Encode and Print Message String to STM
            self.ser.write(str.encode(msg))
            print("Message Sent to STM:%s" % msg)

        except Exception as e:
            print("(stm.py) STM - Error: %s" % str(e))
            self.stmConnection()
            

# testing stm connection
    
if __name__ == "__main__":

    # Start Main Program
    print("Starting Program...")
    
    stmThread = STMInterface()
    stmThread.stmConnection()
    stmThread.readFromSTM()
    stmThread.writeToSTM("helloooo")
