from tkinter import *
from env import LIGHT_GRAY
from library.image import add_brightness, dec_brightness


class BrightnessPanel:

    def __init__(self, parent):
        self.panel = LabelFrame(parent.bottom_panel, text="brightness", bg=LIGHT_GRAY)
        brightness_dec_btn = Button(self.panel, text="-", width=3, height=1, command=dec_brightness)
        brightness_inc_btn = Button(self.panel, text="+", width=3, height=1, command=add_brightness)
        brightness_dec_btn.pack(side=LEFT, padx=15, pady=10)
        brightness_inc_btn.pack(side=LEFT, padx=15, pady=10)

    def pack(self, side=None, padx=0, pady=0):
        self.panel.pack(side=side,  padx=padx, pady=pady)
