# --- JARVIS SKILLS REGISTRY ---

SKILLS = {}

def register_skill(keywords):
    """
    Decorator to register a function as a JARVIS skill.
    'keywords' can be a single string or a list of trigger words.
    """
    def decorator(fn):
        if isinstance(keywords, list):
            for kw in keywords:
                SKILLS[kw.lower()] = fn
                print(f"[SKILL]: Registered [{kw.lower()}]")
        else:
            SKILLS[keywords.lower()] = fn
            print(f"[SKILL]: Registered [{keywords.lower()}]")
        return fn
    return decorator

def execute_skill(command):
    """
    Check if the command contains any registered skill keywords.
    Returns the skill response if found, else None.
    """
    cmd_lower = command.lower()
    
    # Sort keywords by length (longest first) to ensure specific matches win
    sorted_keywords = sorted(SKILLS.keys(), key=len, reverse=True)
    
    for kw in sorted_keywords:
        if kw in cmd_lower:
            return SKILLS[kw](command)
    return None
