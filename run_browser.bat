@echo off
title Moltbot AI - Browser Mode
echo 🚀 Launching Moltbot AI for Browser...

:: Navigate to root
cd /d "%~dp0"

:: Start Backend
echo 🧠 Starting Neural Backend...
start /b python backend/server.py

:: Start Frontend Dev Server
echo 🌐 Starting React UI Engine...
cd frontend
npm start
