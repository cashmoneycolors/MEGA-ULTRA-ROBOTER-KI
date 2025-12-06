#!/usr/bin/env python3
import sqlite3
import json
import time
import paypalrestsdk
from datetime import datetime
from pathlib import Path

class AutoWithdraw:
    def __init__(self):
        self.db_path = "wealth_system.db"
        self.config_file = "paypal_config.json"
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file) as f:
                config = json.load(f)
                self.client_id = config["paypal"]["client_id"]
                self.client_secret = config["paypal"]["client_secret"]
                self.email = config["paypal"]["email"]
        except:
            self.client_id = None
            self.client_secret = None
            self.email = None
    
    def get_current_capital(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT MAX(balance) FROM transactions")
            capital = c.fetchone()[0] or 0
            conn.close()
            return capital
        except:
            return 0
    
    def get_last_withdrawal(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT MAX(timestamp) FROM transactions WHERE type='paypal_withdraw'")
            result = c.fetchone()[0]
            conn.close()
            return result
        except:
            return None
    
    def withdraw_to_paypal(self, amount):
        if not all([self.client_id, self.client_secret, self.email]):
            print("[ERROR] PayPal not configured")
            return False
        
        try:
            paypalrestsdk.configure({
                "mode": "live",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            })
            
            payout = paypalrestsdk.Payout({
                "sender_batch_header": {
                    "sender_batch_id": f"batch_{int(time.time())}",
                    "email_subject": "Wealth System Payout"
                },
                "items": [{
                    "recipient_type": "EMAIL",
                    "amount": {"value": str(amount), "currency": "CHF"},
                    "receiver": self.email,
                    "note": "Wealth System Profit"
                }]
            })
            
            if payout.create():
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO transactions (timestamp, type, amount, balance) VALUES (?, ?, ?, ?)",
                         (datetime.now().isoformat(), "paypal_withdraw", -amount, -amount))
                conn.commit()
                conn.close()
                print(f"[WITHDRAW] {amount:.2f} CHF -> PayPal (Batch: {payout.batch_header.payout_batch_id})")
                return True
            else:
                print(f"[ERROR] PayPal: {payout.error}")
                return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    def run(self):
        print("[AUTO-WITHDRAW] Started")
        while True:
            capital = self.get_current_capital()
            
            if capital > 10000:
                withdraw_amount = capital * 0.1
                self.withdraw_to_paypal(withdraw_amount)
            
            time.sleep(300)

if __name__ == "__main__":
    auto = AutoWithdraw()
    auto.run()
