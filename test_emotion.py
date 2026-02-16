#test_emotion.py

import cv2
from deepface import DeepFace

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False
        )

        emotion = result[0]['dominant_emotion']

        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        print("Emotion:", emotion)

    except Exception as e:
        print("Error:", e)

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
