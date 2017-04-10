import cv2
import numpy as np

# Loading video file
cap = cv2.VideoCapture("zajezdnia3.avi")

while(1):

    _,img = cap.read()

    # color conversion
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # ranges of depot colors
    depot_lower = np.array([0, 0, 240], np.uint8)
    depot_upper = np.array([50, 255, 255], np.uint8)

    # ranges of platforms colors
    platforms_lower = np.array([0, 120, 0], np.uint8)
    platforms_upper = np.array([3, 255, 255], np.uint8)

    # searching in defined range
    depot = cv2.inRange(hsv, depot_lower, depot_upper)
    platforms = cv2.inRange(hsv, platforms_lower, platforms_upper)

    # Morphological transformation, dilation
    kernal = np.ones((5,5), "uint8")
    depot=cv2.dilate(depot,kernal)
    res=cv2.bitwise_and(img,img,mask = depot)

    platforms = cv2.dilate(platforms, kernal)
    res1 = cv2.bitwise_and(img,img, mask = platforms)


    # object contours function
    (_, contours, hierarchy) = cv2.findContours(depot, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>5000 and  area<12000):
            x,y,w,h = cv2.boundingRect(contour)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img, "  ZAJEZDNIA WRZESZCZ   ", (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255))


    # object contours function
    (_, contours, hierarchy) = cv2.findContours(platforms, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>3000 and  area<8000):
            x,y,w,h = cv2.boundingRect(contour)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(img, "  PERONY   ", (120, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255))

    cv2.imshow("Depot and Platforms Tracking", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

