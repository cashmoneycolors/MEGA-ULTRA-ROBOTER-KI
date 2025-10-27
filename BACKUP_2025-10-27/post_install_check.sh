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
exit 0
