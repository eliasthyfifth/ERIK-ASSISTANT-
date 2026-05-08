import psutil
import time
import logging
from .config import config
from .utils import alert

logger = logging.getLogger(__name__)

class ResourceWatchdog:
    def __init__(self):
        self.battery_threshold = 20
        self.ram_threshold = 90
        self.cpu_threshold = 90
        
        self.cooldowns = {"battery": 0, "ram": 0, "cpu": 0}
        self.cooldown_period = config.get("watchdog.cooldown", 600)

    def check(self):
        current_time = time.time()
        
        battery = psutil.sensors_battery()
        if battery and battery.percent <= self.battery_threshold and not battery.power_plugged:
            if current_time - self.cooldowns["battery"] > self.cooldown_period:
                msg_template = config.get("watchdog.battery_low", "Battery is low: {percent}%")
                msg = msg_template.format(percent=battery.percent)
                alert(msg)
                self.cooldowns["battery"] = current_time

        ram = psutil.virtual_memory()
        if ram.percent >= self.ram_threshold:
            if current_time - self.cooldowns["ram"] > self.cooldown_period:
                msg = config.get("watchdog.ram_critical", "RAM critical!")
                alert(msg)
                self.cooldowns["ram"] = current_time

        cpu = psutil.cpu_percent(interval=1)
        if cpu >= self.cpu_threshold:
            if current_time - self.cooldowns["cpu"] > self.cooldown_period:
                msg = config.get("watchdog.cpu_high", "CPU high!")
                alert(msg)
                self.cooldowns["cpu"] = current_time

    def start_loop(self, interval=30):
        logger.info(f"Starting Resource Watchdog (interval: {interval}s)...")
        while True:
            try:
                self.check()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Watchdog Error: {e}")
                time.sleep(interval)
