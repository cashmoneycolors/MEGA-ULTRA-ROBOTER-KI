#!/usr/bin/env python3
import json
from pathlib import Path

def setup_paypal():
    print("\n" + "="*60)
    print("[SETUP] PayPal Business Integration")
    print("="*60 + "\n")
    
    print("Get your PayPal credentials from:")
    print("https://developer.paypal.com/dashboard/\n")
    
    client_id = input("Enter PayPal Client ID: ").strip()
    client_secret = input("Enter PayPal Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("[ERROR] Credentials required")
        return False
    
    config = {
        "paypal": {
            "client_id": client_id,
            "client_secret": client_secret,
            "mode": "sandbox"
        }
    }
    
    with open("paypal_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n[OK] PayPal configured!")
    print("[OK] Config saved to paypal_config.json")
    print("\n" + "="*60)
    print("[READY] App is ready to use!")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    setup_paypal()
