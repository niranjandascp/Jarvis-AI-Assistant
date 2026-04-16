import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  // Back to local state management
  const [messages, setMessages] = useState([{ role: "jarvis", text: "Systems Online, Sir." }]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto scroll to bottom when a new message arrives
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input || loading) return;

    const userText = input;
    setInput("");
    setLoading(true);

    // 1. Add User message to UI immediately
    setMessages((prev) => [...prev, { role: "user", text: userText }]);

    try {
      // 2. Send to Flask
      const res = await axios.post("http://127.0.0.1:5000/chat", { message: userText });
      
      // 3. Add Jarvis reply to UI
      const reply = res.data.reply;
      setMessages((prev) => [...prev, { role: "jarvis", text: reply }]);
      
      // 4. Voice output (Optional)
      const speech = new SpeechSynthesisUtterance(reply);
      window.speechSynthesis.speak(speech);

    } catch (err) {
      setMessages((prev) => [...prev, { role: "jarvis", text: "⚠️ Server connection failed." }]);
    }
    setLoading(false);
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
        {loading && <div className="thinking">🧠 Processing...</div>}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your command..."
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;