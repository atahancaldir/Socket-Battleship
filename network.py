import pickle
from PyQt5 import QtGui, QtCore, QtWidgets

def socketConnection(node, nodeType):
    if nodeType == "client":
        connected = node.connected
    else:
        connected = node.clientConnected
    while connected: # it will listen for a message while the connection is available
                if nodeType == "client":
                    msg = pickle.loads(node.client.recv(node.HEADER)) # getting message from the server and unpacking it using pickle
                else:
                    msg = pickle.loads(node.conn.recv(node.HEADER))
                if msg: # if message is not empty, it will process it
                    print(msg) # printing the message to check if things work correctly
                    if not node.opponentName: # for the first received message, we expect it to be the opponent's name
                        node.game_ui.oppname_label.setText(msg) # placing opponent's name to the GUI
                        node.game_ui.tableWidget.setDisabled(False)
                        node.game_ui.tableWidget_2.setDisabled(False)
                        node.placeShips() # asks the user to start to place his/her ships on the tables because we know that opponent is ready as well

                        if nodeType == "server":
                            node.send(node.username)

                        node.opponentName = True # it will not consider the next messages as the opponent's name

                    if msg == node.DISCONNECT_MSG: # if the opponent quits, we get this message
                        connected = False

                    elif msg == node.ALL_SHIPS_PLACED: # if the opponent placed all of his/her ships, we get this message
                        node.opponentShipsPlaced = True
                        if node.userShipsPlaced: # if the user also finished placing the ships
                            if nodeType == "client":
                                node.setShootTurn(0) # the shoot turn will be on the opponent
                            else:
                                node.setShootTurn(1)

                    elif msg == node.ALL_SHIPS_DESTROYED: # if the opponent's all ships are destroyed, we get this message
                        node.showWarning("Congratulations, " + node.username + "! You won!", "Game End", True)
                        
                    elif type(msg) == type(tuple()): # if the message is a tuple (other ones are strings)
                        if len(msg) == 2: # if the tuple has 2 items (in this case, items are the x and y values of the shooted table cell by the opponent.)
                            try:
                                if node.game_ui.tableWidget.item(msg[0], msg[1]).text():
                                    node.game_ui.tableWidget.item(msg[0], msg[1]).setBackground(QtGui.QColor(255,0,0))
                                    node.playBombSound()

                                    node.gotShootCount += 1
                                    if node.gotShootCount == 14:
                                        node.send(node.ALL_SHIPS_DESTROYED)
                                        node.showWarning("You lost, " + node.username + "! Go and learn more!", "Game End", True)
                                    else:
                                        node.send((node.SHOOT_SUCCESSFULL, msg[0], msg[1]))
                                        
                            except:
                                item = QtWidgets.QTableWidgetItem("X")
                                item.setTextAlignment(QtCore.Qt.AlignCenter)
                                item.setBackground(QtGui.QColor(0,255,0))
                                node.game_ui.tableWidget.setItem(msg[0], msg[1], item)
                                
                                node.playMissSound()
                                node.send((node.SHOOT_MISSED, msg[0], msg[1]))

                            node.setShootTurn(1)

                        if len(msg) == 3: # if the tuple has 3 items (in this case, opponent sends us a feedback after we shoot him/her and tuple values are success/fail status of the shoot, and x and y values of the shooted coordinates)
                            node.game_ui.tableWidget_2.clearSelection()
                            if msg[0] == node.SHOOT_SUCCESSFULL:
                                node.game_ui.tableWidget_2.setItem(msg[1], msg[2], QtWidgets.QTableWidgetItem())
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setBackground(QtGui.QColor(0,255,0))
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setTextAlignment(QtCore.Qt.AlignCenter)
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setText("H")
                                node.playBombSound()

                            elif msg[0] == node.SHOOT_MISSED:
                                item = QtWidgets.QTableWidgetItem("X")
                                item.setTextAlignment(QtCore.Qt.AlignCenter)
                                item.setBackground(QtGui.QColor(255,0,0))
                                node.game_ui.tableWidget_2.setItem(msg[1], msg[2], item)
                                
                                node.playMissSound()

    if nodeType == "server":
        node.conn.close()