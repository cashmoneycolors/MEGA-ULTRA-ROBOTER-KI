using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using MegaUltra.Networking;

namespace MegaUltraSystem
{
    /// <summary>
    /// Kern-Integrator für das MEGA ULTRA Robotersystem mit vereinheitlichter Netzwerk-Schnittstelle.
    /// </summary>
    public partial class MegaUltraAIIntegrator : INetworkComponent, IDisposable
    {
        public delegate void LogMessageHandler(string message, ConsoleColor color);
        public delegate void MetricsUpdateHandler(Dictionary<string, string> metrics);

        public event LogMessageHandler? OnLogMessage;
        public event MetricsUpdateHandler? OnMetricsUpdate;
        public event EventHandler<ComponentEventArgs>? OnComponentEvent;

        public class AIConfig
        {
            public string JWT_SECRET { get; set; } = string.Empty;
            public string MAINTENANCE_KEY { get; set; } = string.Empty;
            public string LLM_MODEL_NAME { get; set; } = "llama3.2:3b";
            public string OLLAMA_TARGET_URL { get; set; } = "http://localhost:11434";
            public string DataDirectory { get; set; } = Path.Combine(Environment.CurrentDirectory, "MEGA_ULTRA_DATA");
            public bool AutoRestart { get; set; } = true;
            public bool EnableLogging { get; set; } = true;
        }

        private readonly AIConfig _config;
        private readonly CancellationTokenSource _lifetimeCts = new();
        private readonly object _stateGate = new();
        private Task? _metricsLoop;
        private Task? _monitoringLoop;
        private bool _disposed;
        private MegaUltraNetworkOrchestrator? _orchestrator;

        public MegaUltraAIIntegrator(AIConfig? config = null)
        {
            _config = config ?? LoadConfigFromEnvironment();
            EnsureSecrets();
            Directory.CreateDirectory(_config.DataDirectory);
            Log("INIT", "MEGA ULTRA AI Integrator initialisiert", ConsoleColor.Green);
        }

        public string ComponentId => $"MegaUltraAI_{Environment.MachineName}";
        public string ComponentType => "AutonomousAI";
        public ComponentStatus Status { get; private set; } = ComponentStatus.Stopped;
        public int RunningPort { get; private set; } = 3000;

        public async Task Initialize()
        {
            if (Status != ComponentStatus.Stopped)
            {
                return;
            }

            Status = ComponentStatus.Starting;
            Log("INIT", "Initialisiere Netzwerkkomponenten...", ConsoleColor.Cyan);

            var networkingSuccess = await StartAutonomousNetworking().ConfigureAwait(false);
            Status = networkingSuccess ? ComponentStatus.Running : ComponentStatus.Error;

            if (networkingSuccess)
            {
                StartMetricsMonitoring();
                OnComponentEvent?.Invoke(this, new ComponentEventArgs
                {
                    ComponentId = ComponentId,
                    EventType = "Initialized",
                    Data = GetStatus()
                });
            }
        }

        public async Task<(bool Success, string Message)> StartMegaUltraSystem()
        {
            await Initialize().ConfigureAwait(false);

            if (Status == ComponentStatus.Running)
            {
                Log("START", "System ist aktiv");
                return (true, "MEGA ULTRA System aktiv");
            }

            Log("ERROR", "Start fehlgeschlagen", ConsoleColor.Red);
            return (false, "Start fehlgeschlagen, siehe Log");
        }

        public Task StartAutonomousMonitoring()
        {
            lock (_stateGate)
            {
                if (_monitoringLoop != null)
                {
                    return Task.CompletedTask;
                }

                _monitoringLoop = Task.Run(async () =>
                {
                    while (!_lifetimeCts.IsCancellationRequested)
                    {
                        try
                        {
                            var status = GetStatus();
                            status["Heartbeat"] = DateTime.UtcNow;
                            OnComponentEvent?.Invoke(this, new ComponentEventArgs
                            {
                                ComponentId = ComponentId,
                                EventType = "Heartbeat",
                                Data = status
                            });
                            await Task.Delay(TimeSpan.FromSeconds(5), _lifetimeCts.Token).ConfigureAwait(false);
                        }
                        catch (OperationCanceledException)
                        {
                            break;
                        }
                        catch (Exception ex)
                        {
                            Log("MON", $"Überwachung unterbrochen: {ex.Message}", ConsoleColor.Yellow);
                            await Task.Delay(TimeSpan.FromSeconds(10), _lifetimeCts.Token).ConfigureAwait(false);
                        }
                    }
                }, _lifetimeCts.Token);
            }

            return Task.CompletedTask;
        }

