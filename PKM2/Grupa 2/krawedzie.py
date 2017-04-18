import numpy as np
import cv2
counter = 0
video = cv2.VideoCapture('C:\Users\Dawid\PycharmProjects\PKM\przeszkody.avi')


while(video.isOpened()):
    empty = True
    _, frame = video.read()
    frame = frame[200:400, 150:350]
    gray = frame
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 100
    numberOfLines = 0
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=10)
    if lines is None:
        empty = False

    # else:
    #     print(lines.__len__())

    if(empty):
        a, b, c = lines.shape
        for i in range(a):
            if (abs(lines[i][0][2] - lines[i][0][0])<50):
                cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
                numberOfLines+=1


    if(numberOfLines >2):
        counter = 15
    elif(numberOfLines == 0):
        counter-=1

    if(counter>2):
        cv2.putText(frame, 'PROSTA!', (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    print(counter)

    cv2.imshow('frame1', gray)

        # warunek ktory zapewnia odstep miedzy klatkami i umozliwajacy wyjscia
    if (cv2.waitKey(1) & 0xFF == ord('q')):
       break