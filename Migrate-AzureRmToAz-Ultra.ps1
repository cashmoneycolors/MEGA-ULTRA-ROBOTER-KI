param(
  [Parameter(Mandatory=$false)]
  [string]$SourcePath,

  [string]$FromAzureRmVersion = "6.13.1",
  [string]$ToAzVersion = "latest",

  [string]$GrokApiKey = $env:GROK_API_KEY,
  [string]$DeepSeekApiKey = $env:DEEPSEEK_API_KEY,

  [string]$GrokModel = "grok-beta",
  [string]$DeepSeekModel = "deepseek-chat",

  [int]$MaxRetries = 5,
  [int]$BaseDelaySeconds = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-WithRetry {
  param(
    [Parameter(Mandatory=$true)][scriptblock]$Action,
    [Parameter(Mandatory=$true)][string]$Name,
    [string]$Id = ""
  )

  for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
    try { return & $Action }
    catch {
      if ($attempt -ge $MaxRetries) { throw }
      $jitter = (Get-Random -Minimum 0 -Maximum 1500) / 1000.0
      $sleep = [math]::Round(($BaseDelaySeconds * [math]::Pow(2, $attempt-1)) + $jitter, 2)
      Write-Warning "Retry $attempt/$MaxRetries: $Name $Id (warte $sleep s)  $($_.Exception.Message)"
      Start-Sleep -Seconds $sleep
    }
  }
}

function Ensure-Module {
  param([Parameter(Mandatory=$true)][string]$Name)
  if (-not (Get-Module -ListAvailable -Name $Name)) {
    Write-Host "Installiere PowerShell Modul: $Name" -ForegroundColor Yellow
    Invoke-WithRetry -Name "Install-Module" -Id $Name -Action {
      Install-Module -Name $Name -Scope CurrentUser -Force -AllowClobber
    } | Out-Null
  }
  Import-Module $Name -Force
}

function Strip-CodeFences([string]$text) {
  if (-not $text) { return $text }
  $t = $text.Trim()
  if ($t -match '^```') {
    $t = $t -replace '^```[a-zA-Z]*\s*', ''
    $t = $t -replace '\s*```$', ''
  }
  return $t.Trim()
}

function Invoke-Grok {
  param([string]$Prompt)

  if (-not $GrokApiKey) { return $null }

  $body = @{ 
    model = $GrokModel
    messages = @(@{ role="user"; content=$Prompt })
    max_tokens = 2200
    temperature = 0
  } | ConvertTo-Json -Depth 10

  $resp = Invoke-WithRetry -Name "Grok API" -Action {
    Invoke-RestMethod -Uri "https://api.x.ai/v1/chat/completions" -Method Post -Body $body -ContentType "application/json" -Headers @{ Authorization = "Bearer $GrokApiKey" } -TimeoutSec 90
  }

  return Strip-CodeFences $resp.choices[0].message.content
}

function Invoke-DeepSeek {
  param([string]$Prompt)

  if (-not $DeepSeekApiKey) { return $null }

  $body = @{ 
    model = $DeepSeekModel
    messages = @(@{ role="user"; content=$Prompt })
    max_tokens = 2200
    temperature = 0
  } | ConvertTo-Json -Depth 10

  $resp = Invoke-WithRetry -Name "DeepSeek API" -Action {
    Invoke-RestMethod -Uri "https://api.deepseek.com/v1/chat/completions" -Method Post -Body $body -ContentType "application/json" -Headers @{ Authorization = "Bearer $DeepSeekApiKey" } -TimeoutSec 90
  }

  return Strip-CodeFences $resp.choices[0].message.content
}

function Resolve-SourcePath {
  param([string]$InputPath)

  $candidates = @()

  if ($InputPath) { $candidates += $InputPath }

  if ($env:AZ_MIGRATION_SOURCEPATH) { $candidates += $env:AZ_MIGRATION_SOURCEPATH }
  if ($env:AZURE_MIGRATION_SOURCEPATH) { $candidates += $env:AZURE_MIGRATION_SOURCEPATH }

  $candidates += (Join-Path $PSScriptRoot 'Scripts')
  $candidates += (Join-Path $PWD 'Scripts')
  $candidates += (Join-Path $PSScriptRoot 'AzureScripts')

  foreach ($p in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
    if (Test-Path $p) {
      return (Resolve-Path $p).Path
    }
  }

  # Auto-Detect: finde Ordner mit AzureRm in *.ps1 (nur begrenzter Scan)
  $scanRoot = $PWD
  $hits = @()
  try {
    $files = Get-ChildItem -Path $scanRoot -Recurse -File -Filter '*.ps1' -ErrorAction SilentlyContinue | Select-Object -First 250
    foreach ($f in $files) {
      $txt = Get-Content -Path $f.FullName -Raw -ErrorAction SilentlyContinue
      if ($txt -match '\bAzureRm\b' -or $txt -match '\bAzureRM\b') {
        $hits += (Split-Path $f.FullName -Parent)
      }
    }
  } catch {}

  $uniqueHitDirs = $hits | Where-Object { $_ } | Select-Object -Unique
  if ($uniqueHitDirs.Count -eq 1) {
    return (Resolve-Path $uniqueHitDirs[0]).Path
  }

  # Interaktiv fragen
  Write-Host "Ich brauche den Ordner mit deinen AzureRM-Skripten (.ps1)." -ForegroundColor Yellow
  Write-Host "Tipp: Lege z.B. einen Ordner 'Scripts' an und kopiere deine .ps1 dort rein." -ForegroundColor Yellow

  while ($true) {
    $typed = Read-Host "Bitte SourcePath eingeben (Ordnerpfad)"
    if ($typed -and (Test-Path $typed)) {
      return (Resolve-Path $typed).Path
    }
    Write-Warning "Pfad existiert nicht: $typed"
  }
}

# ---- Setup Output ----
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Root = Join-Path $PSScriptRoot "AzureMigration-$timestamp"
$Dirs = @(
  "Originals","WorkingCopy","Plans","Upgrades","Errors","AICorrections","Reports"
) | ForEach-Object { Join-Path $Root $_ }

$null = New-Item -ItemType Directory -Path $Root -Force
$Dirs | ForEach-Object { $null = New-Item -ItemType Directory -Path $_ -Force }

$SourcePath = Resolve-SourcePath -InputPath $SourcePath
Write-Host "Quelle: $SourcePath" -ForegroundColor Cyan
Write-Host "Output: $Root" -ForegroundColor Green

# ---- Install needed module ----
Ensure-Module -Name "Az.Tools.Migration"

# ---- Backup originals + working copy (Windows: robocopy) ----
$origDest = Join-Path $Root "Originals"
$workDest = Join-Path $Root "WorkingCopy"

Write-Host "Backup Originals  $origDest" -ForegroundColor Cyan
Invoke-WithRetry -Name "Backup Originals" -Action {
  robocopy $SourcePath $origDest /E /R:2 /W:2 /NFL /NDL /NJH /NJS | Out-Null
  if ($LASTEXITCODE -gt 7) { throw "robocopy code $LASTEXITCODE" }
}

Write-Host "Erzeuge WorkingCopy  $workDest" -ForegroundColor Cyan
Invoke-WithRetry -Name "Create WorkingCopy" -Action {
  robocopy $SourcePath $workDest /E /R:2 /W:2 /NFL /NDL /NJH /NJS | Out-Null
  if ($LASTEXITCODE -gt 7) { throw "robocopy code $LASTEXITCODE" }
}

# ---- Plan ----
Write-Host "Erzeuge Upgrade-Plan (AzureRM  Az)..." -ForegroundColor Cyan
$plan = New-AzUpgradeModulePlan -FromAzureRmVersion $FromAzureRmVersion -ToAzVersion $ToAzVersion -DirectoryPath $workDest

$planJson = Join-Path $Root "Plans\plan.json"
$plan | ConvertTo-Json -Depth 20 | Out-File -FilePath $planJson -Encoding UTF8

$planIssues = $plan | Where-Object { $_.PlanResult -ne "ReadyToUpgrade" }
$planIssuesPath = Join-Path $Root "Errors\plan-issues.txt"
$planIssues | Format-List | Out-File -FilePath $planIssuesPath -Encoding UTF8

Write-Host ("Plan gespeichert: {0}" -f $planJson) -ForegroundColor Gray
Write-Host ("Plan-Issues:      {0} (Count={1})" -f $planIssuesPath, ($planIssues | Measure-Object).Count) -ForegroundColor Gray

# ---- Upgrade (non-destructive) ----
Write-Host "Führe Upgrade aus (SaveChangesToNewFiles)..." -ForegroundColor Cyan
$results = Invoke-AzUpgradeModulePlan -Plan $plan -FileEditMode SaveChangesToNewFiles

$resultsJson = Join-Path $Root "Reports\upgrade-results.json"
$results | ConvertTo-Json -Depth 20 | Out-File -FilePath $resultsJson -Encoding UTF8

# ---- Collect upgraded files (from WorkingCopy) ----
$upgradesDest = Join-Path $Root "Upgrades"
$upgraded = Get-ChildItem -Path $workDest -Recurse -File -Filter "*_az_upgraded*" -ErrorAction SilentlyContinue

if ($upgraded.Count -gt 0) {
  Write-Host "Sammle _az_upgraded Dateien  $upgradesDest" -ForegroundColor Cyan
  foreach ($f in $upgraded) {
    $target = Join-Path $upgradesDest $f.Name
    Copy-Item -Path $f.FullName -Destination $target -Force
  }
} else {
  Write-Warning "Keine _az_upgraded Dateien gefunden (evtl. keine PS1-Dateien / keine ersetzbaren Cmdlets)."
}

