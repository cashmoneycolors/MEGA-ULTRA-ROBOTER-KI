using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using System.Threading;
using System.Text.Json;
using System.Security.Cryptography;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;

namespace MegaUltraAISystem
{
    /// <summary>
    /// 🚀 MEGA ULTRA AI INTEGRATOR - VOLLSTÄNDIG AUTONOM 🚀
    /// Erstellt eigene API-Schlüssel, verwaltet Netzwerk, selbst-heilend
    /// </summary>
    public class MegaUltraAIIntegratorV2 : IDisposable
    {
        private Process? _serverProcess;
        private readonly CancellationTokenSource _cts = new();
        private AIConfig _config;
        private string ConfigPath => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".mega_ultra_config.json");
        public int RunningPort { get; private set; } = 3000;

        public class AIConfig
        {
            public string JWT_SECRET { get; set; } = "";
            public string SYSTEM_API_KEY { get; set; } = "";
            public string INTERNAL_NETWORK_ID { get; set; } = "";
            public string LLM_MODEL_NAME { get; set; } = "llama2";
            public string OLLAMA_BASE_URL { get; set; } = "http://localhost:11434";
            public int MAX_TOKENS_PER_HOUR { get; set; } = 1000000;
            public bool AUTONOMOUS_MODE { get; set; } = true;
            public DateTime LAST_KEY_ROTATION { get; set; } = DateTime.MinValue;
        }

        public MegaUltraAIIntegratorV2()
        {
            _config = LoadOrCreateConfig();
            Log("INFO", "🚀 MEGA ULTRA AI INTEGRATOR V2 gestartet", ConsoleColor.Green);
            EnsureSecurityKeys();
        }

        private void EnsureSecurityKeys()
        {
            bool needsSave = false;

            if (string.IsNullOrEmpty(_config.JWT_SECRET))
            {
                _config.JWT_SECRET = GenerateSecureKey(64);
                needsSave = true;
                Log("SECURITY", "🔐 JWT Secret automatisch generiert", ConsoleColor.Yellow);
            }

            if (string.IsNullOrEmpty(_config.SYSTEM_API_KEY))
            {
                _config.SYSTEM_API_KEY = GenerateApiKey();
                needsSave = true;
                Log("SECURITY", "🗝️ System API Key automatisch erstellt", ConsoleColor.Yellow);
            }

            if (string.IsNullOrEmpty(_config.INTERNAL_NETWORK_ID))
            {
                _config.INTERNAL_NETWORK_ID = GenerateNetworkId();
                needsSave = true;
                Log("NETWORK", "🌐 Interne Netzwerk-ID generiert", ConsoleColor.Cyan);
            }

            if (needsSave)
            {
                SaveConfig();
            }
        }

        private string GenerateSecureKey(int length = 32)
        {
            using var rng = RandomNumberGenerator.Create();
            byte[] bytes = new byte[length];
            rng.GetBytes(bytes);
            return Convert.ToBase64String(bytes).Replace("+", "-").Replace("/", "_").Replace("=", "");
        }

        private string GenerateApiKey()
        {
            var prefix = "muas"; // Mega Ultra AI System
            var timestamp = DateTimeOffset.Now.ToUnixTimeSeconds().ToString("x");
            var random = GenerateSecureKey(16);
            return $"{prefix}_{timestamp}_{random}";
        }

