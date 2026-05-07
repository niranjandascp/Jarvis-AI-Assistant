@echo off
title JARVIS Browser Engine
echo 🚀 Starting JARVIS Neural Backend...
start /b python backend/server.py

echo 🌐 Starting JARVIS React Engine...
cd frontend
npm start
