
from core.echo import Echo

class Oracle:
    """
    The Oracle (PCE): Antizipiert und verhindert Fehler, bevor sie entstehen.
    """
    def __init__(self, echo: Echo):
        self.echo = echo
        self.history = []

    def anticipate(self):
        status = self.echo.get_instantaneous_status()
        self.history.append(status["ram_percent"])
        if len(self.history) > 5 and status["ram_percent"] > 80:
            return {"intervention": True, "reason": "RAM-Drift", "value": status["ram_percent"]}
        return {"intervention": False}
