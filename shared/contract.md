# EmotionEngine WebSocket Contract

## Emotion Event (every 300ms)

Sent from backend → frontend

{
  "emotion": "happy",
  "confidence": 0.84,
  "timestamp": 1707823200,
  "history": ["neutral", "happy", "happy", "stressed"]
}

Fields:
- emotion: string
  angry | disgusted | fearful | happy | sad | surprised | neutral

- confidence: float
  0.0 to 1.0

- timestamp: unix timestamp

- history: array of last emotions


## Narrative Event (every 30s)

{
  "type": "narrative",
  "dialogue": "You seem troubled, traveller."
}


## Safe Mode Event

{
  "type": "safe_mode"
}

