#!/usr/bin/env python3
import paypalrestsdk
import json
from pathlib import Path

class PayPalLive:
    def __init__(self, client_id, client_secret):
        paypalrestsdk.configure({
            "mode": "live",
            "client_id": client_id,
            "client_secret": client_secret
        })
    
    def withdraw_to_paypal(self, amount, email):
        """Zahle echtes Geld auf PayPal aus"""
        try:
            payout = paypalrestsdk.Payout({
                "sender_batch_header": {
                    "sender_batch_id": f"batch_{int(amount)}",
                    "email_subject": "Wealth System Payout"
                },
                "items": [{
                    "recipient_type": "EMAIL",
                    "amount": {"value": str(amount), "currency": "CHF"},
                    "receiver": email,
                    "note": "Wealth System Profit"
                }]
            })
            
            if payout.create():
                return {"status": "success", "batch_id": payout.batch_header.payout_batch_id}
            else:
                return {"status": "error", "message": payout.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_payout_status(self, batch_id):
        """Hole Status der Auszahlung"""
        try:
            payout = paypalrestsdk.Payout.find(batch_id)
            return payout.to_dict() if payout else None
        except:
            return None

if __name__ == "__main__":
    config_file = Path("paypal_config.json")
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        
        paypal = PayPalLive(
            config["paypal"]["client_id"],
            config["paypal"]["client_secret"]
        )
        
        # Test
        result = paypal.withdraw_to_paypal(10, "your-email@example.com")
        print(f"[PAYOUT] {result}")
