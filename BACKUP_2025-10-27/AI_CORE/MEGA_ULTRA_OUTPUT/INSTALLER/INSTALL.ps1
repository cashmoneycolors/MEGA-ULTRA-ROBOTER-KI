# MEGA ULTRA CREATIVE STUDIO INSTALLER
Write-Host "ðŸš€ MEGA ULTRA INSTALLER" -ForegroundColor Cyan

$InstallPath = "$env:ProgramFiles\MEGA ULTRA Creative Studio"
Write-Host "ðŸ“ Installing to: $InstallPath" -ForegroundColor Yellow

# Create directory
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null

# Copy files
Write-Host "ðŸ“‹ Copying files..." -ForegroundColor Yellow
Copy-Item "*.py" $InstallPath -Force
Copy-Item "*.txt" $InstallPath -Force
Copy-Item "*.bat" $InstallPath -Force

# Create desktop shortcut
Write-Host "ðŸ–¥ï¸ Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\MEGA ULTRA Creative Studio.lnk")
$Shortcut.TargetPath = "$InstallPath\MEGA_ULTRA_LAUNCHER.bat"
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.Save()

Write-Host "âœ… INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "Launch from desktop shortcut" -ForegroundColor Cyan
pause
