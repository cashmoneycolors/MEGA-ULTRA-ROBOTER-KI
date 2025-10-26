using System;
using MegaUltra.Networking;
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
using System.Management; // Für RAM-Checks (WMI)

namespace RoboterKIUltra
{
        public class RoboterKIUltraController
        {
            // --- Ultra-Maxima Kernkonstanten ---
            private const string ConfigFileName = "roboter_ki_ultra_config.json";
            private const string NodeServerExe = "opengazai-server.exe";
            private const string NodeServerScript = "opengazai-server.js";
            private const int PublicPort = 3000;
            private const int OllamaPort = 11434;
            private const int MaxRestarts = 5;
            private const int JwtRotationDays = 90;
            private static Mutex? _appMutex;
            private static Process? _serverProcess;
            private static CancellationTokenSource _cts = new CancellationTokenSource();
            private static UltraConfig? _config;
            private static List<int> _badPorts = new List<int>();
            private static string _lastError = string.Empty;

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

        // --- Einstiegspunkt ---
        public static async Task Main(string[] args)
        {
            /***********************************************************************
             * WICHTIG: SECRET-HANDLING (MAXIMALE SICHERHEIT)
             * ---------------------------------------------------------------------
             * Secrets wie JWT_SECRET dürfen NIEMALS im Quellcode hardcodiert werden!
             * 1. Immer zuerst per Umgebungsvariable beziehen (z.B. aus Docker, .env, CI/CD, Key Vault).
             * 2. Falls nicht gesetzt, wird ein sicheres Secret zur Laufzeit generiert (nur für lokale Entwicklung!).
             * 3. WARNUNG: In Produktion MÜSSEN die Secrets gesetzt sein – sonst ist die System-Sicherheit gefährdet!
             * 4. Entwickler:innen werden explizit gewarnt, wenn ein Secret generiert wird.
             ***********************************************************************/

            // --- Secret-Handling: Niemals hardcodieren! ---
            string jwtSecret = Environment.GetEnvironmentVariable("JWT_SECRET");
            if (string.IsNullOrEmpty(jwtSecret)) {
                jwtSecret = Guid.NewGuid().ToString("N");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("[WARNUNG] JWT_SECRET ist NICHT gesetzt! Es wurde ein temporäres Secret generiert. Bitte Secret als Umgebungsvariable setzen (z.B. $env:JWT_SECRET=...) – Niemals im Code speichern!");
                Console.ResetColor();
            }
            // Übernehme Secret in die Config, falls vorhanden
            if (_config != null && !string.IsNullOrEmpty(jwtSecret)) _config.JWT_SECRET = jwtSecret;
            // Single-Instance-Garantie
            _appMutex = new Mutex(true, "Global\\RoboterKIUltraController_Mutex", out bool createdNew);
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
            RotateJwtSecretIfNeeded();

            // Autonomer Start
            var (success, message) = await StartKeyServerAutonom();
            if (!success)
            {
                Console.WriteLine($"[FATAL] {message}");
                Environment.Exit(99);
            }
            Console.WriteLine($"[INFO] {message}");

            // Watchdog starten
            _ = MonitorServerLifetime();

            // Interaktive Schleife (optional)
            while (true)
            {
                Console.WriteLine("q = Quit, s = Status");
                var key = Console.ReadKey(true);
                if (key.KeyChar == 'q') break;
                if (key.KeyChar == 's') ShowStatus();
            }
            _cts.Cancel();
            _serverProcess?.Kill();
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
            int runningPort = portFindTask.Result;
            if (runningPort == 0) return (false, "Kein freier Port gefunden.");
            // Modell-Bereitschaft
            if (!await CheckAndPullOllamaModel(_config.LLM_MODEL_NAME, _config.OLLAMA_TARGET_URL))
                return (false, $"Modell '{_config.LLM_MODEL_NAME}' nicht bereit.");
            // Server-Prozess starten
            try
            {
                var psi = new ProcessStartInfo(NodeServerExe, $"--port {runningPort} --datapath ./data --admin_hash {_config.ADMIN_PASSWORD_HASH} --jwt_secret {_config.JWT_SECRET} --ollama_url {_config.OLLAMA_TARGET_URL} --model_name {_config.LLM_MODEL_NAME}")
                {
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                };
                _serverProcess = Process.Start(psi);
                _serverProcess.PriorityClass = ProcessPriorityClass.AboveNormal;
                // Bereitschaftsprüfung
                if (!await WaitForServerReady(runningPort, _cts.Token))
                {
                    _serverProcess.Kill();
                    return (false, "Node.js Serverstart fehlgeschlagen.");
                }
            }
            catch (Exception ex)
            {
                return (false, $"FEHLER beim Start des Servers: {ex.Message}");
            }
            return (true, $"OpenGazAI gestartet auf Port {runningPort}.");
        }

        // --- Watchdog & Selbstheilung ---
        private static async Task MonitorServerLifetime()
        {
            int restartCount = 0;
            while (!_cts.IsCancellationRequested)
            {
                await Task.Delay(5000, _cts.Token);
                if (_serverProcess == null || _serverProcess.HasExited)
                {
                    if (restartCount < MaxRestarts)
                    {
                        restartCount++;
                        Console.WriteLine($"[WATCHDOG] Server-Prozess beendet. Neustartversuch {restartCount}...");
                        var (success, message) = await StartKeyServerAutonom();
                        if (!success) { _lastError = message; continue; }
                    }
                    else
                    {
                        Console.WriteLine("[WATCHDOG] Max. Neustartversuche erreicht. System-Reset.");
                        Environment.Exit(99);
                    }
                }
                if (!await CheckServerHeartbeat(PublicPort))
                {
                    Console.WriteLine("[WATCHDOG] Heartbeat-Check fehlgeschlagen. Server wird neu gestartet.");
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
                // RAM-Check: Verfügbarer physischer Speicher (in GB)
                var totalRam = GetTotalPhysicalMemoryGb();
                var availableRam = GetAvailablePhysicalMemoryGb();
                if (totalRam < minRamGb)
                {
                    Console.WriteLine($"[RAM] Gesamt-RAM zu gering: {totalRam:F2} GB < {minRamGb} GB");
                    return false;
                }
                if (availableRam < minRamGb * 0.7)
                {
                    Console.WriteLine($"[RAM] Zu wenig freier RAM: {availableRam:F2} GB < {minRamGb * 0.7:F2} GB");
                    return false;
                }
                // Disk-Check: Mindestens 1.5x Modellgröße auf Systemlaufwerk (C:)
                var sysDrive = DriveInfo.GetDrives().FirstOrDefault(d => d.Name.StartsWith("C", StringComparison.OrdinalIgnoreCase) && d.IsReady);
                if (sysDrive != null)
                {
                    long freeGb = sysDrive.AvailableFreeSpace / (1024 * 1024 * 1024);
                    if (freeGb < 10) // 10 GB als Mindestwert
                    {
                        Console.WriteLine($"[DISK] Zu wenig freier Speicher auf {sysDrive.Name}: {freeGb} GB");
                        return false;
                    }
                }
                else
                {
                    Console.WriteLine("[DISK] Systemlaufwerk nicht gefunden oder nicht bereit.");
                    return false;
                }
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] Ressourcen-Check fehlgeschlagen: {ex.Message}");
                return false;
            }
        }
        // --- RAM- und Disk-Check Hilfsmethoden ---
        private static double GetTotalPhysicalMemoryGb()
        {
            try
            {
                // Windows: System.Management (WMI)
                var searcher = new System.Management.ManagementObjectSearcher("SELECT TotalPhysicalMemory FROM Win32_ComputerSystem");
                foreach (var obj in searcher.Get())
                {
                    double bytes = Convert.ToDouble(obj["TotalPhysicalMemory"]);
                    return bytes / (1024 * 1024 * 1024);
                }
            }
            catch { }
            // Fallback: GC
            return GC.GetGCMemoryInfo().TotalAvailableMemoryBytes / (1024.0 * 1024 * 1024);
        }
        private static double GetAvailablePhysicalMemoryGb()
        {
            try
            {
                var searcher = new System.Management.ManagementObjectSearcher("SELECT FreePhysicalMemory FROM Win32_OperatingSystem");
                foreach (var obj in searcher.Get())
                {
                    double kb = Convert.ToDouble(obj["FreePhysicalMemory"]);
                    return kb / (1024 * 1024);
                }
            }
            catch { }
            // Fallback: GC
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
            // Dummy: Immer true (hier Modell-Check und Pull implementieren)
            await Task.Delay(1000); return true;
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
            return JsonSerializer.Deserialize<UltraConfig>(json);
        }
        private static void SaveConfigAtomically(UltraConfig cfg)
        {
            string json = JsonSerializer.Serialize(cfg, new JsonSerializerOptions { WriteIndented = true });
            string tmp = ConfigFileName + ".tmp";
            File.WriteAllText(tmp, json);
            File.Replace(tmp, ConfigFileName, null);
        }
        private static void RotateJwtSecretIfNeeded()
        {
            // Dummy: JWT-Rotation nach 90 Tagen (hier Logik implementieren)
        }
        // --- Integritätsprüfung ---
        private static bool CheckBinaryIntegrity()
        {
            try
            {
                // Eigene .exe/.dll prüfen
                string exePath = Process.GetCurrentProcess().MainModule.FileName;
                string exeHash = ComputeFileSha512Hash(exePath);
                // Node.js-Server prüfen
                string? nodeHash = File.Exists(NodeServerExe) ? ComputeFileSha512Hash(NodeServerExe) : null;
                string? scriptHash = File.Exists(NodeServerScript) ? ComputeFileSha512Hash(NodeServerScript) : null;
                // Referenz-Hashes aus Config laden
                if (_config == null || string.IsNullOrEmpty(_config.EXE_HASH))
                {
                    // Erststart: Hashes speichern
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
                // Prüfen
                if (_config.EXE_HASH != exeHash)
                {
                    Console.WriteLine("[INTEGRITY] EXE-Hash stimmt nicht überein!");
                    return false;
                }
                if (!string.IsNullOrEmpty(_config.NODE_HASH) && nodeHash != null && _config.NODE_HASH != nodeHash)
                {
                    Console.WriteLine("[INTEGRITY] Node.js-Server-Hash stimmt nicht überein!");
                    return false;
                }
                if (!string.IsNullOrEmpty(_config.SCRIPT_HASH) && scriptHash != null && _config.SCRIPT_HASH != scriptHash)
                {
                    Console.WriteLine("[INTEGRITY] Node.js-Skript-Hash stimmt nicht überein!");
                    return false;
                }
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] Integritätsprüfung fehlgeschlagen: {ex.Message}");
                return false;
            }
        }

