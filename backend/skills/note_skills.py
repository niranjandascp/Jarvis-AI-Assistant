import os
import json
import datetime
from skills.registry import register_skill

# Configuration
NOTES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes.json")

def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_notes(notes):
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=4)
        return True
    except IOError:
        return False

@register_skill(["save note", "take a note", "remember this"])
def save_note_skill(command):
    """
    Saves a note to the notes.json file.
    Example: "save note call the mechanic tomorrow"
    """
    # Extract the note text
    # Keywords to strip
    for kw in ["save note", "take a note", "remember this", "save a note"]:
        if kw in command.lower():
            text = command.lower().replace(kw, "").strip()
            break
    else:
        text = command.strip()

    if not text:
        return "Sir, you didn't specify what you wanted me to note down."

    notes = load_notes()
    new_note = {
        "text": text,
        "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    notes.append(new_note)
    
    if save_notes(notes):
        return f"Note secured, Sir: '{text}'."
    else:
        return "Sir, I encountered an error while writing to the data archives."

@register_skill(["read notes", "show my notes", "what are my notes"])
def read_notes_skill(command):
    """
    Reads the last 5 notes.
    """
    notes = load_notes()
    if not notes:
        return "Sir, your data archives are currently empty. No notes found."

    # Get the last 5 notes
    last_notes = notes[-5:]
    response = "Sir, here are your most recent notes:\n"
    for i, note in enumerate(last_notes, 1):
        response += f"{i}. {note['text']} (recorded at {note['timestamp']})\n"
    
    return response.strip()

@register_skill(["clear notes", "delete all notes"])
def clear_notes_skill(command):
    """
    Clears all saved notes.
    """
    if save_notes([]):
        return "Data archives purged, Sir. All notes have been removed."
    else:
        return "Sir, I failed to clear the archives."
