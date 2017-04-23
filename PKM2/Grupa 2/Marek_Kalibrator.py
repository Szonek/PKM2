import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
maxy=0
maxx=0
miny=0
minx=0
offset=10 #offset do obramowania
zatrzask=0
peronWys=True
def nothing(x):
    pass



cv2.namedWindow('image')
cap = cv2.VideoCapture('peroniki_long.avi')
cv2.createTrackbar('HLo','image',0,255,nothing)
cv2.createTrackbar('HUp','image',120,255,nothing)
cv2.createTrackbar('SLo','image',0,255,nothing)
cv2.createTrackbar('SUp','image',255,255,nothing)
cv2.createTrackbar('VLo','image',240,255,nothing)
cv2.createTrackbar('VUp','image',255,255,nothing)

while(cap.isOpened()):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hlo = cv2.getTrackbarPos('HLo','image')
    hup = cv2.getTrackbarPos('HUp', 'image')
    slo = cv2.getTrackbarPos('SLo', 'image')
    sup = cv2.getTrackbarPos('SUp', 'image')
    vlo = cv2.getTrackbarPos('VLo', 'image')
    vup = cv2.getTrackbarPos('VUp', 'image')

    lower_value =(hlo,slo,vlo)
    upper_value = (hup,sup,vup)

    if peronWys:
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
            zatrzask = 15  # zatrzask informujacy nas o tym czy mamy wypisac napis
            peron = True  # licznik potrzebny do wypisywania napisy w konkretnej liczbie klatek i jesli w tej kaltce mamy wypisac napis
            # to postanawiamy ,ze w kolejnych 14 tez wypiszemy-Liczba ta jest opcjonalna i kazdy moze ja indywidualnie dobrac

    if zatrzask > 0:  # kk musi byc wieksze od 0
        cv2.putText(frame, "Peron!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (255, 0, 100))
        zatrzask = zatrzask - 1  # gdy wypisujemy napis zmiejszamy ilosd jego wystapien w przyszlych klatkach o 1
    # cv2.imshow("Frame", obraz) #opcjonale pokazanie fragmentu obrazu ktory bedziemy przetwarzac




    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        if peronWys==False:
                peronWys=True
        else:
         peronWys=False
    elif cv2.waitKey(1) & 0xFF == ord('q'):   #po nacisnieciu klawisza 'q' nastepuje wylaczenie programu
            break

cv2.destroyAllWindows()