# Copilot Instructions für MEGA ULTRA AI SYSTEM

## Architekturüberblick
- **Kernkomponenten:**
  - `MegaUltraAIIntegrator`: Haupt-Integrator, steuert Secrets, LLM, Netzwerk, Events
  - `MegaUltraNetworkOrchestrator`: Orchestriert alle Netzwerk-Komponenten, Echtzeit-Kommunikation (TCP/UDP, REST)
  - `NetworkComponents`: Definiert Netzwerkkomponenten, Status, Events
  - `MegaUltraNetworkDeployment`: Automatisiertes Deployment und Management des Gesamtsystems
- **Lose Kopplung:** Komponenten sind über Events, TCP/UDP und HttpClient verbunden, können dynamisch hinzugefügt werden
- **Konfiguration:** Über Umgebungsvariablen (z.B. `JWT_SECRET`, `MAINTENANCE_KEY`) oder AIConfig-Objekte
- **LLM-Integration:** Über `OLLAMA_TARGET_URL` (z.B. http://localhost:11434) und `LLM_MODEL_NAME`

## Entwickler-Workflows
- **Starten des Systems:**
  - Nutze `RUN_NETWORK_SYSTEM.ps1` für den Start (führt `dotnet run` auf `MegaUltraAIIntegrator.csproj` aus, Fallback: `MegaUltraAISystemV2.csproj`)
- **Projektorganisation:**
  - `FIX_CSHARP_PROJECTS.ps1` erstellt/aktualisiert die Solution und fügt alle Projekte hinzu
- **Abhängigkeiten:**
  - Standardmäßig per `dotnet restore` (Skript `INSTALL_DEPENDENCIES.ps1` ist leer, ggf. manuell ausführen)
- **Debugging:**
  - Über PowerShell-Skripte und Konsolenausgaben (farbige Statusmeldungen)
- **Konfiguration:**
  - Kritische Secrets müssen als Umgebungsvariablen gesetzt werden (siehe `AIConfig` in `MegaUltraAIIntegrator.cs`)

## Projektspezifische Konventionen
- **Namensgebung:**
  - Präfixe wie `MegaUltra*`, `AIIntegrator*`, `Network*` für zentrale Komponenten
- **Events:**
  - Kommunikation zwischen Komponenten über Events (`OnComponentEvent`, `OnLogMessage` etc.)
- **Logging:**
  - Über `Microsoft.Extensions.Logging` und farbige Konsolenausgaben
- **Keine expliziten Testprojekte:**
  - Tests erfolgen über Integration im Hauptsystem

## Integrationspunkte & Abhängigkeiten
- **LLM/AI:** Ollama-Server (lokal oder remote), Modellname konfigurierbar
- **Externe Libraries:** `System.Management`, `System.Text.Json`, `Microsoft.Extensions.Logging`
- **Node.js:** Optional für ServerScriptPath (wird referenziert, aber kein JS-File im Repo)

## Beispiele & Einstiegspunkte
- **Einstieg:** `Program.cs` (Startlogik, Initialisierung)
- **Konfiguration:** `AIConfig`-Klasse in `MegaUltraAIIntegrator.cs`
- **Netzwerk:** `MegaUltraNetworkOrchestrator.cs`, `NetworkComponents.cs`
- **Deployment:** `MegaUltraNetworkDeployment.cs`
- **PowerShell-Workflows:** `RUN_NETWORK_SYSTEM.ps1`, `FIX_CSHARP_PROJECTS.ps1`

---

> Bei Unklarheiten zu Workflows, Konfiguration oder Architektur bitte Rückmeldung geben, damit die Anleitung iterativ verbessert werden kann.
