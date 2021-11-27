import socket
import pickle
from threading import Thread
from game import *

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

        while self.connected: # it will listen for a message while the connection is available
            msg = pickle.loads(self.client.recv(self.HEADER)) # getting message from the server and unpacking it using pickle
            if msg: # if message is not empty, it will process it
                print(msg) # printing the message to check if things work correctly
                if not self.opponentName: # for the first received message, we expect it to be the opponent's name
                    self.game_ui.oppname_label.setText(msg) # placing opponent's name to the GUI
                    self.game_ui.tableWidget.setDisabled(False)
                    self.game_ui.tableWidget_2.setDisabled(False)
                    self.placeShips() # asks the user to start to place his/her ships on the tables because we know that opponent is ready as well

                    self.opponentName = True # it will not consider the next messages as the opponent's name

                if msg == self.DISCONNECT_MSG: # if the opponent quits, we get this message
                    self.connected = False

                elif msg == self.ALL_SHIPS_PLACED: # if the opponent placed all of his/her ships, we get this message
                    self.opponentShipsPlaced = True
                    if self.userShipsPlaced: # if the user also finished placing the ships
                        self.setShootTurn(0) # the shoot turn will be on the opponent

                elif msg == self.ALL_SHIPS_DESTROYED: # if the opponent's all ships are destroyed, we get this message
                    self.showWarning("Congratulations, " + self.username + "! You won!", "Game End", True)
                    
                elif type(msg) == type(tuple()): # if the message is a tuple (other ones are strings)
                    if len(msg) == 2: # if the tuple has 2 items (in this case, items are the x and y values of the shooted table cell by the opponent.)
                        try:
                            if self.game_ui.tableWidget.item(msg[0], msg[1]).text():
                                self.game_ui.tableWidget.item(msg[0], msg[1]).setBackground(QtGui.QColor(255,0,0))
                                self.playBombSound()

                                self.gotShootCount += 1
                                if self.gotShootCount == 14:
                                    self.send(self.ALL_SHIPS_DESTROYED)
                                    self.showWarning("You lost, " + self.username + "! Go and learn more!", "Game End", True)
                                else:
                                    self.send((self.SHOOT_SUCCESSFULL, msg[0], msg[1]))
                                    
                        except:
                            item = QtWidgets.QTableWidgetItem("X")
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setBackground(QtGui.QColor(0,255,0))
                            self.game_ui.tableWidget.setItem(msg[0], msg[1], item)
                            
                            self.playMissSound()
                            self.send((self.SHOOT_MISSED, msg[0], msg[1]))

                        self.setShootTurn(1)

                    if len(msg) == 3: # if the tuple has 3 items (in this case, opponent sends us a feedback after we shoot him/her and tuple values are success/fail status of the shoot, and x and y values of the shooted coordinates)
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