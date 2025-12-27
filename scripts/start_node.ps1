[CmdletBinding()]
param(
    [int]$Port = 3000,
    [string]$BindHost = '0.0.0.0',
    [string]$WebhookBase = 'http://127.0.0.1:8503'
)

$ErrorActionPreference = 'Stop'

function Resolve-NodeExe {
    $explicit = $env:MEGA_NODE_EXE
    if ($explicit -and (Test-Path -LiteralPath $explicit)) {
        return $explicit
    }

    $cmd = Get-Command node -ErrorAction SilentlyContinue
    if ($cmd) {
        return 'node'
    }

    $fnm = Get-Command fnm -ErrorAction SilentlyContinue
    if ($fnm) {
        try {
            # fnm writes shell code that updates PATH
            fnm env --use-on-cd | Out-String | Invoke-Expression
        }
        catch {
            # ignore and re-check for node below
        }

        $cmd2 = Get-Command node -ErrorAction SilentlyContinue
        if ($cmd2) {
            return 'node'
        }
    }

    return $null
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

$nodeExe = Resolve-NodeExe
if (-not $nodeExe) {
    Write-Host '[FATAL] Node.js wurde nicht gefunden (PATH leer / Version-Manager nicht initialisiert).' -ForegroundColor Red
    Write-Host 'Fix-Optionen:' -ForegroundColor Yellow
    Write-Host '  1) Node normal installieren (z.B. nodejs.org), dann erneut starten.'
    Write-Host '  2) Oder in deinem interaktiven Terminal den Node-Pfad holen:'
    Write-Host '       Get-Command node | Select-Object -ExpandProperty Source'
    Write-Host '     und dann setzen (Beispiel):'
    Write-Host '       $env:MEGA_NODE_EXE = "C:\\Pfad\\zu\\node.exe"'
    Write-Host '     Danach dieses Script erneut ausfuehren.'
    exit 2
}

$env:MEGA_WEBHOOK_BASE = $WebhookBase

Write-Host ('== NODE START ==  node={0}  host={1}  port={2}  webhook={3}' -f $nodeExe, $BindHost, $Port, $WebhookBase)

# Keep this PowerShell process alive while node runs (Task background-friendly)
& $nodeExe server.mjs --port $Port --host $BindHost
