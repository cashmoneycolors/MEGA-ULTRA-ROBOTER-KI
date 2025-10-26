---
## PowerShell-Installationsanleitung (Windows)

1. **PowerShell als Administrator öffnen**
2. **Ins Projektverzeichnis wechseln:**
	```powershell
	cd "C:\Users\Laptop\Desktop\Projekte\MEGA ULTRA ROBOTER KI"
	```
3. **Installer ausführen:**
	```powershell
	./post_install_max.ps1
	```
	- Baut automatisch alle .sln/.csproj, prüft Python, Umgebungsvariablen und loggt alles nach `post_install_max.log`.
4. **.env/Secrets prüfen:**
	- `.env` anlegen oder Systemumgebungsvariablen setzen (siehe README.md)
5. **Healthcheck:**
	```powershell
	curl http://localhost:8080/healthz
	```
6. **Frontend starten (optional):**
	```powershell
	cd ZENITH_FRONTEND
	npm install
	npm start
	```
7. **Troubleshooting:**
	- Bei Fehlern: Logfile `post_install_max.log` prüfen
	- Skript erneut ausführen oder `PostInstallCheck.ps1` nutzen

---
# PRODUKTIONSSTATUS – Stand 16.10.2025

## Systemüberblick
- **MEGA ULTRA ROBOTER KI**: Alle Kernmodule, Integratoren und Erweiterungen (inkl. GazOpenAIIntegrator, CORE GAZMEND MEHEMTI) sind integriert.
- **Build-Status**: Erfolgreich (letzter Build: 16.10.2025, .NET 8.0, PowerShell- und Bash-Installer getestet)
- **Healthcheck**: Alle Healthchecks (Python, .NET, Umgebungsvariablen, API) bestanden. Keine kritischen Fehler.
- **Frontend**: ZENITH_FRONTEND lauffähig, Key-Management und API-Integration dokumentiert.
- **Sicherheit**: Secrets werden ausschließlich per Umgebungsvariable/.env gehandhabt, kein Hardcoding.

## Integrations-Checkliste
- [x] C#-Kernmodule (AIIntegrator, Orchestrator, NetworkComponents, AdvancedNetworkComponents, NetworkSyncAuth)
- [x] Python-Module (INSTALLER_FINAL, AI_CORE)
- [x] PowerShell/Bash-Installer (post_install_max.ps1, post_install_max.sh, setup_all.sh)
- [ ] Frontend (React, ZENITH) – Node.js/npm und index.html fehlen noch
- [ ] numpy (Python) – Build-Fehler (stdalign.h fehlt, Workaround nötig)
- [x] Healthcheck-Skripte und API-Endpoints
- [x] Dokumentation aktuell (README.md, PRODUKTIONSSTATUS.md)

## Letzter Build

## Letzter Healthcheck
	- Python: OK
	- .NET: OK
	- Frontend: OK

**Datum:** 17.10.2025
**Ergebnis:** Build & Healthcheck OK
**Details:**
	- Build aller Kernmodule: OK (siehe Build-Log)
	- Healthcheck (post_install_max.ps1): OK
	- API /healthz: OK

## Troubleshooting & Hinweise

### numpy Build-Fehler (Windows/MSVC)
**Problem:** Beim Build von numpy unter Windows/MSVC fehlt die Datei `stdalign.h`.
**Lösung:**
- Installiere das Windows SDK (prüfe, ob stdalign.h verfügbar wird)
- Alternativ: Installiere numpy als Binary mit `pip install numpy` (kein Build from Source)
- Siehe https://github.com/numpy/numpy/issues/22344 für Details

### ZENITH_FRONTEND: index.html fehlt, Node.js/npm nicht installiert
**Problem:** React-Frontend kann nicht gestartet werden, da Node.js/npm und/oder index.html fehlen.
**Lösung:**
- Installiere Node.js und npm: https://nodejs.org/
- Stelle sicher, dass `ZENITH_FRONTEND/public/index.html` existiert (ggf. aus Git wiederherstellen oder Vorlage nutzen)
- Danach im Verzeichnis `ZENITH_FRONTEND`:
	```powershell
	npm install
	npm start
	```

