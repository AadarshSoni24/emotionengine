import requests

BACKEND_URL = "http://127.0.0.1:8000/adjust-difficulty/"


def send_emotion_data(emotion, puzzle_time, error_rate):
    payload = {"emotion": emotion, "puzzle_time": puzzle_time, "error_rate": error_rate}

    try:
        res = requests.post(BACKEND_URL, json=payload)
        if res.ok:
            data = res.json()
            print("[AI Backend Response]", data)
            return data
        else:
            print(f"[ERROR] {res.status_code}: {res.text}")
    except Exception as e:
        print("[EXCEPTION] Backend not reachable:", e)

    return None
