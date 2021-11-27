import socket
from threading import Thread
from game import *

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

        self.game_ui.tableWidget.setDisabled(False)
        self.game_ui.tableWidget_2.setDisabled(False)
        self.placeShips()

        self.clientConnected = True
        while self.clientConnected:
            msg = self.conn.recv(self.HEADER).decode("utf-8")
            if msg:
                print(msg)
                if msg == self.DISCONNECT_MSG:
                    self.clientConnected = False

                if not self.opponentName:
                    self.game_ui.oppname_label.setText(msg)
                    self.opponentName = True
                    self.send(self.username)

        self.conn.close()
        self.gameOver()

    def send(self, msg):
        self.conn.send(msg.encode("utf-8"))

    def gameOver(self):
        pass

s = Server()