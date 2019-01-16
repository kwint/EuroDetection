import sys
import cv2 as cv
import numpy as np
import os



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

cv.namedWindow("detected circles", cv.WINDOW_NORMAL)

cv.resizeWindow("detected circles", 1200,900)

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

            circle_img = np.zeros((src.shape[0], src.shape[1]), np.uint8)
            cv.circle(circle_img, (x, y), r, (255,255,255), -1)
            data_rgb = cv.mean(src, mask=circle_img)[:3]
            print(data_rgb)

            # cv.namedWindow("img" + str(r), cv.WINDOW_NORMAL)
            cv.putText(show, str("%.1f %.1f %.1f" % data_rgb), (x-150, y), cv.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

            if 45 <data_rgb[0] < 65:
                cv.putText(show, "1 2 EU", (x-150, y+50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                cv.circle(show, center, r, (255, 0, 255), 3)

            elif 70 <data_rgb[1] < 100:
                cv.putText(show, "0.1 0.2 0.5 EU", (x-150, y+50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                cv.circle(show, center, r, (255, 0, 255), 3)

            elif 40 < data_rgb[1] < 80 and 65 < data_rgb[2] < 130:
                cv.putText(show, "cent", (x-150, y+50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                cv.circle(show, center, r, (255, 0, 255), 3)

            else:
                cv.circle(show, center, r, (100, 100, 100), 3)

            # cv.imshow("img" + str(r), circle_img)

    cv.imshow("detected circles", show)

    if cv.waitKey(1) in {1048603, 27}:
        cv.destroyAllWindows()
        break

