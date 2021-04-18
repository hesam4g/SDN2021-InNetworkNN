import socket
from threading import Thread
import random
import select
import sys
import os
import time
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

model = tf.keras.models.load_model('models/original.h5')

TCP_IP = '10.50.0.11'
TCP_PORT = 9001
BUFFER_SIZE = 1024


class ServerThread(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
    def run(self):
        recived_f = 'received_file.jpg'
        f = open(recived_f, 'wb')
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            if data == b'':
                f.close()
                break
            f.write(data)
        f.close()
        self.process_image()

    def process_image(self):
        s0 = time.time()
        img = Image.open("received_file.jpg").convert("RGB")
        img = img.resize((180, 180))
        input_data = np.array(img, dtype=np.float32)
        input_data = np.expand_dims(input_data, axis=0)
        img.close()
        s1 = time.time()
        p = model.predict(input_data)
        p = p[0][0]
        p = 1 if p>0.5 else 0
        response = str(p)
        s2 = time.time()
        #print(s2-s1)
       # print(s1-s0)
        self.sock.send(response.encode())
        self.sock.close()



tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    (conn, (ip, port)) = tcpsock.accept()
    newthread = ServerThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

