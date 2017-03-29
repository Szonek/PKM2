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