import socket
import time
import select
import sys
from threading import Thread
import os

TCP_IP = '10.50.0.11'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def send_pic(filename):
    result = -1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    f = open(filename, 'rb')
    l = f.read(BUFFER_SIZE)
    x = ''
    while (l):
        s.send(l)
        l = f.read(BUFFER_SIZE)
    f.close()

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
labels = ["Cat", "Dog"]
r_dog = []
r_cat = []
lat = []
for label in labels:
    d = os.listdir('./PetImages/' + label)
    for i in range (len(d)):
        x = d[i]
        start = time.time()
        r = send_pic("./PetImages/"+label+"/"+x)
        end = time.time()
        if label == "Cat":
            r_cat.append(r)
        else:
            r_dog.append(r)
        print(r, 1000*(end-start))
        lat.append(1000*(end-start))

cat = r_cat.count(0)
dog = r_dog.count(1)
print(sum(lat)/len(lat))
print((cat+dog)/(len(r_cat) + len(r_dog)))
