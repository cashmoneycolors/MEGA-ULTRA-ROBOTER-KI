# Wealth System Pro - PayPal Integration

## Setup

### 1. PayPal Business Account
- Gehe zu https://www.paypal.com/business
- Erstelle einen Business Account

### 2. Developer Credentials
- Gehe zu https://developer.paypal.com/dashboard/
- Melde dich an
- Gehe zu "Apps & Credentials"
- Kopiere deine **Client ID** und **Client Secret**

### 3. App starten
```bash
python launch_pro.py
```

### 4. Credentials eingeben
- Gib deine PayPal Client ID ein
- Gib dein PayPal Client Secret ein
- Klick "Connect"

## Features

### Geld laden
1. Klick "Load Funds"
2. Gib Betrag ein (z.B. 100 CHF)
3. Geld wird von PayPal geladen

### System starten
1. Klick "Start System"
2. Quantum System läuft autonom
3. Verdient automatisch Geld

### Gewinn abheben
1. Klick "Withdraw Profit"
2. Gib Betrag ein
3. Geld wird auf PayPal Business Account überwiesen

## Automatische Auszahlungen

Das System zahlt automatisch Gewinne aus wenn:
- Kapital > 1000 CHF
- Quantum Level > 50
- Täglich um 00:00 Uhr

## Status

✅ PayPal Integration aktiv
✅ Automatische Geldladung
✅ Automatische Auszahlungen
✅ Live Statistiken
✅ Quantum System läuft

## Support

Bei Fragen: Siehe PayPal Developer Docs
https://developer.paypal.com/docs/
