import speech_recognition as sr

def detect_wake_word():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🎧 Waiting for 'Jarvis'...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=2)
                text = recognizer.recognize_google(audio).lower()
                
                if "jarvis" in text:
                    print("🧠 WAKE WORD DETECTED")
                    return True
            except:
                # Ethu error vannalum loop continue cheyyaan (Shabdam onnum kettillengil)
                continue