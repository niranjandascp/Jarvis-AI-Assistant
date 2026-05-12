from wake_word import detect_wake_word
from voice_input import listen_command
import requests
import tts

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

    reply = response.json().get("reply", "Sir, I encountered an issue.")
    print("Jarvis:", reply)
    
    # 🔊 VOICE FEEDBACK
    tts.speak(reply)