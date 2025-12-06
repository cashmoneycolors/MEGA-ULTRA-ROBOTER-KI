#!/usr/bin/env python3
import paypalrestsdk
import sqlite3
from datetime import datetime

class PayPalManager:
    def __init__(self, client_id, client_secret):
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": client_id,
            "client_secret": client_secret
        })
        self.db_path = "wealth_system.db"
        self.setup_db()
    
    def setup_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS paypal_transactions
                     (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, amount REAL, 
                      transaction_id TEXT, status TEXT)''')
        conn.commit()
        conn.close()
    
    def load_funds(self, amount):
        """Lade Geld von PayPal"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [{
                    "amount": {"total": str(amount), "currency": "CHF"},
                    "description": "Wealth System Funding"
                }],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/success",
                    "cancel_url": "http://localhost:8000/cancel"
                }
            })
            
            if payment.create():
                self.record_transaction("load", amount, payment.id, "pending")
                return {"status": "success", "payment_id": payment.id}
            else:
                return {"status": "error", "message": payment.error["message"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def withdraw_profit(self, amount):
        """Zahle Gewinn auf PayPal aus"""
        try:
            payout = paypalrestsdk.Sale.find(amount)
            if payout.execute():
                self.record_transaction("withdraw", amount, payout.id, "completed")
                return {"status": "success", "payout_id": payout.id}
            else:
                return {"status": "error"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def record_transaction(self, trans_type, amount, trans_id, status):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT INTO paypal_transactions 
                     (timestamp, type, amount, transaction_id, status) 
                     VALUES (?, ?, ?, ?, ?)""",
                 (datetime.now().isoformat(), trans_type, amount, trans_id, status))
        conn.commit()
        conn.close()
    
    def get_balance(self):
        """Hole PayPal Balance"""
        try:
            account = paypalrestsdk.Account.find()
            return account.balance if account else 0
        except:
            return 0
