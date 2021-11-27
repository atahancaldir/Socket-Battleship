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
            msg_length = self.conn.recv(self.HEADER).decode("utf-8")
            if msg_length:
                msg_length = int(msg_length)
                msg = self.conn.recv(msg_length).decode("utf-8")
                print(msg)
                if msg == self.DISCONNECT_MSG:
                    self.clientConnected = False

                if self.send_key:
                    self.send()
                    self.send_key = False

        self.conn.close()
        self.gameOver()

    def send(self):
        self.conn.send(self.send_msg.encode("utf-8"))

    def gameOver(self):
        pass

s = Server()