import socket
from _thread import *
import pickle
from game import Game


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

    def threaded_client(self, conn, addr):
        self.game_ui.label.setText("Client connected")

        self.connected = True
        while self.connected:
            msg_length = conn.recv(self.HEADER).decode("utf-8")
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode("utf-8")
                if msg == self.DISCONNECT_MSG:
                    self.connected = False

        """
        #conn.send(pickle.dumps(players[player]))
        reply = ""
        while True:
            try:
                #data = pickle.loads(conn.recv(2048))  # how many bits received show
                players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1: reply = players[0]
                    else: reply = players[1]
                    print("Received: ", data)
                    print("Sending: ", reply)

                conn.sendall(pickle.dumps(reply))
            except:
                break
        
        print("Lost connection")
        conn.close()
        """

while True:
    conn, addr = s.accept()  # accept connection
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1