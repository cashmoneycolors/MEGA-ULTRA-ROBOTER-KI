# AI Converter Toolkit (Sideboard Modul)

**Funktionen:**
- Konvertiert Screenshots/Text zu Word, PDF, JPG, 3D-Modellen
- Modernes FastAPI-Backend mit statischem Frontend (React/HTML möglich)
- Einfach erweiterbar für neue Konverter

## Installation & Start

```powershell
cd PY_SIDEBOARD/ai_converter
./install_ai_converter.ps1
cd app
uvicorn main:app --reload --port 8088
```

Frontend erreichbar unter: [http://localhost:8088/](http://localhost:8088/)

## Sicherheit & Hinweise
- Keine Secrets im Code! API-Keys/Secrets immer per Umgebungsvariable (`os.environ`) setzen.
- Siehe `SECURITY_DOC_AND_TESTS.md` im Hauptprojekt für Best Practices.

## Erweiterung
- Neue Konverter als FastAPI-Endpunkte in `app/main.py` ergänzen.
- Frontend in `frontend/` anpassen.

---
*Teil des MEGA ULTRA ROBOTER KI-Ökosystems*