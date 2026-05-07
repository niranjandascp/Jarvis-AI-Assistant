import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { gsap } from "gsap";
import Visualizer from "./components/Visualizer";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([{ role: "jarvis", text: "Long-term Memory Synced. Systems Online, Sir." }]);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [useServerVoice, setUseServerVoice] = useState(false);
  const [systemReady, setSystemReady] = useState(false);
  const chatEndRef = useRef(null);

  // Voice Recognition Setup
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.lang = "en-US";
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        sendMessage(transcript);
      };
      recognitionRef.current.onend = () => setIsListening(false);
      recognitionRef.current.onerror = () => setIsListening(false);
    }

    const timer = setTimeout(() => setSystemReady(true), 3500);
    const tl = gsap.timeline();
    tl.to(".loading-overlay", { opacity: 0, duration: 1.5, delay: 2, ease: "power2.inOut", onComplete: () => setSystemReady(true) });
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      setIsListening(true);
      recognitionRef.current?.start();
    }
  };

  const sendMessage = async (textOverride = null) => {
    const messageText = textOverride || input;
    if (!messageText || loading) return;

    setInput("");
    setLoading(true);

    // 1. Update UI
    setMessages((prev) => [...prev, { role: "user", text: messageText }]);
    gsap.to(".three-container", { scale: 1.15, duration: 0.2, yoyo: true, repeat: 1 });

    try {
      // 2. Call Backend
      const res = await axios.post("http://127.0.0.1:5000/chat", { 
        message: messageText,
        use_server_voice: useServerVoice 
      });
      
      const reply = res.data.reply;
      setMessages((prev) => [...prev, { role: "jarvis", text: reply }]);
      
      // 3. Handle Voice Output
      if (!useServerVoice) {
        const speech = new SpeechSynthesisUtterance(reply);
        speech.rate = 1.0;
        speech.pitch = 0.9;
        window.speechSynthesis.speak(speech);
      }

    } catch (err) {
      console.error("Connection Error:", err);
      setMessages((prev) => [...prev, { role: "jarvis", text: "⚠️ CRITICAL: Neural Backend Link Severed. Ensure server is running on port 5000." }]);
    }
    setLoading(false);
  };

  return (
    <div className="main-wrapper">
      {!systemReady && (
        <div className="loading-overlay">
          <div className="loader-content">
             <div className="spinner-outer"><div className="spinner-inner"></div></div>
             <p className="loading-text">RECALIBRATING NEURAL MEMORY...</p>
             <div className="progress-bar-container"><div className="progress-bar-fill"></div></div>
          </div>
        </div>
      )}

      <div className={`app-container ${systemReady ? 'visible' : 'hidden'}`}>
        <header className="app-header">
           <div className="status-indicator">
              <span className={`dot ${loading ? 'busy' : 'pulse'}`}></span>
              <span className="status-text">{loading ? "ANALYZING..." : "MEMORY SYNCED"}</span>
           </div>
           <div className="drag-handle">MOLTBOT v1.0.6 - MEMORY ACTIVE</div>
           <div className="header-actions">
              <button className={`server-voice-btn ${useServerVoice ? 'active' : ''}`} onClick={() => setUseServerVoice(!useServerVoice)}>
                {useServerVoice ? "🔊 SERVER" : "🔈 BROWSER"}
              </button>
              <button className="ctrl-btn" onClick={() => window.close()}>×</button>
           </div>
        </header>

        <div className="content-grid">
            <div className="left-panel">
                <div className="reactor-section">
                    <Visualizer active={loading || isListening} />
                    <h1 className="glitch-text" data-text="MOLTBOT">MOLTBOT</h1>
                    <p className="subtitle">PERSISTENT MEMORY MODULE</p>
                </div>
            </div>

            <div className="right-panel">
                <div id="chat-container">
                    {messages.map((msg, index) => (
                        <div key={index} className={`message-wrapper ${msg.role}`}>
                            <div className="message-header">{msg.role === "user" ? "USER_ID: AUTHORIZED" : "JARVIS: CORE_MEMORY"}</div>
                            <div className="message-content">{msg.text}</div>
                        </div>
                    ))}
                    {loading && <div className="thinking-indicator"><span className="typing-dot"></span><span className="typing-dot"></span><span className="typing-dot"></span></div>}
                    <div ref={chatEndRef} />
                </div>

                <div className="input-section">
                    <div className="input-wrapper">
                        <button className={`voice-btn ${isListening ? 'active' : ''}`} onClick={toggleListening}>
                            {isListening ? "🟢" : "🎤"}
                        </button>
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                            placeholder={isListening ? "Listening..." : "Query the neural network..."}
                            autoFocus
                        />
                        <button className={`send-btn ${loading ? 'busy' : ''}`} onClick={() => sendMessage()} disabled={loading}>
                            {loading ? "SYNC" : "EXECUTE"}
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