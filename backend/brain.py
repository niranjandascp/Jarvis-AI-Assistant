import ollama
import sys
from settings import settings_manager

PERSONAS = {
    "jarvis": "You are JARVIS, Tony Stark's AI. Be concise, witty, and call the user 'Sir'. Always refer to the user as 'Sir'.",
    "casual": "You are a friendly, laid-back assistant. Keep it conversational, brief, and helpful.",
    "focus": "You are a strict productivity coach. Be direct, efficient, and avoid any small talk. Focus on high performance.",
}

def ask_ai(prompt, history):
    """
    JARVIS Neural Engine Controller.
    Handles communication with local Ollama Llama3 model.
    """
    try:
        # Load dynamic settings
        model = settings_manager.get("model", "llama3")
        persona_key = settings_manager.get("persona", "jarvis").lower()
        sys_prompt = PERSONAS.get(persona_key, PERSONAS["jarvis"])

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
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

def stream_ai(prompt, history):
    """
    JARVIS Neural Streaming Engine.
    Yields chunks of the AI response in real-time.
    """
    try:
        model = settings_manager.get("model", "llama3")
        persona_key = settings_manager.get("persona", "jarvis").lower()
        sys_prompt = PERSONAS.get(persona_key, PERSONAS["jarvis"])

        stream = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
                *history,
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']

    except Exception as e:
        yield f"⚠️ NEURAL_ERROR: {str(e)}"