import pyautogui
import time
from circles_calibration import get_circles
from filter_function import create_range
from get_resolution import get_resolution
from settings_folder import settings_folder


def calibrate_colors(image_name):
    color_names = ['iridescent.txt', 'purple.txt', 'green.txt', 'yellow.txt', 'brown.txt']
    for name in color_names:
        name = f'{settings_folder}{name}'
        create_range(image_name, name)


def calibrate_circles(image_name):
    color_name = f'{settings_folder}/neighbours.txt'
    output = create_range(image_name, color_name)
    get_circles(output)


if __name__ == '__main__':
    time.sleep(5)
    image = pyautogui.screenshot()
    crop_img = get_resolution(image)
    calibrate_circles(crop_img)
    calibrate_colors(crop_img)
