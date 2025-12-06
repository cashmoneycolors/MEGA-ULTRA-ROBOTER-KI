
# Copilot-Instructions für Kontrollzentrum / CCashMoneyIDE

## Architekturüberblick
- **Plug-and-Play-Modularchitektur:** Jedes Modul liegt in `modules/` und besitzt eine `run()`-Funktion. Module werden automatisch registriert und geladen.
- **Zentrale Key-Prüfung:** Über `core/key_check.py` und den Decorator `require_keys` wird beim Start und vor kritischen Funktionen geprüft, ob alle API-Keys in der `.env`-Datei vorhanden sind. Fehlen Keys, startet die App nicht und gibt eine klare Fehlermeldung aus.
- **Modul-Registry:** Module registrieren sich selbstständig in `modules/module_registry.json` via `register_module()` aus `modules/module_registry.py`.
- **FastAPI-Integration:** KI-Module wie `ki_sideboard.py` bieten HTTP-APIs (z.B. `/openai_vision`, `/mathpix`) und nutzen externe KI-Dienste. Die API-Keys werden aus der `.env` geladen.

## Wichtige Workflows
- **Starten:**
  - Stelle sicher, dass alle Keys in `.env` gesetzt sind (siehe `REQUIRED_KEYS` in `core/key_check.py`).
  - Starte das Kontrollzentrum über `main.py` (z.B. `python main.py`).
- **Testen:**
  - Unittests liegen in `tests/`. Beispiel: `python -m unittest tests/test_new_modules.py`
- **Neue Module:**
  - Lege neue Module in `modules/` an, implementiere eine `run()`-Funktion und dekoriere sie mit `@require_keys`.
  - Beispiel: Siehe `modules/beispiel_modul.py`.
- **API-Keys:**
  - `.env`-Datei im Projektverzeichnis pflegen. Fehlende Keys führen zu Abbruch mit Fehlermeldung.

## Konventionen & Besonderheiten
- **Keine Ausführung ohne vollständige Konfiguration:** Die App läuft nur mit allen erforderlichen Keys.
- **Modulregistrierung:** Jedes Modul ruft beim Start `register_module()` auf.
- **Externe Abhängigkeiten:**
  - FastAPI, requests, dotenv, uvicorn
  - KI-Module nutzen OpenAI, Mathpix etc. – API-Keys sind Pflicht.
- **Beispiel für API-Key-Prüfung:**
  ```python
  from core.key_check import require_keys
  @require_keys
  def run():
      ...
  ```
- **Fehlende Keys:**
  - Klare Fehlermeldung mit Liste der fehlenden Keys und Abbruch.
- **Secrets:** Niemals echte API-Keys oder Secrets im Code oder in Logs speichern. Immer `.env` nutzen.

## Wichtige Dateien
- `core/key_check.py`: Zentrale Key-Prüfung und Decorator
- `modules/module_registry.py`: Modulregistrierung
- `modules/ki_sideboard.py`: Beispiel für FastAPI-Modul mit KI-Integration
- `.env`: API-Keys
- `README.md`: Projektüberblick und Hinweise

---
*Letzte Aktualisierung: 13.10.2025*
- **System-Recovery:**
  - Über Sidebar-Button "System Recovery auslösen" (`self.recover()`).
- **API-Integration:**
  - API-Keys immer aus `.env` laden, z.B.:
    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("API_KEY_NAME", "")
    ```
- **Verschlüsselte API-Keys:**
  - Beispiel für Nutzung:
    ```python
    from modules.apikey_manager import load_api_key
    key = load_api_key("stripe")
    ```
- **Optionale Abhängigkeiten:**
  - Siehe Docstrings der Module für Integrationsdetails und erforderliche Pakete.

---

**Für KI-Agents:**
- Immer das Modul-Prinzip für neue Features nutzen (siehe Beispiele).
- Controller-Methoden für Systemaktionen (Audit, Recovery, Policy Enforcement) verwenden.
- Modul-Docstrings für Integrationsdetails und Abhängigkeiten beachten (z.B. Demo/Produktiv-Modi, optionale Pakete, API-Keys).
- Keine Zugangsdaten oder Secrets hardcoden – immer `.env` nutzen.
- Bei neuen Modulen: Funktionssignatur und Datenübergabe beachten, Registrierung im Sidebar-Menü nicht vergessen.
