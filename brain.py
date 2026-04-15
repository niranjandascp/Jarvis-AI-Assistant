import ollama

def ask_ai(prompt, history):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are Jarvis, an advanced AI assistant."},
            *history,
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]