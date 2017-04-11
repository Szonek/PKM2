import numpy as np
import cv2
from matplotlib import pyplot as plt


#Wersja opencv 3
class HandDetection:

    def __init__(self,name):
        self.cap = cv2.VideoCapture(name)
        # Obraz dlolni ktory bedzie wykorzystany jako punkt odniesienia dla algorytmu
        frames = cv2.imread('ramka.jpg')
        # Rozmiar ramki pokazujacej dlon
        r, a, c, b = 100, 200, 100, 150
        self.track_window = (r, a, c, b)
        # Wyciencie samej dloni z obrazu testowego
        x, y, w, h, = 100, 100, 400, 400
        obrazDloni = frames[y:y + h, x:x + w]
        # Dobor odpowiedniej maski filtrujaca nasza dlon z niepotrzebnych elementow
        dlonHsv = cv2.cvtColor(obrazDloni, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(dlonHsv, np.array((80., 90., 110.)), np.array((190., 160., 255.)))
        mask2 = cv2.inRange(dlonHsv, np.array((0., 98., 90.)), np.array((35., 183., 194.)))
        # Obliczenie histogramu naszej dloni
        self.roi_hist = cv2.calcHist([dlonHsv], [0, 1], mask, [180, 250], [0, 180, 0, 360])
        cv2.normalize( self.roi_hist,  self.roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    def start(self):
        while (1):
            ret, frame = self.cap.read()
            # Odcinami dolna czesc obrazu poniewaz dlon kolorystycznie jest podobna do piasku przy torach
            frame = frame[0:500]

            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Funkcja porownujaca histogram modeluz histogramem z pojedynczej ramki
                dst = cv2.calcBackProject([hsv], [0, 1], self.roi_hist, [0, 180, 0, 250], 2)
                dst = cv2.medianBlur(dst, 3)  # powoduje usuniecie niektorych szumow do testowania

                # Funkcja szukajaca srodka masy tzn przesuwa okno w miejsce wiekszego zagesczenia dst
                ret, self.track_window = cv2.meanShift(dst, self.track_window, self.term_crit)
                x, y, w, h = self.track_window

                # Pobieramy ramke z obrazu rozkladu prawdobodobientwa znalezienia tego samego histogramu
                ramka = dst[y:y + h, x:x + w]
                print(np.sum(ramka))
                # pewnego rodzaju treshold ktory eliminuje szumy i powoduje ze nie pojawia sie obramowanie
                if np.sum(ramka) > 10000:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), 100, 2)
                cv2.imshow('img2', frame)
                cv2.imshow('imsg2', dst)

                k = cv2.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv2.imwrite(chr(k) + ".jpg", frame)



if __name__ == "__main__":
    program = HandDetection('filmiki/przeszkody.avi')
    program.start()