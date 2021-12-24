# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def FaceRec(self):
        from FaceRec3 import FaceRec
        self.window = QtWidgets.QMainWindow()
        self.ui = FaceRec()
        self.ui.setupUi(self.window, self.main_window)
        self.window.show()
        self.main_window.hide()

    def AddUser(self):
        from NewFace import Ui_NewFaceWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_NewFaceWindow()
        self.ui.setupUi(self.window, self.main_window)
        self.window.show()
        self.main_window.hide()

    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 867)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 290, 201, 71))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 420, 201, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton_2.clicked.connect(self.startDetection)
        self.pushButton.clicked.connect(self.addNewUser)
        
        self.main_window.setStyleSheet("background-color: #191919;")
        self.pushButton.setStyleSheet("color: white; border: 2px solid white;")
        self.pushButton_2.setStyleSheet("color: white; border: 2px solid white;")


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Register new face"))
        self.pushButton_2.setText(_translate("MainWindow", "Start Recognition"))

    def startDetection(self):
        self.FaceRec()

    def addNewUser(self):
        self.AddUser()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

