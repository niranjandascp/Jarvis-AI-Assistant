from flask import Flask, request, jsonify
from flask_cors import CORS
from commands import run_command
from brain import ask_ai

app = Flask(__name__)
CORS(app)

# React-inu vendi memory format onnu maatti
memory = [{"role": "jarvis", "text": "Systems Online, Sir."}]
MAX_MEMORY = 10 

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    # 1. Update memory with user message
    memory.append({"role": "user", "text": user_msg})

    # 2. Check for hard-coded commands
    cmd_reply = run_command(user_msg)
    if cmd_reply:
        memory.append({"role": "jarvis", "text": cmd_reply})
        return jsonify({"reply": cmd_reply})

    # 3. AI logic
    try:
        # Brain expects a specific format, so we pass it carefully
        ai_memory = [{"role": m["role"], "content": m["text"]} for m in memory]
        reply = ask_ai(user_msg, ai_memory)
        
        memory.append({"role": "jarvis", "text": reply})
        
        # Keep memory clean
        if len(memory) > MAX_MEMORY * 2:
            memory.pop(1) # Keep "Systems Online" message, pop others
            memory.pop(1)

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        error_msg = "I encountered a glitch, Sir."
        memory.append({"role": "jarvis", "text": error_msg})
        return jsonify({"reply": error_msg})

# 🔴 ITHU ADD CHEYYUKA: Frontend-inu data edukkan vendi
@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(memory)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)