# Record

from socket import *
import sounddevice as sd, numpy as np
from time import time as t
from threading import Thread as TH

server = socket(AF_INET, SOCK_DGRAM)
server.bind((gethostbyname(gethostname()), 8081))

fs = 40100; duration = 2700
sd.default.samplerate =  fs
sd.default.channels = 1

REC = sd.rec(fs * duration)
starting_point = t()

chunk_bytes = lambda data, buffer_size: [data[i:i + buffer_size] for i in range(0, len(data), buffer_size)]

class AudioSender:
    def sec(self):
        return (t()-starting_point)-1

    def send(self):
        _, addr = server.recvfrom(1)
        print(_)
        num = self.sec() - 0.1
        d = REC[int(fs*(num)):int(fs*((num)+1))].tobytes()
        for chunk in chunk_bytes(d, 65_000):
            server.sendto(chunk, addr)
            print(9)

    def PackageSender(self):
        num = 0
        while True:
            sd.sleep(1000)
            TH(target=self.send).start()
            num+=1

sender = AudioSender()
sender.PackageSender()
