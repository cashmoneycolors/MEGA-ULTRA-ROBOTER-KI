# GitHub Push Authentication Fix
# Behebt 403-Fehler beim Pushen

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  GitHub Push Authentication Fix" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# 1. Aktuellen Remote prüfen
Write-Host "📊 Aktueller Remote:" -ForegroundColor Yellow
git remote -v
Write-Host ""

# 2. Token aus gh CLI holen
Write-Host "🔑 Hole GitHub Token..." -ForegroundColor Yellow
$token = gh auth token
if ($token) {
    Write-Host "✅ Token gefunden" -ForegroundColor Green
} else {
    Write-Host "❌ Kein Token gefunden" -ForegroundColor Red
    Write-Host "Führe aus: gh auth login" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# 3. Remote mit Token aktualisieren
Write-Host "🔧 Aktualisiere Remote mit Token..." -ForegroundColor Yellow
$repo = "cashmoneycolors/AutonomousZenithOptimizer"
$newUrl = "https://${token}@github.com/${repo}.git"

git remote set-url origin $newUrl
Write-Host "✅ Remote aktualisiert" -ForegroundColor Green
Write-Host ""

# 4. Erneut versuchen zu pushen
Write-Host "🚀 Versuche Push..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push erfolgreich!" -ForegroundColor Green
} else {
    Write-Host "❌ Push fehlgeschlagen" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative Lösungen:" -ForegroundColor Yellow
    Write-Host "1. Erneut authentifizieren: gh auth login" -ForegroundColor White
    Write-Host "2. Token-Berechtigung prüfen bei: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "3. SSH statt HTTPS nutzen" -ForegroundColor White
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
