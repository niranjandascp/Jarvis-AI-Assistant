from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os
import webbrowser

app = Flask(__name__)
CORS(app)

# 🧠 memory (limited for stability)
memory = []

MAX_MEMORY = 12  # keeps last 12 messages only


# ⚡ COMMAND ENGINE
def run_command(text):
    text = text.lower()

    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in text:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open notepad" in text:
        os.system("notepad")
        return "Opening Notepad"

    if "shutdown" in text:
        os.system("shutdown /s /t 1")
        return "Shutting down system"

    return None


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_msg = data["message"]

    # ⚡ 1. Command check first
    command_result = run_command(user_msg)

    if command_result:
        return jsonify({"reply": command_result})

    # 🧠 2. Add to memory
    memory.append({"role": "user", "content": user_msg})

    # ✂️ MEMORY TRIM (IMPORTANT FIX)
    if len(memory) > MAX_MEMORY:
        memory.pop(0)

    try:
        # 🤖 3. AI response
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are Jarvis, an advanced AI assistant like Iron Man."},
                *memory
            ]
        )

        reply = response["message"]["content"]

    except Exception as e:
        reply = "Sorry, AI brain is not responding right now."
        print("Ollama error:", e)

    # 💾 4. Save response
    memory.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)