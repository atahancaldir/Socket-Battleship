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

                elif type(msg) == type(tuple()):
                    if len(msg) == 2:
                        try:
                            if self.game_ui.tableWidget.item(msg[0], msg[1]).text():
                                self.game_ui.tableWidget.item(msg[0], msg[1]).setBackground(QtGui.QColor(255,0,0))
                                self.playBombSound()
                                
                                self.gotShootCount += 1
                                if self.gotShootCount == 14:
                                    self.send(self.ALL_SHIPS_DESTROYED)
                                else:
                                    self.send((self.SHOOT_SUCCESSFULL, msg[0], msg[1]))
                                    
                        except:
                            item = QtWidgets.QTableWidgetItem("X")
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setBackground(QtGui.QColor(0,255,0))
                            self.game_ui.tableWidget.setItem(msg[0], msg[1], item)

                            self.playMissSound()
                            self.send((self.SHOOT_MISSED, msg[0], msg[1]))

                    if len(msg) == 3:
                        self.game_ui.tableWidget_2.clearSelection()
                        if msg[0] == self.SHOOT_SUCCESSFULL:
                            self.game_ui.tableWidget_2.setItem(msg[1], msg[2], QtWidgets.QTableWidgetItem())
                            self.game_ui.tableWidget_2.item(msg[1], msg[2]).setBackground(QtGui.QColor(0,255,0))
                            self.game_ui.tableWidget_2.item(msg[1], msg[2]).setText("H")
                            self.playBombSound()

                        elif msg[0] == self.SHOOT_MISSED:
                            item = QtWidgets.QTableWidgetItem("X")
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setBackground(QtGui.QColor(255,0,0))
                            self.game_ui.tableWidget_2.setItem(msg[1], msg[2], item)

                            self.playMissSound()

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