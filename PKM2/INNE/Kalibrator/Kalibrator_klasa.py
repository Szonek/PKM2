import cv2
import time
import threading
import numpy as np

def nothing(x):
    pass

class Kal():
    def __init__(self):
        self.frame=None
        self.wyswietlaj=False
        self.wylacz=False
        self.thread_cancelled = False
        self.thread = threading.Thread(target=self.run)
        self.peronWys = False
        self.zajezdniaWys = True

    def start(self):
        self.thread.setDaemon(True)
        self.thread.start()

    def setFrame(self,obraz,wys):
        self.frame=obraz
        self.wyswietlaj=wys

    def breakclass(self):
        return self.wylacz

    def zajezdnia(self,frame, lower_value, upper_value):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # searching in defined range
        zajezdnia2 = cv2.inRange(hsv, lower_value, upper_value)

        # morphological transformation, dilation
        kernal = np.ones((5, 5), "uint8")
        zajezdnia = cv2.dilate(zajezdnia2, kernal)
        res = cv2.bitwise_and(frame, frame, mask=zajezdnia)

        # object contours function
        (_, contours, hierarchy) = cv2.findContours(zajezdnia, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        time_zajezdnia = 0
        # depot tracking
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 5000 and area < 12000):
                x, y, w, h = cv2.boundingRect(contour)
                # img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                time_zajezdnia = 30
        print "zajezdnia"
        return time_zajezdnia, zajezdnia2

    def peron(self,frame, lower_value, upper_value):
        offset = 10  # offset do obramowania
        maxy = 0
        maxx = 0
        miny = 0
        minx = 0
        obraz = frame[0:400, 400:616]  # zmniejszamy nasz obraz,ktory bedziemy przetwarzac
        hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)  # zamiana na HSV
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # odcien szarosci
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)  # wynajdywanie krawedzi

        mask = cv2.inRange(hsv, lower_value,
                           upper_value)  # sprawdzamy czy gdzies na obrazku znajduje sie nasz szukany kolor
        mask = cv2.erode(mask, None, iterations=2)  # usuwamy wszelkie drobne
        mask = cv2.dilate(mask, None, iterations=2)  # bloby ktore zostaly na naszej masce
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,  # wyszukujemy konturow naszego koloru
                                cv2.CHAIN_APPROX_SIMPLE)[
            -2]  # [-2] jest dodane aby kod byl kompatybilny z dwoma wersjami opencv
        n = 0  # zerujemy zmienna zliczajaca wystapienia pikseli w konturze

        if len(cnts) > 1:  # jesli znajdziemy interesujacy nasz kolor wtedy wykonuje sie algorytm
            minx = cnts[0][0][0][0]  # ustawiamy minimalna wartosc x
            miny = cnts[0][0][0][1]  # ustawiamy minimalna wartosc y
            for x in range(len(cnts)):  # przeszukujemy liste w poszukiwaniu najwiekszych oraz
                for y in range(len(cnts[x])):  # najmniejszych wartosci w ramach ktorych znajduje sie nasz kolor
                    if cnts[x][y][0][0] > maxx:
                        maxx = cnts[x][y][0][0]
                    if cnts[x][y][0][0] < minx:
                        minx = cnts[x][y][0][0]
                    if cnts[x][y][0][1] > maxy:
                        maxy = cnts[x][y][0][1]
                    if cnts[x][y][0][1] < miny:
                        miny = cnts[x][y][0][1]

            for x in range(len(contours)):  # nastepnie poszukujemy czy w obszarze w ktorym znajduje sie nasz kolor
                for y in range(len(contours[x])):  # wystepuja jakies kontury
                    if contours[0][0][0][0] > minx + offset & contours[0][0][0][0] < maxx + offset & contours[0][0][0][
                        1] > miny + offset & contours[0][0][0][1] < maxy + offset:
                        n = n + 1;  # zliczamy ile pikseli wchodzi w sklad wszystkich konturow,poniewaz funkcja FindContours z
                        if n > 60:  # z parametrem Retr tree zwraca tylko co ktorys piksel ktory wchodzi w sklad danego
                            maxy = 0  # konturu
                            maxx = 0  # przy liczbie wiekszej niz 50 jestemy juz pewni w naszym obszarze znajduje sie
                            miny = 0  # odpowiednia liczba konturow,ktora wskazuje na nasz peron
                            minx = 0  # liczba ta zostala uzyskana z kilku prob wykonanych na screenach wykonanych z tego
                            break  # filmu.
                            # Nastepnie zerujemy nasze wartosci graniczne

        if n > 60:  # jesli juz 'n' jest takie jak powinno wypisujemy na ekranie napis mowiacy o wystapieniu peronu
            # cv2.putText(frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
            zatrzask = 26  # zatrzask informujacy nas o tym czy mamy wypisac napis
            peron = True  # licznik potrzebny do wypisywania napisy w konkretnej liczbie klatek i jesli w tej kaltce mamy wypisac napis
            # to postanawiamy ,ze w kolejnych 14 tez wypiszemy-Liczba ta jest opcjonalna i kazdy moze ja indywidualnie dobrac
        else:
            zatrzask = 0
        print "peron"
        return zatrzask, mask



    def run(self):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.moveWindow('image', 0, 0)
        #cap = cv2.VideoCapture('peroniki_long.avi')
        cv2.createTrackbar('HLo', 'image', 0, 255, nothing)
        cv2.createTrackbar('HUp', 'image', 120, 255, nothing)
        cv2.createTrackbar('SLo', 'image', 0, 255, nothing)
        cv2.createTrackbar('SUp', 'image', 255, 255, nothing)
        cv2.createTrackbar('VLo', 'image', 240, 255, nothing)
        cv2.createTrackbar('VUp', 'image', 255, 255, nothing)
        cv2.createTrackbar('Zapis', 'image', 0, 1, nothing)
        while not self.thread_cancelled and self.wyswietlaj==True:
            hlo = cv2.getTrackbarPos('HLo', 'image')
            hup = cv2.getTrackbarPos('HUp', 'image')
            slo = cv2.getTrackbarPos('SLo', 'image')
            sup = cv2.getTrackbarPos('SUp', 'image')
            vlo = cv2.getTrackbarPos('VLo', 'image')
            vup = cv2.getTrackbarPos('VUp', 'image')

            lower_value = (hlo, slo, vlo)
            upper_value = (hup, sup, vup)

            if self.peronWys:
                zatrzask, mask = self.peron(self.frame, lower_value, upper_value)
            elif self.zajezdniaWys:
                zatrzask, mask = self.zajezdnia(self.frame, lower_value, upper_value)

            if zatrzask > 0 and self.peronWys:  # kk musi byc wieksze od 0
                cv2.putText(self.frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
                zatrzask = zatrzask - 1  # gdy wypisujemy napis zmiejszamy ilosd jego wystapien w przyszlych klatkach o 1
            elif zatrzask > 0 and self.zajezdniaWys:
                cv2.putText(self.frame, "  ZAJEZDNIA WRZESZCZ   ", (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255))

            if self.peronWys:
                cv2.putText(self.frame, "P", (630, 480), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
            elif self.zajezdniaWys:
                cv2.putText(self.frame, "Z", (630, 480), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
            if (cv2.getTrackbarPos('Zapis', 'image') == 1):
                if self.peronWys:
                    plik = open('peronHSV.txt', 'w')
                    plik.writelines(str(lower_value[0]))
                    plik.writelines("\n")
                    plik.writelines(str(lower_value[1]))
                    plik.writelines("\n")
                    plik.writelines(str(lower_value[2]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[0]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[1]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[2]))
                    plik.close()
                elif self.zajezdniaWys:
                    plik = open('zajezdniaHSV.txt', 'w')
                    plik.writelines(str(lower_value[0]))
                    plik.writelines("\n")
                    plik.writelines(str(lower_value[1]))
                    plik.writelines("\n")
                    plik.writelines(str(lower_value[2]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[0]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[1]))
                    plik.writelines("\n")
                    plik.writelines(str(upper_value[2]))
                    plik.close()

            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.moveWindow('frame', 650, 200)
            cv2.namedWindow('black')
            cv2.moveWindow('black', 650, 0)
            cv2.imshow('frame', self.frame)
            cv2.imshow('black', mask)

            if cv2.waitKey(1) & 0xFF == ord('p'):
                if self.peronWys == False:
                    self.peronWys = True
                    self.zajezdniaWys = False
                else:
                    self.peronWys = False
                    self.zajezdniaWys = True
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                self.wylacz=True
                cv2.destroyAllWindows()  # zamykamy wszystkie otwarte okna
                #self.thread._stop
                self.shut_down()

            #except ThreadError:
             #   self.thread_cancelled = True


    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        self.thread_cancelled = True
        # block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True




