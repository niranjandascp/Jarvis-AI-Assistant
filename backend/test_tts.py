import sys
import os

# Add the current directory to sys.path so we can import tts
sys.path.append(os.path.dirname(__file__))

import tts

if __name__ == "__main__":
    test_text = "Systems initialized. My name is Jarvis, and I am now equipped with high-quality neural voice synthesis. How can I assist you today?"
    print(f"Testing TTS with text: {test_text}")
    tts.speak(test_text)
    print("Test complete.")
