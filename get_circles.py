import cv2
import numpy as np
import json
from settings_folder import settings_folder
circle_filename = f'{settings_folder}circles_detection_data.txt'


def get_circles(image, filter=None):
    with open(circle_filename, 'r') as f:
        data = json.load(f)
    erosion, minDist, param1, param2, minRadius, maxRadius = data

    neigh_filename = 'settings/neighbours.txt'
    with open(neigh_filename, 'r') as f:
        data = json.load(f)
    min_bar = data[0]
    max_bar = data[1]
    hMin, sMin, vMin = min_bar
    hMax, sMax, vMax = max_bar
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)
    kernel = np.ones((erosion, erosion), np.uint8)
    output = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for index, i in enumerate(circles[0, :]):
            cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.putText(output, f"{i[0]} {i[1]}", (i[0] + 20, i[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    return circles, output

