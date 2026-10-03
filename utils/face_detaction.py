import cv2
import os
import urllib.request

# ---------------------------------------------------------------
# Locate or download the Haar cascade file
# ---------------------------------------------------------------
CASCADE_URL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/"
    "data/haarcascades/haarcascade_frontalface_default.xml"
)

# Save the cascade next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

# Download only if it's not already present
if not os.path.exists(CASCADE_PATH):
    print(f"Downloading Haar cascade to: {CASCADE_PATH}")
    try:
        urllib.request.urlretrieve(CASCADE_URL, CASCADE_PATH)
        print("Download complete.")
    except Exception as e:
        raise RuntimeError(f"Failed to download cascade file: {e}")

# Load the face detector
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    raise IOError(f"Failed to load cascade file from: {CASCADE_PATH}")

# ---------------------------------------------------------------
# Open webcam
# ---------------------------------------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Error: Could not open camera (index 0).")

WINDOW_NAME = "HealthFusion AI - Face Detection"

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Could not read frame from camera.")
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),
        )

        # Draw boundary around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                "Face Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        # Display result
        cv2.imshow(WINDOW_NAME, frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Quit if user closes the window with X
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()