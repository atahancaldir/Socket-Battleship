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
                
            except:
                pass

        while self.connected:
            msg = pickle.loads(self.client.recv(self.HEADER))
            if msg:
                print(msg)
                if msg == self.DISCONNECT_MSG:
                    self.connected = False

                elif not self.opponentName:
                    self.game_ui.oppname_label.setText(msg)
                    self.game_ui.tableWidget.setDisabled(False)
                    self.game_ui.tableWidget_2.setDisabled(False)
                    self.placeShips()

                    self.opponentName = True

                elif msg == self.ALL_SHIPS_PLACED:
                    self.opponentShipsPlaced = True
                    if self.userShipsPlaced:
                        self.setShootTurn(0)

                elif type(msg) == type(tuple()):
                    if self.game_ui.tableWidget.item(msg[0], msg[1]).text():
                        self.game_ui.tableWidget.item(msg[0], msg[1]).setBackground(QtGui.QColor(255,0,0))
                        self.gotShoot(1)
    
    def send(self, msg):
        self.client.send(pickle.dumps(msg))

    def signIn(self):
        super().signIn()
        self.send(self.username)

    def placeShips(self):
        super().placeShips()
        if self.userShipsPlaced and self.opponentShipsPlaced:
            self.setShootTurn(0)

"""
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
"""

c = Client()