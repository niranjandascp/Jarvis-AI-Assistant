import os
import webbrowser
import psutil
from datetime import datetime

def run_command(text):
    text = text.lower()

    # 🌐 WEB COMMANDS
    web_map = {
        "open youtube": "https://youtube.com",
        "open google": "https://google.com",
        "open github": "https://github.com",
        "open stack overflow": "https://stackoverflow.com"
    }
    
    for cmd, url in web_map.items():
        if cmd in text:
            webbrowser.open(url)
            return f"Opening {cmd.split()[-1].capitalize()}"

    # 💻 APPS
    if "open notepad" in text:
        os.system("start notepad") # 'start' prevents the script from freezing
        return "Opening Notepad"
    if "open calculator" in text:
        os.system("calc")
        return "Opening Calculator"

    # ⚙️ SYSTEM INFO
    if "battery" in text:
        battery = psutil.sensors_battery()
        return f"Battery is at {battery.percent}%" if battery else "Battery info unavailable."

    if "cpu usage" in text:
        return f"Current CPU usage is {psutil.cpu_percent()}%"

    if "time" in text:
        return f"The time is {datetime.now().strftime('%I:%M %p')}"

    return None