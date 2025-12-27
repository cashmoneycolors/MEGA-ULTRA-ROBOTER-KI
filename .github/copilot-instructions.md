# MEGA ULTRA ROBOTER KI – Copilot Kurzleitfaden

## Big Picture
- Hybrid-Architektur: .NET/C# Haupt-App + Python FastAPI-Services + optionales Node/React Frontend.
- Zentrale Entry Points: [🤖ROBOTER_KI_APP.cs](🤖ROBOTER_KI_APP.cs), [main.py](main.py), [modules/ki_sideboard.py](modules/ki_sideboard.py), [core/key_check.py](core/key_check.py).
- Zweck: C# orchestriert Dienste (LLMs, Zahlungen, Cloud). Python stellt APIs/KI-Module bereit; strikte Key-Policy schützt produktive Endpunkte.

## Service-Grenzen & Flüsse
- C# startet/überwacht: Node (3000), Ollama (11434), FastAPI-Boards (8000/8003). Siehe [RoboterKIUltraController.cs](RoboterKIUltraController.cs).
- Python FastAPI (Header-Auth `X-API-KEY`/`X-APP-ID`): [main.py](main.py) mit `/openai/*`; Sideboard: [modules/ki_sideboard.py](modules/ki_sideboard.py) mit `/modules`, `/module/run`.
- Key-Gate: [core/key_check.py](core/key_check.py) mit `REQUIRED_KEYS`, `check_all_keys()`, `@require_keys`. Bei fehlenden Keys: sofort fehlschlagen.

## Workflows (VS Code Tasks + Commands)
- App starten: Task „Starte 🤖ROBOTER_KI_APP.csproj“ oder
	```powershell
	dotnet run --project 🤖ROBOTER_KI_APP.csproj
	```
- Python API: Env setzen, dann
	```powershell
	$env:API_KEY="..."; $env:APP_ID="..."; $env:OPENAI_API_KEY="..."
	uvicorn main:app --host 0.0.0.0 --port 8000
	```
- Sideboard: benötigt alle Keys
	```powershell
	uvicorn modules.ki_sideboard:app --host 0.0.0.0 --port 8003
	```
- Build/Publish:
	```powershell
	dotnet build -c Release
	dotnet publish -c Release -r win-x64 --self-contained
	```
 - PayPal Webhooks & Dashboard:
	 - VS Code Tasks: „MEGA: Run Webhook Server (8503)“, „MEGA: Run Streamlit Dashboard (8502)“
	 ```powershell
	 python webhook_server.py
	 python -m streamlit run dashboard_ui.py --server.port 8502
	 ```

## Projektkonventionen
- Code nicht in Backups/`integrated_projects/` ändern; arbeite in Top-Level-Dateien.
- Secrets nie committen; nutze `.env.example` und lade via `dotenv`/Environment.
- Python-Module exponieren `run()/install()/describe()`; produktive Funktionen sind mit `@require_keys` geschützt.
- Naming: Emoji-Prefix (🤖/⚡), PascalCase in C#, snake_case in Python.

## Schnittstellen & Integrationen
- AI-Core: [AI_CORE/](AI_CORE) inkl. [MegaUltraAIIntegrator.csproj](AI_CORE/MegaUltraAIIntegrator.csproj) für Orchestrierung.
- OpenAI: über [main.py](main.py) (`/openai/status`, `/openai/generate`). Ollama lokal (11434).
- Payments/Cloud: Stripe/AWS/Azure via C# Module (siehe [QuantumCore.cs](QuantumCore.cs), [QuantumModules.cs](QuantumModules.cs)).
- PayPal Webhook/Dashboard (falls benötigt): Webhook → JSONL → `/stats` → Streamlit; siehe [README.md](README.md).
 - Weitere Module/Tools: [webhook_server.py](webhook_server.py) (Webhook-Endpunkte), [dashboard_ui.py](dashboard_ui.py) (Streamlit Dashboard), [robot_ki_dashboard.py](robot_ki_dashboard.py) (Dashboard-Orchestrierung), [integration_hub.py](integration_hub.py) (Projektbrücke).

## Sicherheit
- Kritische Keys (u. a. `OPENAI_API_KEY`, `STRIPE_API_KEY`, `PAYPAL_CLIENT_ID/SECRET/WEBHOOK_ID`, `AWS_*`, `SMTP_*`).
- Endpoint `/set-openai-key` (in [main.py](main.py)) schreibt `.env`: nur mit Validierung/Audit nutzen; keine Keys in Logs.

## Debug & Health
- Ports prüfen: 3000 (Node), 11434 (Ollama), 8000/8003 (FastAPI), 8502 (Streamlit), 8503 (Webhook).
- Health: `Invoke-WebRequest http://localhost:8000/health` bzw. `http://localhost:8003/health`.
- Häufige Probleme: belegte Ports, fehlendes `.env` (`JWT_SECRET` generieren), Ollama nicht gestartet.

## Do/Don't für Agents
- DO: Änderungen klein halten, Entry-Points stabil, Key-Policy respektieren.
- DO: Bei API-Änderungen Clients/Sideboards im selben PR mitziehen.
- DON'T: Backups/Snapshots ändern; keine Secrets in Code/Tests/Logs.

—
Letzte Aktualisierung: 24. Dezember 2025 · .NET 8 / Python 3.13
