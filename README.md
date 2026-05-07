# 🤖 Moltbot AI - Advanced Neural Interface

Moltbot AI is a high-fidelity, dual-process artificial intelligence assistant inspired by Jarvis. It combines a **React/Electron** frontend with a **Flask/Waitress** backend to provide a seamless, local-first AI experience with stunning 3D visualizations.

![Moltbot Icon]

## 🌌 Features
- **Arc Reactor Visualizer**: A hardware-accelerated 3D core built with Three.js and GSAP that pulses in real-time during AI processing.
- **Neural Brain**: Powered by **Ollama (Llama3)** for sophisticated, local, and private natural language processing.
- **Hybrid Architecture**: 
  - **Dev Mode**: Real-time UI updates via React Dev Server.
  - **Production Mode**: Blazing fast static-build execution.
  - **Browser Mode**: Access your assistant from any device on your local network.
- **Robust Startup**: Automated TCP polling ensures the backend and frontend are synchronized before the UI launches.
- **One-Click Distribution**: Built-in scripts to bundle the entire Python environment and UI into a single standalone `.exe`.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)
- **Ollama** (Download from [ollama.com](https://ollama.com))

### 2. Installation
Clone the repository and run the setup commands:
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd frontend
npm install
```

### 3. Model Setup
Moltbot uses the **Llama3** model. Download it via Ollama:
```bash
ollama pull llama3
```

---

## 🛠️ Usage Guide

### 📂 Quick Launchers (Recommended)
I have provided specialized batch scripts for different workflows:
- **`launch_dev.bat`**: Best for developers. Enables Hot Module Replacement (HMR).
- **`launch_prod.bat`**: Best for daily use. Uses the optimized static build for performance.
- **`run_browser.bat`**: Runs the backend and UI engine for access via Chrome/Edge at `localhost:3000`.

### 📦 Standalone Packaging
To create a single, portable executable icon:
1.  **Bundle Backend**: `python scripts/bundle_backend.py` (Creates `server.exe`).
2.  **Distribute App**: `cd frontend && npm run dist`.
3.  Find your installer in `frontend/dist/`.

---

## 🏗️ Architecture Detail
- **Frontend**: React 19, Three.js, GSAP 3 (Animations).
- **Desktop Wrapper**: Electron 41 (Frameless, Glassmorphic UI).
- **Backend**: Flask + Waitress (Production WSGI).
- **AI Integration**: Ollama API (llama3 model).
- **System Diagnostics**: Psutil (CPU/Battery metrics).

---

## 🔧 Troubleshooting
- **Black Screen**: The UI takes ~3 seconds to "decrypt" (fade in). If it stays black, ensure your ports (3000, 5000) aren't being used by other apps.
- **"Glitch" Response**: Ensure the Ollama server is running and the `llama3` model is downloaded.
- **Voice Issues**: Check your system's default TTS/STT settings.

---

