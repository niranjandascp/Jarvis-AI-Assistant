import ollama
import speech_recognition as sr
import pyttsx3
import time

# ---------------- JARVIS VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # speed
engine.setProperty('volume', 1.0)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- SPEECH RECOGNITION ----------------
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        speak("I didn't catch that.")
        return ""

# ---------------- AI RESPONSE (OLLAMA) ----------------
def ask_ai(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# ---------------- MAIN LOOP ----------------
speak("Jarvis system activated.")

while True:
    command = listen()

    if command == "":
        continue

    if "stop" in command or "exit" in command:
        speak("Shutting down system.")
        break

    reply = ask_ai(command)
    speak(reply)
    time.sleep(0.5)