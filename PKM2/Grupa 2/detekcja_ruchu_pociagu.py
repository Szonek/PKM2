#python_version 2.7
#opencv_verison 3.1

import cv2

height_max = 450
height_min = 300
width_min = 150
width_max = 350
i = 0


def diffImg(t0,t1,t2):
    d1 = cv2.absdiff(t2,t1)
    d2 = cv2.absdiff(t1,t0)
    return cv2.bitwise_and(d1,d2)

video = cv2.VideoCapture('C:\Users\Dawid\PycharmProjects\PKM\czysty.avi')



winName = 'Detektor ruchu'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# pobranie trzech pierwszych klatek
ret, frame = video.read()
subframe = frame[height_min:height_max, width_min:width_max] # wycinamy fragment, na ktorym widac tory
t_minus = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)
ret, frame = video.read()
subframe = frame[height_min:height_max, width_min:width_max]
t = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)
ret, frame = video.read()
subframe = frame[height_min:height_max, width_min:width_max]
t_plus = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

licznik = 0


while(video.isOpened()):
    #cv2.imshow(winName, diffImg(t_minus,t,t_plus))
    #licznik = licznik +1

    t_minus = t
    t = t_plus
    ret, frame = video.read()
    subframe = frame[height_min:height_max, width_min:width_max]
    t_plus = cv2.cvtColor(subframe,cv2.COLOR_RGB2GRAY)

    #thresholding, ktory grupuje wykryte obszary
    thresh = cv2.threshold(diffImg(t_minus, t, t_plus), 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    #Wykrywanie krawedzi
    derp,cnts,cos = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if(cnts == 0):
        i=i-1

    for c in cnts:
        # ignorowanie zbyt malych obszarow
        if cv2.contourArea(c) < 30:
            i = i-1
            continue
        i=7
        #naniesienie ramki
        #(x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(subframe, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(subframe,'pociag jest w ruchu',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))


    if(i>0):
        cv2.putText(frame, 'pociag jest w ruchu', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    cv2.imshow(winName, frame)
    #out.write(frame)

    # warunek ktory zapewnia odstep miedzy klatkami i umozliwa wyjscia
    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break

video.release()
cv2.destroyAllWindows()