import sys
import cv2
from obsluga_nagrania import przetwarzajfilm

peronPrzetwarzaj=False
zajezdniaPrzetwarzaj=False
rekaPrzetwarzaj=False
toryPrzetwarzaj=False
czerwonyPrzetwarzaj=False
twarzPrzetwarzaj=False
filmOrCam=1
sciezka=''





if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        if sys.argv[i].find("1") != -1:
            sciezka = sys.argv[i + 1]
            filmOrCam=2
        elif sys.argv[i].find("peron") != -1:
            if sys.argv[i + 1].find("True") != -1:
                peronPrzetwarzaj = True
            else:
                peronPrzetwarzaj = False
        elif sys.argv[i].find("zajezdnia") != -1:
            if sys.argv[i + 1].find("True") != -1:
                zajezdniaPrzetwarzaj = True
            else:
                zajezdniaPrzetwarzaj = False
        elif sys.argv[i].find("reka") == 1:
            if sys.argv[i + 1].find("True") != -1:
                rekaPrzetwarzaj = True
            else:
                rekaPrzetwarzaj = False
        elif sys.argv[i].find("tory") != -1:
            if sys.argv[i + 1].find("True") != -1:
                toryPrzetwarzaj = True
            else:
                toryPrzetwarzaj = False
        elif sys.argv[i].find("czerwony") != -1:
            if sys.argv[i + 1].find("True") != -1:
                czerwonyPrzetwarzaj = True
            else:
                czerwonyPrzetwarzaj = False
        elif sys.argv[i].find("twarz") != -1:
            if sys.argv[i + 1].find("True") != -1:
                twarzPrzetwarzaj = True
            else:
                twarzPrzetwarzaj = False
    if filmOrCam==2:
        przetwarzajfilm(sciezka,peronPrzetwarzaj)#dodawajcie swoje znaczniki do przekazywania
    else:
        print ""#miejsce dla Ciebie Tomus,podepniesz tutaj funkcje do przetwarzania