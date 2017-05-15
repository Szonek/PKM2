from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cv2
import numpy as np
import os

class Okno(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui',self)       
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        self.ui.button_nagranie_start.clicked.connect(self.nagranie_start)
        self.ui.button_kalibruj.clicked.connect(self.kalibruj_start)
        
                
    def stream_start(self):
            if self.ui.detekcja_zajezdnia_checkBox.isChecked():
                tel.zajezdnia = True
            if self.ui.detekcja_perony_checkBox.isChecked():
                tel.peron = True
            if self.ui.detekcja_przeszkody_checkBox.isChecked():
                tel.tory = True
            if self.ui.detekcja_twarz_checkBox.isChecked():
                tel.twarz = True
            if self.ui.detekcja_reka_checkBox.isChecked():
                tel.reka = True
            if self.ui.detekcja_ruch_checkBox.isChecked():
                                                              
                
    def nagranie_start(self):
            if self.ui.detekcja_zajezdnia_checkBox.isChecked():
                tel.zajezdnia = True
            if self.ui.detekcja_perony_checkBox.isChecked():
                tel.peron = True
            if self.ui.detekcja_przeszkody_checkBox.isChecked():
                tel.tory = True
            if self.ui.detekcja_twarz_checkBox.isChecked():
                tel.twarz = True
            if self.ui.detekcja_reka_checkBox.isChecked():
                tel.reka = True
            if self.ui.detekcja_ruch_checkBox.isChecked():  
            
    def kalibruj(self):
        
            
        
if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    sys.exit(qApp.exec_())

