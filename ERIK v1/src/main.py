import threading
import logging
import os
from .config import config
from .tts import init_tts
from .utils import alert
from .event_listener import SystemEventListener
from .watchdog import ResourceWatchdog
from .bridge import bridge

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("erik")

def main():
    logger.info("ERIK v3 starting up...")
    
    # 1. Initialize TTS
    try:
        init_tts()
    except Exception as e:
        logger.error(f"Failed to initialize TTS: {e}")
        return

    # 2. Welcome Message
    startup_msg = config.get("messages.startup", "System online.")
    alert(startup_msg)

    # 3. Start Bridge (Socket Server for user messages)
    bridge.start()

    # 4. Start Watchdog in a background thread
    watchdog = ResourceWatchdog()
    watchdog_thread = threading.Thread(target=watchdog.start_loop, daemon=True)
    watchdog_thread.start()

    # 5. Start DBus Event Listener (This blocks)
    listener = SystemEventListener()
    try:
        listener.run()
    except KeyboardInterrupt:
        logger.info("Shutdown requested.")
    finally:
        bridge.stop()
        shutdown_msg = config.get("messages.shutdown", "Goodbye.")
        alert(shutdown_msg)

if __name__ == "__main__":
    main()
