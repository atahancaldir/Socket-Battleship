import socket
from threading import Thread
from game import *
import pickle

class Server(Game):
    def __init__(self):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind(self.ADDR)
        except socket.error as e:
            self.game_ui.label.setText("Connection failed!")
        
        self.s.listen()
        self.game_ui.label.setText("Server started, waiting for the client...")

        T = Thread(target=self.socketConnection, daemon=True)
        T.start()

        self.Form_sign_ui.show()
        sys.exit(self.app.exec_())

    def socketConnection(self):
        self.conn, self.addr = self.s.accept()  # waits for the client

        self.clientConnected = True
        while self.clientConnected:
            msg = pickle.loads(self.conn.recv(self.HEADER))
            if msg:
                print(msg)
                if msg == self.DISCONNECT_MSG:
                    self.clientConnected = False

                elif not self.opponentName:
                    self.game_ui.oppname_label.setText(msg)
                    self.game_ui.tableWidget.setDisabled(False)
                    self.game_ui.tableWidget_2.setDisabled(False)
                    self.placeShips()

                    self.send(self.username)
                    self.opponentName = True

                elif msg == self.ALL_SHIPS_PLACED:
                    self.opponentShipsPlaced = True
                    if self.userShipsPlaced:
                        self.setShootTurn(1)

        self.conn.close()
        self.gameOver()

    def send(self, msg):
        self.conn.send(pickle.dumps(msg))

    def gameOver(self):
        pass

    def placeShips(self):
        super().placeShips()
        if self.userShipsPlaced and self.opponentShipsPlaced:
            self.setShootTurn(1)

s = Server()