import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from skills.registry import register_skill
from dotenv import load_dotenv

# Load environment variables for Spotify credentials
load_dotenv()

# Configuration (These should be set in a .env file)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")

# Scope for playback control
SCOPE = "user-modify-playback-state user-read-playback-state"

def get_spotify_client():
    if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
        return None
    try:
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
            open_browser=False # Recommended for background services
        ))
    except Exception as e:
        print(f"[MUSIC SKILL ERROR]: {e}")
        return None

@register_skill(["play music", "resume music", "play track"])
def play_music(command):
    sp = get_spotify_client()
    if not sp:
        return "Sir, the Spotify credentials are not configured in the environment variables."
    
    try:
        # If "play music" or "resume" with no specific query, just resume
        query = command.lower().replace("play music", "").replace("resume music", "").replace("play track", "").replace("play", "").strip()
        
        if not query:
            sp.start_playback()
            return "Resuming your music, Sir."
        
        # Search for the track
        res = sp.search(q=query, limit=1, type="track")
        if res['tracks']['items']:
            track = res['tracks']['items'][0]
            uri = track['uri']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            sp.start_playback(uris=[uri])
            return f"Playing {track_name} by {artist_name}, Sir."
        else:
            return f"Sir, I couldn't find any track matching '{query}'."
            
    except Exception as e:
        if "No active device" in str(e):
            return "Sir, there is no active Spotify device found. Please open Spotify on your device."
        return f"Sir, I encountered an error with Spotify: {str(e)}"

@register_skill(["pause music", "stop music", "pause"])
def pause_music(command):
    sp = get_spotify_client()
    if not sp: return "Spotify credentials missing, Sir."
    try:
        sp.pause_playback()
        return "Music paused, Sir."
    except Exception as e:
        return f"Sir, I couldn't pause the music: {str(e)}"

@register_skill(["next song", "skip track", "next track"])
def next_track(command):
    sp = get_spotify_client()
    if not sp: return "Spotify credentials missing, Sir."
    try:
        sp.next_track()
        return "Skipping to the next track, Sir."
    except Exception as e:
        return f"Sir, I failed to skip the track: {str(e)}"

@register_skill(["previous song", "go back", "previous track"])
def previous_track(command):
    sp = get_spotify_client()
    if not sp: return "Spotify credentials missing, Sir."
    try:
        sp.previous_track()
        return "Playing the previous track, Sir."
    except Exception as e:
        return f"Sir, I failed to return to the previous track: {str(e)}"

@register_skill(["set volume", "music volume"])
def set_volume(command):
    sp = get_spotify_client()
    if not sp: return "Spotify credentials missing, Sir."
    try:
        # Extract numbers from command
        import re
        nums = re.findall(r'\d+', command)
        if nums:
            vol = int(nums[0])
            if 0 <= vol <= 100:
                sp.volume(vol)
                return f"Setting music volume to {vol} percent, Sir."
        return "Sir, please specify a volume level between 0 and 100."
    except Exception as e:
        return f"Sir, I couldn't adjust the volume: {str(e)}"
