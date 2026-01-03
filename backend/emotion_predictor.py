import cv2
import numpy as np
import tensorflow as tf
import os
from collections import deque, Counter

# ---------------- LOAD MODEL ----------------
MODEL_PATH = os.path.join("model", "emotion_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

EMOTIONS = ["angry", "happy", "neutral", "sad", "surprise"]

# ---------------- FACE DETECTOR ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- EMOTION SMOOTHING ----------------
emotion_buffer = deque(maxlen=7)

# ---------------- PREDICTION FUNCTION ----------------
def predict_emotion_from_image(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect face
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return "neutral"

    # Take first detected face
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]

    # Resize to model input
    face = cv2.resize(face, (48, 48))

    # Normalize
    face = face / 255.0
    face = face.reshape(1, 48, 48, 1)

    # Predict
    preds = model.predict(face, verbose=0)
    confidence = np.max(preds)

    # Confidence threshold
    if confidence < 0.55:
        return "neutral"

    emotion = EMOTIONS[np.argmax(preds)]

    # Smooth emotion (majority voting)
    emotion_buffer.append(emotion)
    emotion = Counter(emotion_buffer).most_common(1)[0][0]

    return emotion
