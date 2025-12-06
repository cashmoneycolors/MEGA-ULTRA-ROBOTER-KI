#!/usr/bin/env python3
import paypalrestsdk
import json
from pathlib import Path

print("\n[TEST] PayPal Connection\n")

try:
    with open("paypal_config.json") as f:
        config = json.load(f)
except:
    print("[ERROR] paypal_config.json not found")
    exit(1)

client_id = config["paypal"]["client_id"]
client_secret = config["paypal"]["client_secret"]

print(f"Client ID: {client_id[:10]}...")
print(f"Secret: {client_secret[:10]}...\n")

paypalrestsdk.configure({
    "mode": "live",
    "client_id": client_id,
    "client_secret": client_secret
})

try:
    payout = paypalrestsdk.Payout({
        "sender_batch_header": {
            "sender_batch_id": "test_batch",
            "email_subject": "Test"
        },
        "items": [{
            "recipient_type": "EMAIL",
            "amount": {"value": "0.01", "currency": "CHF"},
            "receiver": config["paypal"]["email"],
            "note": "Test"
        }]
    })
    
    if payout.create():
        print("[OK] PayPal connection successful!")
        print(f"[OK] Batch ID: {payout.batch_header.payout_batch_id}\n")
    else:
        print(f"[ERROR] {payout.error}\n")
except Exception as e:
    print(f"[ERROR] {e}\n")
