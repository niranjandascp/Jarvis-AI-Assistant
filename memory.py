import json

FILE = "memory.json"

def load_memory():
    try:
        return json.load(open(FILE))
    except:
        return []

def save_memory(memory):
    json.dump(memory, open(FILE, "w"), indent=2)
    