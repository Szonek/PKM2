import numpy
import cv2
from ALGORYTMY.peron import peron
from ALGORYTMY.zajezdnia import zajezdnia
from ALGORYTMY.Adam_ruch import ruch
from ALGORYTMY.reka import reka
import numpy as np


zajezdnia_lower_value = (0,0,240)
zajezdnia_upper_value = (50,255,255)

Lower = (0, 120, 0)
Upper = (3, 255, 255)



def przetwarzajfilm(sciezka,peronPrzetwarzaj,przeszkodyPtrzewarzaj,rekaPrzetwarzaj):
    camera = cv2.VideoCapture(sciezka)
    # inicjalizacja flag
    zatrzask=0
    track_window, term_crit, roi_hist = 0
    if rekaPrzetwarzaj:
        track_window, term_crit, roi_hist = initReka()

    counter_proste = 0
    counter_widac_tory = 0
    licznik_ruch =0
    while (camera.isOpened()):
        ret, frame = camera.read()

        if peronPrzetwarzaj:
            zatrzask=peron(frame,Lower,Upper,zatrzask)
        if przeszkodyPtrzewarzaj:
            counter_proste,counter_widac_tory = przeszkodyPtrzewarzaj(frame,counter_proste,counter_widac_tory)
        # if ruchPrzetwarzaj:
        #     licznikruch = (frame,licznik_ruch)
        if rekaPrzetwarzaj:
            track_window, term_crit, roi_hist = reka(frame, track_window, term_crit, roi_hist)

       # if zajezdniaPrzetwarzaj:
        #    zajezdnia(frame,zajezdnia_lower_value,zajezdnia_upper_value)

        # wlasne przetwarzanie


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('frame', frame)

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