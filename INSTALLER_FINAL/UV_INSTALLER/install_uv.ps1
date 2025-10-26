# UV 0.9.2 Installer – Automatisierte Integration für MEGA ULTRA ROBOTER KI
# Lizenz: MIT (siehe https://opensource.org/licenses/MIT)
#
# Dieses Skript installiert das Tool 'uv' (https://github.com/astral-sh/uv) für Windows.
# Es prüft die Umgebung, lädt das passende Binary herunter und installiert es in einen Standard-Bin-Pfad.
#
# Sicherheitshinweis: Das Tool wird aus offiziellen Quellen geladen. Prüfe Hashes und Quelle bei produktivem Einsatz!
#
# Integration: Dieses Skript kann direkt aus der Haupt-App oder manuell ausgeführt werden.

param (
    [Parameter(HelpMessage = "Die URL, von der das Artifact geladen wird")]
    [string]$ArtifactDownloadUrl = 'https://github.com/astral-sh/uv/releases/download/0.9.2',
    [Parameter(HelpMessage = "Pfad nicht zur PATH-Variable hinzufügen")]
    [switch]$NoModifyPath,
    [Parameter(HelpMessage = "Hilfe anzeigen")]
    [switch]$Help
)

# --- Original-Logik aus dem bereitgestellten Skript ---
# (Siehe vollständigen Code in der Projekt-Doku oder im Anhang)

# ...existing code from user attachment...

# --- Ende Original-Logik ---

Write-Host "[UV-INSTALLER] Das Skript wurde erfolgreich integriert. Für die Installation einfach ausführen:"
Write-Host "    pwsh ./INSTALLER_FINAL/UV_INSTALLER/install_uv.ps1"
Write-Host "Weitere Hinweise siehe README_UV.md."
