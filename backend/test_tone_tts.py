import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

import tts

if __name__ == "__main__":
    # Test case 1: Calm
    calm_text = "The weather is quite pleasant today, sir. I recommend a walk in the garden."
    print("\n--- Testing Calm Tone ---")
    tts.speak(calm_text)

    # Test case 2: Excited
    excited_text = "Oh my god! We just won the lottery! This is incredible news, sir!"
    print("\n--- Testing Excited Tone ---")
    tts.speak(excited_text)
