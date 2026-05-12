import edge_tts
import asyncio
import os
import pygame
import ollama

# Initialize pygame mixer for audio playback
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Audio Error: Could not initialize mixer ({e})")

# Tone-to-Voice mapping
VOICES = {
    "calm": "en-US-GuyNeural",
    "excited": "en-US-AndrewNeural",
    "urgent": "en-US-AndrewNeural"  # Fallback to Andrew for urgency
}

def get_tone(text):
    """
    Uses Ollama to analyze the emotional tone of the text.
    """
    try:
        r = ollama.chat(model="llama3", messages=[{
            "role": "user",
            "content": f"Reply ONLY with one word — calm/excited/urgent:\n{text}"
        }])
        tone = r['message']['content'].strip().lower()
        # Clean up any extra punctuation or words LLM might return
        for word in ["calm", "excited", "urgent"]:
            if word in tone:
                return word
        return "calm" # Default
    except Exception as e:
        print(f"Tone Analysis Error: {e}")
        return "calm"

async def speak_async(text):
    """
    Synthesizes text to speech using edge-tts with dynamic tone detection.
    """
    output_file = "reply.mp3"
    
    # 🧠 Detect Tone
    tone = get_tone(text)
    voice = VOICES.get(tone, "en-US-GuyNeural")
    try:
        print(f"Tone detected: {tone} -> Using Voice: {voice}")
    except UnicodeEncodeError:
        print(f"Tone detected: {tone} -> Using Voice: {voice}".encode('ascii', 'ignore').decode('ascii'))

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Play the audio file
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        # Unload to free the file
        pygame.mixer.music.unload()
        
    except Exception as e:
        print(f"Speech Synthesis Error: {e}")

def speak(text):
    """
    Synchronous wrapper for speak_async.
    """
    print("Jarvis:", text)
    try:
        # Run the async function in a new event loop
        asyncio.run(speak_async(text))
    except Exception as e:
        print(f"TTS Execution Error: {e}")