from flask import Flask, request, jsonify
from flask_cors import CORS
from commands import run_command
from brain import ask_ai
from memory import memory_manager
import pyttsx3
import threading
import sys

app = Flask(__name__)
CORS(app) 

# --- SERVER-SIDE VOICE ENGINE ---
engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"Voice Engine Warning: {e}")

engine_lock = threading.Lock()

def speak_text(text):
    if not engine: return
    def run():
        try:
            with engine_lock:
                engine.say(text)
                engine.runAndWait()
        except:
            pass
    threading.Thread(target=run, daemon=True).start()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received, Sir."}), 400
            
        user_msg = data.get("message", "")
        use_server_voice = data.get("use_server_voice", False)

        # 1. Check for system commands
        cmd_reply = run_command(user_msg)
        if cmd_reply:
            if use_server_voice:
                speak_text(cmd_reply)
            return jsonify({"reply": cmd_reply})

        # 2. Get Long-term Memory for context
        context = memory_manager.get_memory(limit=10)

        # 3. Ask AI with context
        reply = ask_ai(user_msg, context)
        
        # 4. Save to persistent memory
        memory_manager.add_interaction(user_msg, reply)

        # 5. Optional Server Voice
        if use_server_voice:
            speak_text(reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({"reply": f"I encountered a neural glitch, Sir: {str(e)}"})

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    if text:
        speak_text(text)
        return jsonify({"status": "speaking"})
    return jsonify({"status": "error"}), 400

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "model": "llama3", "memory_count": len(memory_manager.memory)})

if __name__ == "__main__":
    from waitress import serve
    print("Moltbot Backend starting on http://127.0.0.1:5000")
    serve(app, host="127.0.0.1", port=5000)