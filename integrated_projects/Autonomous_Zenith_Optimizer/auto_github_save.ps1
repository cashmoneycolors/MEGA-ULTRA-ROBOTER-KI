# Automatische GitHub-Speicherung mit Datei-Watcher
# Überwacht Änderungen und commitet automatisch

param(
    [string]$WatchPath = "$env:USERPROFILE\Desktop\Autonomous Zenith Optimizer",
    [int]$DelaySeconds = 30  # Wartezeit nach letzter Änderung
)

Write-Host "Starte automatische GitHub-Speicherung..." -ForegroundColor Cyan
Write-Host "Überwache: $WatchPath" -ForegroundColor Yellow
Write-Host "Drücke Strg+C zum Beenden`n" -ForegroundColor Gray

# Wechsel zum Repository
Set-Location $WatchPath

# FileSystemWatcher erstellen
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $WatchPath
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

# Filter für relevante Dateien
$watcher.Filter = "*.*"
$watcher.NotifyFilter = [System.IO.NotifyFilters]::FileName -bor
                        [System.IO.NotifyFilters]::LastWrite -bor
                        [System.IO.NotifyFilters]::DirectoryName

# Letzte Änderungszeit
$script:lastChange = $null
$script:hasChanges = $false

# Event-Handler für Änderungen
$onChange = {
    param($sender, $e)
    
    # Ignoriere .git Ordner und temporäre Dateien
    if ($e.FullPath -notmatch '\.git\\|\.tmp$|~$|\.swp$') {
        $script:lastChange = Get-Date
        $script:hasChanges = $true
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Änderung: $($e.Name) ($($e.ChangeType))" -ForegroundColor Yellow
    }
}

# Events registrieren
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $onChange | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Created -Action $onChange | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $onChange | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $onChange | Out-Null

Write-Host "Watcher aktiv! Warte auf Änderungen...`n" -ForegroundColor Green

try {
    # Haupt-Loop
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Prüfe ob Änderungen vorliegen und Wartezeit abgelaufen
        if ($script:hasChanges -and $script:lastChange) {
            $timeSinceChange = (Get-Date) - $script:lastChange
            
            if ($timeSinceChange.TotalSeconds -ge $DelaySeconds) {
                Write-Host "`n[$(Get-Date -Format 'HH:mm:ss')] Speichere zu GitHub..." -ForegroundColor Cyan
                
                # Git Add, Commit, Push
                git add .
                $commitMsg = "Auto-save: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
                git commit -m $commitMsg
                git push origin main
                
                Write-Host "✓ Erfolgreich gespeichert!`n" -ForegroundColor Green
                
                # Reset
                $script:hasChanges = $false
                $script:lastChange = $null
            }
        }
    }
}
finally {
    # Cleanup
    $watcher.Dispose()
    Get-EventSubscriber | Unregister-Event
    Write-Host "`nWatcher beendet." -ForegroundColor Red
}
