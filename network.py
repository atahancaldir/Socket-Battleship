import socket
import pickle

class Network():
    def __init__(self):
        self.IP = "127.0.0.1"
        self.PORT = 5555
        self.HEADER = 4096
        self.ADDR = (self.IP, self.PORT)