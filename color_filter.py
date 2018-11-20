import cv2
import numpy as np
import os


def nothing(x):
    pass

def filter_image(img, lower_mask, upper_mask):
    # set sliders to start values
    kernel = np.ones((10, 10), np.uint8)
    cv2.setTrackbarPos('B', 'slider', lower_mask[0])
    cv2.setTrackbarPos('G', 'slider', lower_mask[1])
    cv2.setTrackbarPos('R', 'slider', lower_mask[2])
    cv2.setTrackbarPos('B1', 'slider', upper_mask[0])
    cv2.setTrackbarPos('G1', 'slider', upper_mask[1])
    cv2.setTrackbarPos('R1', 'slider', upper_mask[2])

    # wait a bit to update
    cv2.waitKey(5)

    # Read slider positions
    b = cv2.getTrackbarPos('B', 'slider')
    g = cv2.getTrackbarPos('G', 'slider')
    r = cv2.getTrackbarPos('R', 'slider')
    b1 = cv2.getTrackbarPos('B1', 'slider')
    g1 = cv2.getTrackbarPos('G1', 'slider')
    r1 = cv2.getTrackbarPos('R1', 'slider')

    # Build mask array from sliders
    lower_unit = np.array([b, g, r])
    upper_unit = np.array([b1, g1, r1])

    # Convert image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Filter colors
    mask = cv2.inRange(hsv, lower_unit, upper_unit)
    res = cv2.bitwise_and(img, img, mask=mask)

    # Convert to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Make binary image
    ret, thres = cv2.threshold(gray, 20, 255, 0)

    # Close some holes
    thres = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)

    # Return binary image and slider data, so program remebers their position
    return res, b, g, r, b1, g1, r1


photos = os.listdir('./Photos')

img = cv2.imread("./Photos/" + photos[4])

cv2.namedWindow("img", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("thres", cv2.WINDOW_KEEPRATIO)

cv2.namedWindow('slider', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('slider', 640, 0)
cv2.resizeWindow('slider', 560, 400)
cv2.createTrackbar('B', 'slider', 0, 255, nothing)
cv2.createTrackbar('G', 'slider', 0, 255, nothing)
cv2.createTrackbar('R', 'slider', 0, 255, nothing)

cv2.createTrackbar('B1', 'slider', 0, 255, nothing)
cv2.createTrackbar('G1', 'slider', 0, 255, nothing)
cv2.createTrackbar('R1', 'slider', 0, 255, nothing)

cv2.createTrackbar('color', 'slider', 0, 5, nothing)


cv2.resizeWindow('img', 800, 1200)
cv2.resizeWindow('thres', 800, 1200)


#   None        Green           Blue            Pink              Orange          Yellow
lower_mask = np.array(
    [[0, 0, 0], [59, 95, 101], [0, 99, 0], [119, 90, 107], [107, 143, 141], [83, 131, 131]])
upper_mask = np.array(
    [[0, 0, 0], [79, 255, 255], [28, 255, 222], [149, 225, 218], [120, 255, 230], [94, 255, 233]])


while True:
    cv2.imshow("img", img)

    color_code = cv2.getTrackbarPos("color", "slider")

    thres, b, g, r, b1, g1, r1 = filter_image(img, lower_mask[color_code], upper_mask[color_code])
    lower_mask[color_code] = [b, g, r]
    upper_mask[color_code] = [b1, g1, r1]

    cv2.imshow("thres", thres)
    if cv2.waitKey(1) in {1048603, 27}:
        cv2.destroyAllWindows()
        break
