# MEGA ULTRA INSTALLER
Write-Host "MEGA ULTRA CREATIVE STUDIO INSTALLER" -ForegroundColor Cyan

$InstallDir = "$env:ProgramFiles\MEGA ULTRA Creative Studio"

Write-Host "Creating installation directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

Write-Host "Installing files..." -ForegroundColor Yellow
Copy-Item "*.py" $InstallDir -Force -ErrorAction SilentlyContinue
Copy-Item "*.bat" $InstallDir -Force -ErrorAction SilentlyContinue

Write-Host "Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\MEGA ULTRA.lnk")
$Shortcut.TargetPath = "$InstallDir\START.bat"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Save()

Write-Host ""
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "Launch from desktop: MEGA ULTRA" -ForegroundColor Cyan
pause