        private string GenerateNetworkId()
        {
            try
            {
                var mac = NetworkInterface.GetAllNetworkInterfaces()
                    .FirstOrDefault(nic => nic.OperationalStatus == OperationalStatus.Up)?
                    .GetPhysicalAddress().ToString();
                
                if (string.IsNullOrEmpty(mac))
                {
                    mac = Environment.MachineName + Environment.UserName;
                }

                using var sha256 = SHA256.Create();
                var hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(mac + DateTime.Now.Ticks));
                return Convert.ToHexString(hash)[..16];
            }
            catch
            {
                return Guid.NewGuid().ToString("N")[..16];
            }
        }

        public async Task<(bool Success, string Message)> StartMegaUltraSystem()
        {
            try
            {
                Log("STARTUP", "🚀 Initialisiere MEGA ULTRA System...", ConsoleColor.Cyan);

                // 1. Port finden
                RunningPort = FindAvailablePort(3000);
                Log("NETWORK", $"🔌 Verwende Port: {RunningPort}", ConsoleColor.Green);

                // 2. Ollama prüfen
                await EnsureOllamaModel();

                // 3. Node.js Server starten
                if (!await StartNodeServer())
                {
                    return (false, "❌ Node.js Server konnte nicht gestartet werden!");
                }

                // 4. Health Check
                if (!await WaitForServerReady())
                {
                    return (false, "❌ Server antwortet nicht!");
                }

                // 5. Autonome Überwachung starten
                StartAutonomousMonitoring();

                ShowSystemStatus();
                return (true, $"✅ System läuft auf Port {RunningPort}");
            }
            catch (Exception ex)
            {
                Log("ERROR", $"❌ Fehler beim Start: {ex.Message}", ConsoleColor.Red);
                return (false, ex.Message);
            }
        }

        private async Task<bool> StartNodeServer()
        {
            try
            {
                var serverDir = Path.Combine(Directory.GetCurrentDirectory(), "..", "server");
                if (!Directory.Exists(serverDir))
                {
                    Log("ERROR", $"❌ Server-Verzeichnis fehlt: {serverDir}", ConsoleColor.Red);
                    return false;
                }

                var startInfo = new ProcessStartInfo
                {
                    FileName = "node",
                    Arguments = $"mega-ai-server.js --port={RunningPort} --ollama={_config.OLLAMA_BASE_URL}",
                    WorkingDirectory = serverDir,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                // Umgebungsvariablen für vollständige Autonomie
                startInfo.EnvironmentVariables["JWT_SECRET"] = _config.JWT_SECRET;
                startInfo.EnvironmentVariables["SYSTEM_API_KEY"] = _config.SYSTEM_API_KEY;
                startInfo.EnvironmentVariables["INTERNAL_NETWORK_ID"] = _config.INTERNAL_NETWORK_ID;
                startInfo.EnvironmentVariables["MAX_TOKENS_PER_HOUR"] = _config.MAX_TOKENS_PER_HOUR.ToString();
                startInfo.EnvironmentVariables["AUTONOMOUS_MODE"] = "true";

                _serverProcess = Process.Start(startInfo);
                
                if (_serverProcess != null)
                {
                    Log("PROCESS", $"✅ Server gestartet (PID: {_serverProcess.Id})", ConsoleColor.Green);
                    return true;
                }

                return false;
            }
            catch (Exception ex)
            {
                Log("ERROR", $"❌ Server-Start: {ex.Message}", ConsoleColor.Red);
                return false;
            }
        }

        private async Task EnsureOllamaModel()
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
                var response = await client.GetAsync($"{_config.OLLAMA_BASE_URL}/api/tags");
                
                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    if (content.Contains(_config.LLM_MODEL_NAME))
                    {
                        Log("OLLAMA", $"✅ Model {_config.LLM_MODEL_NAME} bereit", ConsoleColor.Green);
                        return;
                    }
                }

                Log("OLLAMA", $"📥 Lade Model {_config.LLM_MODEL_NAME}...", ConsoleColor.Yellow);
                await PullOllamaModel();
            }
            catch (Exception ex)
            {
                Log("WARNING", $"⚠️ Ollama-Check: {ex.Message}", ConsoleColor.Yellow);
            }
        }

        private async Task PullOllamaModel()
        {
            try
            {
                var pullProcess = new ProcessStartInfo
                {
                    FileName = "ollama",
                    Arguments = $"pull {_config.LLM_MODEL_NAME}",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                };

                using var process = Process.Start(pullProcess);
                if (process != null)
                {
                    await process.WaitForExitAsync();
                    if (process.ExitCode == 0)
                    {
                        Log("OLLAMA", "✅ Model erfolgreich geladen", ConsoleColor.Green);
                    }
                }
            }
            catch (Exception ex)
            {
                Log("WARNING", $"⚠️ Model-Download: {ex.Message}", ConsoleColor.Yellow);
            }
        }

        private int FindAvailablePort(int startPort = 3000)
        {
            for (int port = startPort; port <= 65535; port++)
            {
                try
                {
                    var listener = new TcpListener(IPAddress.Loopback, port);
                    listener.Start();
                    listener.Stop();
                    return port;
                }
                catch
                {
                    continue;
                }
            }
            return startPort; // Fallback
        }

        private async Task<bool> WaitForServerReady()
        {
            using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
            
            for (int i = 0; i < 30; i++)
            {
                try
                {
                    var response = await client.GetAsync($"http://localhost:{RunningPort}/health");
                    if (response.IsSuccessStatusCode)
                    {
                        Log("HEALTH", "✅ Server bereit!", ConsoleColor.Green);
                        return true;
                    }
                }
                catch
                {
                    await Task.Delay(1000);
                }
            }

            Log("ERROR", "❌ Server Timeout!", ConsoleColor.Red);
            return false;
        }

        private void StartAutonomousMonitoring()
        {
            Task.Run(async () =>
            {
                Log("MONITOR", "🤖 Autonome Überwachung gestartet", ConsoleColor.Cyan);
                
                while (!_cts.Token.IsCancellationRequested)
                {
                    try
                    {
                        // Server-Prozess prüfen
                        if (_serverProcess?.HasExited == true)
                        {
                            Log("MONITOR", "⚠️ Server beendet - Neustart...", ConsoleColor.Yellow);
                            await RestartServer();
                        }

                        // Health Check
                        await PerformHealthCheck();
                        
                        // Sicherheits-Rotation (täglich)
                        if ((DateTime.Now - _config.LAST_KEY_ROTATION).TotalDays >= 1)
                        {
                            PerformSecurityRotation();
                        }

                        await Task.Delay(10000, _cts.Token); // 10 Sekunden
                    }
                    catch (Exception ex)
                    {
                        Log("MONITOR", $"⚠️ Überwachungsfehler: {ex.Message}", ConsoleColor.Yellow);
                        await Task.Delay(5000, _cts.Token);
                    }
                }
            }, _cts.Token);
        }

        private async Task PerformHealthCheck()
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(3) };
                var response = await client.GetAsync($"http://localhost:{RunningPort}/health");
                
                if (!response.IsSuccessStatusCode)
                {
                    Log("HEALTH", "⚠️ Health Check fehlgeschlagen", ConsoleColor.Yellow);
                    await RestartServer();
                }
            }
            catch
            {
                // Health Check stillschweigend fehlgeschlagen
            }
        }

        private void PerformSecurityRotation()
        {
            _config.JWT_SECRET = GenerateSecureKey(64);
            _config.SYSTEM_API_KEY = GenerateApiKey();
            _config.LAST_KEY_ROTATION = DateTime.Now;
            SaveConfig();
            Log("SECURITY", "🔄 Automatische Schlüssel-Rotation", ConsoleColor.Green);
        }

        private async Task RestartServer()
        {
            try
            {
                _serverProcess?.Kill();
                await Task.Delay(2000);
                
                if (await StartNodeServer())
                {
                    Log("RESTART", "✅ Server erfolgreich neugestartet", ConsoleColor.Green);
                }
            }
            catch (Exception ex)
            {
                Log("ERROR", $"❌ Neustart fehlgeschlagen: {ex.Message}", ConsoleColor.Red);
            }
        }

        private void ShowSystemStatus()
        {
            Console.Clear();
            Console.WriteLine();
            Log("STATUS", "╔══════════════════════════════════════════════╗", ConsoleColor.Cyan);
            Log("STATUS", "║      MEGA ULTRA AI SYSTEM - V2 AKTIV        ║", ConsoleColor.Yellow);
            Log("STATUS", "║     🤖 Vollständig Autonom & Vernetzt       ║", ConsoleColor.Green);
            Log("STATUS", "╚══════════════════════════════════════════════╝", ConsoleColor.Cyan);
            Console.WriteLine();

            Log("INFO", $"🌐 Server: http://localhost:{RunningPort}", ConsoleColor.Cyan);
            Log("INFO", $"🤖 Model: {_config.LLM_MODEL_NAME}", ConsoleColor.Cyan);
            Log("INFO", $"🔑 API Key: {_config.SYSTEM_API_KEY[..12]}...", ConsoleColor.Yellow);
            Log("INFO", $"🛡️ Network ID: {_config.INTERNAL_NETWORK_ID}", ConsoleColor.Green);
            Log("INFO", $"⚡ Max Tokens/h: {_config.MAX_TOKENS_PER_HOUR:N0}", ConsoleColor.Magenta);
            
            Console.WriteLine();
            Log("FEATURES", "✅ Eigene API-Schlüssel: AKTIV", ConsoleColor.Green);
            Log("FEATURES", "✅ Autonome Überwachung: AKTIV", ConsoleColor.Green);  
            Log("FEATURES", "✅ Selbst-Heilung: AKTIV", ConsoleColor.Green);
            Log("FEATURES", "✅ Interne Vernetzung: AKTIV", ConsoleColor.Green);
            Log("FEATURES", "✅ Sicherheits-Rotation: AKTIV", ConsoleColor.Green);
            
            Console.WriteLine();
            Console.WriteLine("System läuft vollständig autonom. Drücken Sie 'q' zum Beenden...");
        }

        private AIConfig LoadOrCreateConfig()
        {
            try
            {
                if (File.Exists(ConfigPath))
                {
                    var json = File.ReadAllText(ConfigPath);
                    return JsonSerializer.Deserialize<AIConfig>(json) ?? new AIConfig();
                }
            }
            catch (Exception ex)
            {
                Log("WARNING", $"Config-Fehler: {ex.Message}", ConsoleColor.Yellow);
            }

            return new AIConfig();
        }

        private void SaveConfig()
        {
            try
            {
                var json = JsonSerializer.Serialize(_config, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(ConfigPath, json);
            }
            catch (Exception ex)
            {
                Log("ERROR", $"Config-Speichern: {ex.Message}", ConsoleColor.Red);
            }
        }

        private void Log(string type, string message, ConsoleColor color = ConsoleColor.White)
        {
            var timestamp = DateTime.Now.ToString("HH:mm:ss");
            Console.ForegroundColor = color;
            Console.WriteLine($"[{timestamp}] [{type}] {message}");
            Console.ResetColor();
        }

        public void Dispose()
        {
            _cts?.Cancel();
            _serverProcess?.Kill();
            _serverProcess?.Dispose();
            _cts?.Dispose();
        }
    }
}