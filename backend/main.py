import asyncio
import json
import time
import random
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# 1. Initialize the app ONLY ONCE
app = FastAPI()

# 2. Define constants
EMOTIONS = [
    "angry",
    "disgusted",
    "fearful",
    "happy",
    "sad",
    "surprised",
    "neutral"
]

# 3. Connection Manager Class
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Client connected")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print("Client disconnected")

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_text(json.dumps(data))

manager = ConnectionManager()

# 4. Helper function to generate mock data
def get_mock_emotion():
    emotion = random.choice(EMOTIONS)
    confidence = round(random.uniform(0.7, 0.99), 2)
    timestamp = int(time.time())

    return {
        "emotion": emotion,
        "confidence": confidence,
        "timestamp": timestamp,
        "history": [emotion]
    }

# 5. Routes

# HTTP Route
@app.get("/")
def home():
    return {"message": "EmotionEngine backend running"}

# WebSocket Route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = get_mock_emotion()
            await manager.send_json(websocket, data)
            await asyncio.sleep(0.3)  # Send data every 300ms
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

# 6. Entry point
if __name__ == "__main__":
    # Ensure your file is named 'main.py' for this string to work, 
    # or just run the file directly with Python.
    uvicorn.run(app, host="127.0.0.1", port=8000)