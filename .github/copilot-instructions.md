# Copilot Instructions (MEGA-ULTRA-ROBOTER-KI)

## Big Picture
- Kernpfad ist **PayPal Webhook → JSONL → /stats → Streamlit Dashboard** (kein Reporting-API Polling). Siehe [webhook_server.py](../webhook_server.py) und [dashboard_ui.py](../dashboard_ui.py).
- Webhook-Server (FastAPI) bietet: `/health`, `/paypal/webhook`, `/stats`, `/paypal/create-order`, `/paypal/capture-order`.
- Dashboard (Streamlit, Port 8502) liest Umsatz aus `/stats` via `PAYPAL_STATS_URL` oder `PAYPAL_INGEST_BASE_URL` (Fallback: lokale JSONL).

## Lokales Starten
- Empfohlen: VS Code Tasks in [.vscode/tasks.json](../.vscode/tasks.json) (Webhook/Dashboard + DEV Tasks).
- Manuell: `python webhook_server.py` (Port via `WEBHOOK_PORT`/`PORT`, default 8503) und `python -m streamlit run dashboard_ui.py --server.port 8502`.

## Webhook-Verifikation (LIVE-strikt)
- Default: `/paypal/webhook` akzeptiert **nur** Requests mit PayPal-Signatur-Headern; sonst HTTP 400.
- DEV-only: `ALLOW_UNVERIFIED_WEBHOOKS=true` erlaubt unsigned lokale Requests und markiert `_verified: false`.
- Das Script [scripts/send_test_webhook.py](../scripts/send_test_webhook.py) ist **DEV-only** (ohne Signatur-Header; gegen strict-mode wird es abgewiesen).

## Persistenz & Stats
- Events werden append-only als JSONL gespeichert: `data/paypal_events.jsonl` (override: `PAYPAL_EVENTS_PATH`). Record-Shape kommt aus `persist_event` in [webhook_server.py](../webhook_server.py).
- `/stats?limit=N` aggregiert **nur** die lokale JSONL (Blob-Backup ist optional/best-effort; wird nicht gelesen).

## Konfiguration & Repo-Konventionen
- Secrets niemals committen: nutze `env.ini`/Environment; Vorlage: [.env.example](../.env.example). Pflicht für echte Verifikation: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID` (Sandbox-Varianten bei `PAYPAL_ENV=SANDBOX`).
- Viele `*.bak` im Root; nur aktive Dateien pflegen. [manifest.json](../manifest.json) wirkt generiert → nicht editieren.

## Deploy (24/7 Webhook Receiver)
- Azure Container Apps: Einstieg über [azure/README.md](../azure/README.md) und Script [azure/aca_deploy.ps1](../azure/aca_deploy.ps1).
