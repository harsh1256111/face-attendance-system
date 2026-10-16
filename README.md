# Face Attendance System

A real-time attendance tracker that recognizes faces from a webcam feed and logs check-ins to **Firebase Realtime Database**. Built with Python, OpenCV and `face_recognition` (dlib).

## Features
- Live face detection and recognition from a webcam
- Register new people from a photo (CLI) or on the fly with a key press
- Automatic cloud logging of name, date and time to Firebase
- Per-person cooldown to prevent duplicate log spam
- Frame downscaling for smoother real-time performance
- Secrets and biometric data kept out of version control

## How it works
1. A photo is converted into a 128-dimension face encoding and stored as a `.npy` file.
2. Each webcam frame is downscaled, faces are located and encoded.
3. Encodings are compared to registered faces by Euclidean distance; the closest match within the tolerance wins.
4. Matches are pushed to `attendance/` in Firebase, rate-limited per person.

## Tech stack
Python · OpenCV · dlib / face_recognition · NumPy · Firebase Admin SDK (Realtime Database)

## Setup
```bash
git clone https://github.com/<your-username>/face-attendance-system.git
cd face-attendance-system
python -m venv venv
venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
> **Windows tip:** `dlib` needs a prebuilt wheel matching your Python version, or CMake + Visual Studio Build Tools.

### Firebase
1. Create a project and a **Realtime Database** in the [Firebase console](https://console.firebase.google.com/).
2. *Project settings → Service accounts → Generate new private key*, save it as `serviceAccount.json` in the project root (it is git-ignored).
3. Set environment variables:
```bash
# Windows PowerShell
$env:FIREBASE_DATABASE_URL="https://<project-id>-default-rtdb.<region>.firebasedatabase.app/"
# macOS/Linux
export FIREBASE_DATABASE_URL="https://<project-id>-default-rtdb.<region>.firebasedatabase.app/"
```

## Usage
Register a person from a photo:
```bash
python register_face.py "Alice" known_faces/alice.jpg
```
Run the attendance tracker:
```bash
python attendance.py
```
Press **r** to register the face in view, **q** to quit.

## Project structure
```
├── attendance.py      # live recognition + Firebase logging
├── register_face.py   # register a face from an image
├── config.py          # settings (env-based secrets, thresholds)
├── requirements.txt
├── encodings/         # saved face encodings (git-ignored)
└── known_faces/       # source photos (git-ignored)
```

## Privacy & security
Face encodings are biometric data. This repo ignores them by default; only register people who have consented, and never commit credentials or personal photos.

## Future improvements
- Web dashboard to view attendance in real time
- Liveness detection to block photo spoofing
- Export attendance to CSV / Google Sheets

## License
MIT
