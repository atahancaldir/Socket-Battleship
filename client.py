import socket
import pickle
from threading import Thread
from game import *

class Client(Game):
    def __init__(self):
        super().__init__()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_ui.label.setText("Waiting for the host to start...")

        T = Thread(target=self.socketConnection, daemon=True)
        T.start()

        self.Form_sign_ui.show()
        sys.exit(self.app.exec_())

    def socketConnection(self):
        self.connected = False

        while not self.connected:
            try:
                self.client.connect(self.ADDR)
                self.connected = True
                self.game_ui.label.setText("Connected to host!")
            except:
                pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


c = Client()