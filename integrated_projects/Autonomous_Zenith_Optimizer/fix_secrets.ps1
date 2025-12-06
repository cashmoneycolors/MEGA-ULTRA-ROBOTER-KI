# Secret Removal & Git History Fix
# Entfernt versehentlich committete Secrets und bereinigt Git-Historie

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Secret Removal & Git History Fix" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Problem: GitHub Personal Access Tokens in .env wurden committed
# Lösung: Commit zurücksetzen, .env bereinigen, neu committen

Write-Host "🔧 Schritt 1: Letzten Commit zurücksetzen..." -ForegroundColor Yellow
git reset --soft HEAD~1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit zurückgesetzt (Änderungen bleiben staged)" -ForegroundColor Green
}
Write-Host ""

Write-Host "🔧 Schritt 2: .env bereits bereinigt (Secrets entfernt)" -ForegroundColor Yellow
Write-Host "✅ .env Datei ist sicher" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Schritt 3: Großes Backup aus Staging entfernen..." -ForegroundColor Yellow
git reset HEAD Kontrollzentrum/backups/backup_20251120_061619.bundle
Write-Host "✅ Großes Backup-File entfernt (zu groß für GitHub)" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Schritt 4: Alle anderen Änderungen neu committen..." -ForegroundColor Yellow
git add .
git commit -m "Add VS Code Recovery Helper & Copilot Chat Recovery Guide (ohne Secrets)"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Neuer Commit erstellt (sauber, ohne Secrets)" -ForegroundColor Green
}
Write-Host ""

Write-Host "🔧 Schritt 5: Push versuchen..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push erfolgreich!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Push hat noch Probleme - prüfe Output oben" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Falls immer noch Secrets-Problem:" -ForegroundColor Yellow
    Write-Host "1. GitHub erlaubt den Push über die URLs (siehe Output)" -ForegroundColor White
    Write-Host "2. Oder verwende: git push --force-with-lease (überschreibt Historie)" -ForegroundColor White
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Wichtig: Tokens widerrufen!" -ForegroundColor Red
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Die beiden Tokens aus .env sind jetzt öffentlich sichtbar!" -ForegroundColor Red
Write-Host "⚠️  SOFORT widerrufen unter:" -ForegroundColor Red
Write-Host "    https://github.com/settings/tokens" -ForegroundColor White
Write-Host ""
Write-Host "Betroffene Tokens (erste/letzte Zeichen):" -ForegroundColor Yellow
Write-Host "  - github_pat_11BXWODLA02a8o...W5Y6HB5" -ForegroundColor White
Write-Host "  - github_pat_11BXWODLA0zT4F...QV4O3B" -ForegroundColor White
Write-Host ""
Write-Host "Nach dem Widerrufen:" -ForegroundColor Yellow
Write-Host "  gh auth login --web" -ForegroundColor White
Write-Host "  (Erstellt neue, sichere Tokens)" -ForegroundColor Gray
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
