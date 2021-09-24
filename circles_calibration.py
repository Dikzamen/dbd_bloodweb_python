import cv2
import numpy as np
from pathlib import Path
import json
from settings_folder import settings_folder
circles_detection_file = f'{settings_folder}circles_detection_data.txt'


def nothing(_):
    pass


def get_circles(image):
    cv2.namedWindow('Circle detection')
    erosion = 0
    minDist = 10
    param1 = 30
    param2 = 33
    minRadius = 0
    maxRadius = 1000

    stable_erosion = erosion
    stable_minDist = minDist
    stable_param1 = param1
    stable_param2 = param2
    stable_minRadius = minRadius
    stable_maxRadius = maxRadius

    if Path(circles_detection_file).exists():
        try:
            with open(circles_detection_file, 'r') as f:
                data = json.load(f)
            erosion, minDist, param1, param2, minRadius, maxRadius = data
        except EOFError:
            pass

    cv2.createTrackbar('erosion', 'Circle detection', 0, 20, nothing)
    cv2.createTrackbar('minDist', 'Circle detection', 0, 200, nothing)
    cv2.createTrackbar('param1',    'Circle detection', 0, 50, nothing)
    cv2.createTrackbar('param2',    'Circle detection', 0, 50, nothing)
    cv2.createTrackbar('minRadius', 'Circle detection', 0, 200, nothing)
    cv2.createTrackbar('maxRadius', 'Circle detection', 0, 800, nothing)

    cv2.setTrackbarPos('erosion', 'Circle detection', erosion)
    cv2.setTrackbarPos('minDist', 'Circle detection', minDist)
    cv2.setTrackbarPos('param1',  'Circle detection', param1)
    cv2.setTrackbarPos('param2',  'Circle detection', param2)
    cv2.setTrackbarPos('minRadius', 'Circle detection', minRadius)
    cv2.setTrackbarPos('maxRadius', 'Circle detection', maxRadius)
    output_alive = False
    error_alive = False

    while 1:
        erosion = cv2.getTrackbarPos('erosion', 'Circle detection')
        minDist = cv2.getTrackbarPos('minDist', 'Circle detection')
        param1 = cv2.getTrackbarPos('param1', 'Circle detection')
        param2 = cv2.getTrackbarPos('param2', 'Circle detection')
        minRadius = cv2.getTrackbarPos('minRadius', 'Circle detection')
        maxRadius = cv2.getTrackbarPos('maxRadius', 'Circle detection')
        try:
            error = False
            kernel = np.ones((erosion, erosion), np.uint8)
            output = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            cv2.imshow('gray', gray)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                                       minRadius=minRadius, maxRadius=maxRadius)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for index, i in enumerate(circles[0, :]):
                    cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
            stable_erosion = erosion
            stable_minDist = minDist
            stable_param1 = param1
            stable_param2 = param2
            stable_minRadius = minRadius
            stable_maxRadius = maxRadius

        except cv2.error:
            error = True
            erosion = stable_erosion
            minDist = stable_minDist
            param1 = stable_param1
            param2 = stable_param2
            minRadius = stable_minRadius
            maxRadius = stable_maxRadius
            kernel = np.ones((erosion, erosion), np.uint8)
            output = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            cv2.imshow('gray', gray)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                                       minRadius=minRadius, maxRadius=maxRadius)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for index, i in enumerate(circles[0, :]):
                    cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)

            print('Error')
        if error:
            if output_alive:
                cv2.destroyWindow("output")
                output_alive = False
            cv2.imshow('error', output)
            error_alive = True
        else:
            if error_alive:
                cv2.destroyWindow("error")
                error_alive = False
            cv2.imshow('output', output)
            output_alive = True
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    with open(circles_detection_file, "w") as f:
        json.dump([erosion, minDist, param1, param2, minRadius, maxRadius], f)
    cv2.destroyAllWindows()
    if circles is not None:
        circles = np.uint16(np.around(circles))
    return circles, output
