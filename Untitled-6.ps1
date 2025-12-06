# PowerShell-Skript: Fix-CSharpFile.ps1
param(
    [string]$FilePath = "AI_CORE\MegaUltraAIIntegratorEnhanced.cs"
)

# Lies alle Zeilen ein
$lines = Get-Content $FilePath

# Hilfsvariablen
$inClass = $false
$inMethod = $false
$fixedLines = @()
$dummyMethodAdded = $false

foreach ($line in $lines) {
    $trim = $line.Trim()

    # Klasse erkennen
    if ($trim -match "class\s+\w+") {
        $inClass = $true
        $fixedLines += $line
        continue
    }

    # Methoden erkennen
    if ($trim -match "(public|private|protected)\s+\w+\s+\w+\s*\(") {
        $inMethod = $true
        $fixedLines += $line
        continue
    }

    # Methodenende erkennen
    if ($inMethod -and $trim -eq "}") {
        $inMethod = $false
        $fixedLines += $line
        continue
    }

    # Modifizierer an lokalen Variablen entfernen
    if ($trim -match "^(private|public|protected)\s+\w+\s+\w+\s*=") {
        $fixedLines += "# FIX: Modifizierer entfernt: " + $line.Replace("private ","").Replace("public ","").Replace("protected ","")
        continue
    }

    # Anweisungen außerhalb von Methoden in Dummy-Methode verschieben
    if ($inClass -and -not $inMethod -and $trim -ne "" -and -not ($trim -match "{" -or $trim -match "}")) {
        if (-not $dummyMethodAdded) {
            $fixedLines += "    // Automatisch eingefügte Dummy-Methode für verwaiste Anweisungen"
            $fixedLines += "    private void DummyFixMethod() {"
            $dummyMethodAdded = $true
        }
        $fixedLines += "        // FIX: Verwaiste Anweisung automatisch verschoben:"
        $fixedLines += "        " + $line.Trim()
        continue
    }

    $fixedLines += $line
}

# Dummy-Methode schließen, falls nötig
if ($dummyMethodAdded) {
    $fixedLines += "    }"
}

# Datei sichern und überschreiben
Copy-Item $FilePath "$FilePath.bak"
$fixedLines | Set-Content $FilePath -Encoding UTF8

Write-Host "Auto-Fix abgeschlossen. Original als $FilePath.bak gesichert."# PowerShell-Skript: Fix-CSharpFile.ps1
param(
    [string]$FilePath = "AI_CORE\MegaUltraAIIntegratorEnhanced.cs"
)

# Lies alle Zeilen ein
$lines = Get-Content $FilePath

# Hilfsvariablen
$inClass = $false
$inMethod = $false
$fixedLines = @()
$dummyMethodAdded = $false

foreach ($line in $lines) {
    $trim = $line.Trim()

    # Klasse erkennen
    if ($trim -match "class\s+\w+") {
        $inClass = $true
        $fixedLines += $line
        continue
    }

    # Methoden erkennen
    if ($trim -match "(public|private|protected)\s+\w+\s+\w+\s*\(") {
        $inMethod = $true
        $fixedLines += $line
        continue
    }

    # Methodenende erkennen
    if ($inMethod -and $trim -eq "}") {
        $inMethod = $false
        $fixedLines += $line
        continue
    }

    # Modifizierer an lokalen Variablen entfernen
    if ($trim -match "^(private|public|protected)\s+\w+\s+\w+\s*=") {
        $fixedLines += "# FIX: Modifizierer entfernt: " + $line.Replace("private ","").Replace("public ","").Replace("protected ","")
        continue
    }

    # Anweisungen außerhalb von Methoden in Dummy-Methode verschieben
    if ($inClass -and -not $inMethod -and $trim -ne "" -and -not ($trim -match "{" -or $trim -match "}")) {
        if (-not $dummyMethodAdded) {
            $fixedLines += "    // Automatisch eingefügte Dummy-Methode für verwaiste Anweisungen"
            $fixedLines += "    private void DummyFixMethod() {"
            $dummyMethodAdded = $true
        }
        $fixedLines += "        // FIX: Verwaiste Anweisung automatisch verschoben:"
        $fixedLines += "        " + $line.Trim()
        continue
    }

    $fixedLines += $line
}

# Dummy-Methode schließen, falls nötig
if ($dummyMethodAdded) {
    $fixedLines += "    }"
}

# Datei sichern und überschreiben
Copy-Item $FilePath "$FilePath.bak"
$fixedLines | Set-Content $FilePath -Encoding UTF8

Write-Host "Auto-Fix abgeschlossen. Original als $FilePath.bak gesichert."# PowerShell-Skript: Fix-CSharpFile.ps1
param(
    [string]$FilePath = "AI_CORE\MegaUltraAIIntegratorEnhanced.cs"
)

# Lies alle Zeilen ein
$lines = Get-Content $FilePath

# Hilfsvariablen
$inClass = $false
$inMethod = $false
$fixedLines = @()
$dummyMethodAdded = $false

foreach ($line in $lines) {
    $trim = $line.Trim()

    # Klasse erkennen
    if ($trim -match "class\s+\w+") {
        $inClass = $true
        $fixedLines += $line
        continue
    }

    # Methoden erkennen
    if ($trim -match "(public|private|protected)\s+\w+\s+\w+\s*\(") {
        $inMethod = $true
        $fixedLines += $line
        continue
    }

    # Methodenende erkennen
    if ($inMethod -and $trim -eq "}") {
        $inMethod = $false
        $fixedLines += $line
        continue
    }

    # Modifizierer an lokalen Variablen entfernen
    if ($trim -match "^(private|public|protected)\s+\w+\s+\w+\s*=") {
        $fixedLines += "# FIX: Modifizierer entfernt: " + $line.Replace("private ","").Replace("public ","").Replace("protected ","")
        continue
    }

    # Anweisungen außerhalb von Methoden in Dummy-Methode verschieben
    if ($inClass -and -not $inMethod -and $trim -ne "" -and -not ($trim -match "{" -or $trim -match "}")) {
        if (-not $dummyMethodAdded) {
            $fixedLines += "    // Automatisch eingefügte Dummy-Methode für verwaiste Anweisungen"
            $fixedLines += "    private void DummyFixMethod() {"
            $dummyMethodAdded = $true
        }
        $fixedLines += "        // FIX: Verwaiste Anweisung automatisch verschoben:"
        $fixedLines += "        " + $line.Trim()
        continue
    }

    $fixedLines += $line
}

# Dummy-Methode schließen, falls nötig
if ($dummyMethodAdded) {
    $fixedLines += "    }"
}

# Datei sichern und überschreiben
Copy-Item $FilePath "$FilePath.bak"
$fixedLines | Set-Content $FilePath -Encoding UTF8

Write-Host "Auto-Fix abgeschlossen. Original als $FilePath.bak gesichert."