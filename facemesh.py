import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceMeshDetector:
    def __init__(self):
        """
        Initializes the MediaPipe Face Landmarker (Tasks API).
        Uses a local .task model file.
        """

        base_options = python.BaseOptions(
            model_asset_path="face_landmarker.task"
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def process(self, frame):
        """
        Processes a single video frame.

        Returns:
        - frame (with landmarks drawn)
        - landmarks (list of normalized landmarks or None)
        """

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Run face landmark detection
        result = self.detector.detect(mp_image)

        landmarks = None

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]

            h, w, _ = frame.shape

            # Draw landmarks
            for lm in landmarks:
                x = int(lm.x * w)
                y = int(lm.y * h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        return frame, landmarks
