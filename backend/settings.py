import json
import os

class SettingsManager:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(self.script_dir, "settings.json")
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default fallback
        return {
            "model": "llama3",
            "persona": "Jarvis",
            "voice_rate": 170,
            "system_prompt": "You are Jarvis, an advanced AI assistant created by Tony Stark. Be helpful, concise, and professional."
        }

    def save_settings(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Settings Save Error: {e}")
            return False

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

settings_manager = SettingsManager()
