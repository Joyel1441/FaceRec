from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

import cv2
import face_recognition
import pickle

known_faces = []
usr_names = []

with open('saved_embeds.pt', 'rb') as f:
    known_faces = pickle.load(f)

with open('usr_names.pt', 'rb') as f:
    usr_names = pickle.load(f)

face_locations = []
face_encodings = []
face_names = []
frame_number = 0

class FaceRec(object):

    def Main(self, MainWindow):
        from mainScreen import Ui_MainWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.facerec_window.hide()

    def setupUi(self, FaceRecWindow, MainWindow):
        self.main_window = MainWindow
        self.facerec_window = FaceRecWindow
        FaceRecWindow.setObjectName("FaceRecWindow")
        FaceRecWindow.resize(1110, 834)
        self.centralwidget = QtWidgets.QWidget(FaceRecWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, -30, 1091, 811))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.FeedLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FeedLabel.setObjectName("label")
        self.verticalLayout.addWidget(self.FeedLabel)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("Cancel")
        self.verticalLayout.addWidget(self.pushButton)
        FaceRecWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FaceRecWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
        self.menubar.setObjectName("menubar")
        FaceRecWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FaceRecWindow)
        self.statusbar.setObjectName("statusbar")
        FaceRecWindow.setStatusBar(self.statusbar)

        self.Worker1 = Worker1()
        self.Worker1.start()

        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

        self.pushButton.clicked.connect(self.CancelFeed)

        self.facerec_window.setStyleSheet("background-color: #191919;")
        self.pushButton.setStyleSheet("color: white; border: 2px solid white;")
        self.FeedLabel.setStyleSheet("color: white;")

        self.retranslateUi(FaceRecWindow)
        QtCore.QMetaObject.connectSlotsByName(FaceRecWindow)


    def retranslateUi(self, FaceRecWindows):
        _translate = QtCore.QCoreApplication.translate
        FaceRecWindows.setWindowTitle(_translate("FaceRecWindow", "FaceRecWindow"))
        self.FeedLabel.setText(_translate("FaceRecWindow", "Starting..."))
        self.pushButton.setText(_translate("FaceRecWindow", "Cancel"))

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop() 
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
    
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.5)
                    name = None

                    for i in range(len(match)):
                        if match[i]:
                            name = usr_names[i]
                            print(name)
                            break
                            
                
                    face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    if not name:
                        continue

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


                ConvertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)

                

    def stop(self):
        self.ThreadActive = False
        self.quit()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FaceRecWindow = QtWidgets.QMainWindow()
    ui = FaceRec()
    ui.setupUi(FaceRecWindow)
    FaceRecWindow.show()
    sys.exit(app.exec_())

