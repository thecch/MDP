import socket
import time

from config import *


class PCinterface(object):

    def __init__(self):
        
        # Initialize
        self.host = WIFI_IP
        self.port = WIFI_PORT
        self.isConnected = False

    def checkConnection(self):
        return self.checkConnection

    # Establishing PC Connection
    def pcConnection(self):
        try:
            # Assigning new socket variable for Socket library
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.connection.bind((self.host, self.port))
            print("Bind Completed")  # Bind socket

            # Number of unaccepted connections set to 3
            self.connection.listen(3)
            print("Waiting for Connection from PC ...")

            # Assigning new variables clientSocket and address
            self.clientSocket, self.address = self.connection.accept()
            print("Connected to PC with IP Address: ", self.address)
            self.isConnected = True # Set connection to true

        except Exception as e:
            print("(pc.py) PC - Error: %s" % str(e))

    # Disconnecting from PC
    def pcDisconnection(self):
        try:
            if self.connection:
                self.connection.close()
                print('Terminating Server Socket')

            if self.clientSocket:
                self.clientSocket.close()
                print('Terminating Client Socket')

            self.isConnected = False

        except Exception as e:
            print("(pc.py) PC - Failed Disconnection: %s " %str(e))

    # Send Img to PC
    def sender(self):
        
        try:
            f = open(f'/home/pi/RPI/stitched.jpg','rb')
        
            data = f.read(4096)
            while data != bytes(''.encode()):
                self.clientSocket.sendall(data)
                data = f.read(4096)

            print("Image Successfully Sent to PC")
            print(len(data))
            time.sleep(5)
            self.clientSocket.close()

        except Exception as e:
            print("(pc.py) Image to PC - Error: %s " % str(e))
            self.pcConnection()


# testing bluetooth socket connection w android
    
if __name__ == "__main__":

    # Start Main Program
    print("Starting Program...")
    
    PCThread = PCinterface()
    PCThread.pcConnection()
    PCThread.sender()
    

