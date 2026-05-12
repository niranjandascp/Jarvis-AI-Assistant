import sys
import os

# Add the current directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commands import run_command
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

def test_music_commands():
    print("--- TESTING MUSIC SKILLS ---")
    
    # Test cases
    commands = [
        "play music",
        "play track shape of you",
        "pause music",
        "next song",
        "set volume to 50"
    ]
    
    for cmd in commands:
        print(f"\nUser: {cmd}")
        reply = run_command(cmd)
        print(f"JARVIS: {reply}")

if __name__ == "__main__":
    if not os.getenv("SPOTIPY_CLIENT_ID"):
        print("ERROR: SPOTIPY_CLIENT_ID not found in environment.")
        print("Please create a .env file based on .env.example and fill in your credentials.")
    else:
        test_music_commands()
