import sys
import cv2

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QEvent, Qt

from facemesh import FaceMeshDetector
from blinkdetector import BlinkDetector
from reminder import BlinkReminder
from overlay import BlinkOverlay


# -------------------------
# GLOBAL EXIT FLAG
# -------------------------
exit_app = False


# -------------------------
# QT KEY HANDLER (FIXES `q`)
# -------------------------
class ExitKeyFilter(QObject):
    def eventFilter(self, obj, event):
        global exit_app

        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Q, Qt.Key.Key_Escape):
                exit_app = True
                return True

        return False


def main():
    global exit_app

    # -------------------------
    # Qt App (for overlay + keys)
    # -------------------------
    app = QApplication(sys.argv)
    key_filter = ExitKeyFilter()
    app.installEventFilter(key_filter)

    # -------------------------
    # Camera + detectors
    # -------------------------
    cap = cv2.VideoCapture(0)

    face_detector = FaceMeshDetector()
    blink_detector = BlinkDetector()

    reminder = BlinkReminder(                                                  #overlay notif
        remind_after=12,    # seconds without blink
        cooldown=10,        # min gap between reminders
        overlay_duration=3
    )

    # -------------------------
    # DEBUG COUNTERS
    # -------------------------
    blink_count = 0
    reminder_count = 0

    overlay = None

    # -------------------------
    # MAIN LOOP
    # -------------------------
    while not exit_app:
        ret, frame = cap.read()
        if not ret:
            break

        frame, landmarks = face_detector.process(frame)

        # ---- BLINK DETECTION (DEBUG LOG) ----
        if landmarks:
            blink = blink_detector.detect_blink(landmarks, frame.shape)
            if blink:
                blink_count += 1
                print(f"BLINK {blink_count}", flush=True)
                reminder.blink_detected()

        # ---- REMINDER CHECK (DEBUG LOG) ----
        prev_overlay = reminder.overlay_start_time
        reminder.check_and_remind()

        if prev_overlay is None and reminder.overlay_start_time is not None:
            reminder_count += 1
            print(
                f"REMINDER {reminder_count} "
                f"(no blink for {reminder.remind_after}s)",
                flush=True
            )

        # ---- SYSTEM OVERLAY ----
        if reminder.overlay_start_time is not None and overlay is None:
            overlay = BlinkOverlay("👀 Blink now")
            overlay.show_overlay()

        if overlay and not overlay.isVisible():
            overlay = None

        # ---- DEBUG CAMERA WINDOW ----
        cv2.imshow("Eye Blink Reminder (Debug)", frame)

        # Let Qt process events
        app.processEvents()

    # -------------------------
    # CLEAN EXIT
    # -------------------------
    cap.release()
    cv2.destroyAllWindows()
    app.quit()


if __name__ == "__main__":
    main()
