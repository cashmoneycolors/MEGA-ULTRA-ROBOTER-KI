# Copilot Instructions – Autonomous Zenith Optimizer

## Architecture Map
- `start_system.py` is the golden path: load config via `python_modules/config_manager.py`, fetch prices (`market_integration.py`), inspect rigs (`nicehash_integration.py`), then broadcast alerts.
- Domain logic lives in `python_modules/` and exposes `run()`/`main()`; register dashboard-visible modules through `python_modules/module_registry.py` and surface metadata via `docs/module_inventory_38_modules.txt` when adding features.
- `.NET` services in `ZenithCoreSystem/` plus contracts under `Core/*.cs` keep Redis workers alive; ensure DTOs stay compatible with Python producers such as `python_modules/mining_system_max_profit_optimizer.py` and `ZenithCoreSystem/ZenithController.cs`.
- Operational playbooks inside `Kontrollzentrum/` (`README_START_HERE_FIRST.md`, `MASTER_COMPLETE_PROJECT_INTEGRATION.md`, `update_integration.py`) describe orchestrated business flows—update them whenever entrypoints or KPIs move.

## Runtime & Orchestration
- `MASTER_PHASE_ORCHESTRATOR.py` sequences diagnostic phases (`PHASE_1_ERROR_SCAN.py`, extend `PHASES` array) before `final_system_validation.py`; plug new health checks there instead of writing ad-hoc batch files.
- `desktop_app*.py`, `start_production_system.py`, and `MASTER_PHASES_RUN.bat` all rely on the same ConfigManager and alert stack; keep feature flags centralized in `settings.json`.
- Alerts funnel through `python_modules/alert_system.send_system_alert` and escalate via `auto_error_fixing_system.py`; channel-specific code belongs there, not inside modules.
- Backup/report tooling: `auto_backup.py`, `system_backup_script.py`, and timestamped folders under `backups/` + `optimization_reports/`. Do not rename assets referenced in `repo_recovery_steps.local.md` or `BACKUP_config_file_list.txt`.

## Modul-Onboarding
- Neue Module unter `python_modules/` ablegen, `run()` bereitstellen und sich in `module_registry.py` (oder `module_counter.py` + `docs/module_inventory_38_modules.txt`) eintragen.
- Konfiguration: benötigte Settings zuerst in `settings.json` dokumentieren, dann optionale `.env`-Platzhalter (`${VAR}`) via `ConfigManager` referenzieren.
- UI-/Dashboard-Integration: Metadaten in `Kontrollzentrum/README_START_HERE_FIRST.md` ergänzen und ggf. `module_dashboard.py` erweitern, damit das Modul in den FastAPI-/Streamlit-Ansichten sichtbar wird.
- Vor Merge: `python module_counter.py` laufen lassen (Registry-Abgleich) und prüfen, ob Backups/Docs (`MASTER_COMPLETE_PROJECT_INTEGRATION.md`) den neuen Modulstatus reflektieren.

## Build & Test Workflow
- Environment: `python -m venv .venv`, activate, `pip install -r requirements.txt`; demo fallbacks exist but CI expects the full dependency set (see `requirements.txt`).
- Launch commands: `python start_system.py` (integrated run), `python MASTER_PHASE_ORCHESTRATOR.py` (phased validation), `python final_system_validation.py` (pre-release proof), `python module_counter.py` (registry sanity check).
- Tests mirror `.github/workflows/dotnet.yml`: `python -m unittest discover tests/python` for Python, logs land in `tests/logs/`; `dotnet restore/build/test AutonomousZenithOptimizer.sln --configuration Release --collect:"XPlat Code Coverage"` for .NET.
- Run `fix_csharp_projects.py`/`.ps1` before `dotnet` builds if csproj references drift, and capture artifacts noted in `tests/complete_test_results_*.log` when debugging CI.

## Test-Abkürzungen & Checks
- Schnelle Modulprüfung: `python tests/python/test_mining_system.py -k <ModulName>` oder individuelle `pytest`-Runs (lokal) vor den offiziellen `unittest`-Durchläufen.
- Smoke-Test: `python start_system.py --dry-run` (Flag in ConfigManager gesetzt) kombiniert Marktdaten, Rig-Check und Alerts ohne Mining-Auslösung.
- Before/After Vergleiche: `python PHASE_1_ERROR_SCAN.py` erzeugt `error_scan_report.txt`; `python final_system_validation.py --export logs/final_validation.json` liefert diffbare Artefakte.
- Für Notebooks/Dashboards: `streamlit run python_modules/dashboard_modul.py` (wenn vorhanden) nur nach erfolgreichem `module_counter`-Check starten, um Registry-Fehler früh zu erkennen.

## Patterns & Configuration
- `settings.json` + `.env` + `${VAR}` placeholders resolved inside `ConfigManager`; never hardcode API keys—`module_utils.warn_if_demo_mode()` and `ConfigManager.env_vars` expose missing secrets clearly.
- External calls should reuse helpers: caching/retries in `market_integration.py`, strategy selection in `algorithm_switcher.py`, proxy routing in `cloud_autoscaling.py`. New connectors should extend these utilities.
- Rig dict contract from `nicehash_integration.py` is `{id, algorithm, power_limit, efficiency}`; `start_system.py`, `algorithm_optimizer.py`, and dashboards expect those keys.
- Logging: background daemons use `python_modules/enhanced_logging.py` (writes to `logs/`), Streamlit/FastAPI surfaces (`dashboard_modul.py`, `module_dashboard.py`) stick to emoji-rich `print`/Streamlit components for operator clarity.

## Integrations & Ops
- NiceHash + market feeds drive AI brains (`deepseek_mining_brain.py`, `mining_system_max_profit_optimizer.py`, `QUANTUM_OPTIMIZATION_RUNNER.py`); coordinate schema changes across these files and `docs/PROJECT_FINAL_SUMMARY.md` before deployment.
- AI agents (`blackbox_ai_modul.py`, `ki_core_modul.py`, `ai_converter_modul.py`) and automation scripts (`autonomous_execution_system.py`) call models via `OllamaProxyServer`/HTTP proxies defined in `cloud_autoscaling.py`; extend those clients when onboarding new providers.
- Commercial tooling (`stripe_payment_handler.py`, `commercial_subscription_system.py`, `marketing_campaign_launcher.py`) shares data contracts with `commercial_launch_demo.py`; update all consumers when adding payment fields.
- Quality gates: run `python PHASE_1_ERROR_SCAN.py` to regenerate `error_scan_report.txt`, then `python final_system_validation.py` for readiness; attach both artifacts to PRs touching cross-cutting flows. Keep recovery PS scripts in `tools/` aligned with manifest files in `Kontrollzentrum/`.
