import numpy
import cv2
from ALGORYTMY.peron import peron
from ALGORYTMY.zajezdnia import zajezdnia

zajezdnia_lower_value = (0,0,240)
zajezdnia_upper_value = (50,255,255)

Lower = (0, 120, 0)
Upper = (3, 255, 255)


def przetwarzajfilm(sciezka,peronPrzetwarzaj):
    camera = cv2.VideoCapture(sciezka)
    while (camera.isOpened()):
        ret, frame = camera.read()

        if peronPrzetwarzaj:
            peron(frame,Lower,Upper)
        if zajezdniaPrzetwarzaj:
            zajezdnia(frame,zajezdnia_lower_value,zajezdnia_upper_value)




        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('frame', frame)

    camera.release()
    cv2.destroyAllWindows()
