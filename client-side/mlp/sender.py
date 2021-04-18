import socket
import time
import select
import sys
from threading import Thread
import os

import numpy as np
import random
import csv

from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler 


TCP_IP = '10.50.0.11'
TCP_PORT = 9001
BUFFER_SIZE = 1024


def send_test(X):
    result = -1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #while True:
    #    try:
    #        s.connect((TCP_IP, TCP_PORT))
    #        break
    #    except:
    #        continue
    s.connect((TCP_IP, TCP_PORT))
    s.send(str(X).encode())
    s.shutdown(socket.SHUT_WR)
    input1 = [s, sys.stdin]
    while True:
        try:
            readyInput, readyOutput, readyException = select.select (input1, [], [],0)
            for x in readyInput:
                if x == s:
                    while True:
                        data = s.recv(BUFFER_SIZE)
                        result = int(data.decode())
                        s.close()
                        break
        except:
            break
    return result

def clean_row(row):
	row = row[1:-3] + [row[-1]]
	out = []
	for i in range(len(row)-1):
		try:
			out.append(float(row[i]))
		except:
			pass
	out.append(int(row[-1]))
	return out

def csv_reader(file_name):
	fields	=	[]
	rows	=	[]
	with open(file_name, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		fields = next(csvreader)
		for row in csvreader:
			x = clean_row(row)
			# print(x)
			if len(x)==39:
				rows.append(x)

	return fields, rows



h, X = csv_reader("UNSW_NB15_training-set.csv")
X = np.array(X)
X_train, X_test, y_train, y_test = train_test_split(X[:,:-1], X[:,-1], test_size=0.2, random_state=321)
scaler = StandardScaler()
scaler.fit(X_train) 
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

lats = []
for i in range(100):
#for i in range(len(X_test)):
        time.sleep(5/1000)
        start = time.time()
        r = send_test(X_test[i])
        end = time.time()
        if r!=-1:
            lats.append(1000*(end-start))

print("avg: ",sum(lats)/len(lats))
print("max: ",max(lats))
print("min: ", min(lats))
lats = np.array(lats)
print("SD :", np.std(lats))
