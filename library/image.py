from PIL import ImageTk, Image
import cv2
import numpy as np


contrast = 1
brightness = 1


def to_tk_image(mat, dimension):
    im_read = cv2.resize(mat, dimension)
    return ImageTk.PhotoImage(image=Image.fromarray(im_read))


def open_image(path):
    im_read = cv2.imread(path)
    return cv2.cvtColor(im_read, cv2.COLOR_BGR2RGB)


def add_brightness():
    global brightness
    brightness += 10
    print("Brightness adjustment: {}".format(brightness))
    return brightness


def dec_brightness():
    global brightness
    brightness -= 10
    if brightness < 0:
        brightness = 0
    print("Brightness adjustment: {}".format(brightness))
    return brightness


def add_contrast():
    global contrast
    contrast += 0.5
    print("Contrast adjustment: {}".format(contrast))
    return contrast


def dec_contrast():
    global contrast
    contrast -= 0.5
    if contrast < 0:
        contrast = 0
    print("Contrast adjustment: {}".format(contrast))
    return contrast


def apply_adjustments(mat, b=None, c=None):
    global brightness
    global contrast
    if b is None:
        b = brightness
    if c is None:
        c = contrast
    print("brightness: {}, contrast: {}".format(brightness, contrast))
    return cv2.addWeighted(mat, c, np.zeros(mat.shape, mat.dtype), 0, b)
