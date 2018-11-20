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

        show = src.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                x, y, r = i
                center = (x, y)
                # circle center
                cv.circle(show, center, 1, (0, 100, 100), 3)
                # circle outline
                cv.circle(show, center, r, (255, 0, 255), 3)

                mask = np.zeros((rows, gray.shape[1], 3), dtype=np.uint8)
                cv.circle(mask, (x, y), r, (255, 0, 0), -1, 8, 0)
                out = show * mask
                cv.namedWindow("img" + str(r), cv.WINDOW_NORMAL)
                cv.imshow("img" + str(r), out)

        cv.imshow("detected circles", show)

        if cv.waitKey(1) in {1048603, 27}:
            cv.destroyAllWindows()
            break

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
