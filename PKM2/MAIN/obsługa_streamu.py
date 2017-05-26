import numpy
import cv2
from ALGORYTMY.peron import peron
from ALGORYTMY.zajezdnia import zajezdnia
from ALGORYTMY.Adam_ruch import ruchomy
from ALGORYTMY.reka import reka
from ALGORYTMY.twarz import twarz
from ALGORYTMY.przeszkody import  przeszkody
from ALGORYTMY.banan import banan
from ALGORYTMY.train import pociag

import numpy as np
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from cv2 import __version__

zajezdnia_lower_value = (0,0,240)
zajezdnia_upper_value = (50,255,255)

Lower = (0, 120, 0)
Upper = (3, 255, 255)

# inicjalizacja flag



def przetwarzajSTREAM(zajezdniaPrzetwarzaj, peronPrzetwarzaj,przeszkodyPtrzewarzaj,
                      rekaPrzetwarzaj, twarzPrzetwarzaj, ruchPrzetwarzaj,czerwonyPrzetwarzaj,
                      bananPrzetwarzaj):
    zatrzask=0
    url = 'http://192.168.2.1/?action=stream'
    stream = requests.get(url, stream=True)
    bytes = b''

    track_window = 0
    term_crit = 0
    roi_hist = 0
    if rekaPrzetwarzaj:
        track_window, term_crit, roi_hist = initReka()

    counter_proste = 0
    counter_widac_tory = 0
    licznik_ruch = 0

    while True:
        bytes += stream.raw.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # ------------------ insert algorythms HERE ------------------

            # zajezdniaPrzetwarzaj,
            # peronPrzetwarzaj,
            # przeszkodyPtrzewarzaj,
            # rekaPrzetwarzaj,
            # twarzPrzetwarzaj,
            # ruchPrzetwarzaj,
            # bananPrzetwarzaj)
            if zajezdniaPrzetwarzaj:
                zajezdnia(frame,zajezdnia_lower_value,zajezdnia_upper_value)
            if peronPrzetwarzaj:
                zatrzask = peron(frame, Lower, Upper, zatrzask)

            if przeszkodyPtrzewarzaj:
                counter_proste, counter_widac_tory = przeszkody(frame, counter_proste, counter_widac_tory)
            if rekaPrzetwarzaj:
                track_window, term_crit, roi_hist = reka(frame, track_window, term_crit, roi_hist)
            if ruchPrzetwarzaj:
                licznik_ruch = ruchomy(frame,licznik_ruch)
            if twarzPrzetwarzaj:
                twarz(frame)
            if czerwonyPrzetwarzaj:
                pociag(frame)
            if bananPrzetwarzaj:
                banan(frame)


            # Display
            cv2.imshow('Video', frame)
            # ------------------ algorythms end HERE ------------------
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit(0)

    camera.release()
    cv2.destroyAllWindows()


def initReka():
    r, a, c, b = 100, 200, 100, 150
    track_window = (r, a, c, b)
    x, y, w, h, = 100, 100, 400, 400
    frames = cv2.imread('./INNE/ramka.jpg')
    obrazDloni = frames[y:y + h, x:x + w]
    # Dobor odpowiedniej maski filtrujaca nasza dlon z niepotrzebnych elementow
    dlonHsv = cv2.cvtColor(obrazDloni, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(dlonHsv, np.array((80., 90., 110.)), np.array((190., 160., 255.)))
    mask2 = cv2.inRange(dlonHsv, np.array((0., 98., 90.)), np.array((35., 183., 194.)))
    # Obliczenie histogramu naszej dloni
    roi_hist = cv2.calcHist([dlonHsv], [0, 1], mask, [180, 250], [0, 180, 0, 360])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    return track_window,term_crit,roi_hist