pip install streamlit pyserial opencv-python transformers torch torchvision pillow# MEGA ULTRA ROBOTER KI – Schnellstart & Betrieb
#
**Status (16.10.2025):** Alle Kernmodule, Integrationen und Healthchecks erfolgreich. Siehe PRODUKTIONSSTATUS.md für Details zu Build & Healthcheck.

## 1. Start & Healthcheck
## Build & Healthcheck

**Build ausführen:**
```powershell
./AI_CORE/FIX_CSHARP_PROJECTS.ps1
./AI_CORE/RUN_NETWORK_SYSTEM.ps1
# oder direkt:
dotnet build 🤖ROBOTER_KI_APP.csproj
```

**Healthcheck:**
```powershell
./post_install_max.ps1
# oder
./PostInstallCheck.ps1
```

**API-Check:**
Rufe ggf. den Endpoint `/healthz` im laufenden System auf.

**Fehlerbehebung:**
- Prüfe Build-Log und Healthcheck-Ausgabe
- Fehlende Abhängigkeiten nachinstallieren (siehe INSTALL_DEPENDENCIES.ps1)
- Secrets/Umgebungsvariablen prüfen (.env)

**Backend & Frontend starten:**
```sh
docker-compose up -d
```

**Healthcheck prüfen:**
```sh
curl http://localhost:8080/healthz
```

**Frontend lokal (React):**
```sh
cd ZENITH_FRONTEND
npm install
npm start
```

## 2. Secrets & Umgebungsvariablen
- Niemals Secrets/API-Keys im Code speichern!
- Immer per Umgebungsvariable oder `.env` (siehe `.env.example`).
- Für Windows: Systemumgebungsvariablen setzen oder `.env` kopieren.
- Beispiel:
  - Linux/Mac: `export PREMIUM_API_KEY="dein-geheimer-key"`
  - Windows: In Systemsteuerung → Umgebungsvariablen oder `.env` nutzen

## 3. Healthcheck & Installationsprüfung
- **Linux:**
  - `chmod +x post_install_check.sh && sudo ./post_install_check.sh`
- **Windows:**
  - Als Admin: `./PostInstallCheck.ps1`


## 4. Erweiterbarkeit & Support
- Neue Module nach gleichem Muster integrieren (Secret-Handling, Healthcheck, Doku).
- **NEU:** GazOpenAIIntegrator (C# Kontrollturm, hyper-autonom, Self-Healing, Mesh-Ready) ist als Netzwerk-Komponente voll integriert. Siehe PRODUKTIONSSTATUS.md für Details.
- Alle relevanten Doku-Dateien: `SECURITY_DOC_AND_TESTS.md`, `PRODUKTIONSSTATUS.md`, README.
- Für Support oder neue Features: Einfach melden!

## 5. Beispiel-Assets & Testdaten
- Im Ordner `_EXAMPLES` findest du Beispielkonfigurationen, Dummy-API-Keys, Testbilder, PDFs und Demo-Healthcheck-Responses.
- Niemals echte Secrets oder produktive API-Keys dort ablegen!
- Für eigene Tests einfach Dateien ergänzen oder austauschen.

Weitere Details siehe `_EXAMPLES/README.md`.

## 6. Externe Integration: CORE GAZMEND MEHEMTI

## WSL & Docker Integration

Um WSL und Docker unter Windows zu verbinden, kannst du folgendes PowerShell-Skript nutzen:

```powershell
# Starte WSL falls nicht aktiv
wsl.exe -l -v

# Beispiel: Docker-Info aus WSL holen
wsl.exe docker info

# Optional: Container starten
# wsl.exe docker run hello-world
```

**Produktionshinweise:**
- Stelle sicher, dass Docker Desktop und WSL installiert und konfiguriert sind.
- Das Skript kann als `start_wsl_docker.ps1` gespeichert und mit PowerShell ausgeführt werden.
- Bei Fehlern prüfe, ob Docker in WSL verfügbar ist (`wsl.exe docker --version`).
- Für produktiven Einsatz: Container-Images und Netzwerke vorher konfigurieren.

Weitere Infos: https://docs.docker.com/desktop/wsl/
## 7. Beispielmodul: PDF KI-Konverter
- Das Modul `PDF_KI_CONVERTER` analysiert PDF-Dateien, extrahiert Text und exportiert als JSON/CSV.
- Beispiel-PDF im Ordner `_EXAMPLES` (beispiel.pdf).
- Alle Pfade/Exporte per Umgebungsvariable steuerbar, keine Secrets im Code.
- Siehe `PDF_KI_CONVERTER/README.md` für Details und Nutzung.

---

**Statusanzeige und Healthchecks sind in allen Kernkomponenten integriert.**

