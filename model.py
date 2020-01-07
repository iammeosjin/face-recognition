import pickle
import os
import face_recognition
from env import join_path


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



