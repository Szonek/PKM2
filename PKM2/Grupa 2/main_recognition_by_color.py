from collections import deque
import numpy as np
import argparse
import imutils
import cv2


# definiujemy zakresy koloru HSV
redLower = (0, 110, 0)
redUpper = (3, 255, 255)




#pobieramy nasz film
camera = cv2.VideoCapture("czysty.avi")


while (camera.isOpened()):
    #pobieramy aktualn¹ klatkê filmu do przetwarzania
    (grabbed, frame) = camera.read()
    #zawê¿amy zakres poszukiwañ
    obraz = frame[0:800, 400:800]


    
    #przechodzimy z RGB na HSV
    hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)

    #nak³adamy maskê oraz poszukujemy takich zakresów kolorów w danej klatce
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    #odfiltrowujemy ma³e i niepoprawne skupiska koloru
    if len(cnts) > 3:
        #wypisujemy napis na danej klatce
        cv2.putText(frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
