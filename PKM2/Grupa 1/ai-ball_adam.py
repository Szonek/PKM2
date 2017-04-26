# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from cv2 import __version__

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
        fgbg = cv2.createBackgroundSubtractorMOG2()
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
                    height, width = frame.shape[:2]
                    prev_frame = np.zeros([130, width])
                    history = 4

                    obraz = frame[350:height]
                    fgmask = fgbg.apply(obraz, learningRate=1.0 / history)
                    gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

                    # dif = frame - prev_frame;

                    prev_frame = gray

                    # first = fgmask[0:350,0:50]

                    uklad = np.sum(fgmask)
                    print(uklad)
                    if (uklad < 40000):
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, 'stoi', (100, 100), font, 3, (255, 255, 255), 2)
                    else:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, 'Jedzie', (100, 100), font, 3, (255, 255, 255), 2)

                    # cv2.imshow('first', first)
                    cv2.imshow('frame', fgmask)
                    cv2.imshow('frames', frame)
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        cv2.imwrite('trz_ramka.jpg', frame)
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


print('OpenCV version',__version__)
url = 'http://192.168.2.1/?action=stream'
cam = Cam(url)
cam.start()