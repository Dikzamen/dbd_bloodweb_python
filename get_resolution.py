import numpy as np
import cv2
from PIL import ImageGrab
from pathlib import Path
import json
from settings_folder import settings_folder

def nothing(_):
    pass


filename_standard = f'{settings_folder}screen_dimensions.txt'


def get_resolution(img=None, filename=None):
    if img is None:
        image = ImageGrab.grab()
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1]
    if filename is None:
        filename = filename_standard

    if img is not None:
        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1]
    # return None
    x_min = 0
    x_max = 2000
    y_min = 0
    y_max = 1950

    if Path(filename).exists():
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            x_min = data[0]
            x_max = data[1]
            y_min = data[2]
            y_max = data[3]
            print(data)
        except EOFError:
            pass

    cv2.namedWindow('Resolution settings')

    cv2.createTrackbar('X min', 'Resolution settings', 0, 2000, nothing)
    cv2.setTrackbarPos('X min', 'Resolution settings', x_min)

    cv2.createTrackbar('Y min', 'Resolution settings', 0, 2000, nothing)
    cv2.setTrackbarPos('Y min', 'Resolution settings', y_min)
    cv2.createTrackbar('X max', 'Resolution settings', 0, 2000, nothing)
    cv2.setTrackbarPos('X max', 'Resolution settings', x_max)
    cv2.createTrackbar('Y max', 'Resolution settings', 0, 2000, nothing)
    cv2.setTrackbarPos('Y max', 'Resolution settings', y_max)

    while 1:
        x_min = cv2.getTrackbarPos('X min', 'Resolution settings')
        x_max = cv2.getTrackbarPos('X max', 'Resolution settings')
        y_min = cv2.getTrackbarPos('Y min', 'Resolution settings')
        y_max = cv2.getTrackbarPos('Y max', 'Resolution settings')
        crop_img = open_cv_image[y_min:y_max, x_min:x_max]
        cv2.imshow("Cropped screen", crop_img)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            # if cv2.waitKey() & 0xFF == ord('q'):
            print('BREAK LOOP')
            break
    with open(filename, "w") as f:
        json.dump([x_min, x_max, y_min, y_max], f)
    cv2.destroyAllWindows()
    return crop_img
