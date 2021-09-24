import numpy as np
import pyautogui


def screenshot(bounds=None):
    image = pyautogui.screenshot()
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1]
    if bounds is not None:
        x = bounds[0]
        y = bounds[1]
        open_cv_image = open_cv_image[x[0]:x[1], y[0]:y[1]]
    return open_cv_image
