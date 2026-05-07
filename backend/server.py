from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from commands import run_command
from brain import ask_ai, stream_ai
import memory
from settings import settings_manager
import memory # Import the module first
import pyttsx3
import threading
import sys
import os

# --- JARVIS CORE SERVER ---
app = Flask(__name__)
CORS(app) 

# DIAGNOSTIC: Print exactly where we are importing memory from
print(f"DEBUG: Memory Module Location -> {memory.__file__}")

# --- SERVER-SIDE VOICE ENGINE ---
engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"JARVIS_VOICE: Offline ({e})")

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
            return jsonify({"reply": "Sir, I am not receiving your data stream."}), 400
            
        user_msg = data.get("message", "")
        use_server_voice = data.get("use_server_voice", False)

        # 1. Command Execution
        cmd_reply = run_command(user_msg)
        if cmd_reply:
            if use_server_voice:
                speak_text(cmd_reply)
            return jsonify({"reply": cmd_reply})

        # 2. Context retrieval
        context = memory_manager.get_memory(limit=10)

        # 3. AI Inference
        reply = ask_ai(user_msg, context)
        
        # 4. Save interaction
        memory_manager.add_interaction(user_msg, reply)

        # 5. Voice Feedback
        if use_server_voice:
            speak_text(reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"SYSTEM_ERROR: {e}", file=sys.stderr)
        return jsonify({"reply": f"Sir, I encountered a neural glitch: {str(e)}"})

@app.route("/stream", methods=["POST"])
def stream():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")
        
        # 1. Context retrieval
        context = memory_manager.get_memory(limit=10)

        def generate():
            full_reply = ""
            for chunk in stream_ai(user_msg, context):
                full_reply += chunk
                yield f"data: {chunk}\n\n"
            
            # 2. Save interaction after stream ends
            memory_manager.add_interaction(user_msg, full_reply)
            yield "data: [DONE]\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({"reply": f"Streaming Error: {str(e)}"}), 500

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "system": "JARVIS",
        "model": settings_manager.get("model"),
        "history_depth": len(memory_manager.memory)
    })

@app.route("/get-settings", methods=["GET"])
def get_settings():
    return jsonify(settings_manager.settings)

@app.route("/set-model", methods=["POST"])
def set_model():
    try:
        data = request.get_json()
        new_model = data.get("model")
        if not new_model:
            return jsonify({"error": "No model specified"}), 400
        
        settings_manager.set("model", new_model)
        return jsonify({"ok": True, "model": new_model})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    print("------------------------------------------")
    print("      JARVIS NEURAL CORE ACTIVATED        ")
    print(f" BANK: {memory_manager.filepath}")
    print(f" MODULE: {memory.__file__}")
    print("------------------------------------------")
    serve(app, host="127.0.0.1", port=5000)