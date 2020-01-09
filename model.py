import pickle
import os
import face_recognition
from env import join_path
import numpy as np
import cv2


class FaceEncodings:

    encodings = []
    names = []
    known_faces = {}
    _pickle_name = "labels.pickles"

    def __init__(self, root):
        self._root = root

    def read(self):
        file_name = join_path(self._root, self._pickle_name)
        if not os.path.exists(file_name):
            return False

        with open(file_name, "rb") as file:
            self.known_faces = pickle.load(file)
        if self.known_faces is None:
            return False

        for name in self.known_faces:
            self.names.append(name)
            self.encodings.append(self.known_faces[name])
        return True

    def save(self):
        with open(join_path(self._root, self._pickle_name), "wb") as file:
            pickle.dump(self.known_faces, file)

    def load(self):
        has_data = self.read()
        if has_data:
            print("Encodings Loaded")
            return

        print("No saved encodings found.")
        print("Registering encodings. Might take a while...")
        for root, dirs, files in os.walk(self._root):
            for file_name in files:
                if not file_name.endswith(".png") and not file_name.endswith(".jpg"):
                    continue
                image_path = join_path(root, file_name)
                name = file_name[0: -4].title()

                print("Processing {}".format(image_path))

                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                if name not in self.known_faces:
                    self.names.append(name)
                    self.encodings.append(encoding)
                    self.known_faces[name] = encoding
                print("{} encodings added".format(name))
        self.save()
        print("Encodings Loaded")

    def analyze_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.names[best_match_index]

            face_names.append(name)

        return face_locations, face_names

    def recognize(self, frame):
        face_locations, face_names = self.analyze_frame(frame)
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

        return frame
