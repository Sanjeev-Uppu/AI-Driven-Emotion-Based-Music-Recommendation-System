import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONGS_DIR = os.path.join(BASE_DIR, "static", "songs")

def get_song_for_emotion(emotion):
    folder = os.path.join(SONGS_DIR, emotion)

    if not os.path.exists(folder):
        return None

    songs = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if not songs:
        return None

    song = random.choice(songs)
    return f"http://127.0.0.1:5000/static/songs/{emotion}/{song}"
