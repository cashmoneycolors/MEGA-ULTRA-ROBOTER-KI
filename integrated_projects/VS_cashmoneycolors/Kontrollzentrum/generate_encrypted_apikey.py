"""
Hilfsskript zum Generieren eines Fernet-Schlüssels und zum Verschlüsseln eines API-Keys.
Ergebnis: apikey_secret.key und apikeys.enc.json werden erzeugt.
"""
from cryptography.fernet import Fernet
import json
import os

# 1. Fernet-Key generieren und speichern
KEY_FILE = "apikey_secret.key"
STORE_FILE = "apikeys.enc.json"

if not os.path.exists(KEY_FILE):
    fernet_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(fernet_key)
    print(f"Fernet-Key generiert und gespeichert: {fernet_key}")
else:
    with open(KEY_FILE, "rb") as f:
        fernet_key = f.read()
    print(f"Fernet-Key geladen: {fernet_key}")

# 2. API-Key eingeben und verschlüsseln
api_key = input("Gib den API-Key ein, der verschlüsselt werden soll: ").strip()
service = input("Service-Name (z.B. stripe, s3, nft): ").strip()

f = Fernet(fernet_key)
enc_data = {}
if os.path.exists(STORE_FILE):
    with open(STORE_FILE, "rb") as fstore:
        try:
            enc_data = json.loads(f.decrypt(fstore.read()).decode())
        except Exception:
            enc_data = {}
enc_data[service] = f.encrypt(api_key.encode()).decode()
with open(STORE_FILE, "wb") as fstore:
    fstore.write(f.encrypt(json.dumps(enc_data).encode()))
print(f"API-Key für {service} verschlüsselt gespeichert!")