        public void StartMetricsMonitoring()
        {
            lock (_stateGate)
            {
                if (_metricsLoop != null)
                {
                    return;
                }

                _metricsLoop = Task.Run(async () =>
                {
                    while (!_lifetimeCts.IsCancellationRequested)
                    {
                        try
                        {
                            var metrics = new Dictionary<string, string>
                            {
                                ["Timestamp"] = DateTime.UtcNow.ToString("O"),
                                ["Status"] = Status.ToString(),
                                ["RunningPort"] = RunningPort.ToString(),
                                ["ComponentId"] = ComponentId
                            };

                            OnMetricsUpdate?.Invoke(metrics);
                            await Task.Delay(TimeSpan.FromSeconds(2), _lifetimeCts.Token).ConfigureAwait(false);
                        }
                        catch (OperationCanceledException)
                        {
                            break;
                        }
                        catch (Exception ex)
                        {
                            Log("METRICS", $"Fehler beim Sammeln von Metriken: {ex.Message}", ConsoleColor.Yellow);
                            await Task.Delay(TimeSpan.FromSeconds(5), _lifetimeCts.Token).ConfigureAwait(false);
                        }
                    }
                }, _lifetimeCts.Token);
            }
        }

        public async Task<bool> StartAutonomousNetworking()
        {
            if (_orchestrator != null)
            {
                return true;
            }

            try
            {
                _orchestrator = new MegaUltraNetworkOrchestrator();
                await _orchestrator.Initialize().ConfigureAwait(false);
                _orchestrator.RegisterComponent(this);

                Log("NETWORK", "Autonome Vernetzung aktiv", ConsoleColor.Green);
                return true;
            }
            catch (Exception ex)
            {
                Log("NETWORK", $"Vernetzung fehlgeschlagen: {ex.Message}", ConsoleColor.Red);
                _orchestrator = null;
                return false;
            }
        }

        public async Task Shutdown()
        {
            if (Status == ComponentStatus.Stopped)
            {
                return;
            }

            Log("SHUTDOWN", "Stoppe MEGA ULTRA Integrator", ConsoleColor.Cyan);
            Status = ComponentStatus.Stopped;
            _lifetimeCts.Cancel();

            try
            {
                if (_monitoringLoop != null)
                {
                    await _monitoringLoop.ConfigureAwait(false);
                }

                if (_metricsLoop != null)
                {
                    await _metricsLoop.ConfigureAwait(false);
                }
            }
            catch (OperationCanceledException)
            {
                // Ignoriert – erwarteter Abbruch
            }

            if (_orchestrator != null)
            {
                await _orchestrator.Shutdown().ConfigureAwait(false);
                _orchestrator = null;
            }

            OnComponentEvent?.Invoke(this, new ComponentEventArgs
            {
                ComponentId = ComponentId,
                EventType = "Shutdown",
                Data = GetStatus()
            });
        }

        public Dictionary<string, object> GetStatus()
        {
            return new Dictionary<string, object>
            {
                ["ComponentId"] = ComponentId,
                ["ComponentType"] = ComponentType,
                ["Status"] = Status.ToString(),
                ["RunningPort"] = RunningPort,
                ["SecretsConfigured"] = !string.IsNullOrEmpty(_config.JWT_SECRET) && !string.IsNullOrEmpty(_config.MAINTENANCE_KEY),
                ["AutoRestart"] = _config.AutoRestart,
                ["DataDirectory"] = _config.DataDirectory
            };
        }

        public Task<bool> ProcessMessage(NetworkMessage message)
        {
            Log("NETWORK", $"Nachricht empfangen: {message.MessageType}", ConsoleColor.Blue);

            switch (message.MessageType)
            {
                case "AIRequest":
                    return Task.FromResult(true);
                case "GetStatus":
                    OnComponentEvent?.Invoke(this, new ComponentEventArgs
                    {
                        ComponentId = ComponentId,
                        EventType = "StatusRequested",
                        Data = GetStatus()
                    });
                    return Task.FromResult(true);
                default:
                    return Task.FromResult(false);
            }
        }

