import numpy as np
import cv2

#Wersja opencv 2.4.13.2
cap = cv2.VideoCapture('przeszkody.avi')
#inicjalizacja obiektu odpowiedzialneo za porywnywanie klatek
fgbg = cv2.BackgroundSubtractorMOG()

ret, frame = cap.read()
height, width = frame.shape[:2]
prev_frame = np.zeros([130, width])

while(cap.isOpened()):
    ret, frame = cap.read()

    # w tym miejscu okreslony czestotliwosc odswiezania historii
    history = 30

    #Sprawdzamy tylko dolna czesc obrazu
    obraz = frame[350:height]
    #Porownanie nowej klatki  z ostatnio zapisana klatka
    fgmask = fgbg.apply(obraz, learningRate=1.0/history)
    gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

    prev_frame = gray

    #Sprawdzamy czy sa jakies rozniece miedzy nimi 
    uklad = np.sum(fgmask)
    if(uklad == 0):
     font = cv2.FONT_HERSHEY_SIMPLEX
     cv2.putText(frame, 'stoi', (10, 500), font, 4, (255, 255, 255), 2)
    else:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Jedzie', (100, 100), font, 3, (255, 255, 255), 2)

    #qcv2.imshow('first', first)
    #cv2.imshow('frame',fgmask)
    cv2.imshow('frames', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('ramka.jpg',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()