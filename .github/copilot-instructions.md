# Copilot Instructions

> Alle Pfade in dieser Datei sind relativ zum Repo-Root (C:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1). Ziel: mehrere KI-Agenten finden dieselben Einstiegspunkte zuverlässig.

## Repo-Überblick
- Windows-first .NET 8 Desktop/Console-App: 🤖ROBOTER_KI_APP.exe wird aus 🤖ROBOTER_KI_APP.csproj gebaut; Einstiegspunkt ist `RoboterKIMaxUltraApp.Main` in 🤖ROBOTER_KI_APP.cs.
- Kernmodule in C#: QuantumCore.cs, QuantumModules.cs, AutonomousExpander.cs, UnifiedProjectIntegration.cs.
- Python-Teil: `integration_hub.py` als "UniversalIntegrationHub" (scannt `integrated_projects/` und lädt Module aus `modules/`).
- Zusätzlich: `main.py` (FastAPI API-Key-Auth + OpenAI-Integration) und `app.py` (Streamlit-Dashboard).

## Schnellstart-Pfade (1/2/3)
1) EXE (Windows): `./🤖ROBOTER_KI_APP.exe`
2) GUI (Streamlit): `streamlit run app.py`
3) API (FastAPI): `uvicorn main:app --reload` (vorher `API_KEY` und `APP_ID` setzen, sonst crasht `main.py` beim Import)

## Build / Run (Real-World Workflows)
- .NET Build (empfohlen bei Emoji-Dateinamen): `./build_test.ps1` (auto-find *.csproj, Logs: build_*.log)
- .NET manuell: `dotnet build "🤖ROBOTER_KI_APP.csproj" -c Release`; Publish: `dotnet publish "🤖ROBOTER_KI_APP.csproj" -c Release -r win-x64 --self-contained`
- Python deps: `python -m pip install -r requirements.txt` (Repo nutzt `.venv/`)
- Integration Hub: `python integration_hub.py`

## Projekt-Konventionen / Fallstricke
- Die C#-Compilation schließt `BACKUP_*` und `AI_CORE/` aus (siehe 🤖ROBOTER_KI_APP.csproj). Änderungen dort beeinflussen den Build nicht.
- Viele Artefakte/Backups liegen im Repo (`bin/`, `obj/`, `logs/`, `BACKUP_*`): Änderungen dort nur, wenn explizit nötig.
- Secrets: verwende `.env`/`.env.example`; Dateien wie `API_KEY=abcdef12345.txt` nicht als echte Secrets behandeln/committen.

## SpeechRecognition Whisper-API Wrapper (wenn du daran arbeitest)
- Dieser Wrapper-Code liegt typischerweise im installierten Python-Paket (z.B. unter `.venv/Lib/site-packages/speech_recognition/recognizers/whisper_api/`) und ist nicht zwingend Teil des Repos.
- Konvention: `BytesIO.name` muss `SpeechRecognition_audio.wav` sein und Rückgabewert ist immer `transcript.text`.
- Provider-Module (OpenAI/Groq) sollen dünn bleiben und bei fehlendem SDK `SetupError` werfen.
