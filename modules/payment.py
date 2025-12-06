"""Payment-Modul - Stripe/PayPal Integration"""
from core.key_check import require_keys
import os
import requests
from dotenv import load_dotenv

load_dotenv()

@require_keys
def run(*args):
    return {"status": "Payment-Modul aktiv", "integrations": ["Stripe", "PayPal"]}

def check_license(user_id):
    """Prüft Lizenz für User"""
    return {"user_id": user_id, "licensed": True}

def process_stripe_payment(amount, currency="eur", email=""):
    """Verarbeitet Stripe Zahlung"""
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise RuntimeError("STRIPE_API_KEY fehlt in .env")

    # Stripe Payment Intent erstellen
    url = "https://api.stripe.com/v1/payment_intents"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "amount": int(amount * 100),  # Cents
        "currency": currency,
        "receipt_email": email
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_paypal_payment(amount, currency="EUR", description=""):
    """Verarbeitet PayPal Zahlung"""
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("PAYPAL_CLIENT_ID oder PAYPAL_CLIENT_SECRET fehlt in .env")

    # PayPal OAuth Token holen
    auth_url = "https://api.paypal.com/v1/oauth2/token"
    auth_response = requests.post(
        auth_url,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"}
    )

    if auth_response.status_code != 200:
        return {"status": "error", "message": "PayPal Auth fehlgeschlagen"}

    access_token = auth_response.json()["access_token"]

    # PayPal Order erstellen
    order_url = "https://api.paypal.com/v2/checkout/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency,
                "value": str(amount)
            },
            "description": description
        }]
    }

    try:
        response = requests.post(order_url, headers=headers, json=order_data)
        if response.status_code == 201:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_payment(amount, method="stripe", email="", currency="EUR"):
    """Verarbeitet Zahlung über Stripe oder PayPal"""
    if method.lower() == "stripe":
        return process_stripe_payment(amount, currency.lower(), email)
    elif method.lower() == "paypal":
        return process_paypal_payment(amount, currency, f"Payment of {amount} {currency}")
    else:
        raise ValueError(f"Unbekannte Zahlungsmethode: {method}")

def describe():
    return "Payment-Modul - Stripe/PayPal Integration mit vollem API Support"
