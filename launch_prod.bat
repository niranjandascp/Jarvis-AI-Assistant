@echo off
setlocal enabledelayedexpansion
title Moltbot AI - Production Mode
echo 🚀 Initializing Moltbot OS in Production Mode...

:: Navigate to root directory
cd /d "%~dp0"

:: Check for Python dependencies
echo 🔍 Verifying Backend Dependencies...
pip install -r requirements.txt >nul 2>&1

:: Start Flask Backend (Waitress)
echo 🧠 Starting Neural Backend...
start /b python backend/server.py

:: Navigate to frontend
cd frontend

:: Build if missing
if not exist "build" (
    echo 📦 Building UI Engine (First time setup)...
    call npm run build
)

:: Set Production Environment and Start Electron
echo 🖥️ Launching Standalone Interface...
set NODE_ENV=production
call npm run electron

:: Kill background processes on exit
echo 💤 Shutting down systems...
taskkill /f /im python.exe /t >nul 2>&1
pause
