import socket
import pickle
from threading import Thread
from game import *
import network

class Client(Game):
    def __init__(self):
        super().__init__()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket object for client
        self.game_ui.label.setText("Waiting for the host to start...")

        T = Thread(target=self.socketConnection, daemon=True) # creating a new thread for the socket connection
        T.start()

        self.Form_sign_ui.show()
        sys.exit(self.app.exec_())

    def socketConnection(self):
        self.connected = False
        while not self.connected: # it will keep trying to connect to the server until the connection is established
            try:
                self.client.connect(self.ADDR) # connecting to server
                self.connected = True
                
            except:
                pass

        network.socketConnection(self, "client")
    
    def send(self, msg):
        self.client.send(pickle.dumps(msg))

    def signIn(self):
        super().signIn()
        self.send(self.username)

    def placeShips(self):
        super().placeShips()
        if self.userShipsPlaced and self.opponentShipsPlaced:
            self.setShootTurn(0)

c = Client()