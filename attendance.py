"""Real-time face-recognition attendance system.

Reads the webcam, matches faces against registered encodings and logs
attendance to Firebase Realtime Database.

Keys:  r = register the face currently in view   q = quit
"""
import os
import sys
import time
from datetime import datetime

import cv2
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials, db

import config


def init_firebase():
    if not config.DATABASE_URL:
        sys.exit("Set FIREBASE_DATABASE_URL (see README).")
    if not os.path.exists(config.SERVICE_ACCOUNT_PATH):
        sys.exit(f"Service account key not found: {config.SERVICE_ACCOUNT_PATH}")
    cred = credentials.Certificate(config.SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL": config.DATABASE_URL})
    return db.reference("attendance")


def load_known_faces() -> dict:
    os.makedirs(config.ENCODINGS_DIR, exist_ok=True)
    return {
        f[:-4]: np.load(os.path.join(config.ENCODINGS_DIR, f))
        for f in os.listdir(config.ENCODINGS_DIR)
        if f.endswith(".npy")
    }


def best_match(encoding, known: dict):
    """Return the closest registered name within tolerance, else None."""
    if not known:
        return None
    names = list(known)
    distances = face_recognition.face_distance([known[n] for n in names], encoding)
    i = int(np.argmin(distances))
    return names[i] if distances[i] <= config.MATCH_TOLERANCE else None


def main():
    attendance_ref = init_firebase()
    known = load_known_faces()
    last_logged: dict = {}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Could not open webcam.")
    print(f"Loaded {len(known)} registered face(s). Press 'r' to register, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        small = cv2.resize(frame, (0, 0), fx=config.FRAME_SCALE, fy=config.FRAME_SCALE)
        rgb_small = np.ascontiguousarray(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
        locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, locations)
        scale = int(1 / config.FRAME_SCALE)

        for (top, right, bottom, left), encoding in zip(locations, encodings):
            top, right, bottom, left = (v * scale for v in (top, right, bottom, left))
            name = best_match(encoding, known)

            color = (0, 255, 0) if name else (0, 0, 255)
            label = f"Hi {name}" if name else "Unknown - press 'r' to register"
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if name and time.time() - last_logged.get(name, 0) > config.LOG_COOLDOWN_SECONDS:
                now = datetime.now()
                attendance_ref.push({
                    "name": name,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                })
                last_logged[name] = time.time()
                print(f"Logged: {name} at {now:%H:%M:%S}")

        cv2.imshow("Face Attendance", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("r") and encodings:
            new_name = input("Enter name to register: ").strip()
            if new_name:
                np.save(os.path.join(config.ENCODINGS_DIR, f"{new_name}.npy"), encodings[0])
                known[new_name] = encodings[0]
                print(f"{new_name} registered.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
