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
                    if len(msg) == 2:
                        print(type(self.game_ui.tableWidget.item(msg[0], msg[1])))
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
                            self.game_ui.tableWidget_2.item(msg[1], msg[2]).setBackground(QtGui.QColor(0,255,0))
                            self.game_ui.tableWidget_2.item(msg[1], msg[2]).setText("H")
                            self.playBombSound()

                        elif msg[0] == self.SHOOT_MISSED:
                            item = QtWidgets.QTableWidgetItem("X")
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setBackground(QtGui.QColor(255,0,0))
                            self.game_ui.tableWidget_2.setItem(msg[1], msg[2], item)
                            
                            
                            self.playMissSound()
    
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