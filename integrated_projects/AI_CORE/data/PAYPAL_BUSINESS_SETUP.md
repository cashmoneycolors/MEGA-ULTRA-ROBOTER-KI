# PayPal Business Integration Setup

## Schritt 1: PayPal Developer Account erstellen
1. Gehe zu https://developer.paypal.com
2. Registriere dich oder melde dich an
3. Gehe zu "Apps & Credentials"

## Schritt 2: Sandbox Credentials generieren
1. Wähle "Sandbox" (oben rechts)
2. Klicke auf "Create App"
3. Gib einen Namen ein (z.B. "Wealth System")
4. Kopiere:
   - **Client ID**
   - **Secret**

## Schritt 3: .env Datei aktualisieren
```bash
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_sandbox_client_id_here
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret_here
PAYPAL_RECIPIENT_EMAIL=your-email@example.com
```

## Schritt 4: Abhängigkeiten installieren
```bash
pip install requests python-dotenv
```

## Schritt 5: System testen
```bash
python paypal_business.py
```

## Schritt 6: Live-Modus aktivieren
Wenn alles funktioniert:
1. Gehe zu https://developer.paypal.com/dashboard/live
2. Kopiere Live Client ID & Secret
3. Aktualisiere .env:
```bash
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=your_live_client_id_here
PAYPAL_CLIENT_SECRET=your_live_client_secret_here
```

## Features
- ✅ Invoices erstellen & versenden
- ✅ Payment Links generieren
- ✅ Zahlungen erfassen
- ✅ Payouts an Partner
- ✅ Transaktionshistorie

## Wealth System mit PayPal starten
```bash
python cash_money_production_paypal.py
```

Das System wird automatisch:
- Gewinne generieren
- 10% der Gewinne via PayPal auszahlen
- Alle Transaktionen loggen
