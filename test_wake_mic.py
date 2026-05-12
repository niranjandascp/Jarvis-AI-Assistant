import sys
import os

# Add backend to path so we can import wake_word
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from wake_word import detect_wake_word

def test_jarvis():
    print("--- JARVIS WAKE WORD TEST ---")
    print("Instructions:")
    print("1. Say 'Jarvis' clearly into your microphone.")
    print("2. If it works, the terminal will show 'WAKE WORD DETECTED'.")
    print("3. Press Ctrl+C to stop the test.")
    print("-----------------------------")
    
    try:
        while True:
            if detect_wake_word():
                print("\n🌟 SUCCESS: Jarvis heard you!")
                print("Waiting for next trigger...\n")
    except KeyboardInterrupt:
        print("\nTest stopped.")

if __name__ == "__main__":
    test_jarvis()
