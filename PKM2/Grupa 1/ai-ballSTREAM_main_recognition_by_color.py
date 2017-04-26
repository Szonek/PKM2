# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from cv2 import __version__

from collections import deque
# definiujemy zakresy koloru HSV
redLower = (0, 110, 0)
redUpper = (3, 255, 255)

#inicjalizujemy parametry naszego obramowania ==0
maxy=0
maxx=0
miny=0
minx=0
offset=10 #offset do obramowania
zatrzask=0
peron=False


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
                    obraz = frame[0:800, 400:800]
                    hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)

                    # nak³adamy maskê oraz poszukujemy takich zakresów kolorów w danej klatce
                    mask = cv2.inRange(hsv, redLower, redUpper)
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)[-2]
                    center = None

                    # odfiltrowujemy ma³e i niepoprawne skupiska koloru
                    if len(cnts) > 3:
                        # wypisujemy napis na danej klatce
                        cv2.putText(frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
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