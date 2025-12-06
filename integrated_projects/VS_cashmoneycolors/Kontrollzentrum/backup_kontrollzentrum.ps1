# Backup-Skript für Kontrollzentrum-Workspace
$source = "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum"
$backup = "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum_Backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"

Copy-Item -Path $source -Destination $backup -Recurse -Force
Write-Host "Backup erfolgreich erstellt: $backup"