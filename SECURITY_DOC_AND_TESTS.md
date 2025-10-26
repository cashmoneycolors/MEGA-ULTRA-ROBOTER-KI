# Sicherheit & Test-Dokumentation – MEGA ULTRA ROBOTER KI

## Best Practices
- Niemals Secrets/API-Keys im Code speichern!
- Nutzung von Umgebungsvariablen (z.B. `Environment.GetEnvironmentVariable` in C#, `os.environ` in Python) für alle sensiblen Daten.
- Bei fehlenden Secrets: Warnung im Log und Start im Demo-Modus.
- Siehe SecretHelper (C#) und Beispiele in allen Entry-Points.

## Testfälle
- [ ] Start ohne .env: Warnung und Demo-Modus
- [ ] Start mit .env: Secrets werden korrekt geladen
- [ ] API-Endpunkte funktionieren ohne Fehler
- [ ] Sideboards (z.B. Double Gazi, AI Converter) starten unabhängig
- [ ] Frontends (z.B. ZENITH) sind erreichbar

## Entwicklerhinweis
- Erweiterungen immer mit Secret-Handling und Logging versehen.
- Siehe `README.md` und PRODUKTIONSSTATUS.md für Integrationsmuster.
