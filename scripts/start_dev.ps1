[CmdletBinding()]
param(
    [string]$ApiKey = 'dev-local',
    [string]$AppId = 'dev-local',
    [string]$OpenAIKeyPlain = 'sk-test',
    [System.Security.SecureString]$OpenAIKey,
    [System.Security.SecureString]$JwtSecret,
    [System.Security.SecureString]$AdminPasswordHash,
    [int]$PythonPort = 8000,
    [switch]$StartWebhook,
    [switch]$StartStreamlit,
    [int]$WebhookPort = 8503,
    [int]$StreamlitPort = 8502,
    [switch]$RunHealthCheck,
    [int]$PublicPort = 3000
)

$ErrorActionPreference = 'Continue'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

$pythonExe = 'C:/cashmoneycolors/-MEGA-ULTRA-ROBOTER-KI/.venv/Scripts/python.exe'

function ConvertTo-PlainText([SecureString]$Secure) {
    if (-not $Secure) { return '' }
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

$jwtSecretPlain = ConvertTo-PlainText $JwtSecret
$adminHashPlain = ConvertTo-PlainText $AdminPasswordHash
$openAIKeyPlain = ConvertTo-PlainText $OpenAIKey

if (-not $jwtSecretPlain) { $jwtSecretPlain = [guid]::NewGuid().ToString('N') }
if (-not $adminHashPlain) { $adminHashPlain = [guid]::NewGuid().ToString('N') }
if (-not $openAIKeyPlain) { $openAIKeyPlain = $OpenAIKeyPlain }

# Environment (inherited by child processes). This avoids putting secrets into command arguments.
$env:API_KEY = $ApiKey
$env:APP_ID = $AppId
$env:OPENAI_API_KEY = $openAIKeyPlain
$env:JWT_SECRET = $jwtSecretPlain
$env:ADMIN_PASSWORD_HASH = $adminHashPlain

Write-Host '== START DEV =='
Write-Host ('Repo: {0}' -f $repoRoot)

# Ollama presence check (do not start/stop it)
try {
    $ollamaListening = (netstat -ano | Select-String -Pattern ':11434\s+').Count -gt 0
    if (-not $ollamaListening) {
        Write-Host '[WARNUNG] Ollama (11434) ist NICHT listening. Bitte Ollama starten und dann fortfahren.'
    }
}
catch { }

# Start FastAPI (separates Fenster)
Start-Process -FilePath 'powershell.exe' -ArgumentList @(
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-NoExit',
    '-Command',
    "Set-Location '$repoRoot'; & '$pythonExe' -m uvicorn main:app --host 0.0.0.0 --port $PythonPort"
) | Out-Null

Write-Host ('[OK] FastAPI start angefordert (Port {0}).' -f $PythonPort)

if ($StartWebhook) {
    Start-Process -FilePath 'powershell.exe' -ArgumentList @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-NoExit',
        '-Command',
        "Set-Location '$repoRoot'; & '$pythonExe' webhook_server.py"
    ) | Out-Null
    Write-Host ('[OK] Webhook start angefordert (Port {0}).' -f $WebhookPort)
}

if ($StartStreamlit) {
    Start-Process -FilePath 'powershell.exe' -ArgumentList @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-NoExit',
        '-Command',
        "Set-Location '$repoRoot'; & '$pythonExe' -m streamlit run dashboard_ui.py --server.port $StreamlitPort"
    ) | Out-Null
    Write-Host ('[OK] Streamlit start angefordert (Port {0}).' -f $StreamlitPort)
}

# Start C# App (separates Fenster)
Start-Process -FilePath 'dotnet' -WorkingDirectory $repoRoot -ArgumentList @(
    'run', '--project', '🤖ROBOTER_KI_APP.csproj'
) | Out-Null

Write-Host '[OK] C# App start angefordert.'
Write-Host 'Hinweis: Node wird von der App selbst gestartet (nicht separat starten).'

if ($RunHealthCheck) {
    Start-Sleep -Seconds 2
    $healthScript = Join-Path $repoRoot 'scripts/health_check.ps1'
    & 'powershell.exe' -NoProfile -ExecutionPolicy Bypass -File $healthScript -PublicPort $PublicPort
    Write-Host "\nWenn die App auf einen anderen Port ausweicht, rerun:"
    Write-Host '  powershell -NoProfile -ExecutionPolicy Bypass -File scripts/health_check.ps1 -PublicPort <PORT>'
}
