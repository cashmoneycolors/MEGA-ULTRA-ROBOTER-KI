[CmdletBinding()]
param(
    [switch]$Kill,
    [int[]]$Ports = @(3000, 8000, 8003, 8502, 8503),
    [switch]$IncludeOllama
)

$ErrorActionPreference = 'Continue'

function Get-PidsListeningOnPort([int]$Port) {
    $lines = netstat -ano | Select-String -Pattern (":$Port\s+")
    if (-not $lines) { return @() }

    $pids = @()
    foreach ($m in $lines) {
        $line = [string]$m.Line
        if (-not $line) { continue }
        $parts = ($line -split '\s+') | Where-Object { $_ -ne '' }
        if ($parts.Count -lt 5) { continue }
        $pidText = $parts[$parts.Count - 1]
        $pidParsed = 0
        if ([int]::TryParse($pidText, [ref]$pidParsed)) {
            $pids += $pidParsed
        }
    }
    return ($pids | Sort-Object -Unique)
}

function Describe-ProcessId([int]$ProcessId) {
    try {
        $p = Get-Process -Id $ProcessId -ErrorAction Stop
        return "{0} (PID {1})" -f $p.ProcessName, $ProcessId
    }
    catch {
        return "PID {0} (process not found)" -f $ProcessId
    }
}

$allPorts = @($Ports)
if ($IncludeOllama) { $allPorts += 11434 }

Write-Host '== STOP/CLEANUP ==' 
Write-Host ("Mode: {0}" -f ($(if ($Kill) { 'KILL' } else { 'LIST' })))
Write-Host ("Ports: {0}" -f (($allPorts | Sort-Object) -join ', '))

$targets = @()
foreach ($port in ($allPorts | Sort-Object -Unique)) {
    $pids = Get-PidsListeningOnPort -Port $port
    if (-not $pids -or $pids.Count -eq 0) {
        Write-Host ("Port {0}: not listening" -f $port)
        continue
    }

    foreach ($procId in $pids) {
        if ($procId -le 0) { continue }
        Write-Host ("Port {0}: {1}" -f $port, (Describe-ProcessId -ProcessId $procId))
        $targets += [pscustomobject]@{ Port = $port; Pid = $procId }
    }
}

if (-not $Kill) {
    Write-Host "\nNothing stopped. Re-run with -Kill to stop these PIDs." 
    Write-Host "Example: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/stop_services.ps1 -Kill" 
    return
}

if (-not $targets -or $targets.Count -eq 0) {
    Write-Host "\nNo targets to stop." 
    return
}

Write-Host "\nStopping processes..." 
foreach ($t in ($targets | Sort-Object -Property Pid -Unique)) {
    try {
        Stop-Process -Id $t.Pid -Force -ErrorAction Stop
        Write-Host ("Stopped PID {0}" -f $t.Pid)
    }
    catch {
        Write-Host ("FAILED to stop PID {0}: {1}" -f $t.Pid, $_.Exception.Message)
    }
}
