# ==========================================================
# ⚠️ SICHERHEITS-HINWEIS: Kritische Secrets niemals hardcodieren!
# Alle Secrets (z.B. JWT_SECRET, MAINTENANCE_KEY) müssen aus
# Umgebungsvariablen geladen werden. Falls ein Secret fehlt,
# wird es sicher generiert und eine gelbe Warnung ausgegeben.
# ==========================================================
import os
import secrets
import warnings

def get_secret_env(key: str, length: int = 32) -> str:
    value = os.environ.get(key)
    if value is None or not value.strip():
        # Sichere Generierung & explizite Warnung
        value = secrets.token_urlsafe(length)
        warnings.warn(
            f"\033[93mWARNUNG: {key} wurde zur Laufzeit generiert! "
            "Bitte setze das Secret als Umgebungsvariable für Produktion.\033[0m",
            stacklevel=2
        )
    return value

# Beispiel für kritische Secrets:
JWT_SECRET = get_secret_env("JWT_SECRET", 48)
MAINTENANCE_KEY = get_secret_env("MAINTENANCE_KEY", 32)
# ... weitere Secrets nach Bedarf

# ==========================================================
# Ende Sicherheitsblock – ab hier beginnt deine eigentliche App-Logik
# ==========================================================