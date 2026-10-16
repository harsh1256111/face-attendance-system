"""Register a person from a photo.

Usage:
    python register_face.py "Alice" path/to/alice.jpg
"""
import os
import sys

import face_recognition
import numpy as np

import config


def register(name: str, image_path: str) -> bool:
    if not os.path.exists(image_path):
        print(f"Error: image not found: {image_path}")
        return False

    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        print("Error: no face detected in the image.")
        return False
    if len(encodings) > 1:
        print("Warning: multiple faces found, using the first one.")

    os.makedirs(config.ENCODINGS_DIR, exist_ok=True)
    np.save(os.path.join(config.ENCODINGS_DIR, f"{name}.npy"), encodings[0])
    print(f"Success: {name} registered.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Usage: python register_face.py "<name>" <image_path>')
    sys.exit(0 if register(sys.argv[1], sys.argv[2]) else 1)
