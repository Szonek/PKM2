# Python version 3.6

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError


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
                    img = frame

                    # color conversion
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    # ranges of depot colors
                    zajezdnia_lower = np.array([0, 0, 220], np.uint8)
                    zajezdnia_upper = np.array([50, 255, 255], np.uint8)

                    # searching in defined range
                    zajezdnia = cv2.inRange(hsv, zajezdnia_lower, zajezdnia_upper)

                    # morphological transformation, dilation
                    kernal = np.ones((5, 5), "uint8")
                    zajezdnia = cv2.dilate(zajezdnia, kernal)
                    res = cv2.bitwise_and(img, img, mask=zajezdnia)

                    # object contours function
                    (_, contours, hierarchy) = cv2.findContours(zajezdnia, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    # depot tracking
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 3000 and area < 12000):
                            x, y, w, h = cv2.boundingRect(contour)
                            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                            cv2.putText(img, "  ZAJEZDNIA WRZESZCZ   ", (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.4,
                                        (0, 0, 255))

                    # Display the resulting frame
                    cv2.imshow("Depot Tracking", img)
                    cv2.imshow('',res)
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