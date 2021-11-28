import socket
from threading import Thread
from game import *
import pickle
import network

class Server(Game):
    def __init__(self):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket object for server

        try:
            self.s.bind(self.ADDR) # binding to the specified IP(localhost) and PORT(5555) 
        except socket.error as e:
            self.game_ui.label.setText("Connection failed!")
        
        self.s.listen() # setting the server into listening mode
        self.game_ui.label.setText("Server started, waiting for the client...")

        self.Form_sign_ui.show()
        sys.exit(self.app.exec_())

    def socketConnection(self):
        self.conn, self.addr = self.s.accept()  # waits for the client

        self.clientConnected = True

        try:
            network.socketConnection(self, "server")
        except ConnectionResetError:
            self.showWarning("Opponent left the game!", close_program=True)
        finally:
            self.clientConnected = False
            self.conn.close()
        
    def send(self, msg):
        self.conn.send(pickle.dumps(msg))

    def signIn(self):
        super().signIn()

        T = Thread(target=self.socketConnection, daemon=True) # creating a new thread for the socket connection
        T.start()
        
    def placeShips(self):
        super().placeShips()
        if self.userShipsPlaced and self.opponentShipsPlaced:
            self.setShootTurn(1)

s = Server()