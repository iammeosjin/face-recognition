from tkinter import *
from env import LIGHT_GRAY
from gui.library.image import ImageFrame


class Panels:

    def __init__(self, root):
        self.parent = root
        self.window = root.window
        self.main_panel = Frame(self.window)
        self.main_panel.configure(background=LIGHT_GRAY)
        self.main_panel.pack(expand=1)

        self.bottom_panel = Frame(self.window)
        self.bottom_panel.configure(background=LIGHT_GRAY)
        self.bottom_panel.pack(side=BOTTOM)

        self.main_image = ImageFrame(self.main_panel, root.BIG_DIMENSION)
        self.main_image.pack(side=LEFT, padx=10)

        self.side_panel = Frame(self.main_panel)
        self.side_panel.pack(side=RIGHT)

        self.small_image = ImageFrame(self.side_panel, root.SMALL_DIMENSION)
        self.small_image.pack()

        self.guess_label = Label(self.side_panel, text="Unknown", bg="red", fg="white")
        self.guess_label.pack(side=TOP, fill=BOTH, expand=1)

