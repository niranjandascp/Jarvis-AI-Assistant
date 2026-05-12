import dateparser
import threading
from datetime import datetime
try:
    from tts import speak
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tts import speak

from skills.registry import register_skill

@register_skill(["remind me", "set a reminder"])
def reminder_skill(command):
    """
    Sets an asynchronous reminder using natural language time parsing.
    Example: "remind me to call Mom in 5 minutes"
    """
    cmd_lower = command.lower()
    
    # Intelligent extraction of task and time
    task = "something"
    time_str = "in 1 minute"
    
    if "to " in cmd_lower:
        # Split after "remind me to "
        remainder = cmd_lower.split("to ", 1)[1]
        
        # Check for temporal markers
        if " in " in remainder:
            task, time_str = remainder.rsplit(" in ", 1)
            time_str = "in " + time_str
        elif " at " in remainder:
            task, time_str = remainder.rsplit(" at ", 1)
            time_str = "at " + time_str
        else:
            task = remainder
            time_str = "in 1 minute"

    try:
        # Parse the time string into a datetime object
        dt = dateparser.parse(time_str, settings={'PREFER_DATES_FROM': 'future'})
        if not dt:
            return "Sir, my chronometers are failing to parse that specific timeframe."
             
        now = datetime.now()
        delay = (dt - now).total_seconds()
        
        if delay <= 0:
            return "Sir, it appears that time has already slipped past us."

        # The function that will execute when the timer ends
        def fire():
            print(f"[REMINDER] Triggered: {task}")
            speak(f"Sir, I have a reminder for you: {task}")
        
        # Start the background timer
        threading.Timer(delay, fire).start()
        
        return f"Very well, Sir. I have scheduled a reminder to {task} for {dt.strftime('%H:%M')}."
        
    except Exception as e:
        print(f"Reminder Error: {e}")
        return "Sir, I encountered a neural glitch while setting the reminder."
