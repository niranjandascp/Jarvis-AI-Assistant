import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto scroll logic
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🔴 SYNC WITH BACKEND: Voice engine vazhi varunnu updates screen-il kaanan
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/history");
        // Only update if the length changed to avoid flickering
        if (res.data.length !== messages.length) {
          setMessages(res.data);
        }
      } catch (err) {
        console.error("History fetch failed. Check if Flask is running.");
      }
    };

    const interval = setInterval(fetchHistory, 1000);
    return () => clearInterval(interval);
  }, [messages.length]);

  const sendMessage = async () => {
    if (!input || loading) return;
    const userText = input;
    setInput("");
    setLoading(true);

    try {
      // Backend handles memory now, so we just POST
      await axios.post("http://127.0.0.1:5000/chat", { message: userText });
    } catch (err) {
      console.error("Send failed");
    }
    setLoading(false);
  };

  const startVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return alert("Mic not supported in this environment.");
    
    const recognition = new SpeechRecognition();
    recognition.start();
    setListening(true);

    recognition.onresult = async (event) => {
      const voiceText = event.results[0][0].transcript;
      setLoading(true);
      setListening(false);
      try {
        await axios.post("http://127.0.0.1:5000/chat", { message: voiceText });
      } catch (err) { console.error(err); }
      setLoading(false);
    };
  };

  return (
    <div className="app-container">
      <div className="reactor-container">
        <div className={`arc-reactor ${loading ? "active" : ""}`}></div>
        <h2 className="glitch-text">MOLTBOT AI</h2>
      </div>

      <div id="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role === "user" ? "user-msg" : "jarvis-msg"}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="thinking">🧠 Analysing...</div>}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Command me, Sir..."
        />
        <button onClick={startVoice} className={listening ? "listening-btn" : ""}>
          {listening ? "🛑" : "🎤"}
        </button>
      </div>
    </div>
  );
}

export default App;