import cv2
import numpy as np
import os

photos = os.listdir('./Photos')

img = cv2.imread("./Photos/" + photos[0])

cv2.namedWindow("img", )
img = cv2.imshow("img", img)

cv2.waitKey(0)