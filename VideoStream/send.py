from socket import *
from threading import Thread as TH
import cv2

def SendProto(conn, d):
    # send dictionary lingth:
    if conn.recv(1) == chr(0).encode('utf-8'):
        conn.send(len(d.keys()).__str__().encode('utf-8'))
        conn.recv(1) # Synchronizer
    # looging through the whole thing:
    for dic in d.keys():
        # Define Requerments:
        key = dic; data = d[dic]
        dtype = type(d[dic]).__name__
        # send Key & Type:
        if conn.recv(1) == chr(1).encode('utf-8'): conn.send(key.encode('utf-8'))
        if conn.recv(1) == chr(2).encode('utf-8'): conn.send(dtype.encode('utf-8'))
        ## Slice & Send:
        v = d[dic]
        # Encoding process:
        if type(v).__name__ == 'bytes': value = v
        elif type(v).__name__ == 'str': value = v.encode('utf-8')
        elif type(v).__name__ == 'int': value = v.__str__().encode('utf-8')
        else: value = str(v).encode('utf-8')
        # Sending the data size:
        conn.recv(1)
        conn.send(len(value).__str__().encode('utf-8'))
        # sending:
        conn.recv(1)
        conn.sendall(value)
        conn.recv(1)

server = socket(AF_INET, SOCK_STREAM)
server.bind((gethostbyname(gethostname()), 8080))
server.listen(1); conn =  server.accept()[0]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        conn.recv(1)
        SendProto(conn, {'data': frame.tobytes()})


