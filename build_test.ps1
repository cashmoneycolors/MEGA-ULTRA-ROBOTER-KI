# C# Build Test Script
Write-Host "Starting build process..." -ForegroundColor Cyan

# Find .csproj file automatically (handles emoji encoding issues)
$csprojFile = Get-ChildItem -Filter "*.csproj" | Select-Object -First 1
if (-not $csprojFile) {
    Write-Host "ERROR: No .csproj file found!" -ForegroundColor Red
    exit 1
}

Write-Host "Found project: $($csprojFile.Name)" -ForegroundColor Green

# Restore dependencies
Write-Host "`nRestoring NuGet packages..." -ForegroundColor Yellow
dotnet restore $csprojFile.FullName 2>&1 | Tee-Object -FilePath "build_restore.log"

# Build project
Write-Host "`nBuilding project..." -ForegroundColor Yellow
dotnet build $csprojFile.FullName --no-restore 2>&1 | Tee-Object -FilePath "build_output.log"

# Check if build was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild ERFOLGREICH!" -ForegroundColor Green
    
    # List output files
    if (Test-Path "bin\Debug\net8.0") {
        Write-Host "`nGenerierte Dateien:" -ForegroundColor Cyan
        Get-ChildItem "bin\Debug\net8.0" | Format-Table Name, Length, LastWriteTime
    }
} else {
    Write-Host "`nBuild FEHLGESCHLAGEN! Exit Code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host "`nBuild-Logs wurden gespeichert in:" -ForegroundColor Yellow
Write-Host "  - build_restore.log" -ForegroundColor White
Write-Host "  - build_output.log" -ForegroundColor White
