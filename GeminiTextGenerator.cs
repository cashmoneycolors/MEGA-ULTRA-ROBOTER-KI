using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RoboterKIMaxUltra
{
    /// <summary>
    /// Gemini API Text-Generator mit Google Search Grounding für Dropshipping & E-Commerce
    /// Generiert: Produktbeschreibungen, Marketing-Texte, SEO-Content
    /// </summary>
    public class GeminiTextGenerator
    {
        private readonly string _apiKey;
        private readonly HttpClient _httpClient;
        private const string GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent";

        public GeminiTextGenerator(string apiKey)
        {
            if (string.IsNullOrEmpty(apiKey))
                throw new ArgumentException("Gemini API Key darf nicht leer sein", nameof(apiKey));
            
            _apiKey = apiKey;
            _httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(60) };
        }

        /// <summary>
        /// Generiert eine Produktbeschreibung für Dropshipping (mit Google Search Grounding)
        /// </summary>
        public async Task<string> GenerateProductDescription(string productName, string features, string targetAudience = "Allgemein")
        {
            string prompt = $@"
Erstelle eine verkaufsstarke Produktbeschreibung für Dropshipping:

Produkt: {productName}
Eigenschaften: {features}
Zielgruppe: {targetAudience}

Anforderungen:
- Überzeugend und emotional
- SEO-optimiert
- Call-to-Action am Ende
- Maximal 200 Wörter
- Nutzenorientiert
";

            return await GenerateTextWithGrounding(prompt);
        }

        /// <summary>
        /// Generiert Marketing-Text für Social Media / Ads
        /// </summary>
        public async Task<string> GenerateMarketingText(string productName, string platform = "Instagram", int wordLimit = 100)
        {
            string prompt = $@"
Erstelle einen Marketing-Post für {platform}:

Produkt: {productName}
Plattform: {platform}
Wortlimit: {wordLimit}

Anforderungen:
- Aufmerksamkeitsstark
- Emojis verwenden
- Call-to-Action
- Hashtags am Ende (3-5 Stück)
";

            return await GenerateTextWithGrounding(prompt);
        }

        /// <summary>
        /// Generiert SEO-optimierten Content
        /// </summary>
        public async Task<string> GenerateSEOContent(string keyword, string contentType = "Meta Description")
        {
            string prompt = $@"
Erstelle {contentType} für SEO:

Keyword: {keyword}
Content-Typ: {contentType}

Anforderungen:
- SEO-optimiert
- Keyword natürlich eingebaut
- Für Google Rankings optimiert
- Maximal 160 Zeichen (für Meta Description)
";

            return await GenerateTextWithGrounding(prompt);
        }

        /// <summary>
        /// Generiert allgemeinen Text mit Google Search Grounding
        /// </summary>
        public async Task<string> GenerateTextWithGrounding(string prompt)
        {
            try
            {
                var requestBody = new
                {
                    contents = new[]
                    {
                        new
                        {
                            parts = new[]
                            {
                                new { text = prompt }
                            }
                        }
                    },
                    tools = new[]
                    {
                        new
                        {
                            google_search = new { }
                        }
                    },
                    systemInstruction = new
                    {
                        parts = new[]
                        {
                            new { text = "Du bist ein professioneller Copywriter für E-Commerce und Dropshipping. Deine Texte sind verkaufsstark, SEO-optimiert und kundenorientiert." }
                        }
                    }
                };

                string jsonContent = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

                string url = $"{GEMINI_API_URL}?key={_apiKey}";
                var response = await _httpClient.PostAsync(url, content);

                if (!response.IsSuccessStatusCode)
                {
                    string errorContent = await response.Content.ReadAsStringAsync();
                    return $"[FEHLER] API-Aufruf fehlgeschlagen: {response.StatusCode} - {errorContent}";
                }

                string responseBody = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(responseBody);

                // Parse Response
                if (jsonDoc.RootElement.TryGetProperty("candidates", out var candidates) &&
                    candidates.GetArrayLength() > 0)
                {
                    var firstCandidate = candidates[0];
                    if (firstCandidate.TryGetProperty("content", out var content_prop) &&
                        content_prop.TryGetProperty("parts", out var parts) &&
                        parts.GetArrayLength() > 0)
                    {
                        var firstPart = parts[0];
                        if (firstPart.TryGetProperty("text", out var textElement))
                        {
                            string generatedText = textElement.GetString() ?? "[LEER]";

                            // Füge Quellen hinzu, falls vorhanden
                            if (firstCandidate.TryGetProperty("groundingMetadata", out var groundingMetadata) &&
                                groundingMetadata.TryGetProperty("groundingAttributions", out var attributions))
                            {
                                var sources = new List<string>();
                                foreach (var attribution in attributions.EnumerateArray())
                                {
                                    if (attribution.TryGetProperty("web", out var web) &&
                                        web.TryGetProperty("uri", out var uri) &&
                                        web.TryGetProperty("title", out var title))
                                    {
                                        sources.Add($"[{title.GetString()}]({uri.GetString()})");
                                    }
                                }

                                if (sources.Count > 0)
                                {
                                    generatedText += "\n\n---\n**Quellen (Google Search):**\n" + string.Join("\n", sources);
                                }
                            }

                            return generatedText;
                        }
                    }
                }

                return "[FEHLER] Keine Textantwort in API-Response";
            }
            catch (Exception ex)
            {
                return $"[EXCEPTION] {ex.Message}";
            }
        }

        /// <summary>
        /// Generiert Logo-Beschreibung für Bild-Generator
        /// </summary>
        public async Task<string> GenerateLogoPrompt(string companyName, string industry, string style = "modern")
        {
            string prompt = $@"
Erstelle einen detaillierten Prompt für einen AI-Bild-Generator:

Firmename: {companyName}
Branche: {industry}
Stil: {style}

Erstelle einen präzisen Prompt (auf Englisch) für einen Logo-Generator.
Beschreibe:
- Farbschema
- Stil (minimalistisch, modern, etc.)
- Symbole/Icons
- Typographie
- Stimmung/Emotion

Nur der Prompt, keine Erklärungen.
";

            string result = await GenerateTextWithGrounding(prompt);
            // Extrahiere nur den Prompt (entferne eventuelle Markdown-Formatierung)
            result = result.Replace("```", "").Trim();
            return result;
        }
    }
}
