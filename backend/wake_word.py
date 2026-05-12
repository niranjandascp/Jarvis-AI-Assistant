import vosk
import sounddevice as sd
import json
import os
import queue
import sys

# Suppress Vosk logging to keep terminal clean
vosk.SetLogLevel(-1)

# Thread-safe queue for audio data
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Callback for sounddevice to capture audio chunks."""
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def detect_wake_word():
    """
    Detects the wake word 'Jarvis' using Vosk.
    Returns True when detected.
    """
    # Look for the model in the 'model' directory inside backend
    model_path = os.path.join(os.path.dirname(__file__), "model")
    
    if not os.path.exists(model_path):
        print("\n⚠️  Vosk Model not found!")
        print(f"👉 Please download a small model from: https://alphacephei.com/vosk/models")
        print(f"👉 Suggestion: 'vosk-model-small-en-us-0.15'")
        print(f"👉 Extract the folder and rename it to 'model' inside: {os.path.dirname(model_path)}\n")
        return False

    try:
        model = vosk.Model(model_path)
        # Exhaustive vocabulary based on continuous user feedback
        words = '["jarvis", "service", "travis", "java", "charvis", "dad", "was", "john", "jhon", "this", "janice", "jerry", "is", "derek", "down", "with", "damnit", "do", "it", "lewis", "that", "doris", "not", "godwin", "lottery", "really", "da", "of", "dotted", "nada", "[unk]"]'
        recognizer = vosk.KaldiRecognizer(model, 16000, words)
        
        print("🎧 Jarvis listening (Custom Calibrated Engine)...")

        # Start the audio stream
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                else:
                    partial = json.loads(recognizer.PartialResult())
                    text = partial.get("partial", "").lower()
                
                if text:
                    sys.stdout.write(f"\r🎤 Heard: {text}... ")
                    sys.stdout.flush()
                    
                    # Massive trigger list to catch all possible phonetic variations
                    trigger_patterns = [
                        "jarvis", "service", "travis", "java", "charvis",
                        "dad was", "john this", "dad is", "janice", "jerry", "jerrys",
                        "derek", "down with", "damnit", "do it", "john lewis", "doris",
                        "that with", "not with", "john", "janis", "dad", "lewis",
                        "godwin", "lottery", "not really", "really",
                        "da da", "jhon is", "nada", "god with", "this is jhon", "dotted with"
                    ]
                    
                    if any(pattern in text for pattern in trigger_patterns):
                        print("\n🧠 WAKE WORD DETECTED")
                        return True







                
    except Exception as e:
        print(f"\n❌ Vosk/Audio Error: {e}")
        return False

