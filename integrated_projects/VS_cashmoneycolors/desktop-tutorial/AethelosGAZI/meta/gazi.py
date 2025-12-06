
from agents.oracle import Oracle

class GAZI:
    """
    GAZI (Meta-Kognition): Überwacht und optimiert die Regeln des Systems.
    """
    def __init__(self, oracle: Oracle):
        self.oracle = oracle
        self.tuning = {"ram_threshold": 80}

    def audit_and_optimize(self):
        if self.oracle.history and max(self.oracle.history[-5:]) > self.tuning["ram_threshold"]:
            self.tuning["ram_threshold"] += 5
            print(f"GAZI: RAM-Schwellenwert auf {self.tuning['ram_threshold']}% erhöht.")
