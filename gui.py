import tkinter as tk
from tkinter import *
import cv2
from PIL import ImageTk, Image


def open_file():
    global stop_btn
    global open_camera_btn
    global open_file_btn
    open_file_btn.configure(state=DISABLED)
    open_camera_btn.configure(state=DISABLED)
    stop_btn.configure(state=NORMAL)
    print("Open File")


def open_camera():
    global stop_btn
    global open_camera_btn
    global open_file_btn
    open_file_btn.configure(state=DISABLED)
    open_camera_btn.configure(state=DISABLED)
    stop_btn.configure(state=NORMAL)
    print("Open Camera")


def stop():
    global stop_btn
    global open_camera_btn
    global open_file_btn
    open_file_btn.configure(state=NORMAL)
    open_camera_btn.configure(state=NORMAL)
    stop_btn.configure(state=DISABLED)
    print("Stop")


LIGHT_GRAY = "#CDCDCD"
RED = "#FF0000"
WHITE = "#FFFFFF"
IMG_SIZE_BIG = 400
IMG_SIZE_SMALL = 180

window = tk.Tk()
window.geometry("640x480")
window.title("Face Recognition")
window.configure(background=LIGHT_GRAY)

im_read = cv2.imread("input/alexa.png")
im_read = cv2.cvtColor(im_read, cv2.COLOR_BGR2RGB)
im_read = cv2.resize(im_read, (IMG_SIZE_BIG, IMG_SIZE_BIG))
main_image = ImageTk.PhotoImage(image=Image.fromarray(im_read))
im_read = cv2.resize(im_read, (IMG_SIZE_SMALL, IMG_SIZE_SMALL))
small_image = ImageTk.PhotoImage(image=Image.fromarray(im_read))

top_pane = Frame(window)
top_pane.configure(background=LIGHT_GRAY)
top_pane.pack(expand=1)

main_canvas = Canvas(top_pane, width=IMG_SIZE_BIG, height=IMG_SIZE_BIG)
main_canvas.pack(side=LEFT, padx=10)
main_canvas.create_image(0, 0, anchor=NW, image=main_image)

side_pane = Frame(top_pane)
side_pane.pack(side=RIGHT)

label = Label(side_pane, text="Unknown", bg=RED, fg=WHITE)
label.pack(side=TOP, fill=BOTH, expand=1)

small_canvas = Canvas(side_pane, width=IMG_SIZE_SMALL, height=IMG_SIZE_SMALL)
small_canvas.pack()
small_canvas.create_image(0, 0, anchor=NW, image=small_image)

bottom_pane = Frame(window)
bottom_pane.configure(background=LIGHT_GRAY)
bottom_pane.pack(side=BOTTOM)

open_file_btn = Button(bottom_pane, text="Open File", command=open_file)
open_camera_btn = Button(bottom_pane, text="Open Camera", command=open_camera)
stop_btn = Button(bottom_pane, text="Taph! Taph!", command=stop)

stop_btn.configure(state=DISABLED)

open_file_btn.pack(side=LEFT, padx=10, pady=10)
open_camera_btn.pack(side=LEFT, padx=10, pady=10)
stop_btn.pack(side=LEFT, padx=10, pady=10)

window.mainloop()
