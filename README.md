
👁️ Eye Blink Reminder (Local Desktop App)

Prolonged screen usage often leads to reduced blinking, which can cause eye strain, dryness, and discomfort.
Most people are unaware that their blink rate drops significantly while focusing on screens, making the problem hard to notice and correct in real time.
A fully local, privacy-first desktop application that monitors eye blinks using your webcam and gently reminds you to blink when you stare at the screen for too long.
No cloud.
No APIs.
No data leaves your machine.

✨ Features
👀 Real-time blink detection using webcam
⏱️ Smart reminder system (time-based, no spam)
🪟 System-level overlay notification
Appears above all applications
Top-right corner
Smooth fade-out animation
🧾 Debug-friendly terminal logs
BLINK 1, BLINK 2, ...
REMINDER 1, REMINDER 2, ...
🔐 100% local & offline
💻 Works on macOS & Windows
🚪 Clean exit using Q or Esc

🧠 How It Works
Webcam captures frames locally
Face landmarks are detected (MediaPipe)
Eye Aspect Ratio (EAR) is calculated
Real blinks are detected using frame filtering
Timer tracks time since last blink
If you stare too long:
Terminal logs a reminder
A floating overlay appears on screen

📸 Overlay Preview
A subtle, modern reminder pill appears in the top-right corner, above all apps, and fades out automatically.
(UI inspired by modern OS notifications)

🛠️ Tech Stack
Python
OpenCV – camera handling
MediaPipe (Tasks API) – face & eye landmarks
Qt (PyQt6) – system-level overlay UI
Pure math (EAR) – blink detection logic

🔒 Privacy First
❌ No internet required at runtime
❌ No APIs
❌ No tracking
❌ No data storage
All processing happens in memory, on your device.

📁 Project Structure
.
├── main.py          	# App entry point
├── facemesh.py      	# Face landmark detection
├── blinkdetector.py 	# Blink detection logic
├── reminder.py      	# Timer & reminder logic
├── overlay.py       	# System-level overlay UI
├── face_landmarker.task # Local MediaPipe model
└── README.md //td- put this in a code box

⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/cattobooomboom/eye-blink-reminder.git
cd eye-blink-reminder
2️⃣ Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate	# Windows
3️⃣ Install dependencies
pip install opencv-python mediapipe PyQt6
4️⃣ Download the model file
Download and place this file in the project root:
face_landmarker.task
👉 Model link (official MediaPipe):
https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task

▶️ Run the App
python main.py

⌨️ Controls
Key
Action
Q
Exit app
Esc
Exit app


🧪 Debug Output (Terminal)
Example:
BLINK 1
BLINK 2
BLINK 3
REMINDER 1 (no blink for 12s)
BLINK 4. //put this in a code box
Useful for:
Accuracy testing
Threshold tuning
Development & demos

⚠️ Notes (macOS)
macOS may request permissions for:
Camera
Accessibility
Screen Recording
These are required for the overlay to appear above all apps.

🚀 Future Improvements
Click-through overlay
Background blur (glassmorphism)
Tray/menu bar app
Auto-start on boot
Chrome extension version (browser-only)
Blink analytics (per minute / per hour)

🎯 Why This Project?
Most eye-care apps:
Rely on timers only
Use cloud services
Track user behavior
This project:
Responds to real eye behavior
Is fully local
Respects user privacy
Feels like a real desktop utility
 

⭐ If you like this project, consider starring the repo
It helps more than you think 🙂

 

