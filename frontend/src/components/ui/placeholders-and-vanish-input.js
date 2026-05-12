import React, { useCallback, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

export const PlaceholdersAndVanishInput = ({
  placeholders,
  onSubmit,
}) => {
  const [currentPlaceholder, setCurrentPlaceholder] = useState(0);
  const [value, setValue] = useState("");
  const [animating, setAnimating] = useState(false);
  
  const canvasRef = useRef(null);
  const inputRef = useRef(null);
  const particlesRef = useRef([]);

  // --- PLACEHOLDER ROTATION ---
  useEffect(() => {
    const interval = setInterval(() => {
      if (!value && !animating) {
        setCurrentPlaceholder((prev) => (prev + 1) % placeholders.length);
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [placeholders.length, value, animating]);

  // --- CANVAS DRAWING ---
  const draw = useCallback(() => {
    if (!inputRef.current || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, 800, 200);
    ctx.font = "24px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#00f2ff";
    ctx.textBaseline = "middle";
    ctx.fillText(value, 20, 50);

    const imageData = ctx.getImageData(0, 0, 800, 100);
    const pixels = imageData.data;
    const newParticles = [];

    for (let y = 0; y < 100; y += 2) { // Step 2 for performance
      for (let x = 0; x < 800; x += 2) {
        const i = (y * 800 + x) * 4;
        if (pixels[i + 3] > 128) {
          newParticles.push({
            x, y,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            size: Math.random() * 2 + 1,
            color: "#00f2ff",
            alpha: 1
          });
        }
      }
    }
    particlesRef.current = newParticles;
  }, [value]);

  const runVanish = () => {
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;

    const animate = () => {
      ctx.clearRect(0, 0, 800, 200);
      let stillAlive = false;

      particlesRef.current.forEach(p => {
        if (p.alpha > 0) {
          p.x += p.vx;
          p.y += p.vy;
          p.alpha -= 0.02;
          ctx.globalAlpha = p.alpha;
          ctx.fillStyle = p.color;
          ctx.fillRect(p.x, p.y, p.size, p.size);
          stillAlive = true;
        }
      });

      if (stillAlive) {
        requestAnimationFrame(animate);
      } else {
        setAnimating(false);
        setValue("");
      }
    };
    animate();
  };

  const handleAction = (e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    if (!value || animating) return;

    const submittedValue = value;
    setAnimating(true);
    draw();
    runVanish();

    if (onSubmit) {
      onSubmit(submittedValue);
    }
  };

  return (
    <div className="placeholders-container-wrapper" style={{ position: 'relative', width: '100%' }}>
        <form 
            className="placeholders-form" 
            onSubmit={handleAction}
            autoComplete="off"
        >
        <canvas
            ref={canvasRef}
            width="800"
            height="200"
            className="placeholders-canvas"
            style={{
                position: 'absolute',
                top: '-20px',
                left: '0',
                width: '400px',
                height: '100px',
                pointerEvents: 'none',
                zIndex: 50,
                opacity: animating ? 1 : 0
            }}
        />
        
        <input
            ref={inputRef}
            type="text"
            value={value}
            onChange={(e) => !animating && setValue(e.target.value)}
            className="placeholders-input"
            autoFocus
            style={{ 
                opacity: animating ? 0 : 1,
                pointerEvents: animating ? 'none' : 'auto',
                position: 'relative',
                zIndex: 10
            }}
        />

        <button
            type="submit"
            disabled={!value || animating}
            className="submit-circle-btn"
        >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12l14 0M13 18l6 -6M13 6l6 6" />
            </svg>
        </button>

        <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', display: 'flex', alignItems: 'center', zIndex: 1 }}>
            <AnimatePresence mode="wait">
            {!value && !animating && (
                <motion.p
                key={currentPlaceholder}
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: -10, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="placeholder-text"
                >
                {placeholders[currentPlaceholder]}
                </motion.p>
            )}
            </AnimatePresence>
        </div>
        </form>
    </div>
  );
};
