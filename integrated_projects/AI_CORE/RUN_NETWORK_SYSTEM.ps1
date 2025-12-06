# MEGA ULTRA NETWORK - RUN SCRIPT
Write-Host "ðŸš€ Starte MEGA ULTRA Network System..." -ForegroundColor Green

try {
    dotnet run --project MegaUltraAIIntegrator.csproj
} catch {
    Write-Host "Fallback: Direkte AusfÃ¼hrung..." -ForegroundColor Yellow
    dotnet run --project MegaUltraAISystemV2.csproj
}
