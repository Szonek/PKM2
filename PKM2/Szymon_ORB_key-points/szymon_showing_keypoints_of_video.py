import cv2


# opencv 2.4 + python 2.7 !!!!!!!!!

print cv2.__version__
winName = 'Keypointy w video'
video = cv2.VideoCapture("przeszkody.avi")


while(video.isOpened()):
    _, frame = video.read()

   # kpInFrame, desInFrame = orb.detectAndCompute(frame, None)
    _, frame = video.read()
    orb = cv2.ORB()
    kp2, des2 = orb.detectAndCompute(frame, None)

    imgKP2 = cv2.drawKeypoints(frame, kp2)
    cv2.imshow('a', imgKP2)

    # warunek ktory zapewnia odstep miedzy klatkami i umozliwa wyjscia
    if (cv2.waitKey(10) & 0xFF == ord('q')):
            break



video.release()
cv2.destroyAllWindows()


