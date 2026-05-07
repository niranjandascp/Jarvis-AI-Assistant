import ollama

def ask_ai(prompt, history):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are Jarvis, an advanced AI assistant."},
                *history,
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        if "not found" in str(e).lower():
            return "Sir, the 'llama3' model is not installed in Ollama. Please run 'ollama pull llama3' in your terminal."
        return f"Sir, I encountered a neural link error: {str(e)}"