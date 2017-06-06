import cv2
import numpy as np

def zajezdnia(frame, zajezdnia_lower_value, zajezdnia_upper_value):

    # color conversion
    #img = frame poprzednio
    img = frame[150:300,180:550]  
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #ranges of depot colors
    #zajezdnia_lower = np.array([0, 0, 240], np.uint8)
    #zajezdnia_upper = np.array([50, 255, 255], np.uint8)


    #searching in defined range
    zajezdnia = cv2.inRange(hsv, zajezdnia_lower_value, zajezdnia_upper_value)

    #morphological transformation, dilation
    kernal = np.ones((5,5), "uint8")
    zajezdnia=cv2.dilate(zajezdnia,kernal)
    res=cv2.bitwise_and(img,img,mask = zajezdnia)

    #object contours function
    (_, contours, hierarchy) = cv2.findContours(zajezdnia, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #depot tracking
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>5000 and  area<12000):
            x,y,w,h = cv2.boundingRect(contour)
            #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img, "  ZAJEZDNIA WRZESZCZ   ", (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255))
