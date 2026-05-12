import edge_tts
import asyncio
import os
import pygame

# Initialize pygame mixer for audio playback
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Audio Error: Could not initialize mixer ({e})")

async def speak_async(text, voice="en-US-GuyNeural"):
    """
    Synthesizes text to speech using edge-tts and plays it.
    """
    output_file = "reply.mp3"
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
        
        # Optional: Clean up the file
        # os.remove(output_file)
        
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
        # If we are already in an event loop (e.g. running in an async context), 
        # we might need to use a different approach like create_task,
        # but for simple scripts asyncio.run is usually what users want.
        print(f"TTS Execution Error: {e}")