from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, QPropertyAnimation


class BlinkOverlay(QWidget):
    def __init__(self, text="👀 Blink Reminder"):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(320, 70)

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 60, 120, 180);
                color: white;
                font-size: 18px;
                font-weight: 600;
                border-radius: 20px;
                padding: 16px;
            }
        """)
        label.setGeometry(0, 0, 320, 70)

        self._move_top_right()

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(3000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.close)

    def _move_top_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - 360, 40)

    def show_overlay(self):
        self.setWindowOpacity(1.0)
        self.show()
        self.anim.start()
