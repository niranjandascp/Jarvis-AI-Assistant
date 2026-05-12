try:
    from skills.registry import execute_skill
    # Import skills modules relatively
    from skills import system_skills, clipboard_skills, web_search_skills, weather_skills, reminder_skills, music_skills, note_skills
except (ImportError, ValueError):
    try:
        from skills.registry import execute_skill
        import skills.system_skills
        import skills.clipboard_skills
        import skills.web_search_skills
        import skills.weather_skills
        import skills.reminder_skills
        import skills.music_skills
        import skills.note_skills
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'skills'))
        from registry import execute_skill
        import system_skills
        import clipboard_skills
        import web_search_skills
        import weather_skills
        import reminder_skills
        import music_skills
        import note_skills

def run_command(command):
    """
    JARVIS Command Hub.
    Dispatches user commands to the appropriate skill module.
    """
    # 1. Check the Skills Registry
    reply = execute_skill(command)
    if reply:
        return reply

    # 2. Add local logic for one-off commands if needed
    if "hello" in command.lower() or "jarvis" in command.lower() and len(command) < 10:
        return "At your service, Sir."

    # 3. If no skill matches, return None (will fallback to AI)
    return None