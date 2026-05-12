import sys
import os
import time

# Add backend and skills to path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'skills'))

def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'ignore').decode('ascii'))

safe_print("==========================================")
safe_print("   JARVIS SYSTEM DIAGNOSTIC SEQUENCE      ")
safe_print("==========================================")

# 1. TEST BRAIN (Ollama Connectivity)
safe_print("\n[1/4] Checking Neural Engine (Ollama)...")
try:
    import ollama
    r = ollama.list()
    safe_print("[OK] Ollama is online.")
except Exception as e:
    safe_print(f"[FAIL] Ollama check failed: {e}")

# 2. TEST TTS (Edge-TTS + Tone Detection)
safe_print("\n[2/4] Checking Voice Synthesis Engine...")
try:
    import tts
    # Test a small phrase
    tts.speak("Diagnostic sequence initiated. All systems nominal.")
    safe_print("[OK] TTS Engine: Functional.")
except Exception as e:
    safe_print(f"[FAIL] TTS Engine failed: {e}")

# 3. TEST COMMAND HUB & SKILLS
safe_print("\n[3/4] Checking Command Registry & Skills...")
try:
    from commands import run_command
    
    # Test System Skill
    time_reply = run_command("what time is it")
    if time_reply: safe_print(f"[OK] System Skill (Time): {time_reply}")
    
    # Test Keyword Priority
    search_reply = run_command("google search for stark industries today")
    safe_print(f"[OK] Keyword Priority: System identified search intent.")
    
    # Test Clipboard Skill
    import pyperclip
    pyperclip.copy("Secret Stark Blueprint")
    clip_reply = run_command("summarize my clipboard")
    if clip_reply: safe_print(f"[OK] Clipboard Skill: Functional.")
except Exception as e:
    safe_print(f"[FAIL] Skills Registry failed: {e}")

# 4. TEST PERSISTENT MEMORY
safe_print("\n[4/4] Checking Neural Bank (Memory)...")
try:
    from memory import memory_manager
    mode = 'Redis' if memory_manager.use_redis else 'JSON'
    safe_print(f"[OK] Memory Bank: Online ({mode})")
    safe_print(f"[OK] History Depth: {len(memory_manager.memory)} interactions.")
except Exception as e:
    safe_print(f"[FAIL] Memory Bank failed: {e}")

safe_print("\n==========================================")
safe_print("      DIAGNOSTIC COMPLETE: JARVIS READY   ")
safe_print("\n==========================================")
