import logging
import signal
import sys
from pydbus import SystemBus
from gi.repository import GLib
from .config import config
from .utils import alert

logger = logging.getLogger(__name__)

class SystemEventListener:
    def __init__(self):
        self.bus = SystemBus()
        try:
            self.login_manager = self.bus.get("org.freedesktop.login1", "/org/freedesktop/login1")
        except Exception as e:
            logger.error(f"Failed to connect to systemd-logind: {e}")
            sys.exit(1)

    def on_prepare_for_sleep(self, sleeping):
        if sleeping:
            logger.info("System is going to sleep...")
            msg = config.get("messages.suspend", "Goodbye.")
            alert(msg)
        else:
            logger.info("System just woke up!")
            msg = config.get("messages.wake", "I am awake.")
            alert(msg)

    def run(self):
        logger.info("Starting DBus event listener...")
        self.login_manager.PrepareForSleep.connect(self.on_prepare_for_sleep)
        self.loop = GLib.MainLoop()
        signal.signal(signal.SIGINT, lambda *args: self.stop())
        signal.signal(signal.SIGTERM, lambda *args: self.stop())

        try:
            self.loop.run()
        except Exception as e:
            logger.error(f"Event Loop Error: {e}")

    def stop(self):
        logger.info("Stopping event listener...")
        if self.loop:
            self.loop.quit()
