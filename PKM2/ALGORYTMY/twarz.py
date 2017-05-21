import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def twarz(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(20, 20),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

        # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return frame