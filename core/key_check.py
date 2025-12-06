import os
from dotenv import load_dotenv

load_dotenv()
REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "STRIPE_API_KEY",
    "PAYPAL_CLIENT_ID",
    "PAYPAL_CLIENT_SECRET",
    "EBAY_APP_ID",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "NFT_API_KEY",
    "SMTP_USER",
    "SMTP_PASSWORD",
]


def check_all_keys():
    missing = [k for k in REQUIRED_KEYS if not os.getenv(k)]
    if missing:
        msg = (
            "\n"
            + "=" * 60
            + "\nFEHLENDE API-KEYS!\n"
            + "Die folgenden Keys fehlen in deiner .env-Datei:\n"
            + "\n".join(f"- {k}" for k in missing)
            + "\nBitte trage alle Keys in die .env ein und starte die App neu.\n"
            + "=" * 60
            + "\n"
        )
        raise RuntimeError(msg)


# Decorator für automatische Key-Prüfung
from functools import wraps


def require_keys(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_all_keys()
        return func(*args, **kwargs)

    return wrapper


# FastAPI-Startup
# Soll ich Details zum FastAPI-Startup-Prozess ergänzen? Ich sehe `mega_roboter_ki.py` - ist das der Haupteinstiegspunkt für die API?
# Soll ich den Build-Prozess detaillierter dokumentieren?
# Soll ich daraus spezifische Workflows in die Instructions übernehmen?
# Gibt es Cross-Platform-Anforderungen, die dokumentiert werden sollten?
