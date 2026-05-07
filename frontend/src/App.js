import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import { gsap } from "gsap";
import Visualizer from "./components/Visualizer";
import Particles from "./components/Particles";
import { PlaceholdersAndVanishInput } from "./components/ui/placeholders-and-vanish-input";
import Lenis from "lenis";
import "./App.css";

const JARVIS_VERSION = "1.3.0";
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

    return () => {
        lenis.destroy();
    };
  }, []);

  // --- MOUSE SPOTLIGHT TRACKING ---
  useEffect(() => {
    const handleMouseMove = (e) => {
        setMousePos({ x: e.clientX, y: e.clientY });
    };
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
        gsap.to(".boot-sequence", { y: "-100%", duration: 1.2, ease: "expo.inOut" });
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  // --- AUTO SCROLL & REVEAL ---
  useEffect(() => {
    if (chatEndRef.current) {
        chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // --- MESSAGE HANDLER ---
  const sendMessage = useCallback(async (messageText) => {
    if (!messageText || loadingRef.current) return;

    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", text: messageText }]);
    
    gsap.to(".arc-reactor-container", { scale: 1.15, duration: 0.1, yoyo: true, repeat: 1 });

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { 
        message: messageText,
        use_server_voice: useServerVoice 
      });
      
      const reply = res.data.reply;
      setMessages((prev) => [...prev, { role: "jarvis", text: reply }]);
      
      if (!useServerVoice) {
        window.speechSynthesis.cancel();
        const speech = new SpeechSynthesisUtterance(reply);
        speech.rate = 1.05;
        speech.pitch = 0.85;
        window.speechSynthesis.speak(speech);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "jarvis", text: "⚠️ BACKEND_OFFLINE: Re-establish neural server link." }]);
      setBackendStatus("offline");
    } finally {
      setLoading(false);
    }
  }, [useServerVoice]);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
          recognitionRef.current = new SpeechRecognition();
          recognitionRef.current.onresult = (e) => sendMessage(e.results[0][0].transcript);
          recognitionRef.current.onend = () => setIsListening(false);
          recognitionRef.current.start();
          setIsListening(true);
      }
    }
  };

  return (
    <div className="main-wrapper">
      <Particles />
      <div className="scanline"></div>
      
      {/* SPOTLIGHT EFFECT */}
      <div 
        className="mouse-spotlight"
        style={{ 
            left: mousePos.x, 
            top: mousePos.y,
            background: `radial-gradient(600px at ${mousePos.x}px ${mousePos.y}px, rgba(0, 242, 255, 0.05), transparent 80%)`
        }}
      ></div>

      <div className="boot-sequence">
         <div className="boot-content">
            <div className="ring-loader"></div>
            <p className="boot-tag">STARK_SYSTEMS v{JARVIS_VERSION} INITIALIZING</p>
            <div className="boot-load-bar"><div className="fill"></div></div>
         </div>
      </div>

      <div className={`app-grid-container ${systemReady ? 'active' : ''}`}>
        <header className="glass-header">
           <div className="header-left">
              <div className={`status-pill ${backendStatus}`}>
                 <span className="blink-dot"></span>
                 LINK: {backendStatus.toUpperCase()}
              </div>
           </div>
           <div className="header-center">JARVIS_MARK_VII</div>
           <div className="header-right">
              <button className={`mode-pill ${useServerVoice ? 'active' : ''}`} onClick={() => setUseServerVoice(!useServerVoice)}>
                {useServerVoice ? "SRV_AUDIO" : "WEB_AUDIO"}
              </button>
              <button className="exit-circle" onClick={() => window.close()}>×</button>
           </div>
        </header>

        <main className="bento-layout">
            <aside className="bento-sidebar">
                <div className="sidebar-inner">
                    <div className="reactor-module">
                        <Visualizer active={loading || isListening} />
                        <h1 className="reactor-tag">JARVIS</h1>
                        <div className="sensor-data">
                            <div className="data-row"><span>TEMP</span><span className="val">32°C</span></div>
                            <div className="data-row"><span>SYNC</span><span className="val">99.8%</span></div>
                            <div className="data-row"><span>CORES</span><span className="val">08/08</span></div>
                        </div>
                    </div>
                    <div className="info-module">
                        <h3>SYSTEM_LOGS</h3>
                        <div className="log-entries">
                            <p>[OK] Memory Bank Mounted</p>
                            <p>[OK] Neural Engine Hot</p>
                            <p>[OK] Voice Synthesizer Ready</p>
                        </div>
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
                                    <span className="bubble-line"></span>
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