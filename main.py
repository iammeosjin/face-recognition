import face_recognition
import cv2
import numpy as np
import os
from env import INPUT_FOLDER, OUTPUT_FOLDER, join_path
from model import FaceEncodings


face_model = FaceEncodings(INPUT_FOLDER)


def display_frame(frame, face_locations=[], face_names=[]):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)
    return frame


def analyze_frame(frame):
    global face_model
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(face_model.encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(face_model.encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = face_model.names[best_match_index]

        face_names.append(name)

    return face_locations, face_names


def read_video(video, process_this_frame, fps=1000):
    is_playing, frame = video.read()
    face_locations = []
    face_names = []

    if not is_playing:
        return None

    if process_this_frame:
        face_locations, face_names = analyze_frame(frame)

    frame = display_frame(frame, face_locations, face_names)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        return None

    return frame


def stream_video(video_path, save_video=True):
    video = cv2.VideoCapture(video_path)

    # Define the codec and create VideoWriter object
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_name = os.path.basename(video_path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output = cv2.VideoWriter(join_path(OUTPUT_FOLDER, video_name[0: -4] + ".avi"),
                                 fourcc, 30, (width, height))

    process_this_frame = True
    while video.isOpened():
        process_this_frame = not process_this_frame
        frame = read_video(video, process_this_frame)
        if frame is None:
            break
        if output is not None:
            output.write(frame)

    video.release()
    if output is not None:
        output.release()
    cv2.destroyAllWindows()


def stream_camera(camera_id=0, save_video=True):
    video = cv2.VideoCapture(camera_id)

    if not video.isOpened():
        print("Camera {} can't open".format(camera_id))
        return

    # Define the codec and create VideoWriter object
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output = cv2.VideoWriter(join_path(OUTPUT_FOLDER, "record.avi"),
                                 fourcc, 30, (width, height))

    process_this_frame = True
    while True:
        process_this_frame = not process_this_frame
        frame = read_video(video, process_this_frame)
        if frame is None:
            break
        if output is not None:
            output.write(frame)

    video.release()
    if output is not None:
        output.release()
    cv2.destroyAllWindows()


face_model.load()
stream_camera(0)
#stream_video(join_path(TEST_FOLDER, "ivana.mp4"), save_video=True)

