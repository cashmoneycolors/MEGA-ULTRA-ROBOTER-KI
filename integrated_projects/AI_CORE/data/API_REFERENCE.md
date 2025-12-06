# API Reference - Autonomous Wealth System

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Dashboard
```
GET /
```
Zeigt das Web-Dashboard an.

**Response:** HTML Dashboard

---

### 2. System Status
```
GET /api/status
```
Gibt den aktuellen Status des Systems zurück.

**Response:**
```json
{
  "capital": 150.50,
  "target": 10000,
  "progress": 1.5,
  "cycles": 42,
  "art_assets": 18,
  "trades": 84,
  "art_profit": 245.30,
  "active_clones": 2,
  "running": true
}
```

**Parameter:**
- `capital` (float) - Aktuelles Kapital in CHF
- `target` (int) - Zielkapital in CHF
- `progress` (float) - Fortschritt in %
- `cycles` (int) - Anzahl durchgeführter Zyklen
- `art_assets` (int) - Anzahl erstellter KI-Kunstwerke
- `trades` (int) - Anzahl durchgeführter Trades
- `art_profit` (float) - Gesamtgewinn aus Kunstverkäufen
- `active_clones` (int) - Anzahl aktiver Klone
- `running` (bool) - System läuft oder nicht

---

### 3. System starten
```
POST /api/start
```
Startet den autonomen Betrieb des Systems.

**Response:**
```json
{
  "message": "System started",
  "status": "running"
}
```

---

### 4. System stoppen
```
POST /api/stop
```
Stoppt den autonomen Betrieb des Systems.

**Response:**
```json
{
  "message": "System stopped",
  "status": "stopped"
}
```

---

## Datenbank-Schema

### transactions
```sql
CREATE TABLE transactions (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  type TEXT,
  amount REAL,
  balance REAL
)
```

### art_portfolio
```sql
CREATE TABLE art_portfolio (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  cost REAL,
  selling_price REAL,
  profit REAL
)
```

### trading_log
```sql
CREATE TABLE trading_log (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  asset TEXT,
  action TEXT,
  amount REAL,
  price REAL,
  profit REAL
)
```

### clones
```sql
CREATE TABLE clones (
  id INTEGER PRIMARY KEY,
  created_at TEXT,
  status TEXT,
  profit_contribution REAL
)
```

### paypal_transactions
```sql
CREATE TABLE paypal_transactions (
  id INTEGER PRIMARY KEY,
  transaction_id TEXT,
  timestamp TEXT,
  amount REAL,
  status TEXT,
  service TEXT
)
```

---

## Konfiguration

### config.json Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|-------------|
| initial_capital | int | 100 | Startkapital in CHF |
| target_capital | int | 10000 | Zielkapital in CHF |
| cycle_interval | int | 2 | Sekunden zwischen Zyklen |
| art_allocation | float | 0.40 | 40% für KI-Kunst |
| trading_allocation | float | 0.35 | 35% für Trading |
| vector_allocation | float | 0.25 | 25% für Vector Services |
| art_production_cost | float | 8.50 | Produktionskosten pro Kunstwerk |
| art_min_price | int | 45 | Mindestverkaufspreis |
| art_max_price | int | 199 | Maximalverkaufspreis |
| vector_service_cost | float | 35 | Kosten pro Service |
| vector_service_price | float | 85 | Verkaufspreis pro Service |
| clone_creation_cost | float | 85 | Kosten zur Klon-Erstellung |
| max_clones | int | 25 | Maximale Anzahl Klone |
| clone_profit_multiplier | float | 0.03 | 3% Gewinn pro Klon |
| max_clone_multiplier | float | 2.0 | Max. 2x Gewinn-Multiplikator |
| max_trading_risk | float | 0.70 | 70% Risiko beim Trading |

---

## PayPal Integration

### Konfiguration

```json
"paypal": {
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "sandbox_mode": true,
  "currency": "USD"
}
```

### Schritte zur Aktivierung

1. Gehe zu https://developer.paypal.com
2. Melde dich an oder erstelle ein Konto
3. Erstelle eine neue App
4. Kopiere `Client ID` und `Secret`
5. Füge sie in `config.json` ein
6. Setze `enable_payments` auf `true`

---

## Fehlerbehandlung

Das System protokolliert alle Fehler in `system.log`:

```
[2024-01-15 10:30:45] ERROR in cycle: Division by zero
[2024-01-15 10:30:46] ERROR recovered: Cycle resumed
```

Bei 5 aufeinanderfolgenden Fehlern pausiert das System automatisch.

---

## Performance

- **Cycle Time:** ~2 Sekunden (konfigurierbar)
- **Database:** SQLite (lokal)
- **Memory:** ~50-100 MB
- **CPU:** Minimal (< 5%)

---

## Sicherheit

- Keine API-Keys in Logs
- Lokale Datenbank (keine Cloud)
- Verschlüsselte PayPal-Kommunikation
- Error Recovery automatisch

---

## Support

Bei Fragen:
1. Überprüfe `system.log`
2. Stelle sicher, dass alle Dependencies installiert sind
3. Überprüfe die Konfiguration in `config.json`
