from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cv2
import numpy as np

cap = cv2.VideoCapture("zajezdnia3.avi")


class Okno(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui',self)       
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        #self.ui.button_nagranie_start.clicked.connect(self.nagranie_start)
        #self.ui.button_kalibruj.clicked.connect(self.kalibruj_start)
        
                
    def stream_start(self):
        while(1):
            if self.ui.detekcja_zajezdnia_checkBox.isChecked():
                print("Zajezdnia")
                _,img = cap.read()
                cv2.imshow("Stream", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            if self.ui.detekcja_perony_checkBox.isChecked():
                print("Peron")
                
            
    
    #def nagranie_start(self):
        
    #def kalibruj(self):
        
            
        
if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    sys.exit(qApp.exec_())


#self.ui.detekcja_perony_checkBox.isChecked()
#self.ui.detekcja_perony_checkBox.isChecked()
#self.ui.detekcja_przeszkody_checkBox.isChecked()
#self.ui.detekcja_reka_checkBox.isChecked()
#self.ui.detekcja_twarz_checkBox.isChecked()
#self.ui.detekcja_ruch_checkBox.isChecked()
#self.ui.kalibruj_perony_checkBox.isChecked()
s#elf.ui.kalibruj_zajezdnia_checkBox.isChecked()

#kalibruj_perony_checkBox
#kalibruj_zajezdnia_checkBox
#detekcja_zajezdnia_checkBox
#detekcja_perony_checkBox
#detekcja_przeszkody_checkBox
#detekcja_reka_checkBox
#detekcja_twarz_checkBox
#detekcja_ruch_checkBox