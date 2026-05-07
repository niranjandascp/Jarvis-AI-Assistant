@echo off
setlocal enabledelayedexpansion
title JARVIS AI Production
echo 🚀 Initializing JARVIS Production Environment...

:: Navigate to root directory
cd /d "%~dp0"

:: Check for build folder
if not exist "frontend\build" (
    echo 📦 Production build not found. Generating now...
    cd frontend
    call npm run build
    cd ..
)

:: Start Flask Backend in the background
echo 🧠 Starting Neural Backend...
start /b python backend/server.py

:: Start Electron in Production Mode
echo 🖥️ Launching JARVIS Interface...
set NODE_ENV=production
cd frontend
call npm run electron

:: Kill backend on exit
taskkill /f /im python.exe /t >nul 2>&1
pause