# ---- Errors ----
$upgradeErrors = $results | Where-Object { $_.UpgradeResult -ne "UpgradeCompleted" }
$upgradeErrorsJson = Join-Path $Root "Errors\upgrade-errors.json"
$upgradeErrors | ConvertTo-Json -Depth 20 | Out-File -FilePath $upgradeErrorsJson -Encoding UTF8

Write-Host ("Upgrade Errors: {0}" -f ($upgradeErrors | Measure-Object).Count) -ForegroundColor Yellow
Write-Host ("Errors JSON:    {0}" -f $upgradeErrorsJson) -ForegroundColor Gray

# ---- AI Fix (per file) ----
if (($upgradeErrors | Measure-Object).Count -gt 0 -and ($GrokApiKey -or $DeepSeekApiKey)) {
  Write-Host "Starte AI-Korrektur (Grok  DeepSeek Fallback)..." -ForegroundColor Cyan

  $filesToFix = $upgradeErrors | Select-Object -ExpandProperty FullPath -Unique
  foreach ($origFile in $filesToFix) {
    $origName = Split-Path $origFile -Leaf
    $base = [IO.Path]::GetFileNameWithoutExtension($origName)

    $dir = Split-Path $origFile -Parent
    $candidate = Get-ChildItem -Path $dir -File -Filter ($base + "*_az_upgraded*.ps1") -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $candidate) {
      $candidate = Get-ChildItem -Path $upgradesDest -File -Filter ($base + "*_az_upgraded*.ps1") -ErrorAction SilentlyContinue | Select-Object -First 1
    }

    if (-not $candidate) {
      Write-Warning "Kein upgraded Kandidat gefunden für: $origName (skip)"
      continue
    }

    $code = Get-Content -Path $candidate.FullName -Raw -Encoding UTF8
    $errsForFile = $upgradeErrors | Where-Object { $_.FullPath -eq $origFile } | Select-Object Location, UpgradeType, UpgradeResult, UpgradeResultReason, Original, Replacement

    $prompt = @"
Du bist ein Azure PowerShell Experte (AzureRM -> Az).
Kontext: Az.Tools.Migration Upgrade hatte Fehler in dieser Datei.

DATEI: $origName

FEHLER (aus Invoke-AzUpgradeModulePlan):
$($errsForFile | ConvertTo-Json -Depth 10)

CODE (aktuelle upgraded Datei):
$code

AUFGABE:
- Liefere den vollständigen korrigierten PowerShell-Dateiinhalt.
- Az-kompatibel, kein AzureRM.
- Antworte NUR mit Code (kein Markdown, keine Erklärung).
"@

    $fixed = $null
    try { $fixed = Invoke-Grok -Prompt $prompt } catch { $fixed = $null }
    if (-not $fixed) {
      try { $fixed = Invoke-DeepSeek -Prompt $prompt } catch { $fixed = $null }
    }

    if ($fixed) {
      $out = Join-Path $Root ("AICorrections\{0}_ai_fixed.ps1" -f $base)
      $fixed | Out-File -FilePath $out -Encoding UTF8
      Write-Host "AI-fixed gespeichert: $out" -ForegroundColor Green
    } else {
      Write-Warning "AI konnte nicht fixen: $origName"
    }
  }
} else {
  if (($upgradeErrors | Measure-Object).Count -gt 0) {
    Write-Warning "Es gibt Upgrade-Errors, aber keine API Keys gesetzt (GROK_API_KEY/DEEPSEEK_API_KEY)."
  }
}

# ---- Summary ----
$summary = [PSCustomObject]@{
  Timestamp = (Get-Date).ToString("o")
  SourcePath = $SourcePath
  OutputRoot = $Root
  PlanIssuesCount = ($planIssues | Measure-Object).Count
  UpgradeErrorCount = ($upgradeErrors | Measure-Object).Count
  UpgradedFilesCount = ($upgraded | Measure-Object).Count
  AiFixedFilesCount = (Get-ChildItem -Path (Join-Path $Root "AICorrections") -File -ErrorAction SilentlyContinue | Measure-Object).Count
} | ConvertTo-Json -Depth 5

$summaryPath = Join-Path $Root "Reports\summary.json"
$summary | Out-File -FilePath $summaryPath -Encoding UTF8

Write-Host "`nFERTIG." -ForegroundColor Magenta
Write-Host "Summary:  $summaryPath" -ForegroundColor Gray
Write-Host "Upgrades: $(Join-Path $Root 'Upgrades')" -ForegroundColor Gray
Write-Host "AI-Fixes: $(Join-Path $Root 'AICorrections')" -ForegroundColor Gray
