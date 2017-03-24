# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize th
# list of tracked points
greenLower = (0, 100, 140)
greenUpper = (40, 255, 255)
# if a video path was not supplied, grab the reference
# to the webcam


# otherwise, grab a reference to the video file

camera = cv2.VideoCapture("czysty.avi")

# keep looping
while (camera.isOpened()):
    # grab the current frame
    (grabbed, frame) = camera.read()
    obraz = frame[0:800, 400:800]

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video

    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 10:
        cv2.putText(frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()