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
    # Test 1: Time (Existing)
    test_command("what time is it")

    # Test 2: Screenshot (New)
    if test_command("take a screenshot"):
        # Check if screenshot was created
        if os.path.exists("screenshot.png"):
            print("SUCCESS: screenshot.png created.")
            # Optional: remove it
            # os.remove("screenshot.png")
        else:
            print("FAILURE: screenshot.png was not found.")

    # Test 3: Status
    test_command("system diagnostic")
