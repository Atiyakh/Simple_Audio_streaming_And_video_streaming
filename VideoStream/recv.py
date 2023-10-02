from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from socket import *
from threading import Thread as TH
import cv2, numpy as np, sys
from time import sleep as s

server = socket(AF_INET, SOCK_STREAM)
server.connect((gethostbyname(gethostname()), 8080))

def RecvProto(conn, buffersize=1024, dump=False):
    # recv dictionary lingth:
    conn.send(chr(0).encode('utf-8'))
    length = int(conn.recv(1024))
    conn.send(chr(0).encode('utf-8'))
    # Getting the dictionary data:
    d = {}
    for dic in range(length):
        # receive Key & Type:
        conn.send(chr(1).encode('utf-8'))
        key = conn.recv(1024).decode('utf-8')
        conn.send(chr(2).encode('utf-8'))
        dtype = conn.recv(1024).decode('utf-8')
        ## Receive the value fragments and Reassemble them:
        # Receiving data:
        conn.send(b'0')
        SIZE = int(conn.recv(1024))
        conn.send(b'0')
        v = b''
        while (v.__len__() != SIZE):
            v += conn.recv(buffersize)
        conn.send(b'0')
        # Decoding:
        if dtype == 'bytes': value = v
        elif dtype == 'str': value = v.decode('utf-8')
        elif dtype == 'int': value = int(v)
        else: value = v.decode('utf-8')
        d[key] = value
    if dump: return d
    else: conn.__class__.payload = d

class GUI(QMainWindow):
    def Counter(self):
        while 1:
            s(1)
            print(self.count)
            self.count = 0
    def FrameLoader(self):
        self.count = 0
        while True:
            server.send(b'0')
            data = RecvProto(server, dump=True, buffersize=100_000)['data']
            frame = np.frombuffer(data, dtype='uint8').reshape((480, 640, 3))
            cv2.imwrite('img.png', frame)
            img = QPixmap('img.png')
            self.count += 1
            self.Viewer.setPixmap(img)
    def InitUI(self):
        self.Viewer = QLabel(self); self.Viewer.show()
        self.setCentralWidget(self.Viewer)
        self.show()
        TH(target=self.FrameLoader).start()
        TH(target=self.Counter).start()
    def __init__(self):
        super(GUI, self).__init__()
        self.InitUI()

app = QApplication(sys.argv)
gui = GUI()
app.exec_()
