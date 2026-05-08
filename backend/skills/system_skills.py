import os
import subprocess
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
