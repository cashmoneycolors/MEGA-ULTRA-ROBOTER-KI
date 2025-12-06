using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.IO;
using System.Collections.Generic;

/// <summary>
/// 🌟 MEGA ULTRA IMAGEN GENERATOR
/// KI-BILDGENERIERUNG MIT GOOGLE'S IMAGEN MODEL
/// Erstellt: 26. Oktober 2025
///
/// FEATURES:
/// - Text-zu-Bild Generierung
/// - Hochauflösende Bilder (bis 1024x1024)
/// - Mehrere Bildvarianten pro Prompt
/// - Automatische Qualitätsoptimierung
/// - Batch-Verarbeitung
/// - Fehlerbehandlung und Retry-Logik
/// </summary>
public class ImagenGenerator
{
    // ===============================
    // 🔧 KONSTANTEN UND KONFIGURATION
    // ===============================
    private const string ImagenApiUrl = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImage";
    private const int MaxRetries = 3;
    private const int DefaultImageCount = 1;
    private const string DefaultAspectRatio = "1:1";
    private const string DefaultPersonGeneration = "allow_adult";

    private readonly HttpClient _httpClient;
    private readonly string _apiKey;
    private readonly string _outputDirectory;

    // ===============================
    // 📊 GENERIERUNGSSTATISTIKEN
    // ===============================
    public class GenerationStats
    {
        public int TotalGenerations { get; set; }
        public int SuccessfulGenerations { get; set; }
        public int FailedGenerations { get; set; }
        public TimeSpan AverageGenerationTime { get; set; }
        public DateTime LastGeneration { get; set; }
    }

    private readonly GenerationStats _stats = new GenerationStats();

    // ===============================
    // 📡 EVENTS FÜR UI-KOMMUNIKATION
    // ===============================
    public delegate void GenerationProgressHandler(string message, int progress);
    public event GenerationProgressHandler OnGenerationProgress;

    public delegate void GenerationCompleteHandler(ImagenResult result);
    public event GenerationCompleteHandler OnGenerationComplete;

