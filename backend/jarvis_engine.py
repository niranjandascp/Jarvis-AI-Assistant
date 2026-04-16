import requests
from wake_word import detect_wake_word
from stt import listen
from tts import speak

BACKEND = "http://127.0.0.1:5000/chat"

def start_engine():
    print("🚀 Moltbot Systems Online...")
    
    while True:
        # 1. Wait for "Jarvis"
        if detect_wake_word():
            # IVIDEYAANU PASTE CHEYYENDATHU 👇
            speak("Yes Sir?") 
            print("Listening for command...")
            
            # 2. Get voice input
            user_input = listen()
            
            if not user_input or user_input.strip() == "":
                continue

            # 3. Get response from local server
            try:
                response = requests.post(BACKEND, json={"message": user_input})
                reply = response.json().get("reply", "Something went wrong.")
                
                # 4. Speak the response
                speak(reply)
            except Exception as e:
                speak("Sir, the backend server is offline.")

if __name__ == "__main__":
    start_engine()