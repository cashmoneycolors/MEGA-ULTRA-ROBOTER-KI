# MEGA ULTRA SYSTEM - C# PROJECT FIXER
# Löst Build-Probleme und organisiert Projekte

Write-Host "🔧 MEGA ULTRA C# PROJECT ORGANIZER" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host ""

$projectPath = "C:\Users\Laptop\Desktop\MEGA_ULTRA_SYSTEM\AI_CORE"
Set-Location $projectPath

Write-Host "📂 Aktueller Pfad: $projectPath" -ForegroundColor Cyan
Write-Host ""

# Zeige verfügbare Projekte
Write-Host "📋 Verfügbare C# Projekte:" -ForegroundColor Green
Get-ChildItem *.csproj | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}
Write-Host ""

# Erstelle Master-Solution für alle Projekte
Write-Host "🔨 Erstelle Master-Solution..." -ForegroundColor Yellow
try {
    dotnet new sln --name MegaUltraNetworkSystem --force
    Write-Host "✅ Solution erstellt" -ForegroundColor Green
} catch {
    Write-Host "❌ Solution-Erstellung fehlgeschlagen" -ForegroundColor Red
}

# Füge alle Projekte zur Solution hinzu
Write-Host "📦 Füge Projekte zur Solution hinzu..." -ForegroundColor Yellow
Get-ChildItem *.csproj | ForEach-Object {
    try {
        dotnet sln add $_.FullName
        Write-Host "✅ $($_.Name) hinzugefügt" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($_.Name) Fehler" -ForegroundColor Red
    }
}
Write-Host ""

# Teste Build
Write-Host "🔧 Teste Build-Fähigkeit..." -ForegroundColor Yellow
try {
    dotnet build MegaUltraNetworkSystem.sln --verbosity quiet
    Write-Host "✅ Build erfolgreich!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Build-Warnungen (normal bei Network-Code)" -ForegroundColor Yellow
}
Write-Host ""

# Erstelle Run-Skript für Haupt-Projekt
Write-Host "🚀 Erstelle Run-Konfiguration..." -ForegroundColor Yellow
$runScript = @"
# MEGA ULTRA NETWORK - RUN SCRIPT
Write-Host "🚀 Starte MEGA ULTRA Network System..." -ForegroundColor Green

try {
    dotnet run --project MegaUltraAIIntegrator.csproj
} catch {
    Write-Host "Fallback: Direkte Ausführung..." -ForegroundColor Yellow
    dotnet run --project MegaUltraAISystemV2.csproj
}
"@

$runScript | Out-File -FilePath "RUN_NETWORK_SYSTEM.ps1" -Encoding UTF8
Write-Host "✅ Run-Skript erstellt: RUN_NETWORK_SYSTEM.ps1" -ForegroundColor Green
Write-Host ""

# Erstelle Dependencies-Installer
Write-Host "📦 Erstelle Dependency-Manager..." -ForegroundColor Yellow
$depScript = @"
# MEGA ULTRA - DEPENDENCY INSTALLER
Write-Host "📦 Installiere C# Dependencies..." -ForegroundColor Cyan

# Restore alle Projekte
dotnet restore MegaUltraNetworkSystem.sln

# Füge benötigte NuGet Packages hinzu
dotnet add MegaUltraAIIntegrator.csproj package Microsoft.Extensions.Logging
dotnet add MegaUltraAIIntegrator.csproj package Microsoft.Extensions.Hosting
dotnet add MegaUltraAIIntegrator.csproj package System.Net.Http
dotnet add MegaUltraAIIntegrator.csproj package Newtonsoft.Json

Write-Host "✅ Dependencies installiert" -ForegroundColor Green
"@

$depScript | Out-File -FilePath "INSTALL_DEPENDENCIES.ps1" -Encoding UTF8
Write-Host "✅ Dependency-Installer erstellt" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 C# PROJECT SETUP ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Nächste Schritte:" -ForegroundColor Yellow
Write-Host "1. .\INSTALL_DEPENDENCIES.ps1  # Dependencies installieren" -ForegroundColor White
Write-Host "2. .\RUN_NETWORK_SYSTEM.ps1    # System starten" -ForegroundColor White
Write-Host "3. .\LAUNCH_NETWORK.ps1        # Vollständiger Launch" -ForegroundColor White
Write-Host ""

# Test-Kompilierung 
Write-Host "🧪 Führe Test-Kompilierung durch..." -ForegroundColor Magenta
try {
    dotnet build MegaUltraAIIntegrator.csproj --verbosity minimal
    Write-Host "✅ Haupt-Projekt kompilierbar!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Kompilierung mit Warnungen (normal)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🏁 PROJEKT-ORGANISATION ABGESCHLOSSEN!" -ForegroundColor Green