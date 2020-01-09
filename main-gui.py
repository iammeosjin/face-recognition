from tkinter import filedialog
from tkinter import *
from library.video import Video
from gui.library.image import ImageFrame
from model import FaceEncodings
from env import INPUT_FOLDER, LIGHT_GRAY, join_path
from gui.components.panels import Panels
from gui.components.action_buttons import ActionPanel
from gui.components.brightness_buttons import BrightnessPanel
from gui.components.contrast_buttons import ContrastPanel
import library.image as image_lib
import tkinter as tk


class MainFrame:
    BIG_SIZE = 380
    BIG_DIMENSION = (BIG_SIZE, BIG_SIZE)
    SMALL_SIZE = 180
    SMALL_DIMENSION = (SMALL_SIZE, SMALL_SIZE)

    def __init__(self):
        self.video = Video()
        self.video.delay = 10
        self.face_model = FaceEncodings(INPUT_FOLDER)
        self.face_model.load()
        self.window = tk.Tk()
        self.window.geometry("660x480")
        self.window.title("Face Recognition")
        self.window.configure(background=LIGHT_GRAY)

        self.panels = Panels(self)
        self.action_panel = ActionPanel(self.panels)
        self.action_panel.pack(side=LEFT, padx=10, pady=10)
        self.brightness_panel = BrightnessPanel(self.panels)
        self.brightness_panel.pack(side=LEFT, padx=10, pady=10)
        self.contrast_panel = ContrastPanel(self.panels)
        self.contrast_panel.pack(side=LEFT, padx=10, pady=10)

    def show(self):
        self.window.mainloop()

    def take_guess(self, mat):
        face_locations, face_names = self.face_model.analyze_frame(mat)
        face_names = list(filter(lambda face_name: face_name != "Unknown", face_names))
        name = "Unknown"
        if len(face_names) > 0:
            name = face_names[0]

        self.panels.guess_label.configure(text=name)

        if name == "Unknown":
            self.panels.small_image.reset()
            return face_locations, face_names
        image_path = join_path(INPUT_FOLDER, "{}.png".format(name.lower()))
        im_read = image_lib.open_image(image_path)
        self.panels.small_image.update(image_lib.to_tk_image(im_read, self.SMALL_DIMENSION))
        return face_locations, face_names


gui = MainFrame()
gui.show()


