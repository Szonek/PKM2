# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from cv2 import __version__


def nothing(x):
    pass

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
        font = cv2.FONT_HERSHEY_SIMPLEX
        bytes = b''
        cv2.namedWindow('image')
        #cap = cv2.VideoCapture('peroniki_long.avi')
        cv2.createTrackbar('HLo', 'image', 0, 255, nothing)
        cv2.createTrackbar('HUp', 'image', 120, 255, nothing)
        cv2.createTrackbar('SLo', 'image', 0, 255, nothing)
        cv2.createTrackbar('SUp', 'image', 255, 255, nothing)
        cv2.createTrackbar('VLo', 'image', 240, 255, nothing)
        cv2.createTrackbar('VUp', 'image', 255, 255, nothing)
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
                    #obraz = frame[120:250, 315:450]
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    hlo = cv2.getTrackbarPos('HLo', 'image')
                    hup = cv2.getTrackbarPos('HUp', 'image')
                    slo = cv2.getTrackbarPos('SLo', 'image')
                    sup = cv2.getTrackbarPos('SUp', 'image')
                    vlo = cv2.getTrackbarPos('VLo', 'image')
                    vup = cv2.getTrackbarPos('VUp', 'image')

                    lower_value = np.array([hlo, slo, vlo])
                    upper_value = np.array([hup, sup, vup])

                    mask = cv2.inRange(hsv, lower_value, upper_value)

                    res = cv2.bitwise_and(frame, frame, mask=mask)

                    res2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
                    res2 = cv2.medianBlur(res2, 15)
                    #ret, im = cap.read()
                    #blur = cv2.GaussianBlur(im, (0, 0), 1)
                    # cv2.imwrite('MyPic.jpg', blur)

                    # Display the resulting frame
                    cv2.imshow('frame', frame)
                    cv2.imshow('mask', mask)
                    cv2.imshow('res', res)
                    cv2.imshow('res2', res2)
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


print('OpenCV version',__version__)
url = 'http://192.168.2.1/?action=stream'
cam = Cam(url)
cam.start()