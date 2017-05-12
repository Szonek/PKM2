import numpy
import cv2
from ALGORYTMY.peron import peron


Lower = (0, 120, 0)
Upper = (3, 255, 255)


def przetwarzajfilm(sciezka,peronPrzetwarzaj):
    camera = cv2.VideoCapture(sciezka)
    while (camera.isOpened()):
        ret, frame = camera.read()

        if peronPrzetwarzaj:
            peron(frame,Lower,Upper)




        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('frame', frame)

    camera.release()
    cv2.destroyAllWindows()