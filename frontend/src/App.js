import { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input) return;

    const res = await axios.post("http://127.0.0.1:5000/chat", {
      message: input,
    });

    setMessages([
      ...messages,
      { role: "user", text: input },
      { role: "jarvis", text: res.data.reply },
    ]);

    setInput("");
  };

  return (
    <div style={{ background: "black", color: "white", height: "100vh", padding: 20 }}>
      <h1>🧠 JARVIS AI</h1>

      <div style={{ height: "70vh", overflowY: "auto", border: "1px solid gray", padding: 10 }}>
        {messages.map((m, i) => (
          <p key={i}>
            <b>{m.role}:</b> {m.text}
          </p>
        ))}
      </div>

      <div style={{ marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ padding: 10, width: "80%" }}
        />
        <button onClick={sendMessage} style={{ padding: 10 }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;