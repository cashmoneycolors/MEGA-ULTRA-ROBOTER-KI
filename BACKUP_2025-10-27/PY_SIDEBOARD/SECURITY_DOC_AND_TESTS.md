# Sicherheitshinweise & Test-Checkliste für Double Gazi AI Ultimate (Sideboard)

## Sicherheitshinweise
- Dieses Tool läuft unabhängig von der Hauptanwendung und verarbeitet keine sensiblen Nutzerdaten aus dem Hauptsystem.
- KI-Modelle werden lokal geladen, keine API-Keys werden im Code hardcodiert.
- Falls Cloud-Modelle genutzt werden, müssen API-Keys ausschließlich über Umgebungsvariablen oder eine `.env`-Datei bereitgestellt werden (siehe `.env.example`).
- Niemals geheime Schlüssel oder Zugangsdaten im Quellcode speichern!

## Test-Checkliste
- [ ] Startet die App ohne Fehler? (`python double_gazi_ai_ultimate.py`)
- [ ] Funktioniert die Layer-Verwaltung (Hinzufügen, Löschen, Undo/Redo)?
- [ ] Kann ein KI-Logo generiert werden (sofern Modell geladen)?
- [ ] Funktioniert das Inpainting?
- [ ] Werden keine sensiblen Daten im Code oder in Logs ausgegeben?
- [ ] Ist die README aktuell und verständlich?
