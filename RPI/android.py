import time
from bluetooth import *
import os

from config import *

class AndroidInterface(object):

    def __init__(self):
        self.serverSocket = None
        self.clientSocket = None
        self.connection = False
        self.socketName = 0

    def checkConnection(self):
        return self.connection

    # Establishing Android Connection
    def androidConnection(self, UUID):
        try:
            # Endpoint for Bluetooth connection
            self.serverSocket = BluetoothSocket(RFCOMM)
            self.serverSocket.bind(("", PORT_ANY))
            self.serverSocket.listen(1)
            self.port = self.serverSocket.getsockname()[1]
            print(self.port)
            print("Socket name is:", self.serverSocket.getsockname())
            
            os.system('sudo hciconfig hci0 piscan')

            # Start Listening for Incoming Connections
            try:
                advertise_service(self.serverSocket, "Group 29 Server",
                                    service_id=UUID,
                                    service_classes=[UUID, SERIAL_PORT_CLASS],
                                    profiles=[SERIAL_PORT_PROFILE], )
            except Exception as e:
                print("Error: Failed to advertise service")
                print ("Error: %s" %str(e))
            
            print("Connecting to Bluetooth RFCOMM Channel %d" % self.port)
            self.clientSocket, clientAddress = self.serverSocket.accept()

            print("Accepted Connection from ", clientAddress)
            #print("Connected to Android")
            self.connection = True

        except Exception as e:
            print("(android.py) Bluetooth - Failed Connection")
            print ("Error: %s" %str(e))
            self.serverSocket.close()
            print("Closing Server Socket")
            self.connection = False  # Set connection to true
            
    # Disconnecting from Android, close bluetooth socket
    def androidDisconnection (self):
        self.clientSocket.close()
        print("Closing Client Socket")
        self.serverSocket.close()
        print("Closing Server Socket")
        self.connection = False  # Set connection to true

    # Read message from Android
    def readFromAndroid(self):
        try:
            # Decode message and print the message from Android
            msg = self.clientSocket.recv(1024)
            msg = msg.decode('utf-8')
            print("Message Received from Android: %s" % str(msg))
            return (msg)

        except Exception as e:
            print("(android.py) Bluetooth - Error. Reconnecting RPi...")
            print ("Error: %s" %str(e))
            self.androidConnection(UUID)

    # Write message to Android
    def writeToAndroid(self, msg):
        try:
            # Print message sent to Android
            self.clientSocket.send(msg)
            print("Message Sent to Android: %s" % (msg))

        except Exception as e:
            print("(android.py) Bluetooth - Error. Reconnecting RPi...")
            print ("Error: %s" %str(e))
            self.androidConnection(UUID)



# testing bluetooth socket connection w android
    
# if __name__ == "__main__":

#     # Start Main Program
#     print("Starting Program...")
    
#     androidThread = AndroidInterface()
#     androidThread.androidConnection(UUID)
#     androidThread.readFromAndroid()
#     androidThread.writeToAndroid("hello")
#     androidThread.androidDisconnection()
