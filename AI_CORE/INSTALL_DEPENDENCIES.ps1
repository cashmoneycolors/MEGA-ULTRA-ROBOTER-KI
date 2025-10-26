# Installiert alle .NET-Abhängigkeiten für das Projekt
Write-Host "🔧 Starte dotnet restore für alle Projekte..." -ForegroundColor Cyan
dotnet restore
if ($LASTEXITCODE -eq 0) {
	Write-Host "✅ Alle NuGet-Abhängigkeiten installiert!" -ForegroundColor Green
} else {
	Write-Host "❌ Fehler beim Installieren der Abhängigkeiten!" -ForegroundColor Red
	exit 1
}
