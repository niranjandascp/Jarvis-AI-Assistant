import requests
from wake_word import detect_wake_word
from voice_input import listen_command

BACKEND = "http://127.0.0.1:5000/chat"

print("🚀 Jarvis Engine Started...")

while True:

    # 🧠 WAIT FOR "JARVIS"
    detect_wake_word()

    print("🧠 Activated")

    # 🎤 LISTEN COMMAND
    command = listen_command()

    if not command:
        continue

    # ⚡ SEND TO BACKEND
    response = requests.post(BACKEND, json={"message": command})

    print("Jarvis:", response.json()["reply"])