import cv2
from Kalibrator_klasa import Kal



kalibrator = Kal()
kalibrator.start()
cap = cv2.VideoCapture('czysty.avi')
while (cap.isOpened()):
    _, frame = cap.read()
    kalibrator.setFrame(frame,True)
    if kalibrator.breakclass()==True:
        del kalibrator
        break
cap.release()#"uwalniamy" nasz film
