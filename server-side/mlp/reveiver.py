import socket
from threading import Thread
import random
import select
import sys
import os
import time

import numpy as np
import csv
import pickle
from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler 

filename = "model.sav"
clf = pickle.load(open(filename, 'rb'))

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
        data = ''
        s = time.time()
        while True:
            x = self.sock.recv(BUFFER_SIZE)
            if x == b'':
                break
            data = x
        #print(s)
        e = time.time()
        print("Recieved", 1000*(e-s))
        #print(self.start)
        #print(time.time())
        data = data.decode()
        data = data[1:-1].split()
        input_array = [float(i) for i in data]
        input_array = np.array(input_array)
        self.process_input(input_array)

    def process_input(self, input_array):
       response = clf.predict([input_array])
       self.sock.send(str(int(response[0])).encode())
       self.sock.close()



tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    (conn, (ip, port)) = tcpsock.accept()
    s = time.time()
    newthread = ServerThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
