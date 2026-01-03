import cv2
import numpy as np
import tensorflow as tf
import os
import time
from music_recommender import recommend_music

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "emotion_model.h5")

model = tf.keras.models.load_model(MODEL_PATH)

emotion_labels = ['angry', 'happy', 'neutral', 'sad', 'surprise']

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(gray, (48, 48))
    face = face / 255.0
    face = face.reshape(1, 48, 48, 1)

    preds = model.predict(face, verbose=0)
    emotion = emotion_labels[np.argmax(preds)]
    songs = recommend_music(emotion)

    cv2.putText(frame, emotion, (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    y = 80
    for song in songs:
        cv2.putText(frame, song.replace(".mp3", ""), (30, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        y += 30

    cv2.imshow("Emotion Based Music Player", frame)

    time.sleep(0.4)  # ⭐ IMPORTANT LINE

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
