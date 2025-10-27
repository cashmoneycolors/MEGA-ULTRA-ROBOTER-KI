# UV 0.9.2 – PowerShell-Installer

Dieses Modul integriert das Tool [uv](https://github.com/astral-sh/uv) als optionalen Bestandteil der MEGA ULTRA ROBOTER KI-Toolchain.

## Installation

1. Stelle sicher, dass PowerShell 5 oder neuer installiert ist.
2. Führe das Skript aus:
   ```pwsh
   pwsh ./INSTALLER_FINAL/UV_INSTALLER/install_uv.ps1
   ```
3. Folge den Anweisungen im Terminal.

## Sicherheitshinweis
- Das Skript lädt Binaries von GitHub. Prüfe Hashes und Quelle bei produktivem Einsatz!
- Für produktive Deployments empfiehlt sich ein Security-Review und ggf. die Nutzung von Hash-Prüfungen.

## Integration
- Das Skript kann direkt aus der Haupt-App, aus Build-Skripten oder manuell ausgeführt werden.
- Nach erfolgreicher Installation steht das Kommando `uv` systemweit zur Verfügung (sofern PATH angepasst wurde).

## Lizenz
- MIT (siehe https://opensource.org/licenses/MIT)

---

**Letzte Änderung:** 14.10.2025