    // ===============================
    // 🚀 KONSTRUKTOR
    // ===============================
    public ImagenGenerator(string apiKey, string outputDirectory = "generated_images")
    {
        if (string.IsNullOrEmpty(apiKey))
            throw new ArgumentException("API Key ist erforderlich für Imagen-Generierung", nameof(apiKey));

        _apiKey = apiKey;
        _outputDirectory = outputDirectory;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5)
        };

        // Output-Verzeichnis erstellen
        Directory.CreateDirectory(_outputDirectory);

        Console.WriteLine("🌟 MEGA ULTRA IMAGEN GENERATOR INITIALISIERT!");
        Console.WriteLine($"📁 Output-Verzeichnis: {_outputDirectory}");
    }

    // ===============================
    // 🎨 HAUPT-GENERIERUNGSMETHODEN
    // ===============================

    /// <summary>
    /// 🎨 Generiert ein einzelnes Bild aus Text-Prompt
    /// </summary>
    public async Task<ImagenResult> GenerateImageAsync(string prompt, ImagenOptions options = null)
    {
        options ??= new ImagenOptions();

        OnGenerationProgress?.Invoke($"🎨 Generiere Bild: {prompt.Truncate(50)}...", 0);

        var startTime = DateTime.Now;
        var result = new ImagenResult { Prompt = prompt, Options = options };

        try
        {
            var request = BuildGenerationRequest(prompt, options);
            var response = await SendGenerationRequestAsync(request);

            if (response.IsSuccess)
            {
                result.ImageData = response.ImageData;
                result.Success = true;
                result.GenerationTime = DateTime.Now - startTime;

                // Bild speichern
                var filename = await SaveImageAsync(result);
                result.Filename = filename;

                _stats.SuccessfulGenerations++;
                OnGenerationProgress?.Invoke("✅ Bild erfolgreich generiert!", 100);
            }
            else
            {
                result.Success = false;
                result.ErrorMessage = response.ErrorMessage;
                _stats.FailedGenerations++;
                OnGenerationProgress?.Invoke($"❌ Generierung fehlgeschlagen: {response.ErrorMessage}", 0);
            }
        }
        catch (Exception ex)
        {
            result.Success = false;
            result.ErrorMessage = ex.Message;
            _stats.FailedGenerations++;
            OnGenerationProgress?.Invoke($"💥 Fehler: {ex.Message}", 0);
        }

        _stats.TotalGenerations++;
        _stats.LastGeneration = DateTime.Now;
        _stats.AverageGenerationTime = TimeSpan.FromTicks(
            (_stats.AverageGenerationTime.Ticks * (_stats.TotalGenerations - 1) + result.GenerationTime.Ticks) / _stats.TotalGenerations
        );

        OnGenerationComplete?.Invoke(result);
        return result;
    }

    /// <summary>
    /// 🎨 Generiert mehrere Bilder aus einem Prompt (Batch)
    /// </summary>
    public async Task<List<ImagenResult>> GenerateBatchAsync(string prompt, int count, ImagenOptions options = null)
    {
        var results = new List<ImagenResult>();
        options ??= new ImagenOptions();

        OnGenerationProgress?.Invoke($"🎨 Starte Batch-Generierung: {count} Bilder", 0);

        for (int i = 0; i < count; i++)
        {
            OnGenerationProgress?.Invoke($"🎨 Generiere Bild {i + 1}/{count}...", (i * 100) / count);

            // Variiere den Prompt leicht für unterschiedliche Ergebnisse
            var variedPrompt = count > 1 ? VaryPrompt(prompt, i) : prompt;
            var result = await GenerateImageAsync(variedPrompt, options);
            results.Add(result);

            // Kurze Pause zwischen Generierungen
            if (i < count - 1)
                await Task.Delay(1000);
        }

        OnGenerationProgress?.Invoke($"✅ Batch-Generierung abgeschlossen: {results.Count(r => r.Success)}/{count} erfolgreich", 100);
        return results;
    }

    /// <summary>
    /// 🎨 Generiert Bilder aus mehreren Prompts parallel
    /// </summary>
    public async Task<List<ImagenResult>> GenerateMultiplePromptsAsync(List<string> prompts, ImagenOptions options = null)
    {
        var tasks = prompts.Select(prompt => GenerateImageAsync(prompt, options)).ToList();
        var results = await Task.WhenAll(tasks);

        OnGenerationProgress?.Invoke($"✅ Multi-Prompt Generierung abgeschlossen: {results.Count(r => r.Success)}/{prompts.Count} erfolgreich", 100);
        return results.ToList();
    }

    // ===============================
    // 🔧 HILFSMETHODEN
    // ===============================

    /// <summary>
    /// Erstellt die API-Anfrage für Imagen
    /// </summary>
    private object BuildGenerationRequest(string prompt, ImagenOptions options)
    {
        return new
        {
            prompt = new
            {
                text = prompt
            },
            generationConfig = new
            {
                numberOfImages = options.NumberOfImages,
                aspectRatio = options.AspectRatio,
                personGeneration = options.PersonGeneration,
                negativePrompt = options.NegativePrompt,
                safetySettings = new[]
                {
                    new
                    {
                        category = "HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold = "BLOCK_LOW_AND_ABOVE"
                    }
                }
            }
        };
    }

    /// <summary>
    /// Sendet die Generierungsanfrage an die Imagen API
    /// </summary>
    private async Task<dynamic> SendGenerationRequestAsync(object request)
    {
        // Temporäre Klasse für API-Antwort
        dynamic response = new
        {
            IsSuccess = false,
            ImageData = new byte[0],
            ErrorMessage = ""
        };

        for (int attempt = 1; attempt <= MaxRetries; attempt++)
        {
            try
            {
                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var url = $"{ImagenApiUrl}?key={_apiKey}";
                var httpResponse = await _httpClient.PostAsync(url, content);

                if (httpResponse.IsSuccessStatusCode)
                {
                    var responseJson = await httpResponse.Content.ReadAsStringAsync();
                    var apiResponse = JsonSerializer.Deserialize<ImagenApiResponseData>(responseJson);

                    if (apiResponse?.candidates?.Length > 0 && apiResponse.candidates[0]?.image?.bytesBase64 != null)
                    {
                        response.IsSuccess = true;
                        response.ImageData = Convert.FromBase64String(apiResponse.candidates[0].image.bytesBase64);
                        return response;
                    }
                    else
                    {
                        response.ErrorMessage = "Keine Bilddaten in der API-Antwort";
                    }
                }
                else
                {
                    var errorContent = await httpResponse.Content.ReadAsStringAsync();
                    response.ErrorMessage = $"HTTP {httpResponse.StatusCode}: {errorContent}";
                }
            }
            catch (Exception ex)
            {
                response.ErrorMessage = $"Versuch {attempt}/{MaxRetries} fehlgeschlagen: {ex.Message}";
            }

            // Warte vor dem nächsten Versuch
            if (attempt < MaxRetries)
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));
        }

        return response;
    }

    /// <summary>
    /// Speichert das generierte Bild auf der Festplatte
    /// </summary>
    private async Task<string> SaveImageAsync(ImagenResult result)
    {
        var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss_fff");
        var safePrompt = result.Prompt.ReplaceInvalidFileNameChars("_").Truncate(50);
        var filename = $"imagen_{timestamp}_{safePrompt}.png";
        var filepath = Path.Combine(_outputDirectory, filename);

        await File.WriteAllBytesAsync(filepath, result.ImageData);
        return filename;
    }

    /// <summary>
    /// Variiert einen Prompt leicht für unterschiedliche Ergebnisse
    /// </summary>
    private string VaryPrompt(string basePrompt, int variation)
    {
        var variations = new[]
        {
            ", highly detailed",
            ", artistic style",
            ", photorealistic",
            ", vibrant colors",
            ", dramatic lighting"
        };

        return basePrompt + variations[variation % variations.Length];
    }

    // ===============================
    // 📊 STATISTIKEN UND MONITORING
    // ===============================

    /// <summary>
    /// Gibt aktuelle Generierungsstatistiken zurück
    /// </summary>
    public GenerationStats GetStats()
    {
        return new GenerationStats
        {
            TotalGenerations = _stats.TotalGenerations,
            SuccessfulGenerations = _stats.SuccessfulGenerations,
            FailedGenerations = _stats.FailedGenerations,
            AverageGenerationTime = _stats.AverageGenerationTime,
            LastGeneration = _stats.LastGeneration
        };
    }

    /// <summary>
    /// Zeigt detaillierte Statistiken in der Konsole
    /// </summary>
    public void ShowStats()
    {
        var stats = GetStats();
        Console.WriteLine("\n" + "=".PadRight(60, '='));
        Console.WriteLine("📊 MEGA ULTRA IMAGEN GENERATOR - STATISTIKEN");
        Console.WriteLine("=".PadRight(60, '='));
        Console.WriteLine($"🎨 Gesamtgenerierungen: {stats.TotalGenerations}");
        Console.WriteLine($"✅ Erfolgreich: {stats.SuccessfulGenerations}");
        Console.WriteLine($"❌ Fehlgeschlagen: {stats.FailedGenerations}");
        Console.WriteLine($"⏱️ Durchschnittliche Zeit: {stats.AverageGenerationTime.TotalSeconds:F1}s");
        Console.WriteLine($"🕒 Letzte Generierung: {stats.LastGeneration:HH:mm:ss}");
        Console.WriteLine("=".PadRight(60, '='));
    }

    // ===============================
    // 🧹 RESSOURCEN-BEREINIGUNG
    // ===============================
    public void Dispose()
    {
        _httpClient?.Dispose();
    }
}

