import cv2

def diffImg(t0,t1,t2):
    d1 = cv2.absdiff(t2,t1)
    d2 = cv2.absdiff(t1,t0)
    return cv2.bitwise_and(d1,d2)

video = cv2.VideoCapture('C:\Users\Dawid\PycharmProjects\PKM\czysty.avi')



winName = 'Detektor ruchu'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

for i in range(2500):
    ret, frame = video.read()

ret, frame = video.read()
subframe = frame[300:450, 100:300]
t_minus = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)
ret, frame = video.read()
subframe = frame[300:450, 100:300]
t = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)
ret, frame = video.read()
subframe = frame[300:450, 100:300]
t_plus = cv2.cvtColor(subframe, cv2.COLOR_RGB2GRAY)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

licznik = 0


while(video.isOpened()):
     #cv2.imshow(winName, diffImg(t_minus,t,t_plus))

    licznik = licznik +1

    t_minus = t
    t = t_plus
    ret, frame = video.read()
    subframe = frame[300:450, 100:300]
    t_plus = cv2.cvtColor(subframe,cv2.COLOR_RGB2GRAY)

    thresh = cv2.threshold(diffImg(t_minus, t, t_plus), 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    #Wykrywanie krawedzi
    derp,cnts,cos = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for c in cnts:
        # ignorowanie zbyt malych obszarow
        if cv2.contourArea(c) < 40:
            continue
           #naniesienie ramki
        (x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame,'pociag jest w ruchu',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
    cv2.imshow(winName, frame)
    out.write(frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')) or licznik == 500:
        break


video.release()
cv2.destroyAllWindows()