#!/usr/bin/env python3
import json
from pathlib import Path

print("\n" + "="*60)
print("[FIX] PayPal Configuration")
print("="*60 + "\n")

print("Get credentials from: https://developer.paypal.com/dashboard/\n")

client_id = input("Enter PayPal Client ID: ").strip()
client_secret = input("Enter PayPal Client Secret: ").strip()
email = input("Enter PayPal Business Email: ").strip()

if not all([client_id, client_secret, email]):
    print("[ERROR] All fields required")
    exit(1)

config = {
    "paypal": {
        "client_id": client_id,
        "client_secret": client_secret,
        "email": email,
        "mode": "live"
    }
}

with open("paypal_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("\n[OK] PayPal configured!")
print(f"[OK] Client ID: {client_id[:10]}...")
print(f"[OK] Email: {email}")
print("\n" + "="*60 + "\n")