        public Task<NetworkMessage> CreateStatusMessage()
        {
            return Task.FromResult(new NetworkMessage
            {
                ComponentType = ComponentType,
                MessageType = "ComponentStatus",
                Data = GetStatus()
            });
        }

        public async Task<string> SendPrompt(string prompt, string? model = null)
        {
            await Task.Yield();
            Log("PROMPT", $"Prompt empfangen: {prompt}");
            return $"Simulierte Antwort des Modells {model ?? _config.LLM_MODEL_NAME}";
        }

        public async Task<bool> RequestCleanShutdown()
        {
            await Shutdown().ConfigureAwait(false);
            return true;
        }

        public Process? RunDynamicLoadTest(int? vus = null, int? durationSeconds = null)
        {
            Log("LOAD", $"Starte simulierten Load-Test mit {vus ?? 10} VUs für {durationSeconds ?? 60}s");
            return null;
        }

        public void ShowSystemStatus()
        {
            Console.WriteLine("═".PadRight(60, '═'));
            Console.WriteLine(" MEGA ULTRA KI-INTEGRATOR STATUS");
            Console.WriteLine("═".PadRight(60, '═'));
            foreach (var kvp in GetStatus())
            {
                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
            }
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            _lifetimeCts.Cancel();

            if (_monitoringLoop is { IsCompleted: false })
            {
                _monitoringLoop.Wait(TimeSpan.FromSeconds(2));
            }

            if (_metricsLoop is { IsCompleted: false })
            {
                _metricsLoop.Wait(TimeSpan.FromSeconds(2));
            }

            _lifetimeCts.Dispose();
            _orchestrator = null;
        }

        private AIConfig LoadConfigFromEnvironment()
        {
            return new AIConfig
            {
                JWT_SECRET = Environment.GetEnvironmentVariable("JWT_SECRET") ?? string.Empty,
                MAINTENANCE_KEY = Environment.GetEnvironmentVariable("MAINTENANCE_KEY") ?? string.Empty,
                LLM_MODEL_NAME = Environment.GetEnvironmentVariable("LLM_MODEL_NAME") ?? "llama3.2:3b",
                OLLAMA_TARGET_URL = Environment.GetEnvironmentVariable("OLLAMA_TARGET_URL") ?? "http://localhost:11434",
                DataDirectory = Environment.GetEnvironmentVariable("MEGA_ULTRA_DATA") ?? Path.Combine(Environment.CurrentDirectory, "MEGA_ULTRA_DATA"),
                AutoRestart = !string.Equals(Environment.GetEnvironmentVariable("MEGA_ULTRA_AUTORESTART"), "false", StringComparison.OrdinalIgnoreCase),
                EnableLogging = !string.Equals(Environment.GetEnvironmentVariable("MEGA_ULTRA_DISABLE_LOGGING"), "true", StringComparison.OrdinalIgnoreCase)
            };
        }

        private void EnsureSecrets()
        {
            if (string.IsNullOrWhiteSpace(_config.JWT_SECRET))
            {
                _config.JWT_SECRET = Guid.NewGuid().ToString("N");
                Log("SECURITY", "JWT_SECRET nicht gesetzt – temporärer Schlüssel erzeugt", ConsoleColor.Yellow);
            }

            if (string.IsNullOrWhiteSpace(_config.MAINTENANCE_KEY))
            {
                _config.MAINTENANCE_KEY = Guid.NewGuid().ToString("N");
                Log("SECURITY", "MAINTENANCE_KEY nicht gesetzt – temporärer Schlüssel erzeugt", ConsoleColor.Yellow);
            }
        }

        private void Log(string category, string message, ConsoleColor color = ConsoleColor.White)
        {
            var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            var entry = $"[{timestamp}] [{category}] {message}";
            Console.ForegroundColor = color;
            Console.WriteLine(entry);
            Console.ResetColor();

            OnLogMessage?.Invoke(entry, color);

            if (_config.EnableLogging)
            {
                try
                {
                    var logPath = Path.Combine(_config.DataDirectory, "mega_ultra_ai.log");
                    File.AppendAllText(logPath, entry + Environment.NewLine);
                }
                catch (IOException)
                {
                    // Logging darf den Integrator nicht stoppen.
                }
            }
        }
    }
}