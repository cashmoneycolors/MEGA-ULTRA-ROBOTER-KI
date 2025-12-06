$Packages = @("git","7zip","python","tesseract")
$Services = @("wuauserv","Spooler")
$Files = @("C:\Program Files\MeinApp\app.exe","C:\ProgramData\MeinApp\config.yml")
$ChecksumList = @{
  "C:\temp\meinapp.zip" = "ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890"
}

Write-Host "=== Dienste prüfen ==="
foreach ($s in $Services) {
  $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
  if ($svc) {
    Write-Host "Dienst $s: Status=$($svc.Status)"
  } else {
    Write-Host "MISSING: Dienst $s nicht gefunden"
  }
}

Write-Host "n=== Dateien prüfen ==="
foreach ($f in $Files) {
  if (Test-Path $f) {
    $size = (Get-Item $f).Length
    Write-Host "OK: $f ($size bytes)"
  } else {
    Write-Host "MISSING: $f"
  }
}

Write-Host "n=== Checksummen (SHA256) ==="
foreach ($k in $ChecksumList.Keys) {
  if (Test-Path $k) {
    $hash = Get-FileHash -Path $k -Algorithm SHA256
    if ($hash.Hash -eq $ChecksumList[$k]) {
      Write-Host "OK: $k Prüfsumme stimmt"
    } else {
      Write-Host "FAIL: $k Prüfsumme stimmt NICHT (gefunden $($hash.Hash))"
    }
  } else {
    Write-Host "MISSING: $k"
  }
}

Write-Host "n=== Optional: HTTP-Healthcheck ==="
try {
  $resp = Invoke-WebRequest -Uri "http://localhost:8080/healthz" -UseBasicParsing -TimeoutSec 5
  if ($resp.StatusCode -eq 200) { Write-Host "OK: Health endpoint antwortet" }
} catch {
  Write-Host "WARN: Health endpoint nicht erreichbar"
}

Write-Host "nFertig."
