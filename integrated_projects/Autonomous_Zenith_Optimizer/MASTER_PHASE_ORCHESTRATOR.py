"""
MASTER_PHASE_ORCHESTRATOR.py
Python-Alternative zum Batch-Starter.
"""
import subprocess, sys

PHASES = [
    ("Phase 1 Error Scan", [sys.executable, "PHASE_1_ERROR_SCAN.py"]),
    # Weitere Phasen hier eintragen, z.B. ("Phase 2", [sys.executable, "phase2.py"])
]

def run():
    for name, cmd in PHASES:
        print(f"=== Starte {name} ===")
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print(f"[ABBRUCH] {name} meldet Fehler. Siehe Report.")
            return r.returncode
        print(f"[OK] {name} abgeschlossen.")
    print("=== Alle Phasen erfolgreich ===")
    return 0

if __name__ == '__main__':
    sys.exit(run())
