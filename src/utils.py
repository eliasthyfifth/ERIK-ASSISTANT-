import subprocess
import logging
from .config import config

logger = logging.getLogger(__name__)

def notify(message, title=None):
    """Sends a desktop notification using notify-send."""
    if not config.get("notifications.enabled", True):
        return
        
    if not title:
        title = config.get("notifications.title", "ERIK")
        
    try:
        subprocess.run(["notify-send", "--", title, message], check=False)
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

def alert(message, title=None, voice_text=None):
    """Combines a notification and a voice message."""
    # Send notification first (it's instant)
    notify(message, title)
    
    # Then speak
    from .tts import speak
    speak(voice_text if voice_text else message)
