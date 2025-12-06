# PowerShell-Buildskript für das Kontrollzentrum
# Dieses Skript erstellt eine ausführbare Datei aus mega_roboter_ki.py und verschiebt sie ins Zielverzeichnis

$ErrorActionPreference = 'Stop'

# 1. Abhängigkeiten installieren
Write-Host 'Installiere Python-Abhängigkeiten...'
pip install -r requirements.txt

# 2. PyInstaller installieren
Write-Host 'Installiere PyInstaller...'
pip install pyinstaller

# 3. Exe bauen
Write-Host 'Erzeuge .exe mit PyInstaller...'
pyinstaller --onefile --name "🤖ROBOTER_KI_APP" modules/mega_ultra_roboter_ki.py

# 4. Zielverzeichnis anlegen
$ziel = "C:\Users\Laptop\Desktop\Projekte\MEGA ULTRA ROBOTER KI"
if (!(Test-Path $ziel)) {
    New-Item -ItemType Directory -Path $ziel
}

# 5. Exe verschieben
$quelle = "dist\🤖ROBOTER_KI_APP.exe"
if (Test-Path $quelle) {
    Move-Item $quelle $ziel -Force
    Write-Host "Fertig! Die .exe liegt jetzt in: $ziel"
} else {
    Write-Host "Fehler: .exe wurde nicht gefunden!"
}
