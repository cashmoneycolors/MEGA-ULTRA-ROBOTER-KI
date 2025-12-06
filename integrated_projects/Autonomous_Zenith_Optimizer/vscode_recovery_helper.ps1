# VS Code Recovery & GitHub Integration Helper
# Automatische Wiederherstellung für Chat, Editor-Ansichten und GitHub-Integration

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  VS Code Recovery & GitHub Integration Helper" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# 1. GitHub Auth Status prüfen
Write-Host "🔐 Prüfe GitHub-Authentifizierung..." -ForegroundColor Yellow
gh auth status
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ GitHub Auth erfolgreich" -ForegroundColor Green
} else {
    Write-Host "❌ GitHub Auth fehlgeschlagen - führe aus: gh auth login" -ForegroundColor Red
}
Write-Host ""

# 2. Git Status
Write-Host "📊 Git Repository Status..." -ForegroundColor Yellow
git status
Write-Host ""

# 3. Aktiver Branch
Write-Host "🌿 Aktiver Branch:" -ForegroundColor Yellow
git branch --show-current
Write-Host ""

# 4. Letzte Commits
Write-Host "📝 Letzte 10 Commits:" -ForegroundColor Yellow
git log --oneline -n 10
Write-Host ""

# 5. Pull Requests
Write-Host "🔀 Pull Requests:" -ForegroundColor Yellow
gh pr list
Write-Host ""

# 6. Wichtige Dateien öffnen
Write-Host "📂 Öffne wichtige Projekt-Dateien in VS Code..." -ForegroundColor Yellow
$projektPfad = "C:\Users\Laptop\Desktop\Autonomous Zenith Optimizer"

# Kern-Dateien zum Öffnen
$kernDateien = @(
    "conversation_summary.local.md",
    "repo_recovery_steps.local.md",
    "todo.md",
    "MODULE_STATUS.md",
    "README.txt",
    "VS_CODE_AUTOMATION_GUIDE.md",
    "GITHUB_AUTO_SAVE_GUIDE.md"
)

# Prüfe welche Dateien existieren
$vorhandeneDateien = @()
foreach ($datei in $kernDateien) {
    $pfad = Join-Path $projektPfad $datei
    if (Test-Path $pfad) {
        $vorhandeneDateien += $pfad
        Write-Host "  ✓ $datei" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $datei (nicht gefunden)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Nächste Schritte" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "VS Code öffnen:" -ForegroundColor Yellow
Write-Host "  code `"$projektPfad`"" -ForegroundColor White
Write-Host ""
Write-Host "Copilot Chat öffnen:" -ForegroundColor Yellow
Write-Host "  1. Drücke: Strg+Shift+P" -ForegroundColor White
Write-Host "  2. Tippe: 'Copilot: Focus on Chat View'" -ForegroundColor White
Write-Host "  3. Oder: Klicke auf Copilot-Icon in Seitenleiste" -ForegroundColor White
Write-Host ""
Write-Host "GitHub Extensions prüfen:" -ForegroundColor Yellow
Write-Host "  1. Drücke: Strg+Shift+X" -ForegroundColor White
Write-Host "  2. Suche: 'GitHub Copilot'" -ForegroundColor White
Write-Host "  3. Suche: 'GitHub Pull Requests and Issues'" -ForegroundColor White
Write-Host ""
Write-Host "Wichtige Shortcuts:" -ForegroundColor Yellow
Write-Host "  Strg+P         → Datei suchen" -ForegroundColor White
Write-Host "  Strg+Shift+P   → Command Palette" -ForegroundColor White
Write-Host "  Strg+Shift+E   → Explorer" -ForegroundColor White
Write-Host "  Strg+Shift+G   → Git Ansicht" -ForegroundColor White
Write-Host "  Strg+J         → Terminal/Panel umschalten" -ForegroundColor White
Write-Host "  Strg+K V       → Markdown Vorschau" -ForegroundColor White
Write-Host ""

# 7. Optional: VS Code direkt öffnen
Write-Host "VS Code jetzt öffnen? (J/N): " -ForegroundColor Yellow -NoNewline
$antwort = Read-Host
if ($antwort -eq "J" -or $antwort -eq "j") {
    Write-Host "🚀 Öffne VS Code..." -ForegroundColor Green
    code "$projektPfad"
    
    # Warte kurz und öffne dann die wichtigen Dateien
    Start-Sleep -Seconds 3
    foreach ($datei in $vorhandeneDateien) {
        code "$datei"
    }
    
    Write-Host "✅ VS Code geöffnet mit wichtigen Dateien" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Fertig! Viel Erfolg mit deiner Entwicklung! 🚀" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