// ===============================
// 📋 DATENMODELLE
// ===============================

/// <summary>
/// Optionen für die Imagen-Generierung
/// </summary>
public class ImagenOptions
{
    public int NumberOfImages { get; set; } = 1;
    public string AspectRatio { get; set; } = "1:1"; // "1:1", "4:3", "16:9", "3:4", "9:16"
    public string PersonGeneration { get; set; } = "allow_adult"; // "allow_adult", "block_some", "block_all"
    public string NegativePrompt { get; set; } = "";
}

/// <summary>
/// Ergebnis einer Imagen-Generierung
/// </summary>
public class ImagenResult
{
    public string Prompt { get; set; }
    public ImagenOptions Options { get; set; }
    public bool Success { get; set; }
    public byte[] ImageData { get; set; }
    public string Filename { get; set; }
    public string ErrorMessage { get; set; }
    public TimeSpan GenerationTime { get; set; }
}

// API-Response-Klassen wurden entfernt, um Duplikate zu vermeiden

// ===============================
// 🔧 ERWEITERUNGSMETHODEN
// ===============================

public static class ImagenExtensions
{
    /// <summary>
    /// Kürzt einen String auf eine maximale Länge
    /// </summary>
    public static string Truncate(this string value, int maxLength)
    {
        return value.Length <= maxLength ? value : value.Substring(0, maxLength);
    }

    /// <summary>
    /// Ersetzt ungültige Dateinamen-Zeichen
    /// </summary>
    public static string ReplaceInvalidFileNameChars(this string filename, string replacement = "_")
    {
        var invalidChars = Path.GetInvalidFileNameChars();
        return string.Join(replacement, filename.Split(invalidChars));
    }
}
