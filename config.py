"""Central configuration. Secrets come from environment variables, never from the repo."""
import os

# Path to your Firebase service-account key (keep this file OUT of git)
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT", "serviceAccount.json")

# Your Firebase Realtime Database URL, e.g. https://<project-id>-default-rtdb.<region>.firebasedatabase.app/
DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")

ENCODINGS_DIR = "encodings"      # saved face encodings (.npy) - biometric data, git-ignored
KNOWN_FACES_DIR = "known_faces"  # source photos used for registration - git-ignored

MATCH_TOLERANCE = 0.5            # lower = stricter matching
LOG_COOLDOWN_SECONDS = 60        # min gap between two log entries for the same person
FRAME_SCALE = 0.25               # downscale frames for faster detection
