import { useState } from "react";
import axios from "axios";
import logo from "./logo.svg";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [listening, setListening] = useState(false);

  // 🧠 TEXT CHAT
  const sendMessage = async () => {
    if (!input) return;

    const res = await axios.post("http://127.0.0.1:5000/chat", {
      message: input,
    });

    setMessages((prev) => [
      ...prev,
      { role: "user", text: input },
      { role: "jarvis", text: res.data.reply },
    ]);

    setInput("");

    // 🗣️ Speak response
    const speech = new SpeechSynthesisUtterance(res.data.reply);
    speech.rate = 1;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
  };

  // 🎤 VOICE INPUT
  const startVoice = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.start();

    setListening(true);

    recognition.onresult = async (event) => {
      const voiceText = event.results[0][0].transcript;
      setListening(false);

      const res = await axios.post("http://127.0.0.1:5000/chat", {
        message: voiceText,
      });

      setMessages((prev) => [
        ...prev,
        { role: "user", text: voiceText },
        { role: "jarvis", text: res.data.reply },
      ]);

      // 🗣️ Speak response
      const speech = new SpeechSynthesisUtterance(res.data.reply);
      speech.rate = 1;
      speech.pitch = 1;
      window.speechSynthesis.speak(speech);
    };
  };

  return (
    <div className="App" style={{ background: "#000", color: "#fff", height: "100vh" }}>
      
      {/* HEADER */}
      <header className="App-header" style={{ padding: 20 }}>
        <img src={logo} className="App-logo" alt="logo" />

        <h2>🧠 JARVIS AI</h2>

        {/* CHAT BOX */}
        <div
          style={{
            width: "80%",
            height: "50vh",
            overflowY: "auto",
            border: "1px solid gray",
            padding: 10,
            marginTop: 20,
          }}
        >
          {messages.map((m, i) => (
            <p key={i}>
              <b>{m.role}:</b> {m.text}
            </p>
          ))}
        </div>

        {/* INPUT AREA */}
        <div style={{ marginTop: 20, display: "flex", gap: 10 }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{ padding: 10, width: "60%" }}
            placeholder="Ask Jarvis..."
          />

          <button onClick={sendMessage} style={{ padding: 10 }}>
            Send
          </button>

          <button
            onClick={startVoice}
            style={{
              padding: 10,
              background: listening ? "red" : "green",
              color: "white",
            }}
          >
            🎤 {listening ? "Listening..." : "Speak"}
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;