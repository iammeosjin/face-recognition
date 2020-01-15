from model import FaceEncodings
from env import INPUT_FOLDER, join_path
import numpy as np
import picamera


face_model = FaceEncodings(INPUT_FOLDER)
face_model.load()
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    face_locations, face_names = face_model.analyze_frame(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_names = list(filter(lambda face_name: face_name != "Unknown", face_names))
    name = "Unknown"
    if len(face_names) > 0:
        name = face_names[0]

    print("I see someone named {}!".format(name))
