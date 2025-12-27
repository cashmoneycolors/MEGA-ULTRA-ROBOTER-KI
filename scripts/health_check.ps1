param(
    [int]$PublicPort = 3000
)

$ErrorActionPreference = 'Continue'

Write-Host '== PORT CHECK (LISTENING) =='
$ports = @(11434, $PublicPort, 8000, 8502, 8503)
foreach ($p in $ports) {
    $pattern = ":$p\s+"
    $hits = netstat -ano | Select-String -Pattern $pattern
    if ($hits) {
        Write-Host ("Port {0}: LISTENING" -f $p)
        $hits | Select-Object -First 2 | ForEach-Object { $_.Line }
    }
    else {
        Write-Host ("Port {0}: NOT LISTENING" -f $p)
    }
}

Write-Host "\n== HTTP CHECKS =="
function Test-Url([string]$Url) {
    try {
        $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
        Write-Host ("OK   {0} -> {1}" -f $Url, $r.StatusCode)
        if ($r.Content) {
            $c = [string]$r.Content
            if ($c.Length -gt 160) { $c = $c.Substring(0, 160) + '...' }
            Write-Host ("  Body: {0}" -f $c)
        }
    }
    catch {
        Write-Host ("FAIL {0} -> {1}" -f $Url, $_.Exception.Message)
    }
}

Test-Url 'http://127.0.0.1:11434/api/tags'
Test-Url 'http://127.0.0.1:8000/health'
Test-Url 'http://127.0.0.1:8503/health'
Test-Url ("http://127.0.0.1:{0}/status" -f $PublicPort)
Test-Url ("http://127.0.0.1:{0}/health" -f $PublicPort)

Write-Host "\n== TOOLING =="
try { Write-Host ("node:   {0}" -f (node --version)) } catch { Write-Host 'node:   NOT FOUND' }
try { Write-Host ("dotnet: {0}" -f (dotnet --version)) } catch { Write-Host 'dotnet: NOT FOUND' }
try { Write-Host ("python: {0}" -f (C:/cashmoneycolors/-MEGA-ULTRA-ROBOTER-KI/.venv/Scripts/python.exe --version)) } catch { Write-Host 'python venv: NOT FOUND' }
