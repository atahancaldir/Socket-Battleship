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

        try:
            network.socketConnection(self, "client")
        except ConnectionResetError:
            self.showWarning("Opponent left the game!", close_program=True)
        finally:
            self.connected = False
    
    def send(self, msg):
        self.client.send(pickle.dumps(msg))

    def signIn(self):
        super().signIn()
        try:
            self.send(self.username)
        except OSError:
            print("Server should start first!")
            sys.exit()
        

    def placeShips(self):
        super().placeShips()
        if self.userShipsPlaced and self.opponentShipsPlaced:
            self.setShootTurn(0)

c = Client()