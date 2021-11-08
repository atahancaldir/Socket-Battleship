from playsound import playsound

from PyQt5 import QtCore, QtGui, QtWidgets
from QT_designs import main_ui, sign_in_ui

import sys
import os

class Player():
    def __init__(self):
        # sound effects
        self.bomb_sound = os.path.join(os.getcwd(), "Sounds", "bomb_sound.mp3")
        self.miss_sound = os.path.join(os.getcwd(), "Sounds", "miss_sound.mp3")
        self.put_ship_sound = os.path.join(os.getcwd(), "Sounds", "put_ship_sound.mp3")

        self.isShipPlaced = {"Carrier": False, "Battleship": False, "Submarine": False, "Destroyer": False}
        self.currentShip = None
        self.shipSizes = {"Carrier": 5, "Battleship": 4, "Submarine": 3, "Destroyer": 2}

        self.selectedCells = set()

        # for PyQt5
        self.app = QtWidgets.QApplication(sys.argv)

        # initializing sign-in window
        self.Form_sign_ui = QtWidgets.QWidget()
        self.sign_ui = sign_in_ui.Ui_Form()
        self.sign_ui.setupUi(self.Form_sign_ui)

        # initializing main window
        self.Form_game_ui = QtWidgets.QWidget()
        self.game_ui = main_ui.Ui_Form()
        self.game_ui.setupUi(self.Form_game_ui)

        # button events
        self.sign_ui.pushButton.clicked.connect(self.signIn)
        self.sign_ui.lineEdit.returnPressed.connect(self.signIn)
        self.game_ui.placeShipButton.clicked.connect(self.checkShipPlacement)
        self.game_ui.leaveButton.clicked.connect(self.leaveGame)

        self.game_ui.tableWidget.selectionModel().selectionChanged.connect(self.tableSelectionChanged)

        self.Form_sign_ui.show()
        sys.exit(self.app.exec_())

    def tableSelectionChanged(self, selected, deselected):
        for i in selected.indexes():
            self.selectedCells.add((i.row(), i.column()))
        
        for i in deselected.indexes():
            self.selectedCells.remove((i.row(), i.column()))

    def signIn(self):
        if not self.sign_ui.lineEdit.text():
            self.showWarning("Enter a valid username!")
            return

        self.game_ui.username_label.setText(self.sign_ui.lineEdit.text())
        self.Form_sign_ui.close()
        self.Form_game_ui.show()

        self.placeShips()

    def placeShips(self):
        for ship, value in self.isShipPlaced.items():
            if value == False:
                self.game_ui.label.setText("Place the " + ship + " to your table (Size: " + str(self.shipSizes[ship]) + ")")
                self.currentShip = ship
                return

        self.game_ui.label.setText("")
        self.game_ui.tableWidget.setSelectionMode(self.game_ui.tableWidget.NoSelection)
        self.game_ui.tableWidget.clearSelection()

        self.game_ui.tableWidget_2.setSelectionMode(self.game_ui.tableWidget.SingleSelection)

        self.game_ui.placeShipButton.setDisabled(True)

    def checkShipPlacement(self):
        if len(self.selectedCells) != self.shipSizes[self.currentShip]:
            self.showWarning("Selection does not match with the ship size!")
            return
        
        for i in self.selectedCells:
            connected = False

            for j in self.selectedCells:
                if ((i[0] == j[0]-1 or i[0] == j[0]+1) and i[1] == j[1]) or (i[0] == j[0] and (i[1] == j[1]-1 or i[1] == j[1]+1)):
                    connected = True
                elif (i[0] == j[0]-1 or i[0] == j[0]+1) and (i[1] == j[1]-1 or i[1] == j[1]+1):
                    connected = True

            try:
                if self.game_ui.tableWidget.item(i[0], i[1]).text():
                    self.showWarning("Selected cells are not empty!")
                    return
            except:
                pass

            if not connected:
                self.showWarning("Selection does not connected!")
                return

        linearRow = True
        linearCol = True
        col, row = None, None
        for i in self.selectedCells:
            if not row:
                row = i[0]
            if not col:
                col = i[1]

            if i[0] != row:
                linearRow = False
            if i[1] != col:
                linearCol = False

        if linearCol or linearRow:
            for cell in self.selectedCells:
                item = QtWidgets.QTableWidgetItem(self.currentShip[0].upper())
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.game_ui.tableWidget.setItem(cell[0], cell[1], item)

        else:
            self.showWarning("Selection is not linear!")
            return

        self.isShipPlaced[self.currentShip] = True
        self.playPutShipSound()
        self.placeShips()

    def playBombSound(self):
        playsound(self.bomb_sound, block=False)

    def playMissSound(self):
        playsound(self.miss_sound, block=False)

    def playPutShipSound(self):
        playsound(self.put_ship_sound, block=False)

    def showWarning(self, text, title="Warning!"):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)

        msgBox.exec()

    def leaveGame(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Are you sure you want to leave the game?")
        msgBox.setWindowTitle("Leaving")
        msgBox.addButton(QtWidgets.QMessageBox.Yes)
        msgBox.addButton(QtWidgets.QMessageBox.No)

        bttn = msgBox.exec_()

        if bttn == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

client = Player()
client.playBombSound()