# MEGA ULTRA - USER INSTALLATION (Admin-Rechte nicht erforderlich)

Write-Host "🚀 MEGA ULTRA CREATIVE STUDIO - USER INSTALLATION" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Installation in User-Verzeichnis (keine Admin-Rechte nötig)
$InstallDir = "$env:USERPROFILE\MEGA ULTRA Creative Studio"

Write-Host "📁 Installation directory: $InstallDir" -ForegroundColor Yellow

# Erstelle Installations-Verzeichnis
Write-Host "📂 Creating installation directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# Kopiere alle Dateien
Write-Host "📋 Installing files..." -ForegroundColor Yellow
Copy-Item "*.py" $InstallDir -Force
Copy-Item "*.bat" $InstallDir -Force  
Copy-Item "*.txt" $InstallDir -Force

Write-Host "✅ Files copied successfully!" -ForegroundColor Green

# Erstelle Desktop-Verknüpfung
Write-Host "🖥️ Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\🚀 MEGA ULTRA Studio.lnk")
$Shortcut.TargetPath = "$InstallDir\START.bat"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "MEGA ULTRA Creative Studio - AI App Generator"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created!" -ForegroundColor Green

# Erstelle Start Menu Verknüpfung
Write-Host "📋 Creating start menu shortcut..." -ForegroundColor Yellow
$StartMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$StartShortcut = $WshShell.CreateShortcut("$StartMenuPath\🚀 MEGA ULTRA Studio.lnk")
$StartShortcut.TargetPath = "$InstallDir\START.bat"
$StartShortcut.WorkingDirectory = $InstallDir
$StartShortcut.Description = "MEGA ULTRA Creative Studio"
$StartShortcut.Save()

Write-Host "✅ Start menu shortcut created!" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 INSTALLATION COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installed to: $InstallDir" -ForegroundColor Cyan
Write-Host "🖥️ Desktop shortcut: 🚀 MEGA ULTRA Studio" -ForegroundColor Cyan
Write-Host "📋 Start menu: Programs > 🚀 MEGA ULTRA Studio" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Ready to launch! Use one of these methods:" -ForegroundColor Yellow
Write-Host "   • Double-click desktop shortcut" -ForegroundColor White
Write-Host "   • Start menu > 🚀 MEGA ULTRA Studio" -ForegroundColor White
Write-Host "   • Run: $InstallDir\START.bat" -ForegroundColor White
Write-Host ""

# Test ob Python verfügbar ist
Write-Host "System check..." -ForegroundColor Yellow
$PythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Python found: $PythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python not found - please install Python 3.7+" -ForegroundColor Red
    Write-Host "   Download from: https://python.org" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 MEGA ULTRA SYSTEM IS NOW READY!" -ForegroundColor Green
Write-Host "Launch from desktop to start creating apps!" -ForegroundColor Cyan

Read-Host "Press Enter to exit"