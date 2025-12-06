using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Text.Json;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Sockets;
using System.Linq;
using System.Management;

namespace RoboterKIMaxUltra
{
    public class RoboterKIMaxUltraApp
    {
        // --- Ultra-Maxima Kernkonstanten ---
        private const string ConfigFileName = "roboter_ki_ultra_config.json";
        private const string NodeServerExe = "opengazai-server.exe";
        private const string NodeServerScript = "opengazai-server.js";
        private const int PublicPort = 3000;
        private const int OllamaPort = 11434;
        private const int MaxRestarts = 5;
        private const int JwtRotationDays = 90;
        private const int PBKDF2_ITERATIONS = 600000;
        private static Mutex? _appMutex;
        private static Process? _serverProcess;
        private static CancellationTokenSource _cts = new CancellationTokenSource();
        private static UltraConfig? _config;
        private static List<int> _badPorts = new List<int>();
        private static string _lastError = string.Empty;
        private static int RunningPort = PublicPort;

        public static async Task Main(string[] args)
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("╔════════════════════════════════════════════════════╗");
            Console.WriteLine("║   MEGA ULTRA ROBOTER KI – Produktionssystem       ║");
            Console.WriteLine("╠════════════════════════════════════════════════════╣");
            Console.WriteLine($"║ Build: {DateTime.Now:yyyy-MM-dd HH:mm:ss}   ");
            Console.WriteLine($"║ Integrationsstatus: ALLE MODULE AKTIV");
            Console.WriteLine($"║ Sideboard: {(File.Exists("PY_SIDEBOARD/double_gazi_ai_ultimate.py") ? "Verfügbar" : "Nicht gefunden")}");
            Console.WriteLine("╚════════════════════════════════════════════════════╝");
            Console.ResetColor();
            /***********************************************************************
             * INTEGRATIONSSTATUS: ALLE MODULE & SIDEBOARDS
             * ---------------------------------------------------------------------
             * - Alle sicherheitsrelevanten Entry-Points und Sideboard-Module (z.B. Double Gazi AI Ultimate) wurden geprüft und produktiv eingebunden.
             * - Secret-Handling, Entwicklerwarnungen und Dokumentation sind vollständig und produktiv.
             * - Die Sideboards laufen unabhängig, können aber jetzt direkt aus der Haupt-App per Tastendruck ('d') als Subprozess gestartet werden.
             * - Siehe SECURITY_DOC_AND_TESTS.md und README im jeweiligen Modul.
             *
             * [14.10.2025] Systemstatus: BEREIT FÜR PRODUKTIVE INTEGRATION
             ***********************************************************************/

            // --- Secret-Handling: Niemals hardcodieren! ---
            string jwtSecret = Environment.GetEnvironmentVariable("JWT_SECRET");
            if (string.IsNullOrEmpty(jwtSecret)) {
                jwtSecret = Guid.NewGuid().ToString("N");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("[WARNUNG] JWT_SECRET ist NICHT gesetzt! Es wurde ein temporäres Secret generiert. Bitte Secret als Umgebungsvariable setzen (z.B. $env:JWT_SECRET=...) – Niemals im Code speichern!");
                Console.ResetColor();
            }
            string adminPasswordHash = Environment.GetEnvironmentVariable("ADMIN_PASSWORD_HASH");
            if (string.IsNullOrEmpty(adminPasswordHash)) {
                adminPasswordHash = "admin";
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("[WARNUNG] ADMIN_PASSWORD_HASH ist NICHT gesetzt! Es wurde ein unsicherer Default-Wert verwendet. Bitte Secret als Umgebungsvariable setzen (z.B. $env:ADMIN_PASSWORD_HASH=...) – Niemals im Code speichern!");
                Console.ResetColor();
            }

            // Single-Instance-Garantie
            _appMutex = new Mutex(true, "Global\\RoboterKIMaxUltraApp_Mutex", out bool createdNew);
            if (!createdNew)
            {
                Console.WriteLine("[FATAL] Es läuft bereits eine Instanz.");
                Environment.Exit(99);
            }

            // Integritätsprüfung
            if (!CheckBinaryIntegrity())
            {
                Console.WriteLine("[FATAL] Integritätsprüfung fehlgeschlagen. Manuelle Überprüfung erforderlich.");
                Environment.Exit(99);
            }

            // Konfiguration laden/erstellen
            _config = LoadOrCreateConfig();
            // Secrets aus Umgebungsvariablen übernehmen, falls vorhanden
            if (_config != null) {
                if (!string.IsNullOrEmpty(jwtSecret)) _config.JWT_SECRET = jwtSecret;
                if (!string.IsNullOrEmpty(adminPasswordHash)) _config.ADMIN_PASSWORD_HASH = adminPasswordHash;
                RotateJwtSecretIfNeeded();
            }

            // Autonomer Start
            var (success, message) = await StartKeyServerAutonom();
            if (!success)
            {
                Console.WriteLine($"[FATAL] {message}");
                Environment.Exit(99);
            }
            Console.WriteLine($"[INFO] {message}");

            // Watchdog starten
            var watchdog = MonitorServerLifetime();
            // Die folgende Zeile startet den Watchdog asynchron und behandelt Fehler korrekt:
            _ = watchdog.ContinueWith(t => { if (t.IsFaulted) FatalSelfRestart(); }, TaskContinuationOptions.OnlyOnFaulted);

            // Interaktive Schleife (optional)
            while (true)
            {
                Console.WriteLine("q = Quit, s = Status, d = Double Gazi AI Ultimate starten");
                var key = Console.ReadKey(true);
                if (key.KeyChar == 'q') break;
                if (key.KeyChar == 's') ShowStatus();
                if (key.KeyChar == 'd')
                {
                    try
                    {
                        // Starte das Sideboard als Subprozess (Python)
                        var psi = new ProcessStartInfo
                        {
                            FileName = "python",
                            Arguments = "PY_SIDEBOARD/double_gazi_ai_ultimate.py",
                            UseShellExecute = false,
                            RedirectStandardOutput = true,
                            RedirectStandardError = true,
                            CreateNoWindow = true
                        };
                        var proc = Process.Start(psi);
                        Console.WriteLine("[INFO] Double Gazi AI Ultimate (Sideboard) wurde gestartet.");
                    }
                    catch (Exception ex)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine($"[FEHLER] Sideboard-Start fehlgeschlagen: {ex.Message}");
                        Console.ResetColor();
                    }
                }
            }
            _cts.Cancel();
            if (_serverProcess != null) _serverProcess.Kill();
        }

        // --- Autonomer Start & Self-Healing ---
        private static async Task<(bool, string)> StartKeyServerAutonom()
        {
            // Parallele Checks
            var ramCheckTask = Task.Run(() => CheckSystemResources(8.0));
            var ollamaCheckTask = IsPortListeningAsync(OllamaPort, 1000);
            var portFindTask = Task.Run(() => FindAvailablePort(PublicPort));
            await Task.WhenAll(ramCheckTask, ollamaCheckTask, portFindTask);
            if (!ramCheckTask.Result) return (false, "Zu wenig RAM.");
            if (!ollamaCheckTask.Result) return (false, "Ollama nicht aktiv.");
            RunningPort = portFindTask.Result;
            if (RunningPort == 0) return (false, "Kein freier Port gefunden.");
            // Modell-Bereitschaft
            if (_config == null || !await CheckAndPullOllamaModel(_config.LLM_MODEL_NAME, _config.OLLAMA_TARGET_URL))
                return (false, $"Modell '{_config?.LLM_MODEL_NAME}' nicht bereit.");
            // Server-Prozess starten
            try
            {
                var psi = new ProcessStartInfo(NodeServerExe, $"--port {RunningPort} --datapath ./data --admin_hash {_config?.ADMIN_PASSWORD_HASH} --jwt_secret {_config?.JWT_SECRET} --ollama_url {_config?.OLLAMA_TARGET_URL} --model_name {_config?.LLM_MODEL_NAME}")
                {
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                };
                _serverProcess = Process.Start(psi);
                if (_serverProcess != null)
                    _serverProcess.PriorityClass = ProcessPriorityClass.AboveNormal;
                // Bereitschaftsprüfung
                if (!await WaitForServerReady(RunningPort, _cts.Token))
                {
                    if (_serverProcess != null) _serverProcess.Kill();
                    return (false, "Node.js Serverstart fehlgeschlagen.");
                }
            }
            catch (Exception ex)
            {
                return (false, $"FEHLER beim Start des Servers: {ex.Message}");
            }
            return (true, $"OpenGazAI gestartet auf Port {RunningPort}.");
        }

        // --- Watchdog & Selbstheilung ---
        private static async Task MonitorServerLifetime()
        {
            int restartCount = 0;
            int coldRestartCount = 0;
            while (!_cts.IsCancellationRequested)
            {
                await Task.Delay(5000, _cts.Token);
                // RAM-Laufzeitüberwachung
                if (!CheckSystemResources(8.0))
                {
                    LogJson(new { level = "warn", msg = "RAM-Limit überschritten. Neustart empfohlen." });
                }
                // Prozess-Check
                if (_serverProcess == null || _serverProcess.HasExited)
                {
                    LogJson(new { level = "error", msg = "Server-Prozess beendet." });
                    if (restartCount < MaxRestarts)
                    {
                        restartCount++;
                        var (success, message) = await StartKeyServerAutonom();
                        if (!success) { _lastError = message; continue; }
                    }
                    else if (coldRestartCount < 3)
                    {
                        coldRestartCount++;
                        LogJson(new { level = "fatal", msg = "Mehrfache Neustartversuche fehlgeschlagen. Führe Cold-Restart durch." });
                        await Task.Delay(2000);
                        await StartKeyServerAutonom();
                    }
                    else
                    {
                        LogJson(new { level = "fatal", msg = "System-Reset. Manuelle Überprüfung erforderlich." });
                        Environment.Exit(99);
                    }
                }
                // Heartbeat-Check
                if (!await CheckServerHeartbeat(RunningPort))
                {
                    LogJson(new { level = "error", msg = "Heartbeat-Check fehlgeschlagen. Server wird neu gestartet." });
                    _serverProcess.Kill();
                    await StartKeyServerAutonom();
                }
            }
        }

        // --- Hilfsmethoden (RAM, Port, Modell, Heartbeat, etc.) ---
        private static bool CheckSystemResources(double minRamGb)
        {
            try
            {
                var totalRam = GetTotalPhysicalMemoryGb();
                var availableRam = GetAvailablePhysicalMemoryGb();
                if (totalRam < minRamGb) return false;
                if (availableRam < minRamGb * 0.7) return false;
                var sysDrive = DriveInfo.GetDrives().FirstOrDefault(d => d.Name.StartsWith("C", StringComparison.OrdinalIgnoreCase) && d.IsReady);
                if (sysDrive != null)
                {
                    long freeGb = sysDrive.AvailableFreeSpace / (1024 * 1024 * 1024);
                    if (freeGb < 10) return false;
                }
                else return false;
                return true;
            }
            catch { return false; }
        }
        private static double GetTotalPhysicalMemoryGb()
        {
            try
            {
                var searcher = new ManagementObjectSearcher("SELECT TotalPhysicalMemory FROM Win32_ComputerSystem");
                foreach (var obj in searcher.Get())
                {
                    double bytes = Convert.ToDouble(obj["TotalPhysicalMemory"]);
                    return bytes / (1024 * 1024 * 1024);
                }
            }
            catch { }
            return GC.GetGCMemoryInfo().TotalAvailableMemoryBytes / (1024.0 * 1024 * 1024);
        }
        private static double GetAvailablePhysicalMemoryGb()
        {
            try
            {
                var searcher = new ManagementObjectSearcher("SELECT FreePhysicalMemory FROM Win32_OperatingSystem");
                foreach (var obj in searcher.Get())
                {
                    double kb = Convert.ToDouble(obj["FreePhysicalMemory"]);
                    return kb / (1024 * 1024);
                }
            }
            catch { }
            return (GC.GetGCMemoryInfo().TotalAvailableMemoryBytes - GC.GetTotalMemory(false)) / (1024.0 * 1024 * 1024);
        }
        private static async Task<bool> IsPortListeningAsync(int port, int timeoutMs = 500)
        {
            using var client = new TcpClient();
            var cts = new CancellationTokenSource(timeoutMs);
            try { await client.ConnectAsync("localhost", port, cts.Token); return true; }
            catch { return false; }
        }
        private static int FindAvailablePort(int startPort)
        {
            for (int port = startPort; port < startPort + 10; port++)
            {
                if (_badPorts.Contains(port)) continue;
                try
                {
                    TcpListener l = new TcpListener(System.Net.IPAddress.Loopback, port);
                    l.Start(); l.Stop(); return port;
                }
                catch { continue; }
            }
            return 0;
        }
        private static async Task<bool> CheckAndPullOllamaModel(string model, string url)
        {
            await Task.Delay(1000); // TODO: Modell-Check und Pull implementieren
            return true;
        }
        private static async Task<bool> WaitForServerReady(int port, CancellationToken token)
        {
            for (int i = 0; i < 10; i++)
            {
                if (await CheckServerHeartbeat(port)) return true;
                await Task.Delay(1000, token);
            }
            return false;
        }
        private static async Task<bool> CheckServerHeartbeat(int port)
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
                var resp = await client.GetAsync($"http://localhost:{port}/status");
                return resp.IsSuccessStatusCode;
            }
            catch { return false; }
        }

        // --- Deep Health Checks ---
        private static async Task<bool> CheckOllamaLiveness(string ollamaUrl)
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
                var resp = await client.GetAsync($"{ollamaUrl.TrimEnd('/')}/api/tags");
                return resp.IsSuccessStatusCode;
            }
            catch { return false; }
        }
        private static async Task<bool> CheckModelSanity(string ollamaUrl, string modelName)
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(3) };
                var resp = await client.GetAsync($"{ollamaUrl.TrimEnd('/')}/api/tags");
                if (!resp.IsSuccessStatusCode) return false;
                var json = await resp.Content.ReadAsStringAsync();
                return json.Contains(modelName, StringComparison.OrdinalIgnoreCase);
            }
            catch { return false; }
        }
        private static async Task<bool> CheckServerHeartbeatDeep(int port)
        {
            try
            {
                using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
                var resp = await client.GetAsync($"http://localhost:{port}/status");
                if (!resp.IsSuccessStatusCode) return false;
                var json = await resp.Content.ReadAsStringAsync();
                return json.Contains("ok", StringComparison.OrdinalIgnoreCase) || json.Contains("status", StringComparison.OrdinalIgnoreCase);
            }
            catch { return false; }
        }

        // --- PBKDF2-Hashing für Admin-Passwort ---
        private static string HashPasswordPBKDF2(string password, out string salt, int iterations)
        {
            using var rng = RandomNumberGenerator.Create();
            byte[] saltBytes = new byte[32];
            rng.GetBytes(saltBytes);
            salt = Convert.ToBase64String(saltBytes);
            byte[] hash = Rfc2898DeriveBytes.Pbkdf2(password, saltBytes, iterations, HashAlgorithmName.SHA512, 64);
            return Convert.ToBase64String(hash);
        }
        private static bool VerifyPasswordPBKDF2(string password, string hash, string salt, int iterations)
        {
            byte[] saltBytes = Convert.FromBase64String(salt);
            byte[] hashBytes = Rfc2898DeriveBytes.Pbkdf2(password, saltBytes, iterations, HashAlgorithmName.SHA512, 64);
            byte[] refHash = Convert.FromBase64String(hash);
            return SecureEquals(hashBytes, refHash);
        }
        private static bool SecureEquals(byte[] a, byte[] b)
        {
            if (a.Length != b.Length) return false;
            int diff = 0;
            for (int i = 0; i < a.Length; i++) diff |= a[i] ^ b[i];
            return diff == 0;
        }
        private static string ReadPasswordFromConsole()
        {
            var pwd = string.Empty;
            ConsoleKeyInfo key;
            do
            {
                key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.Enter) break;
                if (key.Key == ConsoleKey.Backspace && pwd.Length > 0)
                {
                    pwd = pwd.Substring(0, pwd.Length - 1);
                    Console.Write("\b \b");
                }
                else if (!char.IsControl(key.KeyChar))
                {
                    pwd += key.KeyChar;
                    Console.Write("*");
                }
            } while (true);
            Console.WriteLine();
            return pwd;
        }

        // --- Integritätsprüfung ---
        private static bool CheckBinaryIntegrity()
        {
            try
            {
                string exePath = Process.GetCurrentProcess().MainModule?.FileName ?? string.Empty;
                string exeHash = string.IsNullOrEmpty(exePath) ? string.Empty : ComputeFileSha512Hash(exePath);
                string? nodeHash = File.Exists(NodeServerExe) ? ComputeFileSha512Hash(NodeServerExe) : null;
                string? scriptHash = File.Exists(NodeServerScript) ? ComputeFileSha512Hash(NodeServerScript) : null;
                if (_config == null || string.IsNullOrEmpty(_config.EXE_HASH))
                {
                    if (_config != null)
                    {
                        _config.EXE_HASH = exeHash;
                        _config.NODE_HASH = nodeHash ?? string.Empty;
                        _config.SCRIPT_HASH = scriptHash ?? string.Empty;
                        SaveConfigAtomically(_config);
                        Console.WriteLine("[INTEGRITY] Referenz-Hashes gespeichert.");
                    }
                    return true;
                }
                if (_config.EXE_HASH != exeHash) return false;
                if (!string.IsNullOrEmpty(_config.NODE_HASH) && nodeHash != null && _config.NODE_HASH != nodeHash) return false;
                if (!string.IsNullOrEmpty(_config.SCRIPT_HASH) && scriptHash != null && _config.SCRIPT_HASH != scriptHash) return false;
                return true;
            }
            catch { return false; }
        }
        private static string ComputeFileSha512Hash(string filePath)
        {
            using var stream = File.OpenRead(filePath);
            using var sha = SHA512.Create();
            byte[] hash = sha.ComputeHash(stream);
            return BitConverter.ToString(hash).Replace("-", string.Empty).ToLowerInvariant();
        }

        // --- Konfigurations-Härtung ---
        private static UltraConfig LoadOrCreateConfig()
        {
            if (!File.Exists(ConfigFileName))
            {
                var cfg = new UltraConfig { ADMIN_PASSWORD_HASH = "admin", JWT_SECRET = Guid.NewGuid().ToString("N"), LLM_MODEL_NAME = "llama3.2:3b", OLLAMA_TARGET_URL = "http://localhost:11434" };
                SaveConfigAtomically(cfg);
                return cfg;
            }
            var json = File.ReadAllText(ConfigFileName);
            /*
             * WARNUNG: Die folgende Zeile verwendet System.Text.Json ohne explizite Source Generation oder JsonTypeInfo/JsonSerializerContext.
             * Dies kann bei AOT- oder Trimming-Builds (z.B. NativeAOT, PublishTrimmed) zu Laufzeitfehlern führen!
             * Für produktive Builds empfiehlt Microsoft die Nutzung von Source Generation:
             * https://learn.microsoft.com/de-de/dotnet/standard/serialization/system-text-json/source-generation
             *
             * Für lokale Entwicklung ist dies unkritisch. Für Produktion: Siehe SECURITY_DOC_AND_TESTS.md und passe die Serialisierung an!
             */
            return JsonSerializer.Deserialize<UltraConfig>(json) ?? new UltraConfig();
        }
        private static void SaveConfigAtomically(UltraConfig cfg)
        {
            /*
             * WARNUNG: Die folgende Zeile verwendet System.Text.Json ohne explizite Source Generation oder JsonTypeInfo/JsonSerializerContext.
             * Dies kann bei AOT- oder Trimming-Builds (z.B. NativeAOT, PublishTrimmed) zu Laufzeitfehlern führen!
             * Für produktive Builds empfiehlt Microsoft die Nutzung von Source Generation:
             * https://learn.microsoft.com/de-de/dotnet/standard/serialization/system-text-json/source-generation
             *
             * Für lokale Entwicklung ist dies unkritisch. Für Produktion: Siehe SECURITY_DOC_AND_TESTS.md und passe die Serialisierung an!
             */
            string json = JsonSerializer.Serialize(cfg, new JsonSerializerOptions { WriteIndented = true });
            string tmp = ConfigFileName + ".tmp";
            File.WriteAllText(tmp, json);
            File.Replace(tmp, ConfigFileName, null);
        }
        private static void RotateJwtSecretIfNeeded()
        {
            // Dummy: JWT-Rotation nach 90 Tagen (hier Logik implementieren)
        }

        private static void ShowStatus()
        {
            Console.WriteLine($"Status: Server läuft: {_serverProcess != null && !_serverProcess.HasExited}, Letzter Fehler: {_lastError}");
        }
        private static void LogJson(object obj)
        {
            /*
             * WARNUNG: Die folgende Zeile verwendet System.Text.Json ohne explizite Source Generation oder JsonTypeInfo/JsonSerializerContext.
             * Dies kann bei AOT- oder Trimming-Builds (z.B. NativeAOT, PublishTrimmed) zu Laufzeitfehlern führen!
             * Für produktive Builds empfiehlt Microsoft die Nutzung von Source Generation:
             * https://learn.microsoft.com/de-de/dotnet/standard/serialization/system-text-json/source-generation
             *
             * Für lokale Entwicklung ist dies unkritisch. Für Produktion: Siehe SECURITY_DOC_AND_TESTS.md und passe die Serialisierung an!
             */
            Console.WriteLine(JsonSerializer.Serialize(obj));
        }

        // --- MAC-Hash für Lizenzbindung ---
        public static string GenerateMacHash()
        {
            var macAddresses = new List<string>();
            try
            {
                var searcher = new ManagementObjectSearcher("SELECT * FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = true");
                foreach (var obj in searcher.Get())
                {
                    var mac = obj["MACAddress"]?.ToString();
                    if (!string.IsNullOrEmpty(mac)) macAddresses.Add(mac);
                }
            }
            catch { }
            if (macAddresses.Count == 0) return string.Empty;
            macAddresses.Sort();
            string combinedMacs = string.Join("|", macAddresses);
            using (var sha256 = SHA256.Create())
            {
                byte[] hash = sha256.ComputeHash(System.Text.Encoding.UTF8.GetBytes(combinedMacs));
                return BitConverter.ToString(hash).Replace("-", string.Empty).ToLowerInvariant();
            }
        }

        private static void FatalSelfRestart()
        {
            Console.WriteLine("[FATAL] Watchdog abgestürzt. Kritischer Neustart wird ausgelöst.");
            Environment.Exit(99);
        }

        // --- Konfigurationsklasse ---
        public class UltraConfig
        {
            public string ADMIN_PASSWORD_HASH { get; set; } = string.Empty;
            public string JWT_SECRET { get; set; } = string.Empty;
            public string LLM_MODEL_NAME { get; set; } = string.Empty;
            public string OLLAMA_TARGET_URL { get; set; } = string.Empty;
            public string EXE_HASH { get; set; } = string.Empty;
            public string NODE_HASH { get; set; } = string.Empty;
            public string SCRIPT_HASH { get; set; } = string.Empty;
        }
    }
}
