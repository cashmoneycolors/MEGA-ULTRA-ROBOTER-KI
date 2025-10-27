// Integriert aus: Die Drei Säulen von Aethelos GAZI.txt
// Stand: 15.10.2025
//
// Diese Datei wurde automatisch aus der Textquelle übernommen und ist jetzt Teil des Build-Systems.

// ...EXISTIERENDER INHALT AUS TXT...


/*******************************************************************************
 * 1. C# KONTROLLTURM: GazOpenAIIntegrator.cs
 * Der hyper-autonome Start-, Check- und Selbstheilungs-Mechanismus.
 * (Anmerkung: Alle Hilfsmethoden sind logisch in der Klasse enthalten.)
 ******************************************************************************/

using System.Diagnostics;
using System.Net.Sockets;
using System.Net.Http;
using System.Threading.Tasks;
using System.IO;
using System;
using System.Threading;
using System.Text.Json;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Management;
using System.Net;

using MegaUltra.Networking;

public class GazOpenAIIntegrator : INetworkComponent, IDisposable
{
	public string ComponentId { get; } = "GazOpenAIIntegrator_" + Environment.MachineName;
	public string ComponentType { get; } = "GazOpenAIIntegrator";
	public ComponentStatus Status { get; private set; } = ComponentStatus.Stopped;
	public event EventHandler<ComponentEventArgs> OnComponentEvent;

	private const int PublicPort = 3000;
	private const int OllamaPort = 11434;
	private const string ServerExeName = "opengazai-server.exe";
	private const string ConfigFileName = "opengazai_config.json";

	// ... private Felder und die Config-Klasse (mit ADMIN_PASSWORD_HASH und JWT_SECRET) ...


	   public GazOpenAIIntegrator()
	   {
		   // 1. Initialisierung und Laden/Erstellen der Konfiguration
		   // 2. Ruft PromptForPassword() auf, wenn ADMIN_PASSWORD_HASH == null
		   // 3. Speichert den gehashten Admin-Hash in der Config
	   }

	   public async Task Initialize()
	   {
		   Status = ComponentStatus.Starting;
		   // Initialisierung (z.B. Config laden, Ressourcen prüfen)
		   Status = ComponentStatus.Running;
		   OnComponentEvent?.Invoke(this, new ComponentEventArgs
		   {
			   ComponentId = ComponentId,
			   EventType = "Initialized",
			   Data = new Dictionary<string, object> { { "Timestamp", DateTime.UtcNow }, { "Status", Status.ToString() } }
		   });
	   }

	   public async Task Shutdown()
	   {
		   Status = ComponentStatus.Stopped;
		   OnComponentEvent?.Invoke(this, new ComponentEventArgs
		   {
			   ComponentId = ComponentId,
			   EventType = "Shutdown",
			   Data = new Dictionary<string, object> { { "Timestamp", DateTime.UtcNow } }
		   });
	   }

	   public Dictionary<string, object> GetStatus()
	   {
		   return new Dictionary<string, object>
		   {
			   { "ComponentId", ComponentId },
			   { "Status", Status.ToString() },
			   { "Type", ComponentType },
			   { "Timestamp", DateTime.UtcNow }
		   };
	   }

	   public async Task<bool> ProcessMessage(NetworkMessage message)
	   {
		   // Platzhalter: Nachrichtenverarbeitung für Mesh-Kommunikation
		   switch (message.MessageType)
		   {
			   case "StartKeyServer":
				   var result = await StartKeyServerAutonom();
				   OnComponentEvent?.Invoke(this, new ComponentEventArgs
				   {
					   ComponentId = ComponentId,
					   EventType = "KeyServerStarted",
					   Data = new Dictionary<string, object> { { "Success", result.Success }, { "Message", result.Message } }
				   });
				   return result.Success;
			   case "GetStatus":
				   OnComponentEvent?.Invoke(this, new ComponentEventArgs
				   {
					   ComponentId = ComponentId,
					   EventType = "StatusRequested",
					   Data = GetStatus()
				   });
				   return true;
			   default:
				   return false;
		   }
	   }

	   public async Task<NetworkMessage> CreateStatusMessage()
	   {
		   return new NetworkMessage
		   {
			   ComponentType = ComponentType,
			   MessageType = "ComponentStatus",
			   Data = GetStatus()
		   };
	   }

	public async Task<(bool Success, string Message)> StartKeyServerAutonom()
	{
		Console.WriteLine("\n--- OPENGAZAI MAX++++: SYSTEMSTARTPRÜFUNG ---");

		// 1. Hyper-Check: RAM-Check
		if (!CheckSystemResources(_config.MIN_REQUIRED_RAM_GB))
		{
			 return (false, " KRITISCH: Zu wenig RAM. Systemstart abgebrochen.");
		}

		// 2. Hyper-Check: Ollama-Dienst
		if (!IsPortInUse(OllamaPort))
		{
			 return (false, " KRITISCH: Ollama ist NICHT aktiv. Bitte starten Sie den Dienst.");
		}

		// 3. Hyper-Check: Modell-Bereitschaft (und Pull)
		if (!await CheckAndPullOllamaModel(_config.LLM_MODEL_NAME, _config.OLLAMA_TARGET_URL))
		{
			return (false, $" FEHLER: Modell '{_config.LLM_MODEL_NAME}' nicht bereit.");
		}

		// 4. Dynamischer Port-Fall-Back
		RunningPort = FindAvailablePort(PublicPort);
		if (RunningPort == 0) return (false, " FEHLER: Konnte keinen freien Port finden.");

		// 5. Starte den Server-Prozess (Übergabe aller kritischer Argumente)
		// ... (Logik zur Erstellung der 'arguments' für den Node.js Prozess) ...

		try
		{
			// ... (ProcessStartInfo & Process.Start(_serverProcess) Logik) ...

			// 6. Finale Bereitschaftsprüfung
			if (!await WaitForServerReady(RunningPort, _cts.Token))
			{
				_serverProcess.Kill();
				return (false, " KRITISCHER FEHLER: Node.js Serverstart fehlgeschlagen.");
			}
		}
		catch (Exception ex)
		{
			return (false, $" FEHLER beim Start des Servers: {ex.Message}");
		}

		Console.WriteLine($"\n=======================================================");
		Console.WriteLine($" OPENGAZAI AKTIV: Proxy auf Port {RunningPort}, Admin auf {RunningPort + 1}");
		Console.WriteLine("=======================================================");

		// Startet hier die Logik zur Überwachung (MonitorServerLifetime)

		return (true, $"OpenGazAI gestartet.");
	}

	// ... Implementierungen der Methoden (FindAvailablePort, CheckSystemResources, IsPortInUse,
	//    CheckAndPullOllamaModel, PromptForPassword, ReadPasswordFromConsole, WaitForServerReady) ...

	// ********************************************
	// 3. WICHTIGE HILFSMETHODE (Mac Hash für Lizenzbindung)
	// ********************************************
	public static string GenerateMacHash()
	{
		 // Hier muss die finale Logik zur Erstellung des Hardware-Hashes implementiert werden,
		 // basierend auf den MAC-Adressen, wie im Support-Modus (--show-hash) verwendet.
		 return "GENERATED_MAC_HASH_FOR_LICENSING";
	}
}

