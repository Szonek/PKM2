import numpy as np
import cv2

def ruchomy(frame,licznik,fgbg):
    height, width = frame.shape[:2]
    prev_frame = np.zeros([130, width])


    history = 4

    obraz = frame[350:height]
    fgmask = fgbg.apply(obraz, learningRate=1.0/history)
    gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

    prev_frame = gray

    uklad = np.sum(fgmask)

    font = cv2.FONT_HERSHEY_SIMPLEX
    if(uklad < 40000):
     licznik-=1
    elif (uklad > 40000):
     licznik =6

    if(licznik <=0):
        cv2.putText(frame, 'stoi', (100, 100), font, 3, (255, 255, 255), 2)

    if(licznik > 0):
        cv2.putText(frame, 'Jedzie', (100, 100), font, 3, (255, 255, 255), 2)

    return licznik

