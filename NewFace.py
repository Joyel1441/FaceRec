from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

import cv2
import face_recognition
import pickle
import numpy
from PIL import ImageQt
import os

Image = None


class Ui_NewFaceWindow(object):
    def Main(self, MainWindow):
        from mainScreen import Ui_MainWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.facerec_window.hide()

    def setupUi(self, NewFaceWindow, MainWindow):
        self.new_face_window = NewFaceWindow
        self.main_window = MainWindow
        self.facerec_window = NewFaceWindow
        NewFaceWindow.setObjectName("NewFaceWindow")
        NewFaceWindow.resize(1159, 853)
        self.centralwidget = QtWidgets.QWidget(NewFaceWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, -30, 1161, 821))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.Feedlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Feedlabel.setObjectName("label")
        self.verticalLayout.addWidget(self.Feedlabel)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)


        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)

        NewFaceWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NewFaceWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1159, 26))
        self.menubar.setObjectName("menubar")
        NewFaceWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NewFaceWindow)
        self.statusbar.setObjectName("statusbar")
        NewFaceWindow.setStatusBar(self.statusbar)

        self.Worker1 = Worker1()
        self.Worker1.start()

        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)


        self.exitButton.clicked.connect(self.CancelFeed)
        self.pushButton.clicked.connect(self.Capture)

        self.facerec_window.setStyleSheet("background-color: #191919; color: white;")
        self.exitButton.setStyleSheet("color: white; border: 1px solid white;")
        self.pushButton.setStyleSheet("color: white; border: 1px solid white;")


        self.retranslateUi(NewFaceWindow)
        QtCore.QMetaObject.connectSlotsByName(NewFaceWindow)

    def retranslateUi(self, NewFaceWindow):
        _translate = QtCore.QCoreApplication.translate
        NewFaceWindow.setWindowTitle(_translate("NewFaceWindow", "NewFaceWindow"))
        self.Feedlabel.setText(_translate("NewFaceWindow", "Starting..."))
        self.pushButton.setText(_translate("NewFaceWindow", "Capture"))
        self.exitButton.setText(_translate("NewFaceWindow", "Exit"))

    
    def ImageUpdateSlot(self, Image):
        self.Feedlabel.setPixmap(QPixmap.fromImage(Image))
    

    def CancelFeed(self):
        self.Worker1.stop() 
        self.Main(self.main_window)

    def Capture(self):
        self.Worker1.stop()
        img_name, done = QtWidgets.QInputDialog.getText(self.facerec_window, 'Enter name', 'Enter your name:')


        if done:
            usr_names = []

            image = ImageQt.fromqimage(self.Feedlabel.pixmap().toImage())
            image.save('train.jpg')

            image = face_recognition.load_image_file("train.jpg")
            face_encoding = []

            try:
                face_encoding = face_recognition.face_encodings(image)[0]
                try:
                    with open('usr_names.pt', 'rb') as f:
                        usr_names = pickle.load(f)
                except:
                    pass

                usr_names = usr_names + [img_name]

                with open('usr_names.pt', 'wb') as f:
                    pickle.dump(usr_names, f)

                known_faces = []
                
                try:
                    with open('saved_embeds.pt', 'rb') as f:
                        known_faces = pickle.load(f)
                except:
                    pass
                
                known_faces = known_faces + [face_encoding]

                with open('saved_embeds.pt', 'wb') as f:
                    pickle.dump(known_faces, f)

                os.remove('train.jpg')
                self.Main(self.main_window)
            except:
                print("Face not detected")
                os.remove('train.jpg')
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Face not detected, Try again")
                msg.setWindowTitle("Face not detected")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

                msg.exec_()
                self.Main(self.main_window)
        else:
            self.Main(self.main_window)

  



class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        img = None
        count = 0
        name_list =[]
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)

                

    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewFaceWindow = QtWidgets.QMainWindow()
    ui = Ui_NewFaceWindow()
    ui.setupUi(NewFaceWindow)
    NewFaceWindow.show()
    sys.exit(app.exec_())
