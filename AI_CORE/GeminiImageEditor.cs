using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.IO;
using System.Collections.Generic;

/// <summary>
/// 🎨 MEGA ULTRA GEMINI IMAGE EDITOR
/// KI-BILDBEARBEITUNG MIT GOOGLE'S GEMINI MODEL
/// Erstellt: 26. Oktober 2025
///
/// FEATURES:
/// - Bildbearbeitung mit natürlicher Sprache
/// - Inpainting (Bereichsbasierte Bearbeitung)
/// - Outpainting (Bilderweiterung)
/// - Stiltransfer
/// - Objekterkennung und -bearbeitung
/// - Batch-Verarbeitung
/// - Fehlerbehandlung und Retry-Logik
/// </summary>
public class GeminiImageEditor
{
    // ===============================
    // 🔧 KONSTANTEN UND KONFIGURATION
    // ===============================
    private const string GeminiApiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent";
    private const int MaxRetries = 3;
    private const string DefaultModel = "gemini-1.5-pro";

    private readonly HttpClient _httpClient;
    private readonly string _apiKey;
    private readonly string _outputDirectory;

    // ===============================
    // 📊 BEARBEITUNGSSTATISTIKEN
    // ===============================
    public class EditingStats
    {
        public int TotalEdits { get; set; }
        public int SuccessfulEdits { get; set; }
        public int FailedEdits { get; set; }
        public TimeSpan AverageEditingTime { get; set; }
        public DateTime LastEdit { get; set; }
    }

    private readonly EditingStats _stats = new EditingStats();

    // ===============================
    // 📡 EVENTS FÜR UI-KOMMUNIKATION
    // ===============================
    public delegate void EditingProgressHandler(string message, int progress);
    public event EditingProgressHandler OnEditingProgress;

    public delegate void EditingCompleteHandler(ImageEditResult result);
    public event EditingCompleteHandler OnEditingComplete;

