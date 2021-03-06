#python_version 2.7
#opencv_verison 3.1

import cv2
import numpy as np

video = cv2.VideoCapture('C:\Users\Dawid\PycharmProjects\PKM\przeszkody.avi')

while(video.isOpened()):

    # pobieramy ramke
    _, frame = video.read()
    # wycinamy fragment, na ktorym widac tory
    subframe = frame[300:600, 150:350]


    # konwertujemy BGR do HSV
    hsv = cv2.cvtColor(subframe, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # definiujemy zakres koloru brazowego (mozna tutaj jeszcze poeksperymentowac)
    lower_brown = np.array([0, 0, 0])
    upper_brown = np.array([30, 100, 130])

    # maskowanie w celu uzyskania tylko brazowgo koloru
    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    # Thresholding, ktorego celem jest zdefiniowanie obszaru widocznosci torow
    thresh = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    derp, cnts, cos = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # tutaj przechowujemy obszary
    contours = []

    for c in cnts:
        # ignorowanie zbyt malych obszarow
        if cv2.contourArea(c) < 7000:
            continue
        else:
            widac_tory = True
            contours.append(cv2.contourArea(c))
            # naniesienie ramki
            #(x, y, w, h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if(not widac_tory):
        cv2.putText(frame,'PRZESZKODA!',(30,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255))
    else:
        #fragment kodu potrzebny do pozniejszego ulepszenia algorytmu
        max_contour = max(contours)
        print(max_contour)

    widac_tory = False

    cv2.imshow('frame',frame)

    # warunek ktory zapewnia odstep miedzy klatkami i umozliwajacy wyjscia
    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()