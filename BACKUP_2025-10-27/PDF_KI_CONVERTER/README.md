# PDF KI-Konverter (MEGA ULTRA ROBOTER KI)

Dieses Modul analysiert PDF-Dateien, extrahiert den Text und exportiert ihn als JSON und CSV.

## Features
- PDF-Text-Extraktion (PyPDF2)
- Export als JSON und CSV
- Beispiel-PDF im Ordner `_EXAMPLES`

## Nutzung
1. Abhängigkeiten installieren:
   ```sh
   pip install -r requirements.txt
   ```
2. Beispiel ausführen:
   ```sh
   python main.py
   ```
   (Verwendet standardmäßig `_EXAMPLES/beispiel.pdf`)

## Secret-Handling & Sicherheit
- Keine sensiblen Daten im Code.
- Pfade und Exportnamen per Umgebungsvariable steuerbar.

## Healthcheck
- Script gibt `[OK]`-Meldungen bei erfolgreichem Export aus.

## Beispiel-Asset
- Siehe `_EXAMPLES/beispiel.pdf` für ein Dummy-PDF.
