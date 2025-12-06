# Backend & Frontend bauen
docker-compose up -d
# Healthcheck prüfen
curl http://localhost:8080/healthz# === post_install_check.sh (Linux, ausführbar machen mit chmod +x) ===
#!/usr/bin/env bash
set -euo pipefail

PACKAGES=(curl git unzip tesseract-ocr python3 python3-pip docker)
SERVICES=(ssh docker)
FILES_TO_CHECK=(
  "/usr/local/bin/meinprogramm"
  "/etc/meinprogramm/config.yaml"
)
CHECKSUMS=(
  "/tmp/meinprogramm.tar.gz:abc123def4567890abcdef1234567890"
)
UNIT_TEST_CMD="pytest"
APP_USER="www-data"

echo_h() { echo -e "\n=== $* ==="; }

echo_h "Prüfe installierte Pakete"
if command -v dpkg >/dev/null 2>&1; then
  for p in "${PACKAGES[@]}"; do
    if dpkg -s "$p" >/dev/null 2>&1; then
      echo "OK: Paket $p ist installiert"
    else
      echo "MISSING: Paket $p fehlt"
    fi
  done
else
  echo "Keine dpkg/apt Umgebung erkannt — überspringe Paketprüfung"
fi

echo_h "Prüfe Dienste (systemd)"
if command -v systemctl >/dev/null 2>&1; then
  for s in "${SERVICES[@]}"; do
    if systemctl is-enabled --quiet "$s" 2>/dev/null && systemctl is-active --quiet "$s" 2>/dev/null; then
      echo "OK: Dienst $s ist aktiv und enabled"
    else
      echo "WARN: Dienst $s ist nicht aktiv / nicht enabled"
      systemctl status "$s" --no-pager || true
    fi
  done
else
  echo "Kein systemd erkannt — überspringe Dienstprüfung"
fi

echo_h "Prüfe Dateien"
for f in "${FILES_TO_CHECK[@]}"; do
  if [ -e "$f" ]; then
    echo "OK: $f vorhanden ($(stat -c '%s bytes' "$f"))"
  else
    echo "MISSING: $f nicht gefunden"
  fi
done

echo_h "Prüfe Checksummen"
for entry in "${CHECKSUMS[@]}"; do
  IFS=':' read -r path expect <<< "$entry"
  if [ -f "$path" ]; then
    got=$(sha256sum "$path" | awk '{print $1}')
    if [ "$got" = "$expect" ]; then
      echo "OK: $path Prüfsumme stimmt"
    else
      echo "FAIL: $path Prüfsumme stimmt NICHT (erwartet $expect, gefunden $got)"
    fi
  else
    echo "MISSING: $path nicht vorhanden"
  fi
done

echo_h "Prüfe Eigentümer"
for f in "${FILES_TO_CHECK[@]}"; do
  if [ -e "$f" ]; then
    owner=$(stat -c '%U' "$f")
    echo "$f : Besitzer=$owner"
    if [ "$owner" != "$APP_USER" ]; then
      echo "WARN: $f sollte $APP_USER gehören (ist $owner)"
    fi
  fi
done

echo_h "Führe Unit-Tests aus (falls konfiguriert)"
if command -v bash >/dev/null 2>&1 && [ -n "${UNIT_TEST_CMD:-}" ]; then
  if eval "$UNIT_TEST_CMD"; then
    echo "OK: Unit-Tests erfolgreich"
  else
    echo "FAIL: Unit-Tests nicht bestanden"
  fi
fi

echo_h "Simple HTTP-Healthcheck (localhost:8080)"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS --max-time 5 http://127.0.0.1:8080/healthz >/dev/null; then
    echo "OK: Health endpoint antwortet"
  else
    echo "WARN/FAIL: Health endpoint nicht erreichbar"
  fi
fi

echo_h "Fertig: Post-install Prüfung beendet"
exit 0# === PostInstallCheck.ps1 (Windows, als Admin ausführen) ===
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

Write-Host "nFertig."docker-compose up -d# Backend & Frontend bauen
docker-compose up -d
# Healthcheck prüfen
curl http://localhost:8080/healthz