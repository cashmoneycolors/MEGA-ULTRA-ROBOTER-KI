# Sicherheit & Tests – PDF KI-Konverter

- Keine Secrets im Code, alle Pfade per Umgebungsvariable steuerbar.
- Testfälle:
  - [ ] Start ohne PDF: Fehler und Abbruch
  - [ ] Start mit Beispiel-PDF: Exportiert JSON und CSV
  - [ ] Export-Dateien enthalten den erwarteten Text
- Healthcheck: `[OK]`-Meldungen im Terminal
