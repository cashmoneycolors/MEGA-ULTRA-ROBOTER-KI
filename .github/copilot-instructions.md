# MEGA ULTRA ROBOTER KI - Copilot Instructions

## Architektur-Übersicht
Hybrides C#/.NET + Python autonomes KI-System mit Multi-Projekt-Integration. **Production-Ready** mit 64.95 MB kompiliertem Executable.

**Core-Komponenten:**
- `🤖ROBOTER_KI_APP.cs` (559 Zeilen): C# Haupt-App mit Quantum-Integration
- `main.py`: FastAPI Backend mit OpenAI-Integration & Authentication
- `mega_roboter_ki.py`: Python Automation Core
- `integration_hub.py`: Universal Integration Hub für alle Projekte
- `AI_CORE/`: MegaUltraAIIntegrator.csproj
- `modules/`: 40+ Python-Module (QuantumAvatar-Integration)

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
# main.py - FastAPI API
app = FastAPI()
├── /auth - API Key Authentication (API_KEY, APP_ID)
├── /openai - OpenAI GPT Integration
└── /health - Health Check

# integration_hub.py - Project Bridge
├── ZenithCoreSystem
├── Kontrollturm
├── MegaUltraNetwork
└── AI_CORE Integration
```

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

**Security Requirements:**
```env
# .env (REQUIRED)
JWT_SECRET=<guid-generiert>
ADMIN_PASSWORD_HASH=<pbkdf2-hash>
API_KEY=<service-key>
APP_ID=<app-identifier>
OPENAI_API_KEY=<optional-openai>
```

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

---
*Letzte Aktualisierung: 11. Dezember 2025 | Version 2.0.0 | .NET 8.0 + Python 3.13*
