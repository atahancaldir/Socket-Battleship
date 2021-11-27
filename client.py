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
                
                self.game_ui.tableWidget.setDisabled(False)
                self.game_ui.tableWidget_2.setDisabled(False)
                self.placeShips()
            except:
                pass

        while self.connected:
            msg = self.client.recv(self.HEADER).decode("utf-8")
            if msg:
                print(msg)
                if msg == self.DISCONNECT_MSG:
                    self.connected = False
    
    def send(self):
        message = self.send_msg.encode("utf-8")
        msg_length = len(message)
        send_length = str(msg_length).encode("utf-8")
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def signIn(self):
        super().signIn()
        self.send()

"""
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
"""

c = Client()