import cv2
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from find_obj import filter_matches, explore_match


def filterMatches(kp1, kp2, matches, ratio=0.85):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append(kp1[m.queryIdx])
            mkp2.append(kp2[m.trainIdx])

    pairs = zip(mkp1, mkp2)

    return pairs

def main():
    checkOpennCVVersion()
    img1 = cv2.imread('napis_z_tlem.png', 0)  # duzy obrazek
    img2 = cv2.imread('napis.png', 0)  # maly obrazek, tego szukamy w duzym
    orb = cv2.ORB()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)


    #zapis do pliku wynikowych keypointow
    imgKP1 = cv2.drawKeypoints(img1, kp1)
    cv2.imwrite('orb_keypoints_big.jpg', imgKP1)

    imgKP2 = cv2.drawKeypoints(img2, kp2)
    cv2.imwrite('orb_keypoints.jpg', imgKP2)


    matcher = cv2.BFMatcher(cv2.NORM_L2)
    matches = matcher.knnMatch(des1, trainDescriptors=des2, k=2)
    pairs = filterMatches(kp1, kp2, matches)

    l1 = len( kp1 )
    l2 = len( kp2 )
    lp = len( pairs )
    r = (lp * 100) / l1
    print r, "%"
    cv2.waitKey()
    cv2.destroyAllWindows()
    return None

#funkcja wywolowywana przed mainem. By uzyc ORB musimy byc pewni ze mamy wersje opencv 2.4
def checkOpennCVVersion():
    cv2Ver = cv2.__version__
    if(cv2Ver != '2.4.13'):
        sys.exit()
    else:
        print cv2.__version__ ## be sure that its opencv 2.4.13

if __name__ == "__main__":
    checkOpennCVVersion()
    main()
