import pickle
from PyQt5 import QtGui, QtCore, QtWidgets


# tableWidget: left table(user's table)
# tableWidget_2: right table(opponent's table)

def socketConnection(node, nodeType):
    if nodeType == "client":
        connected = node.connected # client's boolean value to keep connection status
    else:
        connected = node.clientConnected # server's boolean value to keep connection status

    while connected: # it will listen for a message while the connection is available
                if nodeType == "client":
                    msg = pickle.loads(node.client.recv(node.HEADER)) # getting message from the server and unpacking it using pickle (client)
                else:
                    msg = pickle.loads(node.conn.recv(node.HEADER)) # getting message from the server and unpacking it using pickle (server)
                if msg: # if message is not empty, it will process it
                    print(msg) # printing the message to check if things work correctly
                    if not node.opponentName: # for the first received message, we expect it to be the opponent's name
                        node.game_ui.oppname_label.setText(msg) # placing opponent's name to the GUI
                        node.game_ui.tableWidget.setDisabled(False) # making the user's table unselectable to wait the game to start
                        node.game_ui.tableWidget_2.setDisabled(False) # making the opponent's table unselectable to wait the game to start
                        node.placeShips() # asks the user to start to place his/her ships on the tables because we know that opponent is ready as well
                        
                        if nodeType == "server":
                            node.send(node.username) # server sends its username after getting the client's username

                        node.opponentName = True # it will not consider the next messages as the opponent's name

                    if msg == node.DISCONNECT_MSG: # if the opponent quits, we get this message
                        connected = False

                    elif msg == node.ALL_SHIPS_PLACED: # if the opponent placed all of his/her ships, we get this message
                        node.opponentShipsPlaced = True
                        if node.userShipsPlaced: # if the user also finished placing the ships
                            if nodeType == "client":
                                node.setShootTurn(0) # the shoot turn is on the opponent
                            else:
                                node.setShootTurn(1) # the shoot turn is on us

                    elif msg == node.ALL_SHIPS_DESTROYED: # if the opponent's all ships are destroyed, we get this message
                        node.showWarning("Congratulations, " + node.username + "! You won!", "Game End", True)
                        
                    elif type(msg) == type(tuple()): # if the message is a tuple (other ones are strings)
                        if len(msg) == 2: # if the tuple has 2 items (in this case, items are the x and y values of the shooted table cell by the opponent.)
                            try:
                                if node.game_ui.tableWidget.item(msg[0], msg[1]).text(): # if the table button is not empty
                                    node.game_ui.tableWidget.item(msg[0], msg[1]).setBackground(QtGui.QColor(255,0,0)) # set color to red
                                    node.playBombSound() # play bomb explosion sound

                                    node.gotShootCount += 1 # counts our destroyed ships
                                    if node.gotShootCount == 14: # if all of our ships are destroyed
                                        node.send(node.ALL_SHIPS_DESTROYED) # notify the opponent that it won the game
                                        node.showWarning("You lost, " + node.username + "! Go and learn more!", "Game End", True) # show a warning to user
                                    else:
                                        node.send((node.SHOOT_SUCCESSFULL, msg[0], msg[1])) #if we still have undestroyed ships, notify opponent that it made a successful shot but the game goes on
                                        
                            except: # if the table button is empty (opponent made a missed shot)
                                item = QtWidgets.QTableWidgetItem("X") # create a table item with "X" written on it
                                item.setTextAlignment(QtCore.Qt.AlignCenter) # align the text to center
                                item.setBackground(QtGui.QColor(0,255,0)) # set green color
                                node.game_ui.tableWidget.setItem(msg[0], msg[1], item) # add the item to the right coordinates in the left table
                                
                                node.playMissSound() # plays the bomb missed sound
                                node.send((node.SHOOT_MISSED, msg[0], msg[1])) # notify the opponent that it made a missed shot

                            node.setShootTurn(1) # change the shoot turn to user(us)

                        if len(msg) == 3: # if the tuple has 3 items (in this case, opponent sends us a feedback after we shoot him/her and tuple values are success/fail status of the shoot, and x and y values of the shooted coordinates)
                            node.game_ui.tableWidget_2.clearSelection() # deselect all items on the tables
                            if msg[0] == node.SHOOT_SUCCESSFULL: # if we shot the opponent successfully
                                node.game_ui.tableWidget_2.setItem(msg[1], msg[2], QtWidgets.QTableWidgetItem()) # put an empty item to the correct coordinates on the right table
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setBackground(QtGui.QColor(0,255,0)) # make the item green
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setTextAlignment(QtCore.Qt.AlignCenter) # align the texts of the item
                                node.game_ui.tableWidget_2.item(msg[1], msg[2]).setText("H") # write "H" on the item
                                node.playBombSound() # play the bomb explotion sound

                            elif msg[0] == node.SHOOT_MISSED: # if we made a missed shout
                                item = QtWidgets.QTableWidgetItem("X") # create an item with "X" written on it
                                item.setTextAlignment(QtCore.Qt.AlignCenter) # align the text on the item
                                item.setBackground(QtGui.QColor(255,0,0)) # make the item red colored
                                node.game_ui.tableWidget_2.setItem(msg[1], msg[2], item) # put the item to the right coordinates on the right table
                                
                                node.playMissSound() # play the bomb missed sound