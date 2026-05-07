import ollama
import sys

def ask_ai(prompt, history):
    """
    JARVIS Neural Engine Controller.
    Handles communication with local Ollama Llama3 model.
    """
    try:
        # history comes from memory_manager.get_memory(limit=10)
        # It's a list of dictionaries with 'role' and 'content'
        
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are Jarvis, an advanced AI assistant created by Tony Stark. Be helpful, concise, and professional."},
                *history,
                {"role": "user", "content": prompt}
            ]
        )
        
        if 'message' in response and 'content' in response['message']:
            return response["message"]["content"]
        return "Sir, the neural engine returned an empty data stream."

    except Exception as e:
        error_msg = str(e).lower()
        if "not found" in error_msg:
            return "Sir, the 'llama3' model is not detected in your local Ollama instance. Please run 'ollama pull llama3' in your terminal."
        elif "connection" in error_msg:
            return "Sir, I cannot establish a link with the Ollama service. Please ensure Ollama is running in the background."
        
        print(f"Neural Error: {e}", file=sys.stderr)
        return f"Sir, I encountered a neural link error: {str(e)}"