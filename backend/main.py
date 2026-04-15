from stt import listen
from tts import speak
from brain import ask_ai
from memory import load_memory, save_memory


print("🤖 JARVIS STARTED")

memory = load_memory()

while True:
    user_input = listen()

    if not user_input:
        continue

    if "exit" in user_input:
        speak("Shutting down system")
        break

    memory.append({"role": "user", "content": user_input})

    response = ask_ai(user_input, memory)

    memory.append({"role": "assistant", "content": response})
    save_memory(memory)

    speak(response)