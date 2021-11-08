# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os

bomb_icon = os.path.join(os.getcwd(), "Image", "bomb.png")

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1031, 505)
        Form.setFixedSize(1031, 505)
        Form.setStyleSheet("background:black;")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 500, 351))
        self.frame_2.setStyleSheet("background:white;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.username_label = QtWidgets.QLabel(self.frame_2)
        self.username_label.setGeometry(QtCore.QRect(0, 0, 500, 30))
        self.username_label.setMouseTracking(True)
        self.username_label.setTabletTracking(False)
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 30, 500, 321))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        for i in range(10):
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
        
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
################
        header = self.tableWidget.horizontalHeader()
        for i in range(10):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
##################
        
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(520, 10, 500, 351))
        self.frame_3.setStyleSheet("background:white;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.oppname_label = QtWidgets.QLabel(self.frame_3)
        self.oppname_label.setGeometry(QtCore.QRect(0, 0, 500, 30))
        self.oppname_label.setMouseTracking(False)
        self.oppname_label.setTabletTracking(False)
        self.oppname_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.oppname_label.setFont(font)
        self.oppname_label.setObjectName("oppname_label")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.frame_3)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 30, 500, 321))
        self.tableWidget_2.setStyleSheet("")
        self.tableWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_2.setDragEnabled(False)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(10)
        self.tableWidget_2.setRowCount(10)
        self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget_2.setSelectionMode(self.tableWidget_2.NoSelection)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        for i in range(10):
            self.tableWidget_2.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            
            self.tableWidget_2.setHorizontalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)

################
        header = self.tableWidget_2.horizontalHeader()
        for i in range(10):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
##################

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 380, 1011, 41))
        font = QtGui.QFont()
        font.setFamily("Lato Medium")
        font.setPointSize(14)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("background:#00a0ff;\n"
"border-radius:15px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.shootButton = QtWidgets.QPushButton(Form)
        self.shootButton.setGeometry(QtCore.QRect(10, 430, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Lato Medium")
        font.setPointSize(14)
        self.shootButton.setFont(font)
        self.shootButton.setStyleSheet("background:#15b237;\n"
"border-radius:15px;")
        self.shootButton.setObjectName("shootButton")

        self.placeShipButton = QtWidgets.QPushButton(Form)
        self.placeShipButton.setGeometry(QtCore.QRect(121, 430, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Lato Medium")
        font.setPointSize(14)
        self.placeShipButton.setFont(font)
        self.placeShipButton.setStyleSheet("background:#f9c17f;\n"
"border-radius:15px;")
        self.placeShipButton.setObjectName("placeShipButton")

        self.leaveButton = QtWidgets.QPushButton(Form)
        self.leaveButton.setGeometry(QtCore.QRect(920, 430, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Lato Medium")
        font.setPointSize(14)
        self.leaveButton.setFont(font)
        self.leaveButton.setStyleSheet("background:#f2353b;\n"
"border-radius:15px;")
        self.leaveButton.setObjectName("leaveButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "BattleShip - Atahan Caldir & Musa Berkay Kocabasoglu"))
        self.username_label.setText(_translate("Form", "<USERNAME>"))
        self.oppname_label.setText(_translate("Form", "<OPPONENT_NAME>"))

        col_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        for i in range(10):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Form", str(i+1)))

            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Form", col_names[i]))

            item = self.tableWidget_2.verticalHeaderItem(i)
            item.setText(_translate("Form", str(i+1)))

            item = self.tableWidget_2.horizontalHeaderItem(i)
            item.setText(_translate("Form", col_names[i]))
        
        self.label.setText(_translate("Form", "Status"))
        self.leaveButton.setText(_translate("Form", "Leave"))
        self.placeShipButton.setText(_translate("Form", "Place Ship"))
        self.shootButton.setText(_translate("Form", "Shoot!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

