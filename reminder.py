import time


class BlinkReminder:
    def __init__(self, remind_after=10, cooldown=10, overlay_duration=5):
        self.remind_after = remind_after
        self.cooldown = cooldown
        self.overlay_duration = overlay_duration

        self.last_blink_time = time.time()
        self.last_reminder_time = 0
        self.overlay_start_time = None

    def blink_detected(self):
        self.last_blink_time = time.time()
        self.overlay_start_time = None

    def check_and_remind(self):
        now = time.time()
        no_blink = now - self.last_blink_time

        if no_blink >= self.remind_after:
            if now - self.last_reminder_time >= self.cooldown:
                self.last_reminder_time = now
                self.overlay_start_time = now
