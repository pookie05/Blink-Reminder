import cv2
import time
import math
from collections import deque

import mediapipe as mp

# ---------------- CONFIG ----------------
EAR_CONSEC_FRAMES = 3
EAR_SMOOTHING_FRAMES = 5
CALIBRATION_TIME = 5  # seconds
# ---------------------------------------

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmark indices (MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def euclidean(p1, p2):
    return math.dist(p1, p2)


def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


# ---------------- STATE ----------------
blink_counter = 0
total_blinks = 0

ear_buffer = deque(maxlen=EAR_SMOOTHING_FRAMES)

calibrated = False
baseline_ear_values = []
start_time = time.time()
EAR_THRESHOLD = None
# --------------------------------------

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0]

        left_eye = []
        right_eye = []

        for idx in LEFT_EYE:
            lm = face.landmark[idx]
            left_eye.append((int(lm.x * w), int(lm.y * h)))

        for idx in RIGHT_EYE:
            lm = face.landmark[idx]
            right_eye.append((int(lm.x * w), int(lm.y * h)))

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # ---- SMOOTHING ----
        ear_buffer.append(ear)
        ear_smoothed = sum(ear_buffer) / len(ear_buffer)

        # ---- CALIBRATION ----
        if not calibrated:
            baseline_ear_values.append(ear_smoothed)
            elapsed = time.time() - start_time

            cv2.putText(
                frame,
                f"Calibrating... {int(elapsed)}s",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            if elapsed >= CALIBRATION_TIME:
                baseline_ear = sum(baseline_ear_values) / len(baseline_ear_values)
                EAR_THRESHOLD = baseline_ear * 0.75
                calibrated = True

            cv2.imshow("Blink Detector", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # ---- BLINK LOGIC ----
        if ear_smoothed < EAR_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= EAR_CONSEC_FRAMES:
                total_blinks += 1
            blink_counter = 0

        # ---- DEBUG UI ----
        cv2.putText(
            frame,
            f"EAR: {ear_smoothed:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Blinks: {total_blinks}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        for p in left_eye + right_eye:
            cv2.circle(frame, p, 2, (0, 255, 0), -1)

    cv2.imshow("Blink Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
