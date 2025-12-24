1. Previous Conversation  
   - Focus moved from an earlier Git rebase to documenting the MEGA-ULTRA-ROBOTER-KI production workflow.  
   - README.md now explains the launcher-driven install (`START_INSTALL.bat`), dashboard start, and webhook ingestion pipeline.  
   - Repository hygiene (git remotes, `.vscode` settings, tracked files) was validated so teammates like Kilo can work safely in VS Code.

2. Current Work  
   - Branch `worktree-2025-12-23T21-57-39` is clean; README.md, launcher scripts, and VS Code tasks reflect the current system.  
   - `.vscode/tasks.json` provides one-click commands for running the webhook server (strict or DEV), Streamlit dashboard, and webhook load tests.  
   - `git remote -v` shows `mega` as the canonical repo (`cashmoneycolors/-MEGA-ULTRA-ROBOTER-KI.git`) and `origin` as the legacy `quantum-avatar.git`.

3. Key Technical Concepts  
   - Streamlit dashboard (`dashboard_ui.py`) pulls stats from the FastAPI webhook server with fallback to local JSONL.  
   - PayPal webhooks are LIVE-strict by default; DEV mode requires `ALLOW_UNVERIFIED_WEBHOOKS=true`.  
   - Launcher scripts (`START_INSTALL.bat`, `install_launchers.bat`, `INSTALL_NOW.py`) rely on `pywin32` to create desktop/start-menu shortcuts.

4. Relevant Files and Code  
   - `README.md`: Production status, launcher instructions, webhook steps, secret-handling guidance.  
   - `.vscode/tasks.json`: Defines VS Code tasks for running webhook server/dashboards and firing 1/50/10000 webhook test events.  
   - `webhook_server.py`: FastAPI entry point exposing `/health`, `/paypal/webhook`, `/stats`, `/paypal/create-order`, `/paypal/capture-order`.  
   - `dashboard_ui.py`: Streamlit UI locked to LIVE environment, surfacing stats from `/stats` or local JSONL.

5. Problem Solving  
   - Replaced outdated README references to the deprecated launcher with the START_INSTALL-based workflow.  
   - Clarified webhook instructions with numbered steps, strict-mode warning, and env key checklist.  
   - Verified `.vscode` files are purposely tracked so collaborators share identical tasks/extensions.  
   - Workspace search confirms no other files mention the old launcher name; the README is the single source for that setup.

6. Pending Tasks / Next Steps  
   - Coordinate with Kilo via VS Code tasks: run webhook server (8503) + Streamlit dashboard (8502) simultaneously, then use `scripts/send_test_webhook.py` to validate ingest.  
   - If new business modules (`cart.py`, `orders.py`, `products.py`) are ready, add them to git and push to `mega`.  
   - Before deployment, run end-to-end test: `RUN_WEBHOOK_SERVER.bat` + dashboard + webhook load (50x/10000x) to confirm stats aggregation and AI prompts behave as expected.  
   - Current `git status -sb` shows this summary file as the only pending change; commit once the notes look good.
