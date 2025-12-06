# Demo: Alle Kernfunktionen des Systems

## 1. Live-Systemstatus anzeigen (Python)

import requests
print('Systemstatus:', requests.get('http://127.0.0.1:8081/status').json())

## 2. Self-Healing/Optimierung triggern (Python)
print('Optimierung:', requests.post('http://127.0.0.1:8081/optimize').json())

## 3. Datei anlegen, lesen, anzeigen (Python)
# Datei schreiben
r = requests.post('http://127.0.0.1:3000/local/write', json={"filename": "demo.txt", "content": "Hallo Welt!"})
print('Datei schreiben:', r.json())
# Datei lesen
r = requests.post('http://127.0.0.1:3000/local/read', json={"filename": "demo.txt"})
print('Datei lesen:', r.json())
# Dateien anzeigen
r = requests.get('http://127.0.0.1:3000/local/list')
print('Dateien:', r.json())

## 4. Payment-Test-Request (PayPal)
r = requests.post('http://127.0.0.1:3000/pay/paypal', json={"amount": 10})
print('PayPal-Test:', r.json())

## 5. REST-API mit eigenem Client (Python)
# (siehe oben, Status und Optimierung)

# Hinweis: Web-Frontend zeigt Status und Dateioperationen automatisch an.
# Starte vorher das System mit start_all.bat und die C#-API in Visual Studio.
