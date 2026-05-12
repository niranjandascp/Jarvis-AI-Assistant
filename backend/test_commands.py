import sys
import os
import time

# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

from commands import run_command

def test_command(phrase):
    print(f"\n--- Testing Command: '{phrase}' ---")
    reply = run_command(phrase)
    if reply:
        print(f"Jarvis Reply: {reply}")
        return True
    else:
        print("No skill matched this command.")
        return False

if __name__ == "__main__":
    # Test: Reminder
    print("\n[SCENARIO] Testing Reminder")
    test_command("remind me to check the Arc Reactor in 3 seconds")
    
    print("Waiting for reminder to fire...")
    time.sleep(5)
    print("Test complete.")
