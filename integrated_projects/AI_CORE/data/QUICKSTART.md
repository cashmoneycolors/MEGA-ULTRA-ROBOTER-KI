# 🚀 Quick Start Guide

## Installation
```bash
pip install -r requirements.txt
```

## Starten

### Option 1: Interaktives Menü (Empfohlen)
```bash
python main_menu.py
```

### Option 2: Einzelne Komponenten

**Production System starten:**
```bash
python cash_money_production.py
```

**API Server starten (Port 5000):**
```bash
python api_server.py
```

**Web Dashboard starten (Port 8000):**
```bash
python web_server.py
```

**System Monitor:**
```bash
python monitor.py
```

### Option 3: Alle Services auf einmal (Windows)
```bash
start_services.bat
```

## Tools

### 📊 Monitoring
```bash
python monitor.py
```
Live-Statistiken des Systems anzeigen

### 📤 Daten exportieren
```bash
python export_data.py
```
Exportiert alle Daten als JSON und CSV

### ⚙️ Konfiguration verwalten
```bash
python config_manager.py
```
Zeigt und verwaltet die Systemkonfiguration

## Zugriff

- **Web Dashboard:** http://localhost:8000
- **API Endpoints:** http://localhost:5000/api
- **Mobile Dashboard:** http://localhost:8000/mobile_dashboard.html

## API Endpoints

- `GET /api/status` - Aktueller Status
- `GET /api/transactions` - Transaktionshistorie
- `GET /api/clones` - Clone-Informationen
- `GET /api/analytics` - Analytik-Daten
- `POST /api/cycle` - Produktionszyklus ausführen

## Dateien

- `cash_money_production.py` - Hauptsystem
- `api_server.py` - REST API
- `web_server.py` - Web Dashboard
- `config.json` - Konfiguration
- `wealth_system.db` - SQLite Datenbank
- `system.log` - System-Logdatei

## Status

Das System läuft autonom bis zum Ziel von 10.000 CHF und darüber hinaus! 🎉
