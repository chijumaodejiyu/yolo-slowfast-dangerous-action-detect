import cv2
import numpy as np
import face_recognition


class FaceDetector:
    def __init__(self):
        self.names = []
        self.known_encodes = []

    def compare(self, image):
        unknown_encode = face_recognition.face_encodings(image)
        matches = face_recognition.compare_faces(self.known_encodes, unknown_encode)
        distances = face_recognition.face_distance(self.known_encodes, unknown_encode)
        min_distance_arg = np.argmin(distances)
        is_known = False
        name = 'Unknown'
        if matches[min_distance_arg]:
            is_known = True
            name = self.names[min_distance_arg]
        return is_known, name

    def load_known(self, dir):


