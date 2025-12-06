# Kontrollzentrum – Plug-and-Play-Module

Dieses Kontrollzentrum unterstützt Plug-and-Play-Module, zentrale Key-Prüfung und dynamisches Laden aller Kernfunktionen.

## Produktive Module (Beispiele)

| Modul                  | Zweck/Feature                                 |
|------------------------|-----------------------------------------------|
| beispiel_modul.py      | Generisches Testmodul mit run()               |
| wetter_modul.py        | Holt Wetterdaten von Open-Meteo               |
| ki_integration_modul.py| Platzhalter für KI-Integration                |
| dashboard_modul.py     | Visualisiert Ergebnisse aller Module (Streamlit) |
| data_import.py         | Importiert und verarbeitet Daten (pandas)     |
| nft_modul.py           | NFT-Management und -Import                    |
| dropshipping_modul.py  | Dropshipping-Logik                            |
| ki_modul.py            | KI-Produktivmodul (z.B. Textgenerierung)      |
| grafik_design_modul.py | Grafik- und Designfunktionen                  |

## Plug-and-Play-Prinzip
- Jedes Modul liegt im Verzeichnis `modules/` und besitzt eine `run()`-Funktion.
- Die zentrale Key-Prüfung erfolgt über `require_keys` aus `core/key_check.py`.
- Das Kontrollzentrum (`main.py`) lädt und startet alle Module automatisch.

## Testen
- Für jedes neue Modul gibt es Unittests im Verzeichnis `tests/`.
- Beispiel: `python -m unittest tests/test_new_modules.py`

## Erweiterung
- Neue Module einfach in `modules/` ablegen und nach dem Muster mit `run()` und Key-Prüfung gestalten.
- Das Dashboard-Modul visualisiert die Ergebnisse aller Module.

---

*Letzte Aktualisierung: 13.10.2025*

# Kontrollzentrum / CCashMoneyIDE


## Produktiver Betrieb – Wichtige Hinweise

**Diese Anwendung funktioniert ausschließlich im produktiven Modus. Ohne echte API-Keys und eine vollständige, produktive Konfiguration startet die App nicht!**


### Voraussetzungen
- Alle erforderlichen API-Keys müssen in der `.env`-Datei im Projektverzeichnis hinterlegt werden.
- Die Liste der benötigten Keys findest du in `core/key_check.py` unter `REQUIRED_KEYS`.
- Beispiel für eine `.env`-Datei:

```
STRIPE_API_KEY=dein_stripe_key
PAYPAL_API_KEY=dein_paypal_key
NFT_API_KEY=dein_nft_key
# ...weitere Keys gemäß REQUIRED_KEYS...
```


### Fehlende Keys
- Beim Start prüft die App automatisch, ob alle erforderlichen Keys vorhanden sind.
- Fehlen Keys, wird die App mit einer klaren Fehlermeldung beendet. Die Meldung zeigt exakt, welche Keys fehlen und wie sie nachzutragen sind.


### Keys nachtragen
1. Öffne die Datei `.env` im Projektverzeichnis (falls nicht vorhanden, erstelle sie).
2. Trage alle fehlenden Keys im Format `KEY=wert` ein.
3. Starte die App neu.


### Sicherheitshinweis
- Gib deine API-Keys niemals weiter und lade sie nicht in öffentliche Repositories hoch!

---


## Best Practices & Security

- `.env`-Datei und API-Keys **niemals** ins Repository einchecken!
- API-Keys und Secrets **nur** in `.env` pflegen.
- Nutze immer die zentrale Key-Prüfung (`require_keys` oder `check_all_keys()`), um versehentliche API-Aufrufe ohne Key zu verhindern.
- Unittests für jedes neue Modul anlegen und regelmäßig ausführen.
- Logs und Fehlermeldungen beachten – sie helfen beim Troubleshooting.
- Siehe auch `.github/copilot-instructions.md` für Details.

---

## Support & Erweiterung

Bei neuen Modulen oder Erweiterungen kannst du die Key-Prüfung ganz einfach nutzen:

- Entweder `check_all_keys()` direkt aufrufen (z.B. im Konstruktor oder vor API-Aufrufen)
- Oder den Decorator `@require_keys` aus `core/key_check.py` für Funktionen verwenden, die produktive Keys benötigen:

```python
from core.key_check import require_keys

@require_keys
def produktive_funktion(...):
	pass
```

Hinweise zur Erweiterung findest du in `core/key_check.py`.

---


## Studio-Workflow-Übersicht (Quick Reference)


**Projekt starten:**
1. `.env` prüfen/erstellen
2. `python main.py`

**Unittests ausführen:**
1. `cd Kontrollzentrum`
2. `python -m unittest tests/test_new_modules.py`

**Neues Modul anlegen:**
1. Neue Datei in `modules/`
2. `run()`-Funktion mit `@require_keys`
3. Optional: API-Endpoints mit FastAPI
4. Modul registriert sich automatisch beim Import

**API-Keys prüfen:**
1. `.env` öffnen
2. Alle Keys gemäß `core/key_check.py` eintragen

**Fehlende Keys beheben:**
1. Fehlermeldung beim Start beachten
2. Fehlende Keys in `.env` ergänzen
3. App neu starten

**FastAPI-Modul testen:**
1. Modul starten (z.B. `python modules/ki_sideboard.py`)
2. API mit Tool wie Postman testen

**Abhängigkeiten installieren:**
1. `pip install -r requirements.txt`

**Troubleshooting:**
1. Fehlermeldungen lesen
2. `.env` und API-Keys prüfen
3. Abhängigkeiten prüfen
4. Logs beachten

**Beispiel für ein neues Modul:**

```python
from core.key_check import require_keys
@require_keys
def run():
	print("Modul läuft!")
```

---

**Ohne echte Keys läuft hier nichts!**
