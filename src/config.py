import yaml
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

class Config:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                self.data = yaml.safe_load(f)
        else:
            # Fallback defaults
            self.data = {
                "voice": {
                    "default_voice": "af_heart",
                    "default_lang": "en-us",
                    "speed": 1.1
                }
            }

    def get(self, key, default=None):
        keys = key.split(".")
        val = self.data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

config = Config()
