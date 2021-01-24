#!/usr/bin/env python3

import numpy as np
import cv2
import pyscreenshot as ImageGrab
import os
import pync
from datetime import datetime

OUTPUT_DIR = '/Users/lucasmarandat/Screenshots/'
HEIGHT = 600


def get_max_contour(img):
    selected, m = None, 0
    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > m:
            selected, m = contour, area
    if m == 0:
        raise Exception('Contour not found')
    return cv2.boundingRect(selected)


def save_bb_collab_screen():
    screenshot = np.array(ImageGrab.grab(childprocess=False))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    black_color_1 = np.array([0, 0, 0], np.uint8)
    black_color_2 = np.array([45, 45, 45], np.uint8)
    mask = cv2.inRange(screenshot, black_color_1, black_color_2)

    (x1, y1, w1, h1) = get_max_contour(mask)
    cropped_mask = mask[y1:y1+h1, x1:x1+w1]
    cropped_mask = cv2.bitwise_not(cropped_mask)
    (x2, y2, w2, h2) = get_max_contour(cropped_mask)

    img = screenshot[y1+y2:y1+y2+h2, x1+x2:x1+x2+w2]
    width = int(w2 * HEIGHT / h2)
    img = cv2.resize(img, (width, HEIGHT))
    now = datetime.now().strftime('%m-%d-%H-%M-%S')
    file_path = os.path.join(OUTPUT_DIR, f'{now}.png')
    cv2.imwrite(file_path, img)
    return file_path


if __name__ == '__main__':
    try:
        file_path = save_bb_collab_screen()
        pync.notify('😍 Screenshot has been saved', title='BBCS',
                    open=f'file:{file_path}')
    except Exception:
        pync.notify('🤬 No BB Collab screen found', title='BBCS')
