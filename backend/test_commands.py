import sys
import os

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
    # Test 1: Web Search
    print("\n[SCENARIO] Testing Web Search")
    test_command("google what is the price of bitcoin today")
