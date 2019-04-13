from socket import *


class Network:
    def __init__(self):
        self.host = "192.168.0.102"
        self.port = 9999
        self.s = socket()

    @property
    def connected(self):
        try:
            self.s.connect((self.host, self.port))
            return True
        except error:
            return False