    // ===============================
    // 🚀 KONSTRUKTOR
    // ===============================
    public GeminiImageEditor(string apiKey, string outputDirectory = "edited_images")
    {
        if (string.IsNullOrEmpty(apiKey))
            throw new ArgumentException("API Key ist erforderlich für Gemini-Bildbearbeitung", nameof(apiKey));

        _apiKey = apiKey;
        _outputDirectory = outputDirectory;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5)
        };

        // Output-Verzeichnis erstellen
        Directory.CreateDirectory(_outputDirectory);

        Console.WriteLine("🎨 MEGA ULTRA GEMINI IMAGE EDITOR INITIALISIERT!");
        Console.WriteLine($"📁 Output-Verzeichnis: {_outputDirectory}");
    }

    // ===============================
    // 🎨 HAUPT-BEARBEITUNGSMETHODEN
    // ===============================

    /// <summary>
    /// 🎨 Bearbeitet ein Bild basierend auf einem Text-Prompt
    /// </summary>
    public async Task<ImageEditResult> EditImageAsync(string imagePath, string editPrompt, EditOptions options = null)
    {
        options ??= new EditOptions();

        OnEditingProgress?.Invoke($"🎨 Bearbeite Bild: {Path.GetFileName(imagePath)}", 0);

        var startTime = DateTime.Now;
        var result = new ImageEditResult
        {
            OriginalImagePath = imagePath,
            EditPrompt = editPrompt,
            Options = options
        };

        try
        {
            // Bild laden und validieren
            if (!File.Exists(imagePath))
                throw new FileNotFoundException("Bilddatei nicht gefunden", imagePath);

            var imageBytes = await File.ReadAllBytesAsync(imagePath);
            if (imageBytes.Length == 0)
                throw new InvalidDataException("Bilddatei ist leer");

            // MIME-Typ bestimmen
            var mimeType = GetMimeType(imagePath);

            // Bearbeitungsanfrage erstellen
            var request = BuildEditRequest(imageBytes, mimeType, editPrompt, options);
            var response = await SendEditRequestAsync(request);

            if (response.IsSuccess)
            {
                result.EditedImageData = response.ImageData;
                result.Success = true;
                result.EditingTime = DateTime.Now - startTime;

                // Bearbeitetes Bild speichern
                var filename = await SaveEditedImageAsync(result);
                result.EditedImagePath = filename;

                _stats.SuccessfulEdits++;
                OnEditingProgress?.Invoke("✅ Bild erfolgreich bearbeitet!", 100);
            }
            else
            {
                result.Success = false;
                result.ErrorMessage = response.ErrorMessage;
                _stats.FailedEdits++;
                OnEditingProgress?.Invoke($"❌ Bearbeitung fehlgeschlagen: {response.ErrorMessage}", 0);
            }
        }
        catch (Exception ex)
        {
            result.Success = false;
            result.ErrorMessage = ex.Message;
            _stats.FailedEdits++;
            OnEditingProgress?.Invoke($"💥 Fehler: {ex.Message}", 0);
        }

        _stats.TotalEdits++;
        _stats.LastEdit = DateTime.Now;
        _stats.AverageEditingTime = TimeSpan.FromTicks(
            (_stats.AverageEditingTime.Ticks * (_stats.TotalEdits - 1) + result.EditingTime.Ticks) / _stats.TotalEdits
        );

        OnEditingComplete?.Invoke(result);
        return result;
    }

    /// <summary>
    /// 🎨 Bearbeitet mehrere Bilder mit dem gleichen Prompt
    /// </summary>
    public async Task<List<ImageEditResult>> EditBatchAsync(List<string> imagePaths, string editPrompt, EditOptions options = null)
    {
        var results = new List<ImageEditResult>();

        OnEditingProgress?.Invoke($"🎨 Starte Batch-Bearbeitung: {imagePaths.Count} Bilder", 0);

        for (int i = 0; i < imagePaths.Count; i++)
        {
            OnEditingProgress?.Invoke($"🎨 Bearbeite Bild {i + 1}/{imagePaths.Count}...", (i * 100) / imagePaths.Count);

            var result = await EditImageAsync(imagePaths[i], editPrompt, options);
            results.Add(result);

            // Kurze Pause zwischen Bearbeitungen
            if (i < imagePaths.Count - 1)
                await Task.Delay(1000);
        }

        OnEditingProgress?.Invoke($"✅ Batch-Bearbeitung abgeschlossen: {results.Count(r => r.Success)}/{imagePaths.Count} erfolgreich", 100);
        return results;
    }

    /// <summary>
    /// 🎨 Wendet verschiedene Bearbeitungen auf ein Bild an
    /// </summary>
    public async Task<List<ImageEditResult>> ApplyMultipleEditsAsync(string imagePath, List<string> editPrompts, EditOptions options = null)
    {
        var results = new List<ImageEditResult>();

        foreach (var prompt in editPrompts)
        {
            var result = await EditImageAsync(imagePath, prompt, options);
            results.Add(result);
        }

        return results;
    }

    // ===============================
    // 🎯 SPEZIALISIERTE BEARBEITUNGSMETHODEN
    // ===============================

    /// <summary>
    /// 🖼️ Erweitert ein Bild (Outpainting)
    /// </summary>
    public async Task<ImageEditResult> ExtendImageAsync(string imagePath, string direction, string extensionPrompt)
    {
        var editPrompt = $"Extend this image {direction} with: {extensionPrompt}. Make it look natural and seamless.";
        var options = new EditOptions { EditMode = "outpainting" };

        return await EditImageAsync(imagePath, editPrompt, options);
    }

    /// <summary>
    /// 🎭 Wendet einen Stiltransfer an
    /// </summary>
    public async Task<ImageEditResult> ApplyStyleTransferAsync(string imagePath, string styleDescription)
    {
        var editPrompt = $"Apply this artistic style to the image: {styleDescription}. Maintain the original composition and subject.";
        var options = new EditOptions { EditMode = "style_transfer" };

        return await EditImageAsync(imagePath, editPrompt, options);
    }

    /// <summary>
    /// 🔧 Repariert oder verbessert Bildbereiche
    /// </summary>
    public async Task<ImageEditResult> EnhanceImageAsync(string imagePath, string enhancementPrompt)
    {
        var editPrompt = $"Enhance this image by: {enhancementPrompt}. Improve quality, lighting, and details.";
        var options = new EditOptions { EditMode = "enhancement" };

        return await EditImageAsync(imagePath, editPrompt, options);
    }

    // ===============================
    // 🔧 HILFSMETHODEN
    // ===============================

    /// <summary>
    /// Erstellt die API-Anfrage für Gemini
    /// </summary>
    private object BuildEditRequest(byte[] imageBytes, string mimeType, string editPrompt, EditOptions options)
    {
        var base64Image = Convert.ToBase64String(imageBytes);

        return new
        {
            contents = new[]
            {
                new
                {
                    parts = new object[]
                    {
                        new
                        {
                            text = $"Edit this image according to these instructions: {editPrompt}. " +
                                   $"Edit mode: {options.EditMode}. " +
                                   $"Be precise and maintain image quality."
                        },
                        new
                        {
                            inline_data = new
                            {
                                mime_type = mimeType,
                                data = base64Image
                            }
                        }
                    }
                }
            },
            generationConfig = new
            {
                temperature = options.Temperature,
                topK = options.TopK,
                topP = options.TopP,
                maxOutputTokens = options.MaxOutputTokens,
                response_mime_type = "application/json"
            }
        };
    }

    /// <summary>
    /// Sendet die Bearbeitungsanfrage an die Gemini API
    /// </summary>
    private async Task<GeminiImageApiResponse> SendEditRequestAsync(object request)
    {
        var response = new GeminiImageApiResponse();

        for (int attempt = 1; attempt <= MaxRetries; attempt++)
        {
            try
            {
                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var url = $"{GeminiApiUrl}?key={_apiKey}";
                var httpResponse = await _httpClient.PostAsync(url, content);

                if (httpResponse.IsSuccessStatusCode)
                {
                    var responseJson = await httpResponse.Content.ReadAsStringAsync();
                    var apiResponse = JsonSerializer.Deserialize<GeminiImageApiResponseData>(responseJson);

                    if (apiResponse?.candidates?.Length > 0)
                    {
                        var candidate = apiResponse.candidates[0];

                        // Extrahiere Bilddaten aus der Antwort
                        if (candidate.content?.parts?.Length > 0)
                        {
                            foreach (var part in candidate.content.parts)
                            {
                                if (part.inline_data?.data != null)
                                {
                                    response.IsSuccess = true;
                                    response.ImageData = Convert.FromBase64String(part.inline_data.data);
                                    return response;
                                }
                            }
                        }

                        // Fallback: Text-basierte Antwort parsen
                        if (candidate.content?.parts?.Length > 0)
                        {
                            var textPart = candidate.content.parts.FirstOrDefault(p => p.text != null);
                            if (textPart?.text != null)
                            {
                                // Hier könnte eine text-basierte Bildgenerierung erfolgen
                                response.ErrorMessage = "Gemini antwortete mit Text statt Bild. Verwende ImagenGenerator für Neugenerierung.";
                            }
                        }
                        else
                        {
                            response.ErrorMessage = "Keine verwertbaren Daten in der API-Antwort";
                        }
                    }
                    else
                    {
                        response.ErrorMessage = "Keine Kandidaten in der API-Antwort";
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
    /// Speichert das bearbeitete Bild auf der Festplatte
    /// </summary>
    private async Task<string> SaveEditedImageAsync(ImageEditResult result)
    {
        var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss_fff");
        var originalName = Path.GetFileNameWithoutExtension(result.OriginalImagePath);
        var safePrompt = result.EditPrompt.ReplaceInvalidFileNameChars("_").Truncate(30);
        var filename = $"edited_{originalName}_{timestamp}_{safePrompt}.png";
        var filepath = Path.Combine(_outputDirectory, filename);

        await File.WriteAllBytesAsync(filepath, result.EditedImageData);
        return filepath;
    }

    /// <summary>
    /// Bestimmt den MIME-Typ basierend auf der Dateierweiterung
    /// </summary>
    private string GetMimeType(string filePath)
    {
        var extension = Path.GetExtension(filePath).ToLower();
        return extension switch
        {
            ".png" => "image/png",
            ".jpg" => "image/jpeg",
            ".jpeg" => "image/jpeg",
            ".webp" => "image/webp",
            ".gif" => "image/gif",
            _ => "image/png" // Fallback
        };
    }

    // ===============================
    // 📊 STATISTIKEN UND MONITORING
    // ===============================

    /// <summary>
    /// Gibt aktuelle Bearbeitungsstatistiken zurück
    /// </summary>
    public EditingStats GetStats()
    {
        return new EditingStats
        {
            TotalEdits = _stats.TotalEdits,
            SuccessfulEdits = _stats.SuccessfulEdits,
            FailedEdits = _stats.FailedEdits,
            AverageEditingTime = _stats.AverageEditingTime,
            LastEdit = _stats.LastEdit
        };
    }

    /// <summary>
    /// Zeigt detaillierte Statistiken in der Konsole
    /// </summary>
    public void ShowStats()
    {
        var stats = GetStats();
        Console.WriteLine("\n" + "=".PadRight(60, '='));
        Console.WriteLine("📊 MEGA ULTRA GEMINI IMAGE EDITOR - STATISTIKEN");
        Console.WriteLine("=".PadRight(60, '='));
        Console.WriteLine($"🎨 Gesamtbearbeitungen: {stats.TotalEdits}");
        Console.WriteLine($"✅ Erfolgreich: {stats.SuccessfulEdits}");
        Console.WriteLine($"❌ Fehlgeschlagen: {stats.FailedEdits}");
        Console.WriteLine($"⏱️ Durchschnittliche Zeit: {stats.AverageEditingTime.TotalSeconds:F1}s");
        Console.WriteLine($"🕒 Letzte Bearbeitung: {stats.LastEdit:HH:mm:ss}");
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
/// Optionen für die Bildbearbeitung
/// </summary>
public class EditOptions
{
    public string EditMode { get; set; } = "general"; // "general", "inpainting", "outpainting", "style_transfer", "enhancement"
    public double Temperature { get; set; } = 0.8;
    public int TopK { get; set; } = 40;
    public double TopP { get; set; } = 0.95;
    public int MaxOutputTokens { get; set; } = 2048;
}

/// <summary>
/// Ergebnis einer Bildbearbeitung
/// </summary>
public class ImageEditResult
{
    public string OriginalImagePath { get; set; }
    public string EditPrompt { get; set; }
    public EditOptions Options { get; set; }
    public bool Success { get; set; }
    public byte[] EditedImageData { get; set; }
    public string EditedImagePath { get; set; }
    public string ErrorMessage { get; set; }
    public TimeSpan EditingTime { get; set; }
}

/// <summary>
/// API-Antwort von Google Gemini
/// </summary>
internal class GeminiImageApiResponse
{
    public bool IsSuccess { get; set; }
    public byte[] ImageData { get; set; }
    public string ErrorMessage { get; set; }
}

internal class GeminiImageApiResponseData
{
    public GeminiImageCandidate[] candidates { get; set; }
}

internal class GeminiImageCandidate
{
    public GeminiImageContent content { get; set; }
}

internal class GeminiImageContent
{
    public GeminiImagePart[] parts { get; set; }
}

internal class GeminiImagePart
{
    public string text { get; set; }
    public GeminiImageInlineData inline_data { get; set; }
}

internal class GeminiImageInlineData
{
    public string mime_type { get; set; }
    public string data { get; set; }
}