        // --- SHA-512 Datei-Hashing ---
        private static string ComputeFileSha512Hash(string filePath)
        {
            using var stream = File.OpenRead(filePath);
            using var sha = SHA512.Create();
            byte[] hash = sha.ComputeHash(stream);
            return BitConverter.ToString(hash).Replace("-", string.Empty).ToLowerInvariant();
        }

        private static void ShowStatus()
        {
            Console.WriteLine($"Status: Server läuft: {_serverProcess != null && !_serverProcess.HasExited}, Letzter Fehler: {_lastError}");
        }

        // --- PBKDF2-Hashing für Admin-Passwort ---
        private static string HashPasswordPBKDF2(string password, out string salt, int iterations)
        {
            using var rng = RandomNumberGenerator.Create();
            byte[] saltBytes = new byte[32];
            rng.GetBytes(saltBytes);
            salt = Convert.ToBase64String(saltBytes);
            using var pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, iterations, HashAlgorithmName.SHA512);
            byte[] hash = pbkdf2.GetBytes(64);
            return Convert.ToBase64String(hash);
        }
        private static bool VerifyPasswordPBKDF2(string password, string hash, string salt, int iterations)
        {
            byte[] saltBytes = Convert.FromBase64String(salt);
            using var pbkdf2 = new Rfc2898DeriveBytes(password, saltBytes, iterations, HashAlgorithmName.SHA512);
            byte[] hashBytes = pbkdf2.GetBytes(64);
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

        // --- Konfigurationsklasse ---
        public class UltraConfig
        {
            public string ADMIN_PASSWORD_HASH { get; set; } = string.Empty;
            public string JWT_SECRET { get; set; } = string.Empty;
            public string LLM_MODEL_NAME { get; set; } = string.Empty;
            public string OLLAMA_TARGET_URL { get; set; } = string.Empty;
            // Integritäts-Hashes
            public string EXE_HASH { get; set; } = string.Empty;
            public string NODE_HASH { get; set; } = string.Empty;
            public string SCRIPT_HASH { get; set; } = string.Empty;
        }
    }
    }
