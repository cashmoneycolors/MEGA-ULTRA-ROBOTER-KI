# Copilot Instructions (MEGA-ULTRA-ROBOTER-KI)

## Architektur (wichtigster Pfad)
- Primärer Datenpfad ist **Webhook-Ingest → JSONL → Dashboard** (kein Reporting-API Polling im Dashboard; Webhooks funktionieren auch ohne Reporting-Permissions).
- Webhook-Receiver: FastAPI/uvicorn in `webhook_server.py`. Dashboard: Streamlit in `dashboard_ui.py`.

## Entry Points
- Webhook Server: `webhook_server.py` (lokal i.d.R. Port 8503; in Cloud via `PORT`).
- Dashboard: `dashboard_ui.py` (Port 8502).
- Ingest-Test (ohne PayPal-Signatur-Header): `scripts/send_test_webhook.py`.
- `main.py` ist nur Smoke/Beispiel; ältere Flows (`new_dashboard.py`, `paypal_maximizer.py`) nur anfassen, wenn explizit gewünscht.

## Lokaler Workflow (Windows)
- VS Code Tasks (empfohlen): siehe `.vscode/tasks.json` (Run Webhook Server, Run Streamlit Dashboard, Send Test Webhook).
- Start:
  - `python webhook_server.py` → `GET http://127.0.0.1:8503/health`
  - `python -m streamlit run dashboard_ui.py --server.port 8502`
- Test-Ingest: `python scripts/send_test_webhook.py` (postet an `http://127.0.0.1:8503/paypal/webhook`).

## Datenmodell & Persistenz
- Lokale Persistenz ist JSONL: `data/paypal_events.jsonl` (override via `PAYPAL_EVENTS_PATH`).
- Record-Shape (aus `persist_event`): `{ received_at, event_id, event, amount?, estimated_fee?, estimated_net? }`.
- `GET /stats?limit=N` aggregiert die **lokale** JSONL (Default: alle Lines). Azure Blob ist optional/best-effort und wird von `/stats` nicht gelesen.

## PayPal Verifikation & Testmodus
- `/paypal/webhook` verifiziert Signatur nur, wenn PayPal-Header vorhanden sind; sonst wird `_verified: false` gesetzt (lokaler Testmodus).
- Optionaler Fee-Heuristik-Output für `estimated_net`: `EST_PAYPAL_FEE_PCT`, `EST_PAYPAL_FEE_FIXED`, `EST_PAYPAL_FEE_CCY`.

## Konfiguration/Secrets
- Keys werden aus `env.ini`, `.env`, dann Environment geladen; **niemals committen**.
- LIVE/SANDBOX: `PAYPAL_ENV` oder `ENV`.
- Webhook-Verifikation braucht: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID` (bzw. SANDBOX-Varianten).
- Localhost-Checkout kann Captures als Event persistieren: `PERSIST_CAPTURE_AS_EVENT=true`.

## Repo-Konventionen
- Viele `*.bak` Dateien im Root: nur die “aktive” Datei ändern.
- `manifest.json` wirkt wie generiertes Asset-Mapping: nicht manuell bearbeiten.
- Keine Testsuite: Änderungen über `/health`, `/stats` und Test-Webhooks validieren.
