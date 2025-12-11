# ===================================
#  MSIX Package Workflow für MEGA ULTRA ROBOTER KI
# ===================================

$AppName = "MEGA_ULTRA_ROBOTER_KI"
$Version = "2.0.0.0"
$Publisher = "CN=CashMoneyColors"
$OutputDir = "c:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1\MSIX_OUTPUT"

Write-Host " MSIX Package Workflow gestartet" -ForegroundColor Cyan
Write-Host "====================================
"

# Schritt 1: Output-Verzeichnis erstellen
Write-Host "1 Erstelle Output-Verzeichnis..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
Write-Host "    $OutputDir erstellt
"

# Schritt 2: App-Struktur vorbereiten
Write-Host "2 Bereite App-Struktur vor..." -ForegroundColor Yellow
$AppFolder = "$OutputDir\AppPackage"
New-Item -ItemType Directory -Path $AppFolder -Force | Out-Null

# Kopiere Executable
Copy-Item "c:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1\ROBOTER_KI_APP.exe" $AppFolder -Force
Write-Host "    Executable kopiert
"

# Schritt 3: Verfügbare Package-Manifeste anzeigen
Write-Host "3 Verfügbare Package-Manifeste:" -ForegroundColor Yellow
$manifests = @(
    "c:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1\AI_CORE\MEGA_ULTRA_OUTPUT\PACKAGE\App\Package.appxmanifest",
    "c:\Users\nazmi\MEGA-ULTRA-ROBOTER-KI-1\integrated_projects\AI_CORE\MEGA_ULTRA_OUTPUT\PACKAGE\App\Package.appxmanifest"
)
foreach ($m in $manifests) {
    if (Test-Path $m) {
        Write-Host "    $m" -ForegroundColor Green
    }
}

Write-Host "
====================================
"
Write-Host " Vorbereitung abgeschlossen!" -ForegroundColor Green
Write-Host "
Nächste Schritte:" -ForegroundColor Cyan
Write-Host "A) makeappx pack /d $AppFolder /p $OutputDir\$AppName.msix"
Write-Host "B) signtool sign /fd SHA256 /f cert.pfx /p password $OutputDir\$AppName.msix"
Write-Host "C) AppCertKitCmd.exe /a $OutputDir\$AppName.msix
"
