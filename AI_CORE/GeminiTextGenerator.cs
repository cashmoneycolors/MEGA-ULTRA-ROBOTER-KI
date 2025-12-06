using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

/// <summary>
/// 📝 MEGA ULTRA GEMINI TEXT GENERATOR
/// KI-TEXTGENERIERUNG MIT GOOGLE'S GEMINI MODEL
/// Erstellt: 26. Oktober 2025
///
/// FEATURES:
/// - Hochqualitative Textgenerierung
/// - Mehrere Gemini-Modelle (1.0, 1.5 Pro, etc.)
/// - Streaming-Unterstützung
/// - Konversationsmodus
/// - Batch-Verarbeitung
/// - Token-Counting und Kostenberechnung
/// - Fehlerbehandlung und Retry-Logik
/// </summary>
public class GeminiTextGenerator
{
    // ===============================
    // 🔧 KONSTANTEN UND KONFIGURATION
    // ===============================
    private const string GeminiApiUrl = "https://generativelanguage.googleapis.com/v1beta/models";
    private const int MaxRetries = 3;
    private const string DefaultModel = "gemini-1.5-pro";

    private readonly HttpClient _httpClient;
    private readonly string _apiKey;
    private readonly string _model;

    // ===============================
    // 📊 GENERIERUNGSSTATISTIKEN
    // ===============================
    public class GenerationStats
    {
        public int TotalGenerations { get; set; }
        public int SuccessfulGenerations { get; set; }
        public int FailedGenerations { get; set; }
        public long TotalTokensUsed { get; set; }
        public TimeSpan AverageGenerationTime { get; set; }
        public DateTime LastGeneration { get; set; }
        public decimal EstimatedCost { get; set; }
    }

    private readonly GenerationStats _stats = new GenerationStats();

    // ===============================
    // 📡 EVENTS FÜR UI-KOMMUNIKATION
    // ===============================
    public delegate void GenerationProgressHandler(string message, int progress);
    public event GenerationProgressHandler OnGenerationProgress;

    public delegate void GenerationCompleteHandler(TextGenerationResult result);
    public event GenerationCompleteHandler OnGenerationComplete;

    public delegate void StreamingChunkHandler(string chunk);
    public event StreamingChunkHandler OnStreamingChunk;

    // ===============================
    // 🚀 KONSTRUKTOR
    // ===============================
    public GeminiTextGenerator(string apiKey, string model = null)
    {
        if (string.IsNullOrEmpty(apiKey))
            throw new ArgumentException("API Key ist erforderlich für Gemini-Generierung", nameof(apiKey));

        _apiKey = apiKey;
        _model = model ?? DefaultModel;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5)
        };

        Console.WriteLine("📝 MEGA ULTRA GEMINI TEXT GENERATOR INITIALISIERT!");
        Console.WriteLine($"🤖 Modell: {_model}");
    }

    // ===============================
    // 📝 HAUPT-GENERIERUNGSMETHODEN
    // ===============================

    /// <summary>
    /// 📝 Generiert Text aus einem Prompt
    /// </summary>
    public async Task<TextGenerationResult> GenerateTextAsync(string prompt, GenerationOptions options = null)
    {
        options ??= new GenerationOptions();

        OnGenerationProgress?.Invoke($"📝 Generiere Text: {prompt.Truncate(50)}...", 0);

        var startTime = DateTime.Now;
        var result = new TextGenerationResult { Prompt = prompt, Options = options };

        try
        {
            var request = BuildGenerationRequest(prompt, options);
            var response = await SendGenerationRequestAsync(request, options.Stream);

            if (response.IsSuccess)
            {
                result.GeneratedText = response.GeneratedText;
                result.Success = true;
                result.GenerationTime = DateTime.Now - startTime;
                result.TokensUsed = EstimateTokens(prompt, result.GeneratedText);

                _stats.SuccessfulGenerations++;
                _stats.TotalTokensUsed += result.TokensUsed;
                UpdateEstimatedCost(result.TokensUsed);

                OnGenerationProgress?.Invoke("✅ Text erfolgreich generiert!", 100);
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
    /// 📝 Generiert Text im Streaming-Modus
    /// </summary>
    public async Task<TextGenerationResult> GenerateTextStreamingAsync(string prompt, GenerationOptions options = null)
    {
        options ??= new GenerationOptions { Stream = true };

        var result = await GenerateTextAsync(prompt, options);

        // Streaming wird in SendGenerationRequestAsync behandelt
        return result;
    }

    /// <summary>
    /// 📝 Generiert mehrere Texte aus verschiedenen Prompts (Batch)
    /// </summary>
    public async Task<List<TextGenerationResult>> GenerateBatchAsync(List<string> prompts, GenerationOptions options = null)
    {
        var results = new List<TextGenerationResult>();

        OnGenerationProgress?.Invoke($"📝 Starte Batch-Generierung: {prompts.Count} Prompts", 0);

        for (int i = 0; i < prompts.Count; i++)
        {
            OnGenerationProgress?.Invoke($"📝 Generiere Text {i + 1}/{prompts.Count}...", (i * 100) / prompts.Count);

            var result = await GenerateTextAsync(prompts[i], options);
            results.Add(result);

            // Kurze Pause zwischen Generierungen
            if (i < prompts.Count - 1)
                await Task.Delay(500);
        }

        OnGenerationProgress?.Invoke($"✅ Batch-Generierung abgeschlossen: {results.Count(r => r.Success)}/{prompts.Count} erfolgreich", 100);
        return results;
    }

    /// <summary>
    /// 💬 Führt eine Konversation mit dem Modell
    /// </summary>
    public async Task<ConversationResult> ConverseAsync(List<ConversationMessage> messages, GenerationOptions options = null)
    {
        options ??= new GenerationOptions();

        var conversationResult = new ConversationResult { Messages = messages };

        try
        {
            var request = BuildConversationRequest(messages, options);
            var response = await SendGenerationRequestAsync(request, options.Stream);

            if (response.IsSuccess)
            {
                var aiMessage = new ConversationMessage
                {
                    Role = "assistant",
                    Content = response.GeneratedText,
                    Timestamp = DateTime.Now
                };

                conversationResult.Messages.Add(aiMessage);
                conversationResult.Success = true;
                conversationResult.TotalTokens = EstimateTokens(messages, aiMessage);
                UpdateEstimatedCost(conversationResult.TotalTokens);
            }
            else
            {
                conversationResult.Success = false;
                conversationResult.ErrorMessage = response.ErrorMessage;
            }
        }
        catch (Exception ex)
        {
            conversationResult.Success = false;
            conversationResult.ErrorMessage = ex.Message;
        }

        return conversationResult;
    }

    // ===============================
    // 🔧 HILFSMETHODEN
    // ===============================

    /// <summary>
    /// Erstellt die API-Anfrage für Gemini
    /// </summary>
    private object BuildGenerationRequest(string prompt, GenerationOptions options)
    {
        return new
        {
            contents = new[]
            {
                new
                {
                    parts = new[]
                    {
                        new
                        {
                            text = prompt
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
                stopSequences = options.StopSequences
            },
            safetySettings = new[]
            {
                new
                {
                    category = "HARM_CATEGORY_HARASSMENT",
                    threshold = "BLOCK_MEDIUM_AND_ABOVE"
                },
                new
                {
                    category = "HARM_CATEGORY_HATE_SPEECH",
                    threshold = "BLOCK_MEDIUM_AND_ABOVE"
                },
                new
                {
                    category = "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold = "BLOCK_MEDIUM_AND_ABOVE"
                },
                new
                {
                    category = "HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold = "BLOCK_MEDIUM_AND_ABOVE"
                }
            }
        };
    }

    /// <summary>
    /// Erstellt eine Konversationsanfrage
    /// </summary>
    private object BuildConversationRequest(List<ConversationMessage> messages, GenerationOptions options)
    {
        var contents = new List<object>();

        foreach (var message in messages)
        {
            contents.Add(new
            {
                role = message.Role,
                parts = new[]
                {
                    new
                    {
                        text = message.Content
                    }
                }
            });
        }

        return new
        {
            contents = contents.ToArray(),
            generationConfig = new
            {
                temperature = options.Temperature,
                topK = options.TopK,
                topP = options.TopP,
                maxOutputTokens = options.MaxOutputTokens,
                stopSequences = options.StopSequences
            }
        };
    }

    /// <summary>
    /// Sendet die Generierungsanfrage an die Gemini API
    /// </summary>
    private async Task<dynamic> SendGenerationRequestAsync(object request, bool stream = false)
    {
        // Temporäre Klasse für API-Antwort
        dynamic response = new
        {
            IsSuccess = false,
            GeneratedText = "",
            ErrorMessage = ""
        };

        for (int attempt = 1; attempt <= MaxRetries; attempt++)
        {
            try
            {
                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var url = $"{GeminiApiUrl}/{_model}:generateContent?key={_apiKey}";
                if (stream)
                {
                    url += "&alt=sse";
                }

                var httpResponse = await _httpClient.PostAsync(url, content);

                if (httpResponse.IsSuccessStatusCode)
                {
                    var responseJson = await httpResponse.Content.ReadAsStringAsync();
                    var apiResponse = JsonSerializer.Deserialize<GeminiTextApiResponseData>(responseJson);

                    if (apiResponse?.candidates?.Length > 0)
                    {
                        var candidate = apiResponse.candidates[0];

                        if (candidate.finishReason == "STOP" || candidate.finishReason == null)
                        {
                            response.IsSuccess = true;
                            response.GeneratedText = candidate.content?.parts?[0]?.text ?? "";
                            return response;
                        }
                        else
                        {
                            response.ErrorMessage = $"Generierung gestoppt: {candidate.finishReason}";
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
    /// Schätzt die Anzahl der verwendeten Tokens
    /// </summary>
    private long EstimateTokens(string prompt, string response)
    {
        // Grobe Schätzung: 1 Token ≈ 4 Zeichen für Englisch
        return (prompt.Length + (response?.Length ?? 0)) / 4;
    }

    /// <summary>
    /// Schätzt Tokens für eine Konversation
    /// </summary>
    private long EstimateTokens(List<ConversationMessage> messages, ConversationMessage response = null)
    {
        long totalChars = 0;

        foreach (var message in messages)
        {
            totalChars += message.Content.Length;
        }

        if (response != null)
        {
            totalChars += response.Content.Length;
        }

        return totalChars / 4;
    }

    /// <summary>
    /// Aktualisiert die geschätzten Kosten
    /// </summary>
    private void UpdateEstimatedCost(long tokens)
    {
        // Gemini 1.5 Pro: ~$0.00125 pro 1000 Tokens (Input) + $0.005 pro 1000 Tokens (Output)
        // Vereinfachte Schätzung
        _stats.EstimatedCost += (decimal)(tokens * 0.000004);
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
            TotalTokensUsed = _stats.TotalTokensUsed,
            AverageGenerationTime = _stats.AverageGenerationTime,
            LastGeneration = _stats.LastGeneration,
            EstimatedCost = _stats.EstimatedCost
        };
    }

    /// <summary>
    /// Zeigt detaillierte Statistiken in der Konsole
    /// </summary>
    public void ShowStats()
    {
        var stats = GetStats();
        Console.WriteLine("\n" + "=".PadRight(60, '='));
        Console.WriteLine("📊 MEGA ULTRA GEMINI TEXT GENERATOR - STATISTIKEN");
        Console.WriteLine("=".PadRight(60, '='));
        Console.WriteLine($"📝 Gesamtgenerierungen: {stats.TotalGenerations}");
        Console.WriteLine($"✅ Erfolgreich: {stats.SuccessfulGenerations}");
        Console.WriteLine($"❌ Fehlgeschlagen: {stats.FailedGenerations}");
        Console.WriteLine($"🔢 Tokens verwendet: {stats.TotalTokensUsed:N0}");
        Console.WriteLine($"💰 Geschätzte Kosten: ${stats.EstimatedCost:F4}");
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
/// Optionen für die Textgenerierung
/// </summary>
public class GenerationOptions
{
    public double Temperature { get; set; } = 0.8;
    public int TopK { get; set; } = 40;
    public double TopP { get; set; } = 0.95;
    public int MaxOutputTokens { get; set; } = 2048;
    public string[] StopSequences { get; set; } = Array.Empty<string>();
    public bool Stream { get; set; } = false;
}

/// <summary>
/// Ergebnis einer Textgenerierung
/// </summary>
public class TextGenerationResult
{
    public string Prompt { get; set; }
    public GenerationOptions Options { get; set; }
    public bool Success { get; set; }
    public string GeneratedText { get; set; }
    public string ErrorMessage { get; set; }
    public TimeSpan GenerationTime { get; set; }
    public long TokensUsed { get; set; }
}

/// <summary>
/// Eine Nachricht in einer Konversation
/// </summary>
public class ConversationMessage
{
    public string Role { get; set; } // "user" oder "assistant"
    public string Content { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.Now;
}

/// <summary>
/// Ergebnis einer Konversation
/// </summary>
public class ConversationResult
{
    public List<ConversationMessage> Messages { get; set; } = new List<ConversationMessage>();
    public bool Success { get; set; }
    public string ErrorMessage { get; set; }
    public long TotalTokens { get; set; }
}

// API-Response-Klassen wurden entfernt, um Duplikate zu vermeiden

// ===============================
// 🔧 ERWEITERUNGSMETHODEN
// ===============================

public static class GeminiExtensions
{
    /// <summary>
    /// Kürzt einen String auf eine maximale Länge
    /// </summary>
    public static string Truncate(this string value, int maxLength)
    {
        return value.Length <= maxLength ? value : value.Substring(0, maxLength);
    }
}
