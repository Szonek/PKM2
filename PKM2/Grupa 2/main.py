import numpy as np
import cv2

cap = cv2.VideoCapture('filmiki/przeszkody.avi')
fgbg = cv2.createBackgroundSubtractorMOG2()

ret, frame = cap.read()
height, width = frame.shape[:2]
prev_frame = np.zeros([130, width])

while(cap.isOpened()):
    ret, frame = cap.read()
    history = 4

    obraz = frame[350:height]
    fgmask = fgbg.apply(obraz, learningRate=1.0/history)
    gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)


    #dif = frame - prev_frame;

    prev_frame = gray

    #first = fgmask[0:350,0:50]

    uklad = np.sum(fgmask)
    print(uklad)
    if(uklad < 40000):
     font = cv2.FONT_HERSHEY_SIMPLEX
     cv2.putText(frame, 'stoi', (100, 100), font, 3, (255, 255, 255), 2)
    else:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Jedzie', (100, 100), font, 3, (255, 255, 255), 2)


    #cv2.imshow('first', first)
    cv2.imshow('frame',fgmask)
    cv2.imshow('frames', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('trz_ramka.jpg',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()