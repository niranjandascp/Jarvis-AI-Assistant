import ollama
import speech_recognition as sr
import pyttsx3
import threading

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- SPEECH RECOGNITION ----------------
recognizer = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=6)

        text = recognizer.recognize_google(audio)
        print("You (voice):", text)
        return text.lower()

    except:
        return ""

# ---------------- AI BRAIN ----------------
def ask_ai(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# ---------------- INPUT HANDLER ----------------
def get_input():
    mode = input("\nType or say (t/v): ").lower()

    if mode == "v":
        return listen()
    else:
        return input("You (text): ").lower()

# ---------------- MAIN LOOP ----------------
speak("Jarvis hybrid system activated.")

while True:
    command = get_input()

    if not command:
        continue

    if "stop" in command or "exit" in command:
        speak("Shutting down system.")
        break

    print("Processing:", command)

    reply = ask_ai(command)

    speak(reply)