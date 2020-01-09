from tkinter import *
from env import LIGHT_GRAY
from library.image import add_contrast, dec_contrast


class ContrastPanel:

    def __init__(self, parent):
        self.panel = LabelFrame(parent.bottom_panel, text="contrast", bg=LIGHT_GRAY)
        contrast_dec_btn = Button(self.panel, text="-", width=3, height=1, command=dec_contrast)
        contrast_inc_btn = Button(self.panel, text="+", width=3, height=1, command=add_contrast)
        contrast_dec_btn.pack(side=LEFT, padx=15, pady=10)
        contrast_inc_btn.pack(side=LEFT, padx=15, pady=10)

    def pack(self, side=None, padx=0, pady=0):
        self.panel.pack(side=side,  padx=padx, pady=pady)
