

# post_install_max.ps1
# 🧬 Universeller Premium-Build-Installer für Visual Studio & Terminal
# ---------------------------------------------------------------
# • Direkt in Visual Studio oder im Terminal ausführen
# • Automatische Erkennung und Build aller .sln/.csproj-Dateien
# • Robustes Logging, Fehlerbehandlung, Healthchecks
# • Erweiterbar: SVG-Dashboard, NFT-Galerie, Smart Contract-Trigger
# ---------------------------------------------------------------


param(
	[string]$LogFile = "./post_install_max.log",
	[switch]$EnableDashboard,
	[switch]$EnableNFT,
	[switch]$EnableSmartContract
)


function Write-Log {
	param([string]$Message)
	$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
	$logEntry = "$timestamp $Message"
	Write-Host $logEntry
	Add-Content -Path $LogFile -Value $logEntry
}


function Check-EnvVar {
	param([string]$VarName)
	$value = (Get-Item -Path Env:$VarName -ErrorAction SilentlyContinue).Value
	if (-not $value) {
		Write-Log "[WARN] Umgebungsvariable '$VarName' ist NICHT gesetzt!"
		return $false
	} else {
		Write-Log "[OK] Umgebungsvariable '$VarName' gefunden."
		return $true
	}
}


function Install-Dependency {
	param([string]$Command, [string]$Description)
	Write-Log "[INFO] Installiere: ${Description} ..."
	try {
		Invoke-Expression $Command
		Write-Log "[OK] ${Description} installiert."
	} catch {
		Write-Log "[ERROR] Fehler bei Installation von ${Description}: $_"
		exit 1
	}
}


# Healthcheck für Python
function Check-Python {
	Write-Log "[INFO] Prüfe Python-Installation ..."
	try {
		$python = & python --version 2>&1
		Write-Log "[OK] Python gefunden: $python"
	} catch {
		Write-Log "[ERROR] Python nicht gefunden! $_"
		exit 1
	}
}

# Automatischer Build für alle .sln/.csproj-Dateien
function Build-AllCSharpProjects {
	Write-Log "[INFO] Suche nach .sln- und .csproj-Dateien ..."
	$slns = Get-ChildItem -Path . -Recurse -Filter *.sln -ErrorAction SilentlyContinue
	$csprojs = Get-ChildItem -Path . -Recurse -Filter *.csproj -ErrorAction SilentlyContinue
	if ($slns.Count -eq 0 -and $csprojs.Count -eq 0) {
		Write-Log "[WARN] Keine .sln- oder .csproj-Dateien gefunden!"
		return
	}
	foreach ($sln in $slns) {
		Write-Log "[INFO] Baue Solution: $($sln.FullName) ..."
		try {
			dotnet restore $sln.FullName
			dotnet build $sln.FullName --no-restore
			Write-Log "[OK] Build abgeschlossen: $($sln.Name)"
		} catch {
			Write-Log "[ERROR] Build fehlgeschlagen: $($sln.Name) $_"
		}
	}
	foreach ($proj in $csprojs) {
		Write-Log "[INFO] Baue Projekt: $($proj.FullName) ..."
		try {
			dotnet restore $proj.FullName
			dotnet build $proj.FullName --no-restore
			Write-Log "[OK] Build abgeschlossen: $($proj.Name)"
		} catch {
			Write-Log "[ERROR] Build fehlgeschlagen: $($proj.Name) $_"
		}
	}
}

# Erweiterungshooks (Platzhalter)
function Run-Dashboard {
	if ($EnableDashboard) {
		Write-Log "[HOOK] SVG-Dashboard-Integration aktiv! (Platzhalter)"
		# Hier eigenen Code für Dashboard einfügen
	}
}
function Run-NFT {
	if ($EnableNFT) {
		Write-Log "[HOOK] NFT-Galerie-Integration aktiv! (Platzhalter)"
		# Hier eigenen Code für NFT-Galerie einfügen
	}
}
function Run-SmartContract {
	if ($EnableSmartContract) {
		Write-Log "[HOOK] Smart Contract-Trigger aktiv! (Platzhalter)"
		# Hier eigenen Code für Smart Contract einfügen
	}
}


# Hauptlogik
Write-Log "==== Starte post_install_max.ps1 (Premium-Build-Installer) ===="

# 1. Healthchecks & Umgebungsvariablen
Check-EnvVar -VarName "JWT_SECRET" | Out-Null
Check-EnvVar -VarName "MAINTENANCE_KEY" | Out-Null
Check-Python

# 2. Abhängigkeiten installieren (Beispiel)
# Install-Dependency -Command "pip install -r requirements.txt" -Description "Python requirements"

# 3. Automatischer Build aller C#-Projekte
Build-AllCSharpProjects

# 4. Erweiterungshooks (SVG-Dashboard, NFT, Smart Contract)
Run-Dashboard
Run-NFT
Run-SmartContract

Write-Log "==== post_install_max.ps1 abgeschlossen ===="
