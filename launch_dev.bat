@echo off
setlocal enabledelayedexpansion
title JARVIS AI Launcher
echo 🚀 Initializing JARVIS Systems...

:: Navigate to root directory
cd /d "%~dp0"

:: Check for Python dependencies
echo 🔍 Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1

:: Ensure Ollama is running
echo 🧠 Checking Ollama service...
curl -s http://127.0.0.1:11434 >nul 2>&1
if errorlevel 1 (
    echo 🔄 Starting Ollama...
    start /b ollama serve >nul 2>&1
    timeout /t 5 /nobreak >nul
    echo ✅ Ollama launched.
) else (
    echo ✅ Ollama already running.
)

:: Start Flask Backend in the background
echo 🧠 Starting Neural Backend...
start /b python backend/server.py

:: Navigate to frontend
cd frontend

:: Check for Node dependencies
if not exist "node_modules" (
    echo 📦 Installing frontend dependencies...
    call npm install
)

:: Start React Dev Server in the background
echo 🌐 Starting React Engine...
start /b npm start

:: Wait for servers to wake up
echo ⏳ Warming up systems (5s)...
timeout /t 5 /nobreak >nul

:: Start Electron
echo 🖥️ Launching Holographic Interface...
call npm run electron

:: Kill background processes on exit
echo 💤 Shutting down systems...
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im node.exe /t >nul 2>&1
pause
