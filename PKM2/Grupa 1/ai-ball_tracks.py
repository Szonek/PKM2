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
        counter_widac_tory = 0
        counter_proste = 0
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
                    # wycinamy fragment, na ktorym widac tory
                    subframe = frame[200:350, 150:350]

                    # zmiennne uzywane do wykrywania krawedzi
                    empty = True
                    gray = frame[200:400, 150:350]

                    # konwertujemy BGR do HSV
                    hsv = cv2.cvtColor(subframe, cv2.COLOR_BGR2HSV)
                    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    # definiujemy zakres koloru brazowego (mozna tutaj jeszcze poeksperymentowac)
                    lower_brown = np.array([0, 15, 21])
                    upper_brown = np.array([46, 106, 130])

                    # maskowanie w celu uzyskania tylko brazowgo koloru
                    mask = cv2.inRange(hsv, lower_brown, upper_brown)

                    # Thresholding, ktorego celem jest zdefiniowanie obszaru widocznosci torow
                    thresh = cv2.threshold(mask, 25, 30, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    derp, cnts, cos = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # tutaj przechowujemy obszary
                    contours = []

                    for c in cnts:
                        # ignorowanie zbyt malych obszarow
                        if cv2.contourArea(c) < 9000:
                            continue
                        else:
                            widac_tory = True
                            counter_widac_tory = 20
                            contours.append(cv2.contourArea(c))
                            # #naniesienie ramki
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(subframe, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # wykrywanie krawedzi
                    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                    minLineLength = 80
                    numberOfLines = 0
                    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                                            minLineLength=minLineLength, maxLineGap=10)
                    if lines is None:
                        empty = False

                    if (empty):
                        a, b, c = lines.shape
                        for i in range(a):
                            if (abs(lines[i][0][2] - lines[i][0][0]) < 50):
                                cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
                                         (0, 0, 255), 3, cv2.LINE_AA)
                                numberOfLines += 1

                    if (numberOfLines > 2):
                        counter_proste = 15
                    elif (numberOfLines == 0):
                        counter_proste -= 1

                    if (counter_proste <= 1):
                        cv2.putText(frame, 'ZAKRET ALBO PRZESZKODA', (30, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                    (255, 255, 255))

                    if (counter_widac_tory <= 0 and counter_proste <= 0):
                        cv2.putText(frame, 'PRZESZKODA!', (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
                    else:
                        # fragment kodu potrzebny do pozniejszego ulepszenia algorytmu
                        if (widac_tory):
                            max_contour = max(contours)
                            # print(max_contour)

                    widac_tory = False
                    counter_widac_tory -= 1
                    print(counter_proste)




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