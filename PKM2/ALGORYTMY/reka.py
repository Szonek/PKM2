import numpy as np
import cv2


#TODO Przed odpaleniem zczytywania obrzu trzeba dodac taie cos (przed łówną pętlą)
# r, a, c, b = 100, 200, 100, 150
# track_window = (r, a, c, b)

def reka( frame, track_window, term_crit, roi_hist ):
    # Obraz dlolni ktory bedzie wykorzystany jako punkt odniesienia dla algorytmu

    # Rozmiar ramki pokazujacej dlon

    # Wyciencie samej dloni z obrazu testowego



    # Odcinami dolna czesc obrazu poniewaz dlon kolorystycznie jest podobna do piasku przy torach
    frame = frame[0:500]


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Funkcja porownujaca histogram modeluz histogramem z pojedynczej ramki
    dst = cv2.calcBackProject([hsv], [0, 1], roi_hist, [0, 180, 0, 250], 2)
    dst = cv2.medianBlur(dst, 3)  # powoduje usuniecie niektorych szumow do testowania

    # Funkcja szukajaca srodka masy tzn przesuwa okno w miejsce wiekszego zagesczenia dst
    ret, track_window = cv2.meanShift(dst, track_window,term_crit)
    x, y, w, h = track_window

    # Pobieramy ramke z obrazu rozkladu prawdobodobientwa znalezienia tego samego histogramu
    ramka = dst[y:y + h, x:x + w]
    # pewnego rodzaju treshold ktory eliminuje szumy i powoduje ze nie pojawia sie obramowanie
    if np.sum(ramka) > 10000:
        cv2.rectangle(frame, (x, y), (x + w, y + h), 100, 2)

    return  track_window, term_crit, roi_hist

