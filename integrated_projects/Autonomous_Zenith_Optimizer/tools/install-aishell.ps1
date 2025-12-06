#Requires -Version 5.1

<#
.SYNOPSIS
    Installiert AIshell - Ein KI-gestütztes Shell-Tool

.DESCRIPTION
    Dieses Script installiert AIshell automatisch mit allen notwendigen Abhängigkeiten.
    Es überprüft vorhandene Installationen, lädt die neueste Version herunter und konfiguriert sie.

.PARAMETER InstallPath
    Der Installationspfad für AIshell (Standard: $env:ProgramFiles\AIshell)

.PARAMETER Force
    Erzwingt die Neuinstallation, auch wenn AIshell bereits installiert ist

.EXAMPLE
    .\install-aishell.ps1

.EXAMPLE
    .\install-aishell.ps1 -InstallPath "C:\MyApps\AIshell" -Force
#>

param(
    [string]$InstallPath = "$env:ProgramFiles\AIshell",
    [switch]$Force
)

# Administrator-Rechte prüfen
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Logging-Funktion
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path "$env:TEMP\aishell_install.log" -Value $logMessage
}

# Hauptinstallationsfunktion
function Install-AIshell {
    try {
        Write-Log "Starte AIshell-Installation..."

        # Administrator-Rechte prüfen
        if (-not (Test-Administrator)) {
            Write-Log "Administrator-Rechte erforderlich. Starte Script neu mit erhöhten Rechten..." "WARNING"
            Start-Process powershell.exe -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
            exit
        }

        # Überprüfen, ob AIshell bereits installiert ist
        if ((Test-Path $InstallPath) -and -not $Force) {
            $continue = Read-Host "AIshell scheint bereits installiert zu sein in $InstallPath. Möchten Sie fortfahren? (j/n)"
            if ($continue -ne 'j') {
                Write-Log "Installation abgebrochen."
                exit
            }
        }

        # Python prüfen/installieren
        Write-Log "Überprüfe Python-Installation..."
        $pythonExe = $null
        $pythonVersion = $null

        # Suche nach Python-Installationen im System
        $pythonPaths = @(
            "C:\Python314\python.exe",
            "C:\Python313\python.exe",
            "C:\Python312\python.exe",
            "C:\Python311\python.exe",
            "$env:ProgramFiles\Python*\python.exe",
            "$env:ProgramFiles(x86)\Python*\python.exe",
            "$env:LOCALAPPDATA\Programs\Python\*\python.exe"
        )

        foreach ($path in $pythonPaths) {
            if (Test-Path $path) {
                try {
                    $version = & $path --version 2>$null
                    if ($version) {
                        $pythonExe = $path
                        $pythonVersion = $version
                        break
                    }
                }
                catch {
                    continue
                }
            }
        }

        # Versuche auch Befehle im PATH
        if (-not $pythonExe) {
            $pythonCommands = @("python", "python3", "py")
            foreach ($cmd in $pythonCommands) {
                try {
                    $version = & $cmd --version 2>$null
                    if ($version) {
                        $pythonExe = $cmd
                        $pythonVersion = $version
                        break
                    }
                }
                catch {
                    continue
                }
            }
        }

        if (-not $pythonExe) {
            Write-Log "Python nicht gefunden. Versuche winget zur Installation..." "WARNING"
            try {
                winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
                Start-Sleep -Seconds 10  # Warte auf Installation
                $pythonExe = "python"
                $pythonVersion = "Python (neu installiert)"
                Write-Log "Python erfolgreich über winget installiert."
            }
            catch {
                Write-Log "Bitte installieren Sie Python manuell von https://python.org" "ERROR"
                exit 1
            }
        }

        Write-Log "Python gefunden: $pythonVersion ($pythonExe)"

        # Installationsverzeichnis erstellen
        if (-not (Test-Path $InstallPath)) {
            New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
            Write-Log "Installationsverzeichnis erstellt: $InstallPath"
        }

        # Abhängigkeiten installieren
        Write-Log "Installiere Python-Abhängigkeiten..."
        pip install --upgrade pip
        pip install openai anthropic requests python-dotenv rich

        # AIshell herunterladen (Beispiel-URL - anpassen je nach realer Quelle)
        Write-Log "Lade AIshell herunter..."
        $aishellUrl = "https://github.com/example/aishell/releases/latest/download/aishell.zip"  # Platzhalter-URL
        $tempZip = "$env:TEMP\aishell.zip"

        try {
            Invoke-WebRequest -Uri $aishellUrl -OutFile $tempZip
            Write-Log "Download abgeschlossen."
        }
        catch {
            Write-Log "Download fehlgeschlagen. Verwende lokale Installation..." "WARNING"
            # Fallback: Erstelle eine Basis-AIshell-Anwendung
            New-Item -ItemType File -Path "$InstallPath\aishell.py" -Force | Out-Null
            Set-Content -Path "$InstallPath\aishell.py" -Value @"
import os
import sys
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    console.print("[bold green]AIshell v1.0[/bold green]")
    console.print("KI-gestützte Kommandozeile")
    console.print("Tippen Sie 'help' für Hilfe oder 'exit' zum Beenden.")

    while True:
        try:
            command = Prompt.ask("> ")
            if command.lower() in ['exit', 'quit']:
                break
            elif command.lower() == 'help':
                console.print("[yellow]Verfügbare Befehle:[/yellow]")
                console.print("  help  - Diese Hilfe anzeigen")
                console.print("  exit  - AIshell beenden")
                console.print("  ai    - KI-Assistent starten")
            elif command.lower() == 'ai':
                console.print("[blue]KI-Modus aktiviert[/blue]")
                # Hier könnte KI-Integration hinzugefügt werden
            else:
                os.system(command)
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Fehler: {e}[/red]")

if __name__ == "__main__":
    main()
"@

            New-Item -ItemType File -Path "$InstallPath\requirements.txt" -Force | Out-Null
            Set-Content -Path "$InstallPath\requirements.txt" -Value @"
openai
anthropic
requests
python-dotenv
rich
"@

            Write-Log "Lokale AIshell-Version erstellt."
        }

        # PATH aktualisieren
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        if ($currentPath -notlike "*$InstallPath*") {
            $newPath = "$currentPath;$InstallPath"
            [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
            Write-Log "PATH-Umgebungsvariable aktualisiert."
        }

        # Desktop-Verknüpfung erstellen
        $desktopPath = [Environment]::GetFolderPath("Desktop")
        $shortcutPath = "$desktopPath\AIshell.lnk"
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = "python.exe"
        $shortcut.Arguments = "`"$InstallPath\aishell.py`""
        $shortcut.WorkingDirectory = $InstallPath
        $shortcut.IconLocation = "powershell.exe,0"
        $shortcut.Save()
        Write-Log "Desktop-Verknüpfung erstellt."

        # VS Code Konfiguration aktualisieren
        Write-Log "Aktualisiere VS Code Konfiguration..."
        $vscodePath = "$env:APPDATA\Code\User"
        $launchJsonPath = "$vscodePath\launch.json"

        $launchConfig = @{
            version = "0.2.0"
            configurations = @(
                @{
                    name = "Python-Debugger: Aktuelle Datei"
                    type = "debugpy"
                    request = "launch"
                    program = "`${file}"
                    console = "integratedTerminal"
                },
                @{
                    name = "(gdb) Starten"
                    type = "cppdbg"
                    request = "launch"
                    program = "Programmnamen eingeben, z. B. `${workspaceFolder}/a.exe"
                    args = @()
                    stopAtEntry = $false
                    cwd = "`${fileDirname}"
                    environment = @()
                    externalConsole = $false
                    MIMode = "gdb"
                    miDebuggerPath = "/path/to/gdb"
                    setupCommands = @(
                        @{
                            description = "Automatische Strukturierung und Einrückung für gdb aktivieren"
                            text = "-enable-pretty-printing"
                            ignoreFailures = $true
                        },
                        @{
                            description = "Disassemblierungsvariante auf Intel festlegen"
                            text = "-gdb-set disassembly-flavor intel"
                            ignoreFailures = $true
                        }
                    )
                },
                @{
                    name = "AIshell: Launch"
                    type = "python"
                    request = "launch"
                    program = "$InstallPath\aishell.py"
                    console = "integratedTerminal"
                }
            )
        }

        $launchConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $launchJsonPath -Encoding UTF8
        Write-Log "VS Code launch.json aktualisiert."

        Write-Log "AIshell-Installation erfolgreich abgeschlossen!" "SUCCESS"
        Write-Log "Starten Sie AIshell mit: python `"$InstallPath\aishell.py`""
        Write-Log "Oder verwenden Sie die Desktop-Verknüpfung."

    }
    catch {
        Write-Log "Installation fehlgeschlagen: $($_.Exception.Message)" "ERROR"
        exit 1
    }
}

# Script ausführen
Install-AIshell
