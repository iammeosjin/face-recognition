import tkinter as tk
import numpy as np
from PIL import ImageTk, Image


def create_empty_image(dimension):
    return ImageTk.PhotoImage(image=Image.fromarray(np.empty(dimension)))


def create_empty_mat(dimension):
    return np.ones(dimension)


class ImageFrame:

    def __init__(self, parent, dimension):
        (width, height) = dimension
        self.width = width
        self.height = height
        self.dimension = dimension
        self.content = tk.Label(parent, image=create_empty_image(dimension))

    def reset(self):
        self.content.configure(image=None)
        self.content.image = None

    def pack(self, side=None, padx=10):
        self.content.pack(side=side, padx=padx, expand=True)

    def update(self, image):
        self.content.configure(image=image)
        self.content.image = image
