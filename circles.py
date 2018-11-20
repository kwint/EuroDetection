import sys
import cv2 as cv
import numpy as np
import os


def main(argv):
    photos = os.listdir('./Photos')
    #
    # img = cv.imread("./Photos/" + photos[4], 0)
    # filename = argv[0] if len(argv) > 0 else default_file
    # # Loads an image
    src = cv.imread("./Photos/" + photos[0], cv.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        # print('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1

    cv.namedWindow("detected circles", cv.WINDOW_NORMAL)
    # cv.resizeWindow("detected circles", 200)

    while True:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

        gray = cv.medianBlur(gray, 5)

        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 10,
                                  param1=130, param2=30,
                                  minRadius=100, maxRadius=300)

        show = src
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(show, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(show, center, radius, (255, 0, 255), 3)

        cv.imshow("detected circles", show)

        cv.waitKey(0)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
