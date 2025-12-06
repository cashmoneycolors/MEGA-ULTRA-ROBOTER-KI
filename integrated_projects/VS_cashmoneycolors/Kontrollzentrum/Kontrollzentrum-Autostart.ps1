
# CORE GAZMEND MEHMETI – Mega Ultra Roboter Autostart
# Stand: 15.10.2025


param(
	[string]$LogFile = ""
)

$ErrorActionPreference = 'Stop'
$global:errors = @()


function Log {
	param([string]$msg)
	Write-Host $msg
	if ($LogFile) { Add-Content -Path $LogFile -Value $msg }
}

function Try-Step {
	param(
		[string]$desc,
		[scriptblock]$action
	)
	try {
		Log "[INFO] $desc ..."
		& $action
		Log "[OK]   $desc abgeschlossen."
	} catch {
		$global:errors += "[FEHLER] $desc: $($_.Exception.Message)"
		Log "[FEHLER] $desc: $($_.Exception.Message)"
	}
}


# 1. Chocolatey installieren, falls nicht vorhanden
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
	Try-Step "Chocolatey wird installiert (CORE GAZMEND MEHMETI)" {
		Set-ExecutionPolicy Bypass -Scope Process -Force
		[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
		iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
	}
} else {
	Log "[INFO] Chocolatey ist bereits installiert (CORE GAZMEND MEHMETI)."
}

# 2. Chocolatey selbst updaten

Try-Step "Chocolatey Update (CORE GAZMEND MEHMETI)" { choco upgrade chocolatey -y }

# 3. Tools installieren/aktualisieren
$tools = @(
	@{ name = "python" },
	@{ name = "vscode" },
	@{ name = "git" },
	@{ name = "nodejs" },
	@{ name = "visualstudio2022community"; params = "'--add Microsoft.VisualStudio.Workload.ManagedDesktop'" }
)

foreach ($tool in $tools) {
	$name = $tool.name
	$params = $tool.params
	$desc = "Installiere/Update $name (CORE GAZMEND MEHMETI)"
	if ($params) {
		Try-Step $desc { choco install $name -y --package-parameters $params }
	} else {
		Try-Step $desc { choco install $name -y }
	}
}



# 4. Selbsttest: Sind alle Kern-Tools im PATH verfügbar?
$requiredTools = @(
	@{ name = 'choco'; cmd = 'choco' },
	@{ name = 'python'; cmd = 'python' },
	@{ name = 'vscode'; cmd = 'code' },
	@{ name = 'git'; cmd = 'git' },
	@{ name = 'nodejs'; cmd = 'node' },
	@{ name = 'Visual Studio'; cmd = 'devenv' }
)
$missing = @()
foreach ($tool in $requiredTools) {
	if (!(Get-Command $tool.cmd -ErrorAction SilentlyContinue)) {
		$missing += $tool.name
	}
}

if ($missing.Count -eq 0 -and $global:errors.Count -eq 0) {
	Log "[TEST] 100%: Alle Kern-Tools sind installiert und im PATH! (CORE GAZMEND MEHMETI ist bereit)"
	# Desktop-Verknüpfung automatisch öffnen, damit das Fenster sichtbar ist
	$desktop = [Environment]::GetFolderPath('Desktop')
	$shortcutPath = Join-Path $desktop 'CORE GAZMEND MEHMETI.lnk'
	if (Test-Path $shortcutPath) {
		Start-Process $shortcutPath
		Log "[INFO] CORE GAZMEND MEHMETI wurde automatisch auf dem Desktop gestartet."
	}
	exit 0
} else {
	if ($global:errors.Count -eq 0) {
		Log "[TEST] Fehler: Folgende Tools fehlen im PATH: $($missing -join ', ')"
	} else {
		Log "[FERTIG] Es gab Fehler bei folgenden Schritten (CORE GAZMEND MEHMETI):"
		$global:errors | ForEach-Object { Log $_ }
	}
	exit 1
}


# 5. Desktop-Verknüpfung für CORE GAZMEND MEHMETI Mega Ultra Roboter anlegen
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'CORE GAZMEND MEHMETI.lnk'
$target = 'powershell.exe'
$workingDir = "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum"
$script = 'Kontrollzentrum-Autostart.ps1'
$arguments = "-NoExit -ExecutionPolicy Bypass -File `"$workingDir\\$script`""

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDir
$shortcut.WindowStyle = 1
$shortcut.IconLocation = "$workingDir\\sideboard.ico"
$shortcut.Description = "Starte CORE GAZMEND MEHMETI – Mega Ultra Roboter (vormals Kontrollzentrum)"
$shortcut.Save()


# Branding: Mega Ultra Roboter KI Autonom Generierung
Log "[INFO] Desktop-Verknüpfung 'MEGA ULTRA ROBOTER KI AUTONOM GENERIERUNG' wurde erstellt. Du kannst den Mega Ultra Roboter KI jetzt jederzeit per Doppelklick starten!"

$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'MEGA ULTRA ROBOTER KI AUTONOM GENERIERUNG.lnk'
$target = 'powershell.exe'
$workingDir = "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum"
$script = 'Kontrollzentrum-Autostart.ps1'
$arguments = "-NoExit -ExecutionPolicy Bypass -File `"$workingDir\\$script`""

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDir
$shortcut.WindowStyle = 1
$shortcut.IconLocation = "$workingDir\\sideboard.ico"
$shortcut.Description = "Starte MEGA ULTRA ROBOTER KI AUTONOM GENERIERUNG (vormals Kontrollzentrum/Core Gazmend Mehmeti)"
$shortcut.Save()

cd "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum"
python main.py alle install
python main.py alle run
# Kontrollzentrum-Autostart.ps1
# Dieses Skript wechselt ins richtige Verzeichnis und startet die Automatisierung

cd "C:\Users\Laptop\Documents\CCashMoneyIDE\Kontrollzentrum"
python main.py alle install
python main.py alle run
