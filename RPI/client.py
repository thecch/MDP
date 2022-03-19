## to be run on the pc to receive stitched image

import socket
import time
import os

s = socket.socket()
host = '192.168.29.29'  # Get local machine name (PC)
port = 5001   # Reserve port for service

print("Connecting")
connect = True

while connect:
    try:
        s.connect((host, port))
        print("Connected")
        connect = False
        #tgt = s.recv(8096)
        data = s.recv(4096)
        print("Receiving image file..")
        f = open(f'image.jpg', 'wb')
        
        while data != bytes(''.encode()):
            f.write(data)
            data = s.recv(4096)
        print("Image received")
        time.sleep(2)
        s.close()
        break
    except KeyboardInterrupt:
        print("Client exited")

        # if tgt == '':
        #     continue
        # else:
        #     break
    # print(tgt)
    # s.send(f'AD, {tgt}')


#s.close()
