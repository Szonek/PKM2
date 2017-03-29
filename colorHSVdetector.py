import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('image')
cap = cv2.VideoCapture(0)
cv2.createTrackbar('HLo','image',0,255,nothing)
cv2.createTrackbar('HUp','image',120,255,nothing)
cv2.createTrackbar('SLo','image',0,255,nothing)
cv2.createTrackbar('SUp','image',255,255,nothing)
cv2.createTrackbar('VLo','image',240,255,nothing)
cv2.createTrackbar('VUp','image',255,255,nothing)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hlo = cv2.getTrackbarPos('HLo','image')
    hup = cv2.getTrackbarPos('HUp', 'image')
    slo = cv2.getTrackbarPos('SLo', 'image')
    sup = cv2.getTrackbarPos('SUp', 'image')
    vlo = cv2.getTrackbarPos('VLo', 'image')
    vup = cv2.getTrackbarPos('VUp', 'image')

    lower_value = np.array([hlo,slo,vlo])
    upper_value = np.array([hup,sup,vup])

    mask = cv2.inRange(hsv, lower_value, upper_value)

    res = cv2.bitwise_and(frame,frame,mask= mask)

    res2 = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    res2 = cv2.medianBlur(res2,15)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res', res)
    cv2.imshow('res2', res2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()