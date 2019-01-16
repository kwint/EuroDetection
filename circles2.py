# Quinty van Dijk en Bas Vermeulen

import sys
import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

# Coin class, holds all properties of a coin and can calc it's value
class Coin:
    def __init__(self, number, circle, value=0, material="None"):
        self.number = number
        self.circle = circle
        self.area = self.circle[2]**2*np.pi
        self.material = material
        self.biggest = False
        self.value = value

    # Calc coin value with the area of the biggest coin and it's value
    def calc_value(self, biggest_area, biggest_value):
        ratio = self.area / biggest_area
        if self.value == 0:
            if self.material == "copper":
                if biggest_value == 2:
                    if ratio > 1:
                        self.value = 0
                    if 0.3 < ratio < 0.48:
                        self.value = 0.01
                    if 0.48 < ratio < 0.74:
                        self.value = 0.02
                    if 0.74 < ratio < 0.9:
                        self.value = 0.05
            if self.material == "messing":
                if biggest_value == 2:
                    if ratio > 1:
                        self.value = 0
                    if 0.45 < ratio < 0.75:
                        self.value = 0.10
                    if 0.75 < ratio < 0.9:
                        self.value = 0.20
                    if 0.9 < ratio < 1.05:
                        self.value = 0.50


# Function checks if a coin is a 1 euro or 2 euro coin
def is_euro(hsv_img, circle):
    x, y, r = circle

    # Get color value of center of coin and of edge
    hsv1 = hsv_img[y, x]
    hsv2 = hsv_img[int(y+(r*0.9)), x]

    # Get dif in saturation
    diff = abs(int(hsv1[1]) - int(hsv2[1])) # converting to int to tackle overflow errors
    print(diff)
    print(hsv1, hsv2)

    # if heu is less than 50 this is not a euro coin
    if hsv1[0] < 50:
        return False

    # if diff is bigger than 38 its a 1 euro or 2 euro coin
    if diff > 38:
        if hsv1[1] < hsv2[1]: # If outside has bigger saturation than inside its a 1 euro
            print("1 Euro")
            return 1
        else:
            print("2 Euro")
            return 2
    else: # calc average color of coin and find if it's a copper or messing coin
        circle_img = np.zeros((src.shape[0], src.shape[1]), np.uint8)
        cv.circle(circle_img, (x, y), int(r*0.8), (255, 255, 255), -1)
        data_rgb = cv.mean(hsv_img, mask=circle_img)[:3]
        print(data_rgb)
        if data_rgb[1] > 75 and data_rgb[2] > 70:
            if data_rgb[0] > 105:
                print("copper")
                return 5
            else:
                return 10
        else:
            return False


photos = os.listdir('./Photos')
src = cv.imread("./Photos/" + "z2_edit.png", cv.IMREAD_COLOR)

# Check if image is loaded correctly
if src is None:
    print('Error opening image!')

cv.namedWindow("detected circles", cv.WINDOW_NORMAL)
cv.resizeWindow("detected circles", 1200, 900)

coins = []

while True:
    # convert to grayscale
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # apply median blur to show edges better, relative big kernel because high resolution picture
    gray = cv.medianBlur(gray, 15)

    # Find circles
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 10,
                              param1=200, param2=23,
                              minRadius=100, maxRadius=300)

    # Create a copy for visualization
    show = src.copy()

    if circles is not None:
        circles = np.uint16(np.around(circles))

        # This for loop looks for the biggest coin on screen. Stops when it found a 2 euro coin
        for i, circle in enumerate(circles[0, :]):
            return_euro = is_euro(cv.cvtColor(src, cv.COLOR_RGB2HSV), circle)
            if return_euro == 2:
                biggest_coin = circle, 2, circle[2]**2*np.pi
                break

            if return_euro == 1:
                biggest_coin = circle, 1, circle[2]**2*np.pi

        # When no biggest coin is found stop program
        if biggest_coin:
            print("Biggest coin: ", biggest_coin)
        else:
            raise Exception

        # For every circle found check which coin it is
        for i, circle in enumerate(circles[0, :]):
            print("coin nr: ", i)
            x, y, r = circle
            center = (x, y)
            # print circle number to img
            cv.putText(show, str(i), (x, y), cv.FONT_HERSHEY_PLAIN, 4,
                       (255, 0, 0), 6)

            # check if circle is 1 or 2 euro or messing or copper, then print it to screen and add coin to coin array
            return_euro = is_euro(cv.cvtColor(src, cv.COLOR_RGB2HSV), circle)
            if return_euro == 1:
                cv.circle(show, center, r, (255, 0, 0), 3)
                cv.putText(show, "1 Euro", (x, y+50), cv.FONT_HERSHEY_PLAIN, 4,
                           (255, 255, 255), 4)
                coins.append(Coin(i, circle, value=1))

            if return_euro == 2:
                cv.circle(show, center, r, (0, 255, 0), 3)
                cv.putText(show, "2 Euro", (x, y+50), cv.FONT_HERSHEY_PLAIN, 4,
                           (255, 255, 255), 4)
                coins.append(Coin(i, circle, value=2))

            if return_euro == 10:
                cv.circle(show, center, r, (0, 0, 255), 3)
                cv.putText(show, "messing", (x, y+50), cv.FONT_HERSHEY_PLAIN, 4,
                           (255, 255, 255), 4)
                coins.append(Coin(i, circle, material="messing"))

            if return_euro == 5:
                cv.circle(show, center, r, (255, 255, 0), 3)
                cv.putText(show, "copper", (x, y+50), cv.FONT_HERSHEY_PLAIN, 4,
                           (255, 255, 255), 4)
                coins.append(Coin(i, circle, material="copper"))

            if not return_euro:
                cv.circle(show, center, r, (125, 125, 125), 3)

        # Finally, show coin ratio and value on screen and get the total sum of coins
        total = 0
        for coin in coins:
            coin.calc_value(biggest_coin[2], biggest_coin[1])
            ratio = coin.area /  biggest_coin[2]
            cv.putText(show, "{:1.3f}".format(ratio), (coin.circle[0], coin.circle[1] + 100), cv.FONT_HERSHEY_PLAIN, 4,
                           (255, 255, 255), 8)
            coin.calc_value(biggest_coin[2], biggest_coin[1])
            cv.putText(show, str(coin.value), (coin.circle[0], coin.circle[1] - 50), cv.FONT_HERSHEY_PLAIN, 6,
                           (0, 0, 255), 8)
            total = total + coin.value
            # cv.imshow("img" + str(r), circle_img)

    cv.imshow("detected circles", show)


    print("Gevonden bedrag: € {:1.2f}".format(total))
    if cv.waitKey(0) in {1048603, 27}:
        cv.destroyAllWindows()
        break

print(coins)