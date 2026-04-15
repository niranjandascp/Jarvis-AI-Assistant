import ollama
import pyttsx3

engine = pyttsx3.init()

print("🤖 MoltBot Voice Started!\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': user_input}]
    )

    reply = response['message']['content']

    print("Bot:", reply)

    engine.say(reply)
    engine.runAndWait()