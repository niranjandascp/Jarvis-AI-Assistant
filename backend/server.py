from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

memory = []

@app.route("/chat", methods=["POST"])
def chat():
    global memory

    user_msg = request.json["message"]

    memory.append({"role": "user", "content": user_msg})

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are Jarvis, a smart AI assistant."},
            *memory
        ]
    )

    reply = response["message"]["content"]

    memory.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)