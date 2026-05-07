import json
import os
import sys

class MemoryManager:
    def __init__(self):
        """
        JARVIS Persistent Memory Controller.
        Uses Absolute Pathing to ensure data integrity across all execution environments.
        """
        # CRITICAL: Use abspath to ensure dirname doesn't return an empty string
        current_file_path = os.path.abspath(__file__)
        self.script_dir = os.path.dirname(current_file_path)
        self.filepath = os.path.join(self.script_dir, "memory.json")
        
        print(f"--- JARVIS NEURAL BANK INITIALIZED ---")
        print(f"Target Path: {self.filepath}")
        
        self.memory = self.load_memory()

    def load_memory(self):
        # Create file if it doesn't exist to prevent 'No such file' errors
        if not os.path.exists(self.filepath):
            try:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
                return []
            except Exception as e:
                print(f"FAILED TO CREATE MEMORY BANK: {e}")
                return []
            
        try:
            if os.path.getsize(self.filepath) == 0:
                return []
                
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def save_memory(self, history):
        try:
            self.memory = history
            # Atomic save: temp -> replace
            temp_path = self.filepath + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4, ensure_ascii=False)
            
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            os.rename(temp_path, self.filepath)
        except Exception as e:
            print(f"MEMORY_SAVE_FAILURE: {e}", file=sys.stderr)

    def get_memory(self, limit=15):
        return self.memory[-limit:] if self.memory else []

    def add_interaction(self, user_msg, ai_reply):
        self.memory.append({"role": "user", "content": user_msg})
        self.memory.append({"role": "assistant", "content": ai_reply})
        
        if len(self.memory) > 200:
            self.memory = self.memory[-200:]
            
        self.save_memory(self.memory)

# Instantiate the global manager
memory_manager = MemoryManager()