# Startet Backend, Frontend und prüft Healthcheck (Windows)
Write-Host "[1/3] Starte Backend & Frontend (Docker Compose) ..."
docker-compose up -d
Start-Sleep -Seconds 5

Write-Host "[2/3] Healthcheck Backend ..."
try {
  $resp = Invoke-WebRequest -Uri "http://localhost:8080/healthz" -UseBasicParsing -TimeoutSec 5
  if ($resp.StatusCode -eq 200) { Write-Host "OK: Backend Healthcheck erfolgreich" }
  else { Write-Host "WARN: Backend Healthcheck fehlgeschlagen ($($resp.StatusCode))" }
} catch {
  Write-Host "WARN: Backend Healthcheck fehlgeschlagen ($_)."
}

Write-Host "[3/3] Starte Frontend (React) ..."
Push-Location ZENITH_FRONTEND
npm install
npm start
Pop-Location
