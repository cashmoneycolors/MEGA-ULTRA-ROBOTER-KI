#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class PayPalBusiness:
    def __init__(self):
        self.mode = os.getenv("PAYPAL_MODE", "sandbox")
        self.client_id = os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
        self.db_path = "wealth_system.db"
        
        if self.mode == "sandbox":
            self.api_url = "https://api.sandbox.paypal.com"
        else:
            self.api_url = "https://api.paypal.com"
        
        self.access_token = None
        self.setup_db()
    
    def setup_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS paypal_business_transactions
                     (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, amount REAL, 
                      currency TEXT, transaction_id TEXT, status TEXT, description TEXT)''')
        conn.commit()
        conn.close()
    
    def get_access_token(self):
        """Get PayPal OAuth2 Access Token"""
        try:
            auth = (self.client_id, self.client_secret)
            headers = {"Accept": "application/json", "Accept-Language": "en_US"}
            data = {"grant_type": "client_credentials"}
            
            response = requests.post(
                f"{self.api_url}/v1/oauth2/token",
                auth=auth,
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                return self.access_token
            else:
                print(f"Error getting token: {response.text}")
                return None
        except Exception as e:
            print(f"Token error: {str(e)}")
            return None
    
    def create_invoice(self, amount, description, customer_email):
        """Create PayPal Invoice for Business"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            invoice_data = {
                "detail": {
                    "currency_code": "CHF",
                    "invoice_number": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "invoice_date": datetime.now().isoformat()
                },
                "invoicer": {
                    "name": {"given_name": "Wealth", "surname": "System"},
                    "email_address": "business@wealthsystem.ch"
                },
                "primary_recipients": [{
                    "billing_info": {"email_address": customer_email}
                }],
                "items": [{
                    "name": description,
                    "quantity": "1",
                    "unit_amount": {"currency_code": "CHF", "value": str(amount)}
                }],
                "amount": {
                    "currency_code": "CHF",
                    "value": str(amount)
                }
            }
            
            response = requests.post(
                f"{self.api_url}/v1/invoicing/invoices",
                headers=headers,
                json=invoice_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.record_transaction("invoice", amount, "CHF", result.get("id"), "created", description)
                return {"status": "success", "invoice_id": result.get("id")}
            else:
                print(f"Invoice error: {response.text}")
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def send_invoice(self, invoice_id):
        """Send Invoice to Customer"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.post(
                f"{self.api_url}/v1/invoicing/invoices/{invoice_id}/send",
                headers=headers,
                json={"send_to_invoicer": True}
            )
            
            if response.status_code == 202:
                self.record_transaction("invoice_sent", 0, "CHF", invoice_id, "sent", "Invoice sent")
                return {"status": "success"}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_payment_link(self, amount, description):
        """Create PayPal Payment Link for Quick Checkout"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            payment_data = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "CHF",
                        "value": str(amount)
                    },
                    "description": description
                }],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "return_url": "http://localhost:8000/success",
                            "cancel_url": "http://localhost:8000/cancel"
                        }
                    }
                }
            }
            
            response = requests.post(
                f"{self.api_url}/v1/checkout/orders",
                headers=headers,
                json=payment_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                order_id = result.get("id")
                approval_link = next(
                    (link["href"] for link in result.get("links", []) if link["rel"] == "approve"),
                    None
                )
                self.record_transaction("payment_link", amount, "CHF", order_id, "created", description)
                return {"status": "success", "order_id": order_id, "approval_url": approval_link}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def capture_payment(self, order_id):
        """Capture Payment after Approval"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.post(
                f"{self.api_url}/v1/checkout/orders/{order_id}/capture",
                headers=headers,
                json={}
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                amount = float(result["purchase_units"][0]["amount"]["value"])
                self.record_transaction("payment_captured", amount, "CHF", order_id, "completed", "Payment captured")
                return {"status": "success", "amount": amount}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_payout(self, recipient_email, amount, description):
        """Create Payout to Business Partner"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            payout_data = {
                "sender_batch_header": {
                    "sender_batch_id": f"PAYOUT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "email_subject": "You have a payout from Wealth System",
                    "email_message": description
                },
                "items": [{
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": str(amount),
                        "currency": "CHF"
                    },
                    "description": description,
                    "receiver": recipient_email
                }]
            }
            
            response = requests.post(
                f"{self.api_url}/v1/payments/payouts",
                headers=headers,
                json=payout_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                batch_id = result.get("batch_header", {}).get("payout_batch_id")
                self.record_transaction("payout", amount, "CHF", batch_id, "processing", description)
                return {"status": "success", "batch_id": batch_id}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_transaction_details(self, transaction_id):
        """Get Transaction Details"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(
                f"{self.api_url}/v1/checkout/orders/{transaction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def record_transaction(self, trans_type, amount, currency, trans_id, status, description):
        """Record Transaction in Database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""INSERT INTO paypal_business_transactions 
                         (timestamp, type, amount, currency, transaction_id, status, description) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)""",
                     (datetime.now().isoformat(), trans_type, amount, currency, trans_id, status, description))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB error: {str(e)}")
    
    def get_transaction_history(self, limit=10):
        """Get Recent Transactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""SELECT * FROM paypal_business_transactions 
                         ORDER BY timestamp DESC LIMIT ?""", (limit,))
            transactions = c.fetchall()
            conn.close()
            return transactions
        except Exception as e:
            print(f"Error: {str(e)}")
            return []

if __name__ == "__main__":
    paypal = PayPalBusiness()
    
    # Test: Create Payment Link
    result = paypal.create_payment_link(50, "AI Art Generation Service")
    print(f"Payment Link: {result}")
    
    # Test: Create Invoice
    invoice = paypal.create_invoice(100, "Vector Services", "customer@example.com")
    print(f"Invoice: {invoice}")
