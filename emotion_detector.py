# emotion_detector.py
"""
EmotionDetector class for face detection and emotion prediction.
"""
import cv2
import mediapipe as mp
from torchvision import transforms
from PIL import Image
import numpy as np
import sys
import os
import torch
import requests
import time
from typing import Optional

# Handle imports properly whether run as script or module
try:
    # Try direct import first (when running directly)
    from emotion_model import EmotionCNN
except ImportError:
    # Fall back to package import (when imported as module)
    from emotion_detector.emotion_model import EmotionCNN


class EmotionDetector:
    def __init__(
        self,
        model_path="emotion_detector/models/emotion_model.pth",
        api_url: Optional[str] = None,
    ):
        self.model = EmotionCNN()
        self.model.load_state_dict(
            torch.load(model_path, map_location=torch.device("cpu"))
        )
        self.model.eval()
        self.api_url = api_url
        self.transform = transforms.Compose(
            [
                transforms.Resize((48, 48)),
                transforms.Grayscale(num_output_channels=1),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5], std=[0.5]),
            ]
        )
        self.emotions = [
            "Anger",
            "Disgust",
            "Fear",
            "Happiness",
            "Sadness",
            "Surprise",
            "Neutral",
        ]
        self.mp_face_mesh = mp.solutions.face_mesh  # type: ignore
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5)

    def detect_emotion(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_frame)
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                h, w, _ = frame.shape
                face_region = self.extract_face_roi(face_landmarks, w, h, frame)
                if face_region is not None:
                    face_image = Image.fromarray(face_region)
                    input_tensor = self.transform(face_image).unsqueeze(0)  # type: ignore
                    with torch.no_grad():
                        output = self.model(input_tensor)
                        _, predicted = torch.max(output, 1)
                        return self.emotions[predicted.item()]  # type: ignore
        return "Neutral"

    def extract_face_roi(self, landmarks, width, height, frame):
        face_points = [
            (int(landmark.x * width), int(landmark.y * height))
            for landmark in landmarks.landmark
        ]
        x_min = max(min(face_points, key=lambda x: x[0])[0], 0)
        x_max = min(max(face_points, key=lambda x: x[0])[0], width)
        y_min = max(min(face_points, key=lambda x: x[1])[1], 0)
        y_max = min(max(face_points, key=lambda x: x[1])[1], height)
        if x_max <= x_min or y_max <= y_min:
            return None
        roi = frame[y_min:y_max, x_min:x_max]
        if roi.size == 0:
            return None
        return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    def run_continuous_detection(self, update_interval: float = 1.0):
        """Run continuous emotion detection and send updates to the backend."""
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                emotion = self.detect_emotion(frame)
                if self.api_url:
                    self.send_emotion_update(emotion)

                time.sleep(update_interval)
        finally:
            cap.release()

    def send_emotion_update(self, emotion: str):
        """Send emotion update to the backend API."""
        if not self.api_url:
            return

        try:
            response = requests.post(
                f"{self.api_url}/adjust-difficulty/", json={"emotion": emotion}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error sending emotion update: {e}")

    def start_api_service(self, host: str = "127.0.0.1", port: int = 8001):
        """Start the emotion detector as an API service."""
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI()

        @app.get("/detect")
        async def detect_emotion():
            cap = cv2.VideoCapture(0)
            try:
                ret, frame = cap.read()
                if ret:
                    emotion = self.detect_emotion(frame)
                    return {"emotion": emotion}
                return {"emotion": "Neutral"}
            finally:
                cap.release()

        uvicorn.run(app, host=host, port=port)
