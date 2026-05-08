import socket
import os
import threading
import logging
import asyncio
from .brain import brain
from .utils import alert

logger = logging.getLogger(__name__)

SOCKET_PATH = "/tmp/erik.sock"

class ErikBridge:
    def __init__(self):
        self.running = False

    def start(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
            
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(SOCKET_PATH)
        self.server.listen(1)
        self.running = True
        
        logger.info(f"Communication Bridge started at {SOCKET_PATH}")
        
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        # We need a new event loop for this thread to run the async brain
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while self.running:
            try:
                conn, _ = self.server.accept()
                data = conn.recv(1024)
                if data:
                    user_msg = data.decode("utf-8").strip()
                    if user_msg:
                        # Process message via brain
                        reply = loop.run_until_complete(brain.chat(user_msg))
                        # Speak and Notify the reply
                        alert(reply, title="ERIK Reply")
                conn.close()
            except Exception as e:
                if self.running:
                    logger.error(f"Bridge Loop Error: {e}")

    def stop(self):
        self.running = False
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

bridge = ErikBridge()
