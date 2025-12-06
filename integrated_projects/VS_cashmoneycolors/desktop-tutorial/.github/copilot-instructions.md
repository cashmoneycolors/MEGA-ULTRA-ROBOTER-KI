
# Copilot Instructions for desktop-tutorial

## Architektur & Komponenten
- **Python-Teil (AethelosGAZI/):**
  - `main.py`: Einstiegspunkt für Systemüberwachung & Optimierung (Echo, Oracle, GAZI).
  - `api/rest.py`: FastAPI-REST-API, zentrale Schnittstelle für Status & Optimierung.
  - `webapp/app.py`: Flask-Web-Frontend, spricht REST-API & C#-API an, bietet Monitoring, Payment, Dateiverwaltung.
  - `core/`, `agents/`, `meta/`: Kernlogik (Status, Vorhersage, Optimierung).
- **C#-Teil (zenith/ & zenithapi/):**
  - `ZenithControllerBlueprint.cs`: Self-Correcting System Core (RAM-Überwachung, Schwellenwertanpassung).
  - `zenithapi/`: ASP.NET Core REST-API, bietet Status, Dateiverwaltung, Schwellenwert-API.
- **Integration:**
  - Web-Frontend und Python-API kommunizieren mit C#-API über HTTP (localhost:5000).
  - Lokale Dateiverwaltung über `/local/*`-Routen in Python & C#.

## Entwickler-Workflows
- **Starten (empfohlen):**
  - `start_all.bat` ausführen: Startet Python-REST-API und Web-Frontend nacheinander.
  - C#-API separat in Visual Studio starten (`AethelosGAZI/zenithapi/`).
- **Tests & Debugging:**
  - Python: Direktes Ausführen von `main.py` oder REST-API.
  - C#: Demo in `ZenithControllerBlueprintDemo.cs` oder REST-API-Endpoints testen.
- **Konfiguration:**
  - Kritische Konstanten (z.B. Preise, Links, Schwellenwerte) sind am Anfang der Skripte als Listen/Konstanten gepflegt.
  - Zeitzonen & Zeitberechnung sind zentral (`pytz`, `datetime`).

## Projektkonventionen & Besonderheiten
- Variablennamen, Kommentare & Struktur sind teils deutsch, philosophisch/metaphorisch.
- Systemlogik folgt: Audit → Launch/Steuerung → Optimierung.
- REST-API ist zentrale Integrationsschnittstelle (für Web, C#, Automatisierung).
- Payment-Integration (PayPal/Twint) ist vorbereitet, aber noch nicht produktiv.
- Synchronisiere Werte/Links, die mehrfach gepflegt werden (Preise, Links, Schwellenwerte).

## Beispiele & Einstieg
- Python: `AethelosGAZI/main.py`, `AethelosGAZI/api/rest.py`, `AethelosGAZI/webapp/app.py`
- C#: `AethelosGAZI/zenith/ZenithControllerBlueprint.cs`, `AethelosGAZI/zenithapi/ZenithApiController.cs`
- Web: `AethelosGAZI/webapp/templates/index.html`

---
Letzte Aktualisierung: 2025-10-07
