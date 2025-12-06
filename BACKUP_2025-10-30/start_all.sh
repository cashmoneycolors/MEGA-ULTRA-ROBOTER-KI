#!/usr/bin/env bash
# Startet Backend, Frontend und prüft Healthcheck
set -e

echo "[1/3] Starte Backend & Frontend (Docker Compose) ..."
docker-compose up -d
sleep 5

echo "[2/3] Healthcheck Backend ..."
curl -fsS http://localhost:8080/healthz && echo "OK: Backend Healthcheck erfolgreich" || echo "WARN: Backend Healthcheck fehlgeschlagen"

echo "[3/3] Starte Frontend (React) ..."
cd ZENITH_FRONTEND
npm install
npm start
