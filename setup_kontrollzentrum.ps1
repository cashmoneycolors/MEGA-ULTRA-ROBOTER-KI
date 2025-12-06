
# MEGA ULTRA ROBOTER KI – Setup & Aufgaben für Team-Support

## 1. requirements.txt anlegen und Premium-Pakete installieren
Erstelle im Projektverzeichnis eine Datei requirements.txt mit folgendem Inhalt:
torch
torchvision
torchaudio
tensorflow-gpu
optimum
onnxruntime-gpu
huggingface_hub
ray[serve]
poetry
pipenv
modin[all]
dask[dataframe]
pyarrow
uvicorn[gunicorn]
sentry-sdk
bandit
openai
boto3
s3transfer
google-cloud-storage
azure-storage-blob
python-dotenv
reportlab
jwt
pandas
gtts
SpeechRecognition
cryptography
streamlit

Installiere alle Pakete:
```powershell
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

## 2. Kontrollzentrum Komplett-Setup
if (!(Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Erstelle virtuelle Umgebung..."
}
.venv\Scripts\Activate.ps1
Write-Host "Aktiviere virtuelle Umgebung..."
pip install -r requirements.txt
Write-Host "Installiere Python-Abhängigkeiten..."
$envPath = ".env"
if (!(Test-Path $envPath)) {
    @"
DEBUG=True
DATABASE_URL=sqlite:///modules.db
PORT=8002
OLLAMA_API_KEY=dein-ollama-key
OLLAMA_API_URL=http://localhost:11434
OPENAI_API_KEY=dein-openai-key
"@ | Out-File $envPath -Encoding utf8
    Write-Host "Lege .env-Datei mit Platzhaltern an..."
}
python autofill_module_registry.py
Write-Host "Fülle Modul-Registry automatisch auf..."
Start-Process python -ArgumentList "dashboard_modul.py"
Write-Host "Starte Dashboard-Modul..."
python plugin_system.py
Write-Host "Lade Plugins..."
python build_pipeline.py
Write-Host "Starte Build-Pipeline..."
pwsh .\AI_CORE\FIX_CSHARP_PROJECTS.ps1
Write-Host "Starte PowerShell/.NET-Integration für C#-Projekte..."
dotnet restore
dotnet build
Start-Process python -ArgumentList "OllamaProxyServer/main.py"
Write-Host "Starte OllamaProxyServer..."
python -m pytest
Write-Host "Führe alle Tests aus..."
Write-Host "Setup abgeschlossen! Kontrollzentrum ist komplett integriert und einsatzbereit."
