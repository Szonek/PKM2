import cv2
import numpy as np

video = cv2.VideoCapture('C:\Users\Dawid\PycharmProjects\PKM\przeszkody.avi')

while(video.isOpened()):

    # Take each frame
    _, frame = video.read()
    subframe = frame[300:550, 150:350]

    # Convert BGR to HSV
    hsv = cv2.cvtColor(subframe, cv2.COLOR_BGR2HSV)


    # define range of blue color in HSV
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([30, 100, 130])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #upiekszenia
    thresh = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    derp, cnts, cos = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for c in cnts:
        # ignorowanie zbyt malych obszarow
        if cv2.contourArea(c) < 7000:
            continue
           #naniesienie ramki
        #(x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        widactory = True

    if(not widactory):
        cv2.putText(frame,'mamy przeszkode',(30,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))

    widactory = False
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()