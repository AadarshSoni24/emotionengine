from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# IMPORT your emotion detector class
from emotion_detector.detect_emotion import EmotionDetector

# Initialize FastAPI
app = FastAPI()

# Allow Unity / frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("neuro_maze")

# Initialize the detector
detector = EmotionDetector()

# In-memory state: This is what Unity will eventually read
state = {
    "difficulty": "Normal",
    "feedback": "Waiting for data...",
    "emotion": "unknown"
}

# Root endpoint to check if server is alive
@app.get("/")
async def root():
    return {
        "message": "NeuroMaze Backend Running",
        "status": "active"
    }

# THE MAIN FUNCTION: Detects emotion and updates difficulty in one go
@app.get("/detect-emotion/")
async def detect_emotion():
    # 1. Get emotion from DeepFace via your detector class
    emotion = detector.detect_emotion()

    # Fallback if DeepFace can't find a face
    if emotion is None:
        emotion = "neutral"

    # 2. THE ADAPTIVE LOGIC (The "Brain" of your project)
    # We map emotions to difficulty levels here
    current_emotion = emotion.lower()
    
    if current_emotion in ["angry", "sad", "fear", "disgust"]:
        diff = "Easy"
        fb = f"Detected {emotion}. Player seems stressed. Reducing challenge."

    elif current_emotion in ["happy", "surprise"]:
        diff = "Hard"
        fb = f"Detected {emotion}. Player is confident! Increasing challenge."

    else:
        diff = "Normal"
        fb = "Player is stable. Keeping standard difficulty."

    # 3. UPDATE THE GLOBAL STATE
    state["emotion"] = emotion
    state["difficulty"] = diff
    state["feedback"] = fb

    logger.info(f"Update: Emotion={emotion}, Difficulty={diff}")

    # 4. Return the full dictionary so the browser/Unity sees everything
    return state

# Unity will call this every few seconds to stay synced
@app.get("/state/")
async def get_state():
    return state