import os
import subprocess
import pyautogui
import ctypes
from skills.registry import register_skill

@register_skill(["time", "clock"])
def get_time(command):
    from datetime import datetime
    now = datetime.now().strftime("%H:%M")
    return f"Sir, the current time is {now}."

@register_skill(["date", "today"])
def get_date(command):
    from datetime import datetime
    today = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}, Sir."

@register_skill(["open calculator", "calc"])
def open_calc(command):
    try:
        if os.name == 'nt':
            subprocess.Popen('calc.exe')
        return "Opening calculator for you, Sir."
    except:
        return "Sir, I failed to initialize the calculator module."

@register_skill(["status", "diagnostic"])
def system_status(command):
    return "All systems are functioning within normal parameters. Arc Reactor output is steady at 99.8%."

@register_skill(["open chrome", "browser"])
def open_chrome(command):
    try:
        subprocess.Popen("chrome")
        return "Launching Chrome for you, Sir."
    except:
        return "I could not find the Chrome executable, Sir."

@register_skill(["screenshot", "capture screen"])
def take_screenshot(command):
    try:
        pyautogui.screenshot().save("screenshot.png")
        return "Snapshot taken and saved to the root directory, Sir."
    except:
        return "Sir, I encountered an error during the capture sequence."

@register_skill(["volume up", "louder"])
def volume_up(command):
    pyautogui.press("volumeup")
    return "Increasing audio output, Sir."

@register_skill(["lock screen", "lock windows"])
def lock_screen(command):
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Systems locked, Sir. Stay safe."
    except:
        return "Sir, the security protocols failed to initialize."
@register_skill(["volume down", "quieter"])
def volume_down(command):
    pyautogui.press("volumedown")
    return "Decreasing audio output, Sir."

@register_skill(["mute", "silence"])
def volume_mute(command):
    pyautogui.press("volumemute")
    return "Audio output silenced, Sir."

@register_skill(["shutdown system", "power off"])
def shutdown_system(command):
    if os.name == 'nt':
        os.system("shutdown /s /t 1")
    return "Initiating shutdown sequence, Sir. Goodbye."

@register_skill(["restart system", "reboot"])
def restart_system(command):
    if os.name == 'nt':
        os.system("shutdown /r /t 1")
    return "Initiating system reboot, Sir. I will be back shortly."
