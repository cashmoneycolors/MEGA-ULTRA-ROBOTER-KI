# Sicherheit & Test-Dokumentation – AI Converter Toolkit

## Best Practices
- Niemals Secrets/API-Keys im Code speichern!
- Nutzung von Umgebungsvariablen (`os.environ`) für alle sensiblen Daten.
- Bei fehlenden Secrets: Warnung im Log und Start im Demo-Modus.
- Siehe Hauptprojekt für zentrale Secret-Helper und Muster.

## Testfälle
- [ ] Start ohne .env: Warnung und Demo-Modus
- [ ] Start mit .env: Secrets werden korrekt geladen
- [ ] API-Endpunkte funktionieren ohne Fehler
- [ ] Frontend wird als StaticFile ausgeliefert

## Entwicklerhinweis
- Erweiterungen immer mit Secret-Handling und Logging versehen.
- Siehe `README.md` und Hauptprojekt für Integrationsmuster.
