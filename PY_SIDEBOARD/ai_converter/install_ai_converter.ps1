# Installationsskript für AI Converter Modul (PowerShell)
# Installiert alle Python-Abhängigkeiten und startet das Backend

Write-Host "[AI Converter] Installiere Python-Abhängigkeiten..."
$ErrorActionPreference = 'Stop'

# Wechsle ins App-Verzeichnis
Push-Location "$PSScriptRoot/app"

# Prüfe, ob requirements.txt existiert, sonst erstellen
if (!(Test-Path requirements.txt)) {
    Write-Host "[AI Converter] requirements.txt nicht gefunden. Erstelle Minimaldatei..."
    @(
        "fastapi",
        "uvicorn[standard]",
        "python-docx",
        "Pillow",
        "reportlab",
        "trimesh"
    ) | Set-Content requirements.txt
}

# Installiere Abhängigkeiten
pip install -r requirements.txt

Pop-Location

Write-Host "[AI Converter] Installation abgeschlossen. Starte Backend mit:"
Write-Host "    cd app && uvicorn main:app --reload --port 8088"
