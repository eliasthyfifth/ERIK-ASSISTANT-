import psutil
from ollama import AsyncClient
import logging
import json
from .config import config

logger = logging.getLogger(__name__)

def get_system_info():
    """Fetches real-time system stats."""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    batt_str = f"{battery.percent}%" if battery else "Unknown"
    
    return {
        "cpu_usage": f"{cpu}%",
        "ram_usage": f"{ram}%",
        "battery_level": batt_str
    }

class ErikBrain:
    def __init__(self):
        self.model = config.get("ollama.model", "qwen3:0.6b")
        self.system_prompt = config.get("ollama.system_prompt", "You are ERIK.")
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.max_history = 10
        self.client = AsyncClient()
        
        # Define tools for the model
        self.tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'get_system_info',
                    'description': 'Get the current CPU, RAM, and Battery levels of the computer.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                    },
                },
            },
        ]

    async def chat(self, user_input):
        # Inject real-time system stats secretly
        stats = get_system_info()
        context_hint = f"(System Context: CPU {stats['cpu_usage']}, RAM {stats['ram_usage']}, Battery {stats['battery_level']})"
        
        self.history.append({"role": "user", "content": f"{context_hint}\n{user_input}"})
        
        if len(self.history) > self.max_history:
            self.history = [self.history[0]] + self.history[-(self.max_history-1):]

        try:
            logger.info(f"Ollama Request: {user_input}")
            
            response = await self.client.chat(
                model=self.model,
                messages=self.history,
            )
            
            reply = response['message']['content']
            
            # Clean up the history so we don't clog it with endless system hints
            self.history[-1]["content"] = user_input
            self.history.append({"role": "assistant", "content": reply})
            
            logger.info(f"Ollama Reply: {reply}")
            return reply
            
        except Exception as e:
            logger.error(f"Ollama Error: {e}")
            return "Baka! My brain is lagging! (Error)"

brain = ErikBrain()
