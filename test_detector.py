#test_detector.py
from emotion_detector.detect_emotion import EmotionDetector
import time

detector = EmotionDetector()

while True:
    emotion = detector.detect_emotion()
    print("Detected emotion:", emotion)
    time.sleep(2)
