import json
import os
import sys
import redis

class MemoryManager:
    def __init__(self):
        """
        JARVIS Persistent Memory Controller.
        Now supports Redis (Docker) with JSON fallback.
        """
        current_file_path = os.path.abspath(__file__)
        self.script_dir = os.path.dirname(current_file_path)
        self.filepath = os.path.join(self.script_dir, "memory.json")
        
        # Redis Connection Settings
        self.redis_client = None
        self.use_redis = False
        self.redis_key = "jarvis_memory_v1"

        self.init_redis()
        
        print(f"--- JARVIS NEURAL BANK INITIALIZED ---")
        print(f"Mode: {'REDIS + JSON' if self.use_redis else 'JSON ONLY'}")
        
        self.memory = self.load_memory()

    def init_redis(self):
        """Try to establish a connection to the Redis Docker container."""
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            # Ping to check if server is actually up
            if self.redis_client.ping():
                self.use_redis = True
                print("[DATABASE] Redis Neural Link: CONNECTED")
        except Exception:
            print("[DATABASE] Redis Link: FAILED (Falling back to JSON)")
            self.use_redis = False

    def load_memory(self):
        # 1. Try to load from Redis first
        if self.use_redis:
            try:
                redis_data = self.redis_client.get(self.redis_key)
                if redis_data:
                    return json.loads(redis_data)
            except Exception as e:
                print(f"REDIS_LOAD_ERROR: {e}")

        # 2. Fallback to JSON
        if not os.path.exists(self.filepath):
            return []
            
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []

    def save_memory(self, history):
        self.memory = history
        
        # 1. Save to Redis
        if self.use_redis:
            try:
                self.redis_client.set(self.redis_key, json.dumps(self.memory))
            except Exception as e:
                print(f"REDIS_SAVE_ERROR: {e}")

        # 2. Always save to JSON as a permanent backup
        try:
            temp_path = self.filepath + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4, ensure_ascii=False)
            
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            os.rename(temp_path, self.filepath)
        except Exception as e:
            print(f"JSON_BACKUP_FAILURE: {e}", file=sys.stderr)

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