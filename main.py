import cv2
import numpy as np
import os


def nothing(x):
    pass



photos = os.listdir('./Photos')

img = cv2.imread("./Photos/" + photos[4])

cv2.namedWindow("img", cv2.WINDOW_KEEPRATIO)

cv2.resizeWindow('img', 800, 1200)

while True:
    cv2.imshow("img", img)

    color_code = cv2.getTrackbarPos("color", "slider")

    if cv2.waitKey(1) in {1048603, 27}:
        cv2.destroyAllWindows()
        break
