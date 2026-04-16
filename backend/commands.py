import os
import webbrowser
import psutil

def run_command(text):

    text = text.lower()

    # 🌐 WEB
    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in text:
        webbrowser.open("https://google.com")
        return "Opening Google"

    # 💻 APPS
    if "open notepad" in text:
        os.system("notepad")
        return "Opening Notepad"

    if "open calculator" in text:
        os.system("calc")
        return "Opening Calculator"

    # ⚙️ SYSTEM INFO
    if "battery" in text:
        battery = psutil.sensors_battery()
        return f"Battery is at {battery.percent}%"

    if "cpu usage" in text:
        return f"CPU usage is {psutil.cpu_percent()}%"

    return None