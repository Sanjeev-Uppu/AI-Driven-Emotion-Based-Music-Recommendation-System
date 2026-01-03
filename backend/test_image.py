import os
from emotion_predictor import predict_emotion_from_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "..", "test_images", "test.jpg")

emotion = predict_emotion_from_image(IMAGE_PATH)
print("Detected Emotion:", emotion)
