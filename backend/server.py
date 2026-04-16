from flask import Flask, request, jsonify
from flask_cors import CORS  # Ensure you ran: pip install flask-cors
from commands import run_command
from brain import ask_ai

app = Flask(__name__)
# This allows ANY frontend to talk to this backend
CORS(app) 

memory = []

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")

        # 1. Check for commands
        cmd_reply = run_command(user_msg)
        if cmd_reply:
            return jsonify({"reply": cmd_reply})

        # 2. Ask the AI
        reply = ask_ai(user_msg, memory)
        
        # Update memory
        memory.append({"role": "user", "content": user_msg})
        memory.append({"role": "assistant", "content": reply})
        
        if len(memory) > 10:
            memory.pop(0)
            memory.pop(0)

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "I encountered a glitch, Sir."})

if __name__ == "__main__":
    # Change host to 127.0.0.1 to match your terminal exactly
    app.run(host="127.0.0.1", port=5000, debug=True)