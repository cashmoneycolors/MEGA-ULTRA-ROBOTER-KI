# TODO: MEGA ULTRA ROBOTER KI - Vollständige Einrichtung und Überprüfung

## Schritt 1: Umgebung vorbereiten
- [ ] .env-Datei prüfen und korrekt setzen (OPENAI_API_KEY, andere Secrets)
- [ ] Virtuelle Umgebung aktivieren (.venv)
- [ ] Abhängigkeiten installieren (pip install -r requirements.txt)

## Schritt 2: Build und Healthcheck
- [ ] C#-Projekte bauen (dotnet build 🤖ROBOTER_KI_APP.csproj)
- [ ] PowerShell-Installer ausführen (./post_install_max.ps1)
- [ ] Healthcheck-Skripte laufen lassen (./PostInstallCheck.ps1)

## Schritt 3: Backend starten
- [ ] Docker-Container starten (docker-compose up -d)
- [ ] API-Healthcheck: curl http://localhost:8080/healthz

## Schritt 4: Frontend starten
- [ ] React-Frontend: cd ZENITH_FRONTEND && npm install && npm start
- [ ] Streamlit-App: streamlit run app.py (nach OpenAI-Fix)

## Schritt 5: OpenAI-Quota beheben
- [ ] OpenAI-Abonnement überprüfen und aufladen
- [ ] Alternativ: OpenAI-API-Key entfernen oder kostenloses Modell verwenden

## Schritt 6: Komponenten testen
- [ ] Login in Streamlit-App testen
- [ ] KI-Textanalyse testen (ohne OpenAI)
- [ ] Bilderkennung testen
- [ ] USB/Kamera testen (falls Hardware vorhanden)
- [ ] System-Check testen

## Schritt 7: Sicherheit und Dokumentation
- [ ] Secrets prüfen (kein Hardcoding)
- [ ] Dokumentation aktualisieren (README.md, PRODUKTIONSSTATUS.md)
- [ ] Git-Commit aller Änderungen

## Schritt 8: Finale Überprüfung
- [ ] Alle Komponenten laufen stabil
- [ ] Keine Fehler in Logs
- [ ] System ist "safe" für Produktion
