from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cv2
import numpy as np
import os

tel = {'peron':True,'zajezdnia':False,'reka':False,'tory':False,"czerwony":False,'twarz':False}
cap = cv2.VideoCapture("zajezdnia3.avi")

class Okno(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui',self)       
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        self.ui.button_nagranie_start.clicked.connect(self.nagranie_start)
       # self.ui.button_kalibruj.clicked.connect(self.kalibruj_start)
        
        #if self.ui.comboBox.currentIndex = 0:
                
            
            
    def stream_start(self):
        print("Start detekcji na strumieniu: \n")
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            #  tel.zajezdnia = True
            print("Detekcja zajezdni aktywna")
        if self.ui.detekcja_perony_checkBox.isChecked():
            # tel.peron = True
            print("Detekcja peronow aktywna")
        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            # tel.tory = True
            print("Detekcja przeszkod aktywna")
        if self.ui.detekcja_twarz_checkBox.isChecked():
            # tel.twarz = True
            print("Detekcja twarzy aktywna")
        if self.ui.detekcja_reka_checkBox.isChecked():
            #  tel.reka = True
            print("Detekcja ruchu reka aktywna")
        if self.ui.detekcja_ruch_checkBox.isChecked():
            print("Detekcja ruchu pociagu aktywna")                                       
                
    def nagranie_start(self):
        print("Start detekcji na nagraniu: \n")
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            print("Detekcja zajezdni aktywna")
            # tel.zajezdnia = True
        if self.ui.detekcja_perony_checkBox.isChecked():
            print("Detekcja peronow aktywnea")
            #tel.peron = True
        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            print("Detekcja przeszkod aktywna")
            #tel.tory = True
        if self.ui.detekcja_twarz_checkBox.isChecked():
            print("Detekcja twarzy aktywna")
            #tel.twarz = True
        if self.ui.detekcja_reka_checkBox.isChecked():
            print("Detekcja ruchu reka aktywna")
            #tel.reka = True
        if self.ui.detekcja_ruch_checkBox.isChecked():  
            print("Detekcja ruchu pociagu aktywna")   
            
   # def kalibruj(self):
        
            
        
if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    sys.exit(qApp.exec_())

