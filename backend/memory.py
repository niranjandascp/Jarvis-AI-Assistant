import json
import os

class MemoryManager:
    def __init__(self, filepath="backend/memory.json"):
        self.filepath = filepath
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_memory(self, history):
        self.memory = history
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f, indent=4)

    def get_memory(self, limit=20):
        # Return last N messages for context
        return self.memory[-limit:]

    def add_interaction(self, user_msg, ai_reply):
        self.memory.append({"role": "user", "content": user_msg})
        self.memory.append({"role": "assistant", "content": ai_reply})
        # Keep only last 100 interactions in file for performance
        if len(self.memory) > 200:
            self.memory = self.memory[-200:]
        self.save_memory(self.memory)

memory_manager = MemoryManager()