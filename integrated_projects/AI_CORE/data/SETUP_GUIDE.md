# Autonomous Wealth System - Setup Guide

## Installation

### 1. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 2. App starten
```bash
python start_app.py
```

Die App öffnet sich automatisch auf `http://localhost:5000`

## Konfiguration

### config.json anpassen

Öffne `config.json` und passe folgende Parameter an:

```json
{
  "initial_capital": 100,
  "target_capital": 10000,
  "cycle_interval": 2,
  "art_allocation": 0.40,
  "trading_allocation": 0.35,
  "vector_allocation": 0.25
}
```

### PayPal Integration (Optional)

1. Gehe zu https://developer.paypal.com
2. Erstelle eine App
3. Kopiere `client_id` und `client_secret`
4. Füge sie in `config.json` ein:

```json
"paypal": {
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "sandbox_mode": true
}
```

## Web Dashboard

Das Dashboard zeigt:
- 💰 Aktuelles Kapital
- 🎯 Zielkapital
- 📊 Fortschritt in %
- 🔄 Anzahl der Zyklen
- 🎨 Erstellte KI-Kunstwerke
- 📈 Durchgeführte Trades
- 🤖 Aktive Klone
- ⚙️ System-Status

### Steuerung

- **▶️ Start System** - Startet autonomen Betrieb
- **⏹️ Stop System** - Stoppt das System
- **🔄 Refresh** - Aktualisiert die Anzeige

## Datenbank

Die Transaktionen werden in `wealth_system.db` gespeichert:
- `transactions` - Alle Transaktionen
- `art_portfolio` - KI-Kunstwerke
- `trading_log` - Trading-Aktivitäten
- `clones` - Autonome Klone
- `paypal_transactions` - PayPal-Zahlungen

## Logs

Alle Aktivitäten werden in `system.log` protokolliert.

## Troubleshooting

### Port 5000 bereits in Verwendung
```bash
python start_app.py --port 8000
```

### Datenbank zurücksetzen
```bash
rm wealth_system.db
```

## Features

### KI-Kunst Produktion (40%)
- Automatische Erstellung von KI-Kunstwerken
- Verkauf mit Gewinn
- Portfolio-Tracking

### Asset Trading (35%)
- Multi-Asset Trading (BTC, ETH, Gold, Silver)
- Automatische Preisanalyse
- Gewinn-Optimierung

### Vector Services (25%)
- Professionelle Vector-Design Services
- Automatische Preisberechnung
- Service-Tracking

### Clone Management
- Autonome Replikation des Systems
- Gewinn-Multiplikator
- Maximale Anzahl: 25 Klone

## Support

Bei Fragen oder Problemen:
1. Überprüfe `system.log`
2. Stelle sicher, dass alle Dependencies installiert sind
3. Überprüfe die Konfiguration in `config.json`
