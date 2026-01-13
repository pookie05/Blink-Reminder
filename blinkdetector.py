import math


class BlinkDetector:
    def __init__(self, ear_threshold=0.23, min_closed_frames=3):
        self.ear_threshold = ear_threshold
        self.min_closed_frames = min_closed_frames
        self.closed_frames = 0
        self.eye_closed = False

    def _dist(self, p1, p2):
        return math.dist(p1, p2)

    def _ear(self, eye):
        v1 = self._dist(eye[1], eye[5])
        v2 = self._dist(eye[2], eye[4])
        h = self._dist(eye[0], eye[3])
        return (v1 + v2) / (2.0 * h)

    def detect_blink(self, landmarks, frame_shape):
        h, w, _ = frame_shape

        LEFT = [33, 160, 158, 133, 153, 144]  #standard int values
        RIGHT = [362, 385, 387, 263, 373, 380]

        def pts(idxs):
            return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in idxs]

        ear = (self._ear(pts(LEFT)) + self._ear(pts(RIGHT))) / 2.0

        if ear < self.ear_threshold:
            self.closed_frames += 1
            self.eye_closed = True
        else:
            if self.eye_closed and self.closed_frames >= self.min_closed_frames:
                self.closed_frames = 0
                self.eye_closed = False
                return True

            self.closed_frames = 0
            self.eye_closed = False

        return False
