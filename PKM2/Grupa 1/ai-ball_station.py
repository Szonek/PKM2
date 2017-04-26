# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

from collections import deque
import numpy as np
import argparse
#import imutils

#ustawiamy parametru HSV koloru jaki ma zostac wykryty
Lower = (0, 120, 0)
Upper = (3, 255, 255)
#inicjalizujemy parametry naszego obramowania ==0

offset=10 #offset do obramowania
font = cv2.FONT_HERSHEY_SIMPLEX

class Cam():
    def __init__(self, url):

        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print("camera initialised")

    def start(self):
        self.thread.start()
        print("camera stream started")

    def run(self):
        bytes = b''
        while not self.thread_cancelled:
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #------------------ insert algorythms HERE ------------------
                    #(grabbed, frame) = camera.read()
                    obraz = frame[0:400, 400:616]  # zmniejszamy nasz obraz,ktory bedziemy przetwarzac
                    hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)  # zamiana na HSV
                    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # odcien szarosci
                    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
                    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                                cv2.CHAIN_APPROX_SIMPLE)  # wynajdywanie krawedzi

                    mask = cv2.inRange(hsv, Lower,
                                       Upper)  # sprawdzamy czy gdzies na obrazku znajduje sie nasz szukany kolor
                    mask = cv2.erode(mask, None, iterations=2)  # usuwamy wszelkie drobne
                    mask = cv2.dilate(mask, None, iterations=2)  # bloby ktore zostaly na naszej masce
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,  # wyszukujemy konturow naszego koloru
                                            cv2.CHAIN_APPROX_SIMPLE)[
                        -2]  # [-2] jest dodane aby kod byl kompatybilny z dwoma wersjami opencv
                    n = 0  # zerujemy zmienna zliczajaca wystapienia pikseli w konturze
                    maxy = 0
                    maxx = 0
                    miny = 0
                    minx = 0
                    if len(cnts) > 1:  # jesli znajdziemy interesujacy nasz kolor wtedy wykonuje sie algorytm
                        minx = cnts[0][0][0][0]  # ustawiamy minimalna wartosc x
                        miny = cnts[0][0][0][1]  # ustawiamy minimalna wartosc y
                        for x in range(len(cnts)):  # przeszukujemy liste w poszukiwaniu najwiekszych oraz
                            for y in range(
                                    len(cnts[x])):  # najmniejszych wartosci w ramach ktorych znajduje sie nasz kolor
                                if cnts[x][y][0][0] > maxx:
                                    maxx = cnts[x][y][0][0]
                                if cnts[x][y][0][0] < minx:
                                    minx = cnts[x][y][0][0]
                                if cnts[x][y][0][1] > maxy:
                                    maxy = cnts[x][y][0][1]
                                if cnts[x][y][0][1] < miny:
                                    miny = cnts[x][y][0][1]

                        for x in range(
                                len(contours)):  # nastepnie poszukujemy czy w obszarze w ktorym znajduje sie nasz kolor
                            for y in range(len(contours[x])):  # wystepuja jakies kontury
                                if contours[0][0][0][0] > minx + offset & contours[0][0][0][0] < maxx + offset & \
                                        contours[0][0][0][1] > miny + offset & contours[0][0][0][1] < maxy + offset:
                                    n = n + 1;  # zliczamy ile pikseli wchodzi w sklad wszystkich konturow,poniewaz funkcja FindContours z
                                    if n > 50:  # z parametrem Retr tree zwraca tylko co ktorys piksel ktory wchodzi w sklad danego
                                        maxy = 0  # konturu
                                        maxx = 0  # przy liczbie wiekszej niz 50 jestemy juz pewni w naszym obszarze znajduje sie
                                        miny = 0  # odpowiednia liczba konturow,ktora wskazuje na nasz peron
                                        minx = 0  # liczba ta zostala uzyskana z kilku prob wykonanych na screenach wykonanych z tego
                                        break  # filmu.
                                        # Nastepnie zerujemy nasze wartosci graniczne

                    if n > 50:  # jesli juz 'n' jest takie jak powinno wypisujemy na ekranie napis mowiacy o wystapieniu peronu
                        cv2.putText(frame, 'Peron', (100, 100), font, 3, (255, 255, 255), 2)
                    # cv2.imshow("Frame", obraz) #opcjonale pokazanie fragmentu obrazu ktory bedziemy przetwarzac

                    # Display the resulting frame
                    cv2.imshow("mask", frame)  # pokazac pelnego obrazu
                    # ------------------ algorythms end HERE ------------------
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        exit(0)
            except ThreadError:
                self.thread_cancelled = True

    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        self.thread_cancelled = True
        # block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True



url = 'http://192.168.2.1/?action=stream'
cam = Cam(url)
cam.start()