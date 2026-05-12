from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from commands import run_command
from brain import ask_ai, stream_ai
from memory import memory_manager
import memory
from settings import settings_manager
import pyttsx3
import subprocess
import shutil
import time
import threading
import requests as http_requests
import sys
import os
import json
import queue
import vosk
import sounddevice as sd

# Suppress Vosk logging
vosk.SetLogLevel(-1)

# ============================================================
#  OLLAMA AUTO-START ENGINE
#  Ensures the Ollama service is alive before JARVIS boots.
# ============================================================
OLLAMA_API = "http://127.0.0.1:11434"

def is_ollama_running():
    """Check if Ollama API is responding."""
    try:
        r = http_requests.get(OLLAMA_API, timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def start_ollama():
    """
    Launch 'ollama serve' as a detached background process.
    Works on Windows (CREATE_NO_WINDOW) and falls back for other OS.
    """
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        # Try common Windows install location
        default = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama.exe")
        if os.path.isfile(default):
            ollama_path = default
        else:
            print("[WARN] OLLAMA NOT FOUND - Install from https://ollama.com", file=sys.stderr)
            return False

    print(f"[BOOT] Starting Ollama from: {ollama_path}")
    try:
        # Launch as a fully detached background process
        if sys.platform == "win32":
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                [ollama_path, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=CREATE_NO_WINDOW,
            )
        else:
            subprocess.Popen(
                [ollama_path, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return True
    except Exception as e:
        print(f"[WARN] Failed to launch Ollama: {e}", file=sys.stderr)
        return False

def ensure_ollama(max_wait=30):
    """
    Guarantee Ollama is running. If not, start it and wait until it responds.
    """
    if is_ollama_running():
        print("[OK] Ollama is already running.")
        return True

    print("[BOOT] Ollama not detected - launching automatically...")
    if not start_ollama():
        return False

    # Poll until Ollama is ready
    for i in range(max_wait):
        time.sleep(1)
        if is_ollama_running():
            print(f"[OK] Ollama is online (took {i + 1}s)")
            return True
        if i % 5 == 4:
            print(f"   [WAIT] Still waiting for Ollama... ({i + 1}s)")

    print("[FAIL] Ollama failed to start within timeout.", file=sys.stderr)
    return False


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
    ollama_ok = is_ollama_running()
    return jsonify({
        "status": "online",
        "system": "JARVIS",
        "model": settings_manager.get("model"),
        "ollama": "online" if ollama_ok else "offline",
        "history_depth": len(memory_manager.memory)
    })

@app.route("/ollama-status", methods=["GET"])
def ollama_status():
    """Dedicated endpoint to check / restart Ollama."""
    if is_ollama_running():
        return jsonify({"ollama": "online"})
    
    # Try to auto-recover
    print("Ollama went offline - attempting auto-recovery...")
    recovered = ensure_ollama(max_wait=15)
    return jsonify({
        "ollama": "online" if recovered else "offline",
        "recovered": recovered
    })

@app.route("/get-settings", methods=["GET"])
def get_settings():
    return jsonify(settings_manager.settings)

@app.route("/stt-stream", methods=["GET"])
def stt_stream():
    """Streams real-time transcription from the backend microphone to the frontend."""
    def generate():
        model_path = os.path.join(os.path.dirname(__file__), "model")
        if not os.path.exists(model_path):
            yield f"data: {json.dumps({'error': 'Vosk Model not found'})}\n\n"
            return

        model = vosk.Model(model_path)
        recognizer = vosk.KaldiRecognizer(model, 16000)
        
        audio_q = queue.Queue()
        def callback(indata, frames, time, status):
            audio_q.put(bytes(indata))

        print("[STT] Backend stream started...")
        
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                                   channels=1, callback=callback):
                while True:
                    data = audio_q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "")
                        if text:
                            yield f"data: {json.dumps({'text': text, 'final': True})}\n\n"
                            break # End stream after one full sentence
                    else:
                        partial = json.loads(recognizer.PartialResult())
                        text = partial.get("partial", "")
                        if text:
                            yield f"data: {json.dumps({'text': text, 'final': False})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            print("[STT] Backend stream closed.")

    return Response(generate(), mimetype='text/event-stream')

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

    # ── STEP 0: Ensure Ollama is alive ──
    ensure_ollama()

    print("------------------------------------------")
    print("      JARVIS NEURAL CORE ACTIVATED        ")
    print(f" BANK: {memory_manager.filepath}")
    print(f" MODULE: {memory.__file__}")
    print("------------------------------------------")
    serve(app, host="127.0.0.1", port=5000)