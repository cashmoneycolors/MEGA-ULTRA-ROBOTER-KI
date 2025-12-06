"""
MEGA ULTRA ROBOTER KI – Kontrollzentrum
SICHERHEITSHINWEIS (SECRETS):
-------------------------------------------------------------
Kritische Secrets (z.B. API-Keys) werden ausschließlich über Umgebungsvariablen bezogen oder sicher zur Laufzeit generiert. Niemals hardcodieren!

- Wenn ein Secret generiert wird, erscheint eine gelbe Warnung.
- In Produktion MÜSSEN die Secrets gesetzt sein!
- Siehe MEGA_WORKFLOW_CHECKLISTE.md und README.md für Details.
"""

import sys
import os  # os wurde hier hinzugefügt

def check_critical_keys():
    required_keys = ["APPGEN_API_KEY", "PMAK_API_KEY", "OPENAI_API_KEY", "MATHPIX_API_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        print(f"\033[93m[WARNUNG] Kritische Secrets fehlen: {', '.join(missing)}. Bitte als Umgebungsvariable setzen! Niemals im Code speichern!\033[0m", file=sys.stderr)
        return False
    print("[OK] Alle kritischen Secrets sind gesetzt.")
    return True