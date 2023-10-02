# Play

from socket import *
import sounddevice as sd, numpy as np
from time import time as t
from threading import Thread as TH

HOST = ('85.114.121.194', 8081)
fs = 40100; duration = 2700
sd.default.samplerate =  fs
sd.default.channels = 1
done = True; data = []

class Main:
    def Play(self):
        self.ctx = sd.play(self.REC)
        self.starting_time = t()
        sd.wait()

    def sec(self):
        return t()-self.starting_time

    def RecvPackage(self):
        server = socket(AF_INET, SOCK_DGRAM)
        server.sendto(b'0', HOST)
        d = b''
        while True:
            d+=server.recv(65_000)
            if len(d) == 160400:
                break
        return np.frombuffer(d, dtype='float32').reshape(-1,1)

    def recv(self):
        d = self.RecvPackage()
        num = self.sec()
        try: self.ctx.data[int(num*fs):int(fs*(num+1))] = d
        except: print('array broadcasting error')

    def LoadData(self):
        for _ in range(1, duration):
            sd.sleep(1000)
            TH(target=self.recv).start()

    def __init__(self):
        self.REC = np.zeros(fs*duration)
        TH(target=self.Play).start()
        self.LoadData()

if __name__ == "__main__":
        main = Main()
