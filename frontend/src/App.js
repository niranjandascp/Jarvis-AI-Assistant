import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import { gsap } from "gsap";
import Visualizer from "./components/Visualizer";
import Particles from "./components/Particles";
import HistoryPanel from "./components/HistoryPanel";
import { PlaceholdersAndVanishInput } from "./components/ui/placeholders-and-vanish-input";
import Lenis from "lenis";
import "./App.css";

// Check if running in Electron
let ipcRenderer = null;
try {
    if (window.require) {
        const electron = window.require("electron");
        ipcRenderer = electron.ipcRenderer;
    }
} catch (e) {
    console.log("Not running in Electron environment.");
}

const JARVIS_VERSION = "1.4.0";
const PLACEHOLDERS = [
  "Execute system diagnostic...",
  "Analyze regional energy patterns.",
  "Check orbital satellite status.",
  "Jarvis, initiate protocol zero.",
  "Search for encrypted Stark files.",
  "Optimize thruster output.",
];

function App() {
  const [messages, setMessages] = useState([
    { role: "jarvis", text: "Neural Link Established. System calibration complete. Ready for orders, Sir." }
  ]);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [useServerVoice, setUseServerVoice] = useState(false);
  const [systemReady, setSystemReady] = useState(false);
  const [backendStatus, setBackendStatus] = useState("checking");
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [sessions, setSessions] = useState(
    JSON.parse(localStorage.getItem('jarvis_sessions') || '[]')
  );
  
  const chatEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const loadingRef = useRef(false);

  useEffect(() => {
    loadingRef.current = loading;
  }, [loading]);

  // --- LENIS SMOOTH SCROLL ---
  useEffect(() => {
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
        infinite: false,
    });

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    return () => lenis.destroy();
  }, []);

  // --- MOUSE SPOTLIGHT TRACKING ---
  useEffect(() => {
    const handleMouseMove = (e) => setMousePos({ x: e.clientX, y: e.clientY });
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // --- HEALTH MONITOR ---
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/status");
        if (res.data.status === "online") setBackendStatus("online");
      } catch {
        setBackendStatus("offline");
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  // --- SYSTEM BOOT ---
  useEffect(() => {
    const timer = setTimeout(() => {
        setSystemReady(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  // --- AUTO SCROLL ---
  useEffect(() => {
    if (chatEndRef.current) {
        chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // --- MESSAGE HANDLER (STREAMING ENABLED) ---
  const sendMessage = useCallback(async (messageText) => {
    if (!messageText || loadingRef.current) return;

    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", text: messageText }]);
    setMessages((prev) => [...prev, { role: "jarvis", text: "" }]); // Placeholder for stream
    
    gsap.to(".arc-reactor-container", { scale: 1.15, duration: 0.1, yoyo: true, repeat: 1 });

    try {
      const response = await fetch("http://127.0.0.1:5000/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageText })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n\n");
        
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.replace("data: ", "");
            if (data === "[DONE]") break;
            
            fullText += data;
            setMessages((prev) => {
              const newMsgs = [...prev];
              newMsgs[newMsgs.length - 1].text = fullText;
              return newMsgs;
            });
          }
        }
      }
      
      if (!useServerVoice) {
        window.speechSynthesis.cancel();
        const speech = new SpeechSynthesisUtterance(fullText);
        speech.rate = 1.05;
        speech.pitch = 0.85;
        window.speechSynthesis.speak(speech);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "jarvis", text: "⚠️ STREAM_ERROR: Connection to neural core failed." }]);
      setBackendStatus("offline");
    } finally {
      setLoading(false);
    }
  }, [useServerVoice]);

  // --- SESSION MANAGEMENT ---
  const saveSession = useCallback(() => {
    if (messages.length <= 1) return; // Don't save empty or intro-only sessions
    const newSession = { id: Date.now(), messages: [...messages] };
    const updatedSessions = [newSession, ...sessions].slice(0, 50); // Keep last 50
    setSessions(updatedSessions);
    localStorage.setItem('jarvis_sessions', JSON.stringify(updatedSessions));
    
    // Reset messages for new session
    setMessages([
        { role: "jarvis", text: "New session initialized. Neural Link stable. Waiting for your next directive, Sir." }
    ]);
  }, [messages, sessions]);

  const selectSession = (session) => {
    setMessages(session.messages);
    gsap.fromTo(".chat-row", { opacity: 0, x: -20 }, { opacity: 1, x: 0, stagger: 0.05, duration: 0.4 });
  };

  const clearHistory = () => {
    if (window.confirm("Sir, are you sure you want to purge the session archives? This action is irreversible.")) {
        setSessions([]);
        localStorage.removeItem('jarvis_sessions');
    }
  };

  const [transcript, setTranscript] = useState("");

  const toggleListening = async () => {
    if (isListening) {
      // In this new mode, we just set the state to false and let the stream close naturally
      setIsListening(false);
      return;
    }

    setIsListening(true);
    setTranscript("INITIALIZING NEURAL LINK...");
    console.log("🎤 Starting Backend STT Stream...");

    try {
      const eventSource = new EventSource("http://127.0.0.1:5000/stt-stream");

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.error) {
          console.error("❌ Backend STT Error:", data.error);
          setTranscript(`⚠️ ERROR: ${data.error.toUpperCase()}`);
          eventSource.close();
          setIsListening(false);
          return;
        }

        if (data.text) {
          setTranscript(data.text);
          if (data.final) {
            console.log("📝 Final Transcription:", data.text);
            sendMessage(data.text);
            eventSource.close();
            setIsListening(false);
            setTranscript("");
          }
        }
      };

      eventSource.onerror = () => {
        console.error("❌ STT Stream Connection Failed");
        setTranscript("⚠️ ERROR: BACKEND_LINK_LOST");
        eventSource.close();
        setIsListening(false);
      };

    } catch (err) {
      console.error("Failed to connect to STT stream:", err);
      setIsListening(false);
    }
  };



  // --- WINDOW CONTROLS ---
  const handleWindowAction = (action) => {
    console.log(`Executing window action: ${action}`);
    if (ipcRenderer) {
        ipcRenderer.send(`window-${action}`);
    } else {
        // Fallback for browser testing
        if (action === 'close') window.close();
    }
  };

  return (
    <div className="main-wrapper">
      <div className="window-drag-handle"></div>
      <Particles />
      <div className="scanline"></div>

      {/* --- LIVE TRANSCRIPTION HUD --- */}
      {transcript && (
        <div className="transcription-hud">
           <div className="hud-line"></div>
           <p><span className="hud-tag">🎤 NEURAL_LINK:</span> {transcript.toUpperCase()}</p>
        </div>
      )}
      
      <div 
        className="mouse-spotlight"
        style={{ 
            left: mousePos.x, 
            top: mousePos.y,
            background: `radial-gradient(800px at ${mousePos.x}px ${mousePos.y}px, rgba(0, 242, 255, 0.05), transparent 80%)`
        }}
      ></div>

      <div className={`boot-sequence ${systemReady ? 'exit' : ''}`}>
         <div className="boot-content">
            <div className="apple-loader"></div>
            <p className="boot-tag">SYSTEM_BOOT_V{JARVIS_VERSION}</p>
         </div>
      </div>

      <div className={`app-grid-container ${systemReady ? 'active' : ''}`}>
        <header className="glass-header">
           <div className="header-left traffic-lights">
              <button className="light close" onClick={() => handleWindowAction('close')}></button>
              <button className="light minimize" onClick={() => handleWindowAction('minimize')}></button>
              <button className="light maximize" onClick={() => handleWindowAction('maximize')}></button>
           </div>
           
           <div className="header-center">JARVIS_MARK_VII</div>
           
           <div className="header-right no-drag">
              <div className={`status-pill ${backendStatus}`}>
                 LINK: {backendStatus.toUpperCase()}
              </div>
              <button className={`mode-pill ${useServerVoice ? 'active' : ''}`} onClick={() => setUseServerVoice(!useServerVoice)}>
                {useServerVoice ? "SRV_VOICE" : "WEB_VOICE"}
              </button>
              <button className="new-chat-btn" onClick={saveSession}>
                NEW_LINK
              </button>
           </div>
        </header>

        <main className="bento-layout">
            <aside className="bento-sidebar">
                <div className="sidebar-inner">
                    <div className="reactor-module">
                        <Visualizer active={loading || isListening} />
                        <h1 className="reactor-tag">JARVIS</h1>
                        <div className="sensor-data">
                            <div className="data-row"><span>CORE_TEMP</span><span className="val">32°C</span></div>
                            <div className="data-row"><span>SYNC_RATE</span><span className="val">99.8%</span></div>
                        </div>
                    </div>
                    <div className="info-module">
                        <HistoryPanel 
                            sessions={sessions} 
                            onSelectSession={selectSession} 
                            onClearHistory={clearHistory}
                        />
                    </div>
                </div>
            </aside>

            <section className="bento-main">
                <div className="chat-interface">
                    <div className="chat-messages" id="chat-container">
                        {messages.map((msg, index) => (
                            <div key={index} className={`chat-row ${msg.role}`}>
                                <div className="avatar-tag">{msg.role === "user" ? "USR" : "JRV"}</div>
                                <div className="chat-bubble">
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="loading-dots">
                                <span></span><span></span><span></span>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    <div className="input-dock-wrapper">
                        <div className="floating-dock">
                            <button className={`mic-circle ${isListening ? 'active' : ''}`} onClick={toggleListening}>
                                {isListening ? "📡" : "🎤"}
                            </button>
                            <div className="vanish-input-container">
                                <PlaceholdersAndVanishInput
                                    placeholders={PLACEHOLDERS}
                                    onSubmit={(e) => sendMessage(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
      </div>
    </div>

  );
}

export default App;