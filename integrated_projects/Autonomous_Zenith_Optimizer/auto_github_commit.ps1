# Automatisches Git Commit und Push Skript
param(
    [string]$Message = "Auto-commit: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [string]$Branch = "main"
)

# Wechsel zum Repository-Verzeichnis
Set-Location "$env:USERPROFILE\Desktop\Autonomous Zenith Optimizer"

# Git Status anzeigen
Write-Host "Git Status:" -ForegroundColor Cyan
git status

# Alle Änderungen hinzufügen
Write-Host "`nFüge alle Änderungen hinzu..." -ForegroundColor Yellow
git add .

# Commit erstellen
Write-Host "`nErstelle Commit..." -ForegroundColor Yellow
git commit -m $Message

# Push zu GitHub
Write-Host "`nPushe zu GitHub..." -ForegroundColor Yellow
git push origin $Branch

Write-Host "`n✓ Erfolgreich zu GitHub gepusht!" -ForegroundColor Green