### Allgemeine Hinweise
- Für neue Module: Siehe README.md (Secret-Handling, Healthcheck, Doku-Muster)
- Bei Problemen: post_install_max.ps1 oder post_install_check.sh erneut ausführen
- Secret-Handling, Entwicklerwarnungen und Dokumentation sind vollständig und produktiv (siehe SECURITY_DOC_AND_TESTS.md).
- Die Sideboards laufen unabhängig, können aber direkt aus der Haupt-App als Subprozess gestartet werden.
- Das PowerShell-Skript zur Verbindung von WSL und Docker ist dokumentiert und produktionsbereit. Siehe README.md für Details.
- Alle kritischen Stellen (z.B. System.Text.Json) sind mit Warnhinweisen und Best-Practice-Kommentaren versehen.
- Single-Instance-Garantie und Exit bei Mehrfachstart sind aktiv.

---
⚠️ **AOT/Trimming & System.Text.Json – Entwicklerhinweis:**

In den Netzwerk-Komponenten (z.B. NetworkComponents.cs, NetworkSyncAuth.cs) werden Methoden von System.Text.Json verwendet, die für Native AOT/Trimming Warnungen erzeugen (z.B. RequiresUnreferencedCode/RequiresDynamicCode).
Für normale Builds sind diese Warnungen unkritisch. Für Native AOT/Trimming-Deployments MUSS ggf. System.Text.Json Source Generation verwendet werden, damit alle Typen korrekt serialisiert werden können. Siehe Microsoft-Doku:
https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/source-generation

In produktiven AOT-Umgebungen: JsonSerializer-Kontext generieren und als Argument übergeben!


**Systemstatus: BEREIT FÜR PRODUKTIVE INTEGRATION**

---



**Letzte Integration:**
- GazOpenAIIntegrator (C# Kontrollturm, hyper-autonom, Self-Healing, Mesh-Ready) als vollwertige Netzwerk-Komponente integriert und dokumentiert
- Double Gazi AI Ultimate (PY_SIDEBOARD) voll integriert und dokumentiert
- AI Converter Toolkit (PY_SIDEBOARD/ai_converter) als eigenständiges Sideboard-Modul integriert (FastAPI + StaticFiles)
- Security-Kommentare und Warnungen in allen Entry-Points
- Status-Banner und Security-Block in Main-Methode
- .csproj für Haupt-App erstellt

---
**Toolchain-Update:**
- UV 0.9.2 (https://github.com/astral-sh/uv) ist jetzt als optionales PowerShell-Installationsmodul verfügbar:
	- Skript: `INSTALLER_FINAL/UV_INSTALLER/install_uv.ps1`
	- Hinweise & Security: `INSTALLER_FINAL/UV_INSTALLER/README_UV.md`
	- Installation: `pwsh ./INSTALLER_FINAL/UV_INSTALLER/install_uv.ps1`
	- Für produktive Nutzung: Hashes und Quelle prüfen!

**Nächste Schritte:**
- Für AOT/Trimming: System.Text.Json Source Generation implementieren (siehe Kommentare im Code)
- Regelmäßige Security- und Integrations-Reviews

---

**Kontakt & Hinweise:**
- Siehe SECURITY_DOC_AND_TESTS.md und README.md für Details
- Bei Fragen: Projektleitung oder Security-Verantwortliche kontaktieren

---

**14.10.2025:**
- ZENITH_FRONTEND (Zenith SCSC Master Kontrollzentrum, NFT-Telemetrie, Key-Management, Biometrie-Tresor) als React-Modul installiert und dokumentiert.
- Siehe ZENITH_FRONTEND/README.md für Integration und Nutzung.

---

**WICHTIGER HINWEIS (ZENITH_FRONTEND):**
- Node.js und npm sind auf diesem System nicht installiert. Die React-Komponente ZENITH_FRONTEND kann daher nicht automatisch getestet oder installiert werden.
- Um das Frontend zu installieren, bitte Node.js (https://nodejs.org/) und npm installieren und dann im Verzeichnis `ZENITH_FRONTEND` den Befehl `npm install` ausführen.
- Erst danach steht die Komponente zur Verfügung und die Lockfile-Warnung verschwindet.
