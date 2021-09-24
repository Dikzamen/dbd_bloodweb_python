import cv2
import numpy as np
import json
from pathlib import Path


def nothing(x):
    pass


def create_range(image_name, range_name):
    image = image_name
    cv2.namedWindow('Filter by color')

    hMin = sMin = vMin = 0
    hMax = 179
    sMax = vMax = 255
    cv2.createTrackbar('HMin', 'Filter by color', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'Filter by color', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'Filter by color', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'Filter by color', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'Filter by color', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'Filter by color', 0, 255, nothing)

    if Path(range_name).exists():
        try:
            with open(range_name, 'r') as f:
                data = json.load(f)
            min_bar = data[0]
            max_bar = data[1]
            print('min bar import', min_bar)
            print('max bar import', max_bar)
            hMin, sMin, vMin = min_bar
            hMax, sMax, vMax = max_bar
        except EOFError:
            pass

    # Set default value for MAX HSV trackbars.

    cv2.setTrackbarPos('HMin', 'Filter by color', hMin)
    cv2.setTrackbarPos('HMax', 'Filter by color', hMax)
    cv2.setTrackbarPos('SMax', 'Filter by color', sMax)
    cv2.setTrackbarPos('SMin', 'Filter by color', sMin)
    cv2.setTrackbarPos('VMax', 'Filter by color', vMax)
    cv2.setTrackbarPos('VMin', 'Filter by color', vMin)

    while 1:
        hMin = cv2.getTrackbarPos('HMin', 'Filter by color')
        sMin = cv2.getTrackbarPos('SMin', 'Filter by color')
        vMin = cv2.getTrackbarPos('VMin', 'Filter by color')
        hMax = cv2.getTrackbarPos('HMax', 'Filter by color')
        sMax = cv2.getTrackbarPos('SMax', 'Filter by color')
        vMax = cv2.getTrackbarPos('VMax', 'Filter by color')
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        numpy_vertical_concat = output
        cv2.imshow(range_name, numpy_vertical_concat)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break
    with open(range_name, "w") as f:
        json.dump([[hMin, sMin, vMin], [hMax, sMax, vMax]], f)
    cv2.destroyAllWindows()
    return output.copy()
