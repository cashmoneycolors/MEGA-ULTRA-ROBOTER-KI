# MEGA ULTRA USER INSTALLER - Korrigiert
Write-Host "🚀 MEGA ULTRA CREATIVE STUDIO - USER INSTALLATION" -ForegroundColor Cyan

$InstallDir = "$env:USERPROFILE\MEGA ULTRA Creative Studio"
Write-Host "📁 Installing to: $InstallDir" -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Write-Host "✅ Directory created" -ForegroundColor Green

Copy-Item "*.py" $InstallDir -Force
Copy-Item "*.bat" $InstallDir -Force  
Copy-Item "*.txt" $InstallDir -Force
Write-Host "✅ Files copied" -ForegroundColor Green

$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\MEGA ULTRA Studio.lnk")
$Shortcut.TargetPath = "$InstallDir\START.bat"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Save()
Write-Host "✅ Desktop shortcut created" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "📍 Location: $InstallDir" -ForegroundColor Cyan
Write-Host "🚀 Launch from desktop: MEGA ULTRA Studio" -ForegroundColor Yellow

pause