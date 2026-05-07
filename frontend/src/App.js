import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { gsap } from "gsap";
import Visualizer from "./components/Visualizer";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([{ role: "jarvis", text: "Systems Online, Sir. How may I assist you today?" }]);
  const [loading, setLoading] = useState(false);
  const [systemReady, setSystemReady] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Robust startup sequence
    const timer = setTimeout(() => {
        setSystemReady(true);
    }, 3500); // Fail-safe: Always show UI after 3.5s

    const tl = gsap.timeline();
    tl.to(".loading-overlay", { 
        opacity: 0, 
        duration: 1.5, 
        delay: 2, 
        ease: "power2.inOut",
        onComplete: () => setSystemReady(true) 
    });

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input || loading) return;

    const userText = input;
    setInput("");
    setLoading(true);

    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    
    gsap.to(".three-container", { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { message: userText });
      const reply = res.data.reply;
      
      setMessages((prev) => [...prev, { role: "jarvis", text: reply }]);
      
      const speech = new SpeechSynthesisUtterance(reply);
      speech.rate = 1.1;
      window.speechSynthesis.speak(speech);

    } catch (err) {
      setMessages((prev) => [...prev, { role: "jarvis", text: "⚠️ SYSTEM ERROR: Neural Backend Link Severed." }]);
    }
    setLoading(false);
  };

  return (
    <div className="main-wrapper">
      {/* Loading Overlay remains until systemReady */}
      {!systemReady && (
        <div className="loading-overlay">
          <div className="loader-content">
             <div className="spinner-outer">
                <div className="spinner-inner"></div>
             </div>
             <p className="loading-text">DECRYPTING MOLTBOT OS...</p>
             <div className="progress-bar-container">
                <div className="progress-bar-fill"></div>
             </div>
          </div>
        </div>
      )}

      {/* Main App Container - always rendered but hidden by overlay */}
      <div className={`app-container ${systemReady ? 'visible' : 'hidden'}`}>
        <header className="app-header">
           <div className="status-indicator">
              <span className="dot pulse"></span>
              <span className="status-text">ENCRYPTED LINK ACTIVE</span>
           </div>
           <div className="drag-handle">MOLTBOT v1.0.4</div>
           <div className="window-controls">
              <button className="ctrl-btn" onClick={() => window.close()}>×</button>
           </div>
        </header>

        <div className="content-grid">
            <div className="left-panel">
                <div className="reactor-section">
                    <Visualizer active={loading} />
                    <h1 className="glitch-text" data-text="MOLTBOT">MOLTBOT</h1>
                    <p className="subtitle">ADVANCED NEURAL INTERFACE</p>
                </div>
            </div>

            <div className="right-panel">
                <div id="chat-container">
                    {messages.map((msg, index) => (
                        <div key={index} className={`message-wrapper ${msg.role}`}>
                            <div className="message-header">
                                {msg.role === "user" ? "AUTHORIZATION: USER" : "SOURCE: JARVIS"}
                            </div>
                            <div className="message-content">
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="thinking-indicator">
                            <span className="typing-dot"></span>
                            <span className="typing-dot"></span>
                            <span className="typing-dot"></span>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>

                <div className="input-section">
                    <div className="input-wrapper">
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                            placeholder="Enter system command..."
                            autoFocus
                        />
                        <button 
                            className={`send-btn ${loading ? 'busy' : ''}`} 
                            onClick={sendMessage} 
                            disabled={loading}
                        >
                            {loading ? "PROCESS" : "EXECUTE"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;