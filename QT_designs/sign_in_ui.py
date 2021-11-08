# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign_in_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 134)
        Form.setFixedSize(411, 134)
        Form.setStyleSheet("background:black;")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 371, 23))
        self.lineEdit.setStyleSheet("background:white;")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 151, 16))
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(310, 90, 80, 23))
        self.pushButton.setStyleSheet("background:green;")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "BattleShip - Atahan Caldir & Musa Berkay Kocabasoglu"))
        self.label.setText(_translate("Form", "Enter your username"))
        self.pushButton.setText(_translate("Form", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

