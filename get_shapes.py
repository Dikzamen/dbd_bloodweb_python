import cv2
import json
import numpy as np


def get_color_shapes(image, color_filename):
    image = image.copy()
    with open(color_filename, 'r') as f:
        data = json.load(f)
    min_bar = data[0]
    max_bar = data[1]
    hMin, sMin, vMin = min_bar
    hMax, sMax, vMax = max_bar
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    result = []
    for index, c in enumerate(contours):
        if cv2.arcLength(c, True) < 40:
            continue
        M = cv2.moments(c)
        try:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            result.append((x, y))
        except ZeroDivisionError:
            print('Zero div')
    return result, clean
