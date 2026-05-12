import pyperclip
try:
    import brain
    from memory import memory_manager
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import brain
    from memory import memory_manager

from skills.registry import register_skill

@register_skill(["summarize", "what did i copy"])
def summarize_clipboard(command):
    """
    Retrieves text from the clipboard and asks the AI to summarize it.
    """
    content = pyperclip.paste()
    if not content.strip():
        return "Sir, your clipboard appears to be empty."
    
    # Get recent history for context
    history = memory_manager.get_memory(limit=5)
    
    print(f"[CLIPBOARD] Summarizing content: {content[:50]}...")
    summary = brain.ask_ai(f"Please provide a concise summary of this clipboard content:\n\n{content}", history)
    return summary

@register_skill(["copy that", "copy response"])
def copy_last_response(command):
    """
    Copies the AI's last response to the clipboard.
    """
    history = memory_manager.get_memory(limit=5)
    last_reply = None
    
    # Search for the last assistant response in memory
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            last_reply = msg.get("content")
            break
            
    if last_reply:
        pyperclip.copy(last_reply)
        return "Sir, the last response has been successfully copied to your clipboard."
    else:
        return "Sir, I could not find a recent response to copy."
