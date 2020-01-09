import cv2
import os
from env import OUTPUT_FOLDER, join_path
from library.image import to_tk_image, apply_adjustments

class Video:

    def __init__(self):
        self.path = ""
        self.video = None
        self.fps = 29
        self.delay = 33
        self.process_this_frame = True
        self.valid = False
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.dimension = (0, 0)
        self.video_writer = None
        self.video_name = "record.avi"
        self.font = cv2.FONT_HERSHEY_DUPLEX

    def init(self, source):
        self.path = source
        if os.path.exists(source):
            self.video_name = os.path.basename(source)
            self.video_name = "{}.avi".format(self.video_name[0: -4])
        try:
            self.video = cv2.VideoCapture(source)
            self.dimension = (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                              int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.valid = self.video.isOpened()
            if not self.valid:
                print("Video {} can't open".format(source))
                return
            self.fps = self.video.get(cv2.CAP_PROP_FPS)
            self.delay = int(1000 / self.fps)
        except:
            print("Error in opening video")

    def play(self, container, window, take_guess=None, record=False):
        if record:
            self.video_writer = cv2.VideoWriter(join_path(OUTPUT_FOLDER, self.video_name),
                                                self.fourcc, self.delay, self.dimension)

        while self.valid and self.video.isOpened:
            is_playing, frame = self.video.read()
            if not is_playing:
                return False

            frame = apply_adjustments(frame)
            locations = []
            names = []
            if self.process_this_frame and take_guess:
                locations, names = take_guess(frame)

            self.process_this_frame = not self.process_this_frame

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.video_writer:
                for (top, right, bottom, left), name in zip(locations, names):
                    if name == "Ivana Alawi":
                        name = "Nambawan"
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), self.font, 1.0, (255, 255, 255), 1)
                self.video_writer.write(frame)
            container.update(to_tk_image(rgb_frame, (container.width, container.height)))
            window.update()
            cv2.waitKey(self.delay - 10)

        self.stop()

    def stop(self):
        print("stopping video")
        self.valid = False
        if self.video:
            self.video.release()
            self.video = None

        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
