# Backup-Skript für den gesamten AI_CORE-Workspace
# Erstellt ein ZIP-Archiv mit Zeitstempel im gleichen Verzeichnis


# Backup-Skript: Erkennt und sichert ALLE Dateien und Ordner im Workspace rekursiv – keine Ausschlüsse, alles wird automatisch erkannt und gesichert.
$workspace = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backupName = "AI_CORE_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
$backupPath = Join-Path $workspace $backupName

Write-Host "Erkenne und sichere ALLE Dateien und Ordner im Workspace..." -ForegroundColor Cyan
Write-Host "(Es werden KEINE Dateien oder Ordner ausgeschlossen - alles wird gesichert!)" -ForegroundColor Yellow

Compress-Archive -Path "$workspace\*" -DestinationPath $backupPath -Force -CompressionLevel Optimal

Write-Host "Backup abgeschlossen!" -ForegroundColor Green
Write-Host "Datei gespeichert unter: $backupPath" -ForegroundColor Yellow
