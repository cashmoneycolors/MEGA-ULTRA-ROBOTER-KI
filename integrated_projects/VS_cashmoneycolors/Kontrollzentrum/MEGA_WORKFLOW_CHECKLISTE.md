# Mega-Workflow für das Kontrollzentrum (Studio Edition)

Diese Checkliste bündelt alle wichtigen Workflows (Modul-Entwicklung, Key-Handling, Testen, API-Integration, Backup) zu einem durchgängigen, teamfähigen Prozess. Sie ist für die Nutzung im Editor/Studio optimiert.

---

## 1. Projekt initialisieren

- [ ] Repository clonen oder neuen Workspace anlegen
- [ ] Sicherstellen, dass die Ordner `modules/`, `core/`, `tests/`, `.github/` existieren
- [ ] `.env.example` kopieren und als `.env` anlegen
- [ ] Alle API-Keys gemäß `core/key_check.py` eintragen

## 2. Abhängigkeiten installieren

- [ ] `pip install -r requirements.txt` ausführen

## 3. Neues Modul entwickeln

- [ ] Neue Datei in `modules/` anlegen
- [ ] `run()`-Funktion mit `@require_keys` implementieren
- [ ] Optional: FastAPI-Endpunkte hinzufügen
- [ ] Modul registriert sich automatisch beim Import

## 4. Testen

- [ ] Neue Tests in `tests/` anlegen (z.B. `test_modulname.py`)
- [ ] `python -m unittest discover` ausführen
- [ ] Fehler beheben und Tests wiederholen

## 5. API-Integration prüfen

- [ ] FastAPI-Modul starten (z.B. `python modules/ki_sideboard.py`)
- [ ] Endpunkte mit Postman/curl testen
- [ ] Logs und Rückgaben prüfen

## 6. Backup & Restore

- [ ] Backup mit `python backup.py` oder manuell als ZIP erstellen
- [ ] Wichtige Dateien/Ordner sichern (ohne Secrets)
- [ ] Restore-Anleitung im `backup_README.md` beachten

## 7. Dokumentation aktuell halten

- [ ] Änderungen in `.github/copilot-instructions.md` und `README.md` dokumentieren
- [ ] Onboarding für neue Teammitglieder vereinfachen

---

**Tipp:**

- Nutze diese Checkliste als Vorlage für dein Team oder als README im Hauptverzeichnis.
- Für maximale Automatisierung kann ein Python-Setup-Skript oder Makefile zusätzlich erstellt werden.
