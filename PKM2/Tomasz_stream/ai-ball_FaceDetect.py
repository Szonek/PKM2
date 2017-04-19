# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

#Haar's method face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class Cam():
    def __init__(self, url):

        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print("camera initialised")

    def start(self):
        self.thread.start()
        print("camera stream started")

    def run(self):
        bytes = b''
        while not self.thread_cancelled:
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #------------------ insert algorythms HERE ------------------
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

                    # Display the resulting frame
                    cv2.imshow('Video', frame)
                    # ------------------ algorythms end HERE ------------------
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        exit(0)
            except ThreadError:
                self.thread_cancelled = True

    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        self.thread_cancelled = True
        # block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True



url = 'http://192.168.2.1/?action=stream'
cam = Cam(url)
cam.start()