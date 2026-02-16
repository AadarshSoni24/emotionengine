import cv2
from deepface import DeepFace

class EmotionDetector:

    def __init__(self):
        # Open camera once when class is initialized
        self.cap = cv2.VideoCapture(0)

    def detect_emotion(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        try:
            # 1. Analyze for emotion
            # We set enforce_detection=False so it doesn't crash if you move out of frame
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )

            # Get the data for the first face detected
            face_data = result[0]
            emotion = face_data['dominant_emotion']
            conf = face_data['emotion'][emotion] # This is the confidence score (0-100)
            
            # 2. GET FACE COORDINATES
            region = face_data['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            # 3. DRAW UI ON THE FRAME
            # Draw Main Face Box (Cyan)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

            # Draw "Confidence Bar" Background (Grey)
            cv2.rectangle(frame, (x, y + h + 10), (x + w, y + h + 30), (50, 50, 50), -1)
            
            # Draw "Confidence Bar" Fill (Green)
            bar_width = int((conf / 100) * w)
            cv2.rectangle(frame, (x, y + h + 10), (x + bar_width, y + h + 30), (0, 255, 0), -1)

            # Add Text: Emotion + Confidence %
            label = f"{emotion.upper()} ({int(conf)}%)"
            cv2.putText(frame, label, (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            # 4. SHOW THE WINDOW
            cv2.imshow('NeuroMaze AI Vision', frame)
            
            # This allows the UI to refresh lively
            cv2.waitKey(1) 

            return emotion

        except Exception as e:
            print("AI Vision Error:", e)
            return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = EmotionDetector()
    print("--- NeuroMaze AI Vision Started ---")
    print("Press 'q' on the camera window to exit.")
    
    try:
        while True:
            # This calls your detection + the new UI logic
            emo = detector.detect_emotion()
            
            # Press 'q' to stop the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        detector.release()
        print("Camera released.")