from flask import Flask, request, jsonify
from flask_cors import CORS
from commands import run_command
from brain import ask_ai

app = Flask(__name__)
CORS(app) 

memory = []

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")

        cmd_reply = run_command(user_msg)
        if cmd_reply:
            return jsonify({"reply": cmd_reply})

        reply = ask_ai(user_msg, memory)
        
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
    from waitress import serve
    print("Neural Backend starting on http://127.0.0.1:5000")
    serve(app, host="127.0.0.1", port=5000)