import psutil
import time

class Echo:
    """
    The Echo (ICB): Liefert die atomare Wahrheit der Gegenwart.
    """
    def get_instantaneous_status(self):
        ram = psutil.virtual_memory().percent
        now = time.time()
        return {"ram_percent": ram, "timestamp": now}
