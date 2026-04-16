from wake_word import detect_wake_word
from voice_input import listen_command
import requests

BACKEND = "http://127.0.0.1:5000/chat"

while True:

    # 🧠 WAIT FOR WAKE WORD
    detect_wake_word()

    print("🧠 Jarvis Activated")

    # 🎤 LISTEN COMMAND
    command = listen_command()

    if not command:
        continue

    # ⚡ SEND TO BACKEND
    response = requests.post(BACKEND, json={"message": command})

    print("Jarvis:", response.json()["reply"])