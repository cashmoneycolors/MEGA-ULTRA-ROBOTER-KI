# MEGA ULTRA ROBOTER KI - Copilot Instructions

## Architektur-Übersicht
Hybrides C#/.NET + Python System mit Sideboards (FastAPI) und optionalem Frontend. Das Repo enthält sowohl Produktiv-Artefakte (Executable) als auch Dev-/Integrationscode.

**Core-Komponenten (wichtigste Entry-Points/Orte):**
- `🤖ROBOTER_KI_APP.cs`: C# Haupt-App (Windows), startet/überwacht u. a. Node-Server und Sideboards
- `main.py`: FastAPI API mit Header-Auth (API_KEY/APP_ID) und OpenAI-Integration
- `modules/ki_sideboard.py`: FastAPI „Sideboard“ zur Modulsteuerung + KI-Endpunkte (nutzt strikte Key-Policy)
- `core/key_check.py`: zentrale Key-Policy (`REQUIRED_KEYS`, `check_all_keys()`, `@require_keys`)
- `mega_roboter_ki.py`: Python Automation/Orchestrierung (Wizard/Batch-Workflows)
- `integration_hub.py`: Bridge/Hub für integrierte Projekte
- `AI_CORE/`: .NET/C# AI-Integrationen
- `ZENITH_FRONTEND/`: optionales Frontend (Node/React)

**Projektbeziehung:**
- `c:\Users\nazmi\-MEGA-ULTRA-ROBOTER-KI\` - Original Source Repository
- `c:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1\` - **DIESES PROJEKT** - Production Build mit Executable

## Architektur-Pattern (Hybrid C#/Python)

**C# Layer (Hauptsystem):**
```csharp
// 🤖ROBOTER_KI_APP.cs - Entry Point
RoboterKIMaxUltraApp.Main()
├── QuantumCore: IQuantumModule Interface
│   ├── QuantumAIModule (OpenAI, Ollama)
│   ├── QuantumPaymentModule (Stripe)
│   └── QuantumCloudModule (AWS, Azure)
├── AutonomousExpander: Self-Optimization
├── UnifiedProjectIntegration: Cross-Project Orchestration
└── RoboterKIUltraController: Runtime Management
```

**Python Layer (Services):**
```python
# main.py - FastAPI API (Header Auth)
app = FastAPI()
├── Header Auth via `X-API-KEY` + `X-APP-ID` (API_KEY, APP_ID)
├── /health - Health Check
├── /something - Beispiel-Endpoint (auth required)
├── /openai/status, /openai/generate - OpenAI Integration (auth required)
└── /set-openai-key - Admin-Endpoint (schreibt in `.env`, sicherheitskritisch)

# modules/ki_sideboard.py - Sideboard API (Modulsteuerung)
app = FastAPI()
├── /modules - Discovery + Capabilities
├── /module/run - führt module.<action>() aus (strikte Key-Prüfung)
├── /openai_chat, /openai_vision - delegiert an modules.openai_integration
└── /status - Team-Log Snapshot

# core/key_check.py - Zero-Tolerance Key Gate
check_all_keys()  # wirft RuntimeError, wenn REQUIRED_KEYS fehlen
@require_keys     # Decorator für produktive Funktionen

# integration_hub.py - Project Bridge
├── ZenithCoreSystem
├── Kontrollturm
├── MegaUltraNetwork
└── AI_CORE Integration
```

## Repo-Hygiene (für Agents)
- **Nicht in `BACKUP_*/` oder `integrated_projects/` entwickeln.** Diese Ordner sind Snapshots/Backups. Änderungen gehören in die „Top-Level“-Implementierungen.
- **Secrets niemals committen oder hardcoden.** Keine Schlüssel in Code, Logs oder Beispiel-Dateien schreiben.
- Wenn du Konfig/Secrets brauchst: nutze `.env.example` als Vorlage und lies Werte via `dotenv`/Environment.
- Vor jedem PR/Push: sicherstellen, dass **keine** `.env`- oder sonstigen Secret-Dateien in `git status` auftauchen.

## Key-Policy (kritisch)
Die produktiven Python-Module/Sideboards nutzen `core/key_check.py`.

`REQUIRED_KEYS` (müssen gesetzt sein, sonst Abbruch):
- `OPENAI_API_KEY`, `STRIPE_API_KEY`
- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`
- `EBAY_APP_ID`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- `NFT_API_KEY`
- `SMTP_USER`, `SMTP_PASSWORD`

Regel: Bei fehlenden Keys **sofort fehlschlagen** (RuntimeError/HTTP 500) statt „Demo-Modus“, Fallbacks oder Platzhalter.

## Entwickler-Workflows

**Build & Run (3 Modi):**

**1. Executable (Production):**
```powershell
# Direkt starten (kein Build nötig)
.\🤖ROBOTER_KI_APP.exe

# Automatisch startet:
# - Node.js Server (Port 3000)
# - Ollama Integration (Port 11434)
# - Python Sideboards (falls vorhanden)
```

**2. C# Development:**
```powershell
# Build .NET Projekt
dotnet build -c Release

# Publish standalone
dotnet publish -c Release -r win-x64 --self-contained

# Run direkt
dotnet run --project 🤖ROBOTER_KI_APP.csproj
```

**3. Python API Server:**
```powershell
# Environment setup
$env:API_KEY = "your-api-key"
$env:APP_ID = "your-app-id"
$env:OPENAI_API_KEY = "sk-..."

# Start FastAPI Server
python main.py
# oder
uvicorn main:app --host 0.0.0.0 --port 8000
```

**4. Sideboard API (Modulsteuerung):**
```powershell
# Strikte Key-Policy: benötigt alle REQUIRED_KEYS aus core/key_check.py
uvicorn modules.ki_sideboard:app --host 0.0.0.0 --port 8003
```

**Ports (üblich):**
- Node Server: `3000`
- Ollama: `11434`
- FastAPI `main.py`: `8000`
- FastAPI Sideboard: `8003`

**VS Code Tasks (verfügbar):**
- `Starte 🤖ROBOTER_KI_APP.exe`: Dotnet Run (🤖ROBOTER_KI_APP.cs)
- `Starte 🤖ROBOTER_KI_APP.csproj`: Dotnet Run (csproj)
- `Build MegaUltraAIIntegrator`: AI_CORE Build

## Konventionen & Patterns

**C# Patterns:**
- **Interface-Driven Modules**: `IQuantumModule` für alle Quantum-Services
- **Auto-Restart Logic**: Max 5 Restarts bei Port-Konflikten
- **JWT Token Rotation**: Alle 90 Tage (PBKDF2, 600k Iterations)
- **Single-Instance Enforcement**: Mutex-basiert
- **Config Persistence**: `roboter_ki_ultra_config.json`

**Python Patterns:**
- **Environment-First Config**: `.env` für alle Secrets (nie hardcoden!)
- **FastAPI CORS**: Allow-All (Production: restrict!)
- **Pydantic Models**: Type-Safe Request/Response
- **Logging**: Standard `logging` Module (INFO Level)

**Module Pattern (`modules/*.py`):**
- Exponiere, wo sinnvoll: `run()`, `install()`, `describe()`, optional `to_svg()`/`to_word()`
- Für produktive Ausführung: `@require_keys` (oder explizit `check_all_keys()` am Anfang)
- Module sollen import-sicher sein: keine Side-Effects beim Import (keine Netzwerk-Calls beim Import)

**Security Requirements:**
```env
# .env (REQUIRED)
JWT_SECRET=<guid-generiert>
ADMIN_PASSWORD_HASH=<pbkdf2-hash>
API_KEY=<service-key>
APP_ID=<app-identifier>
OPENAI_API_KEY=<optional-openai>
```

Hinweis: `main.py` aktualisiert aktuell `.env` über einen Endpoint (`/set-openai-key`). Wenn du daran arbeitest, behandle das als **sicherheitskritisch** (Validierung, Dateirechte, Audit-Logging, keine Key-Leaks in Logs).

**Naming Convention:**
- Emoji-Prefixes: 🤖 für Roboter/AI, ⚡ für Quantum
- PascalCase: C# Classes (`QuantumCore`, `AutonomousExpander`)
- snake_case: Python Modules (`integration_hub.py`, `mega_roboter_ki.py`)

## Integration Points

**Cross-Project-References (via UnifiedProjectIntegration.cs):**

| Projekt | Pfad | Integration |
|---------|------|-------------|
| **QuantumAvatar** | `c:\Users\nazmi\QuantumAvatar` | 35 Python-Services |
| **Kontrollzentrum** | `c:\Users\nazmi\Kontrollzentrum` | Module-Registry, Team-Modus |
| **AutonomousZenithOptimizer** | `c:\Users\nazmi\AutonomousZenithOptimizer` | C# Zenith-Controller |
| **modules** | `c:\Users\nazmi\modules` | Shared Python-Module |
| **desktop-tutorial** | `c:\Users\nazmi\desktop-tutorial` | AethelosGAZI Integration |

**Interne Module:**
- `AI_CORE/MegaUltraAIIntegrator.csproj`: AI Services Orchestration
- `PY_SIDEBOARD/`: Python Sideboards (double_gazi_ai_ultimate.py)
- `ZENITH_FRONTEND/`: Frontend-Komponenten
- `integrated_projects/`: Sub-Project Snapshots

**External Services:**
- **OpenAI**: GPT-3.5/4 (via main.py `/openai` Endpoint)
- **Ollama**: Local LLM (Port 11434, auto-detect)
- **Stripe**: Payment Gateway (QuantumPaymentModule)
- **AWS/Azure**: Cloud Services (QuantumCloudModule)

## Debugging & Troubleshooting

**Executable-Probleme:**
```powershell
# Logs prüfen
Get-Content build_output.log
Get-Content build_restore.log

# Port-Konflikte
netstat -ano | findstr :3000
netstat -ano | findstr :11434

# Single-Instance Check
Get-Process -Name "🤖ROBOTER_KI_APP" -ErrorAction SilentlyContinue
```

**Python API Debugging:**
```powershell
# Environment Check
python check_roboter_ki.ps1

# Direct Test
python import_test.py
python gemini_test.py
python chat_test.py

# Requirements Validation
python test_requirements.py
```

**Sideboard Quick Checks:**
```powershell
Invoke-WebRequest http://localhost:8003/health
Invoke-WebRequest http://localhost:8003/modules
```

**Common Issues:**

| Fehler | Ursache | Fix |
|--------|---------|-----|
| Port 3000 belegt | Node-Server läuft bereits | `Stop-Process -Name node` |
| JWT_SECRET fehlt | .env nicht geladen | `$env:JWT_SECRET = [guid]::NewGuid()` |
| Ollama nicht erreichbar | Service nicht gestartet | Ollama Desktop App starten |
| API_KEY ungültig | .env nicht gesetzt | `.env` aus `.env.example` erstellen |

**Git Status Check:**
```powershell
# Unstaged Changes prüfen
git status

# Backup vor Änderungen
# Siehe: BACKUP_2025-10-30/ für automatische Backups
```

## Production Deployment

**Pre-Deployment Checklist:**
- [ ] `.env` vollständig konfiguriert (JWT_SECRET, API_KEY, etc.)
- [ ] `dotnet build -c Release` erfolgreich
- [ ] `python test_requirements.py` alle Tests OK
- [ ] Port 3000 & 11434 verfügbar
- [ ] Ollama installiert & gestartet
- [ ] SECURITY_DOC_AND_TESTS.md reviewed

**Build Executable:**
```powershell
# Full Production Build
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true

# Output: bin/Release/net8.0/win-x64/publish/🤖ROBOTER_KI_APP.exe
```

**Post-Deployment:**
```powershell
# Health Check
Invoke-WebRequest http://localhost:3000/health

# API Test
Invoke-WebRequest http://localhost:8000/health -Method GET
```

## Agent-Do/Don't (kurz)
- DO: Änderungen klein halten, entry-points kompatibel lassen, `core/key_check.py` als Source-of-Truth behandeln.
- DO: Wenn du API-Schemas änderst, update Clients/Sideboards im selben PR.
- DON'T: Backups/Snapshots „reparieren“ (Ordner `BACKUP_*`, `integrated_projects/`).
- DON'T: Secrets hinzufügen, echte Keys in Tests/Logs ausgeben, oder neue Demo-Fallbacks einbauen.

---
*Letzte Aktualisierung: 11. Dezember 2025 | Version 2.0.0 | .NET 8.0 + Python 3.13*
