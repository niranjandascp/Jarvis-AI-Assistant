# Moltbot AI - Advanced System Refactor

Moltbot has been upgraded to a production-ready, robust architecture with automated system health checks.

## Key Upgrades
1.  **System Polling**: Electron now uses TCP polling to verify that the **Neural Backend (5000)** and **UI Engine (3000)** are fully active before showing the interface. No more "Connection Refused" errors.
2.  **Waitress Integration**: Replaced the Flask development server with **Waitress**, a production-grade WSGI server, ensuring stability and performance.
3.  **Production Mode**: A new `launch_prod.bat` allows you to run the app using the static build folder, bypassing the heavy React development server for a faster, "standalone-like" experience.
4.  **One-Click Packaging**: Updated bundling scripts to handle relative path mapping for the neural backend, ensuring the app works perfectly after being packaged into a single icon.

## Setup & Launch

### 1. Development Mode (Fast Updates)
Double-click `launch_dev.bat`. This will start the React dev server, allowing you to see code changes in real-time.

### 2. Production Mode (Optimized)
Double-click `launch_prod.bat`. This builds the UI (if not already built) and runs it as a standalone static app. This is the fastest way to run the finished assistant.

### 3. Packaging into a Single EXE
1.  Run `python scripts/bundle_backend.py`.
2.  Run `cd frontend && npm run dist`.
The resulting `.exe` in `frontend/dist` will be fully self-contained.

## Dependencies
- **Backend**: Flask, Waitress, Ollama, Psutil, Pyttsx3, PyAudio.
- **Frontend**: React, Three.js, GSAP, Electron.

---
*Systems Optimized by Antigravity AI.*
