from tkinter import *
from tkinter import filedialog
from env import LIGHT_GRAY
import library.image as image_lib
import os


class ActionPanel:
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.parent
        self.video = self.root.video
        self.record = IntVar()
        self.action_frame = LabelFrame(parent.bottom_panel, text="actions", bg=LIGHT_GRAY)
        self.open_file_btn = Button(self.action_frame, text="Open File", command=self.open_file)
        self.open_camera_btn = Button(self.action_frame, text="Open Camera", command=self.open_camera)
        self.stop_btn = Button(self.action_frame, text="Taph! Taph!", command=self.stop)
        self.record_box = Checkbutton(self.action_frame, text="Rec", variable=self.record, bg=LIGHT_GRAY)
        self.stop_btn.configure(state=DISABLED)

        self.open_file_btn.pack(side=LEFT, padx=10, pady=10)
        self.open_camera_btn.pack(side=LEFT, padx=10, pady=10)
        self.stop_btn.pack(side=LEFT, padx=10, pady=10)
        self.record_box.pack(side=LEFT, padx=10, pady=10)

    def pack(self, side=None, padx=0, pady=0):
        self.action_frame.pack(side=side, padx=padx, pady=pady)

    def stop(self):
        self.open_file_btn.configure(state=NORMAL)
        self.open_camera_btn.configure(state=NORMAL)
        self.stop_btn.configure(state=DISABLED)
        self.record_box.configure(state=NORMAL)
        self.video.stop()
        print("Stop")

    def open_camera(self):
        self.open_file_btn.configure(state=DISABLED)
        self.open_camera_btn.configure(state=DISABLED)
        self.stop_btn.configure(state=NORMAL)
        self.record_box.configure(state=DISABLED)

        should_record = False
        if self.record.get() == 1:
            should_record = True
        self.video.init(0)
        self.video.play(self.parent.main_image, self.root.window, take_guess=self.root.take_guess, record=should_record)
        print("Open Camera")

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename()
            if len(file_path) == 0:
                return
            file_name = os.path.basename(file_path)
            if file_name.endswith(".mp4") or file_name.endswith(".avi"):
                print("playing video", file_name)
                self.open_file_btn.configure(state=DISABLED)
                self.open_camera_btn.configure(state=DISABLED)
                self.stop_btn.configure(state=NORMAL)
                self.record_box.configure(state=DISABLED)
                should_record = False
                if self.record.get() == 1:
                    should_record = True
                self.video.init(file_path)
                self.video.play(self.parent.main_image, self.root.window,
                                take_guess=self.root.take_guess, record=should_record)
            elif file_name.endswith(".png") or file_name.endswith(".jpg"):
                im_read = image_lib.open_image(file_path)
                self.parent.main_image.update(image_lib.to_tk_image(im_read, (
                    self.parent.main_image.width, self.parent.main_image.height)))
                self.root.take_guess(im_read)
            else:
                print("Invalid file type!")
                return
        except:
            pass
