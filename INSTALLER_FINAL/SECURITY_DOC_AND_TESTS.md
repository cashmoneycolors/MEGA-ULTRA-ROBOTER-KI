# Dokumentation & Testhinweise für Secret-Handling und produktive Nutzung

## Sicherheits-Policy (Secrets)
- Kritische Secrets (z.B. JWT_SECRET, MAINTENANCE_KEY) werden ausschließlich über Umgebungsvariablen bezogen oder sicher zur Laufzeit generiert.
- Niemals hardcodieren! Bei Generierung erscheint eine gelbe Warnung.
- In Produktion MÜSSEN die Secrets gesetzt sein.
- Produktive Nutzung: Secrets werden für Authentifizierung, Admin-Kommandos und Token-Validierung verwendet.
- Siehe copilot-instructions.md und Projektdoku für Details.

## Testhinweise
- Setze die Umgebungsvariablen JWT_SECRET und MAINTENANCE_KEY vor dem Start:
  - PowerShell: $env:JWT_SECRET="dein_geheimes_secret"; $env:MAINTENANCE_KEY="dein_admin_key"
- Starte die Anwendung und prüfe, dass keine gelbe Warnung erscheint.
- Teste Admin- und Authentifizierungsfunktionen produktiv (z.B. perform_critical_update in Python, Admin-Kommandos in C#).
- Prüfe, dass bei fehlenden Secrets eine Warnung und/oder ein Abbruch erfolgt.

## Beispiel für produktiven Admin-Check (Python)
```python
if is_admin(input("Admin-Key: ")):
    perform_critical_update(admin_key=input("Admin-Key: "))
```

## Beispiel für produktiven Token-Check (C#)
```csharp
// Im NetworkAuthManager: Token-Validierung
if (!ValidateToken(token, "admin.access"))
{
    // Zugriff verweigern
}
```

---
Letzte Aktualisierung: 13. Oktober 2025
