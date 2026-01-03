from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import numpy as np
import cv2
import os

from emotion_predictor import predict_emotion_from_image
from music_recommender import get_song_for_emotion

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
SONGS_DIR = os.path.join(STATIC_DIR, "songs")

app = Flask(__name__)
CORS(app)

# ---------------- SERVE SONGS (🔥 IMPORTANT FIX) ----------------
@app.route("/songs/<emotion>/<filename>")
def serve_song(emotion, filename):
    folder = os.path.join(SONGS_DIR, emotion)
    return send_from_directory(folder, filename)

# ---------------- EMOTION API ----------------
@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.json
        image_data = data["frame"]

        encoded = image_data.split(",")[1]
        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        emotion = predict_emotion_from_image(frame)

        song_url = get_song_for_emotion(emotion)

        return jsonify({
            "emotion": emotion,
            "song_url": song_url
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Emotion detection failed"}), 500


if __name__ == "__main__":
    app.run(debug=False)
