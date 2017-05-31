from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cv2
import numpy as np
import os

#Zdecydowac ktora opcje tel wybieramy
tel = {'peron':False,'zajezdnia':False,'reka':False,'przeszkody':False,"czerwony":False,'twarz':False, 'ruch':False, 'banan':False}

#A to gdzie ? 
#os.system("python skryptRozdzielajacy.py "+str(filmOrCam)+ " czysty.avi "+str(tel))

class Okno(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui',self)
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        self.ui.button_nagranie_start.clicked.connect(self.nagranie_start)
        self.ui.button_kalibruj.clicked.connect(self.kalibruj_start)
      
    
    def kalibruj_start(self):
        os.system("python obsluga_kalibratora.py ")

    def stream_start(self):
        
        filmOrCam = 2      
        print("\nStart detekcji na strumieniu: \n")
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            tel['zajezdnia'] = True
            print("Detekcja zajezdni aktywna")
        else:
            tel['zajezdnia'] = False
            
        if self.ui.detekcja_perony_checkBox.isChecked():
            tel['peron'] = True
            print("Detekcja peronow aktywna")
        else:
            tel['peron'] = False
            
        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            tel['przeszkody'] = True
            print("Detekcja przeszkod aktywna")
        else:
            tel['przeszkody'] = False
            
        if self.ui.detekcja_twarz_checkBox.isChecked():
            tel['twarz'] = True
            print("Detekcja twarzy aktywna")
        else:
            tel['twarz'] = False
            
        if self.ui.detekcja_reka_checkBox.isChecked():
            tel['reka'] = True
            print("Detekcja ruchu reka aktywna")
        else:
            tel['reka'] = False
            
        if self.ui.detekcja_ruch_checkBox.isChecked():
            tel['ruch'] = True
            print("Detekcja ruchu pociagu aktywna")
        else:
            tel['ruch'] = False
            
        if self.ui.detekcja_czerwony_pociag_checkBox.isChecked():
            tel['czerwony'] = True
            print("Detekcja czerwonego pociągu aktywna")
        else:
            tel['czerwony'] = False

        if self.ui.detekcja_banan_checkBox.isChecked():
            tel['banan'] = True
            print("Detekcja banana aktywna")
        else:
            tel['banan'] = False

        os.system("python skryptRozdzielajacy.py " + str(3) + " czysty.avi " + str(tel))
                              
    def nagranie_start(self):
        
        filmOrCam = 1      
        print("\nStart detekcji na nagraniu: \n")
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            tel['zajezdnia'] = True
            print("Detekcja zajezdni aktywna")
            
        if self.ui.detekcja_perony_checkBox.isChecked():
            tel['peron'] = True
            print("Detekcja peronow aktywna")

        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            tel['przeszkody'] = True
            print("Detekcja przeszkod aktywna")

        if self.ui.detekcja_twarz_checkBox.isChecked():
            tel['twarz'] = True
            print("Detekcja twarzy aktywna")

        if self.ui.detekcja_reka_checkBox.isChecked():
            tel['reka'] = True
            print("Detekcja ruchu reka aktywna")

        if self.ui.detekcja_ruch_checkBox.isChecked(): 
            tel['ruch'] = True
            print("Detekcja ruchu pociagu aktywna")   
            
        if self.ui.detekcja_czerwony_pociag_checkBox.isChecked():
            tel['czerwony'] = True
            print("Detekcja czerwonego pociągu aktywna")  
            
        if self.ui.detekcja_banan_checkBox.isChecked():
            tel['banan'] = True
            print("Detekcja banana aktywna")

        os.system("python skryptRozdzielajacy.py " + str(filmOrCam) + " czysty.avi " + str(tel))
        print(tel)
        
if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    sys.exit(qApp.exec_())

