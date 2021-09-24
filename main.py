import pyautogui
import json
from get_shapes import get_color_shapes
import numpy as np
from pathlib import Path
import time
from math import hypot, sqrt
from get_circles import get_circles

from settings_folder import settings_folder

filename = f'{settings_folder}screen_dimensions.txt'
x_max = None
x_min = 0
y_min = 0

def screenshot(bounds=None):
    image = pyautogui.screenshot()
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1]
    if bounds is not None:
        x = bounds[0]
        y = bounds[1]
        open_cv_image = open_cv_image[y[0]:y[1], x[0]:x[1]]
    return open_cv_image

if Path(filename).exists():
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            x_min = data[0]
            x_max = data[1]
            y_min = data[2]
            y_max = data[3]

        except EOFError:
            pass

color_names = ['iridescent.txt', 'purple.txt', 'green.txt', 'yellow.txt', 'brown.txt']
def close(center1, center2):
    if sqrt(hypot(center1[0] - center2[0], center1[1] - center2[1])) < 8:
        return True
    return False

time.sleep(2)
def main(reverse=False):
    while 1:

        t1 = time.time()
        # image = screenshot()
        image = pyautogui.screenshot()
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1]
        if x_max is not None:
            open_cv_image = open_cv_image[y_min:y_max, x_min:x_max]
        t2 = time.time()
        print(f'screenshot and crop = {t2 - t1}')
        # skip_button = pyautogui.locate('click_to_continue.jpg', open_cv_image, grayscale=True, confidence=0.7)
        skip_button = pyautogui.locateOnScreen('click_to_continue.jpg', grayscale=True, confidence=0.7)
        if skip_button is not None:
            pyautogui.click(x_min + skip_button[0] + skip_button[2] // 2, y_min + skip_button[1] + skip_button[3] // 2)
            pyautogui.moveTo(10, 10)
            time.sleep(0.8)
            continue
        t3 = time.time()
        print(f'locating click and continue {t3 - t2}')
        circles, output = get_circles(open_cv_image.copy())

        if circles is None:
            time.sleep(1.5)
            continue

        queue = []
        circles = circles.tolist()[0]

        t4 = time.time()
        print(f'locating circles {t4 - t3}')

        images = []
        for color in color_names:
            color = f'{settings_folder}{color}'
            shapes, img = get_color_shapes(open_cv_image, color)
            images.append(img)
            for shape in shapes:
                for circle in circles[:]:
                    if close(circle, shape):
                        circles.remove(circle)
                        queue.append(circle)

        queue.extend(circles)

        t5 = time.time()
        print(f'locating shapes {t5 - t4}')
        if reverse:
            queue = queue[::-1]
        pyautogui.moveTo(queue[0][0] + x_min, queue[0][1] + y_min)
        pyautogui.mouseDown()
        time.sleep(0.4)
        pyautogui.mouseUp()
        pyautogui.moveTo(10, 10, 0.04)
        # time.sleep(0.04)
        print()

if __name__ == '__main__':
    main()