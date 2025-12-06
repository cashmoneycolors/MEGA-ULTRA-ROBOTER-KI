using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.IO;

namespace RoboterKIMaxUltra
{
    /// <summary>
    /// Google Imagen 3.0 API Generator für Text-zu-Bild (T2I)
    /// Generiert: Logos, Produktbilder, Marketing-Grafiken für Dropshipping
    /// </summary>
    public class ImagenGenerator
    {
        private readonly string _apiKey;
        private readonly HttpClient _httpClient;
        private const string IMAGEN_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict";

        public ImagenGenerator(string apiKey)
        {
            if (string.IsNullOrEmpty(apiKey))
                throw new ArgumentException("Google API Key darf nicht leer sein", nameof(apiKey));
            
            _apiKey = apiKey;
            _httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(120) }; // Längeres Timeout für Bildgenerierung
        }

        /// <summary>
        /// Generiert ein Produktlogo
        /// </summary>
        public async Task<ImageResult> GenerateLogo(string companyName, string industry, string style = "modern minimalist")
        {
            string prompt = $"Professional logo for {companyName}, {industry} industry, {style} style, clean design, vector art, high quality, commercial use";
            return await GenerateImage(prompt, 512, 512);
        }

        /// <summary>
        /// Generiert ein Produktbild für Dropshipping
        /// </summary>
        public async Task<ImageResult> GenerateProductImage(string productDescription, string background = "white studio background")
        {
            string prompt = $"Professional product photography of {productDescription}, {background}, commercial photography, high resolution, 4k, studio lighting";
            return await GenerateImage(prompt, 1024, 1024);
        }

        /// <summary>
        /// Generiert Social Media Grafik
        /// </summary>
        public async Task<ImageResult> GenerateSocialMediaGraphic(string content, string platform = "Instagram")
        {
            string prompt = $"{platform} post graphic: {content}, professional design, eye-catching, modern aesthetic, high quality";
            
            // Instagram: Quadratisch, Facebook: Landscape
            int width = platform.ToLower() == "instagram" ? 1080 : 1200;
            int height = platform.ToLower() == "instagram" ? 1080 : 630;
            
            return await GenerateImage(prompt, width, height);
        }

        /// <summary>
        /// Generiert ein Bild basierend auf Text-Prompt (T2I)
        /// </summary>
        public async Task<ImageResult> GenerateImage(string prompt, int width = 1024, int height = 1024, int sampleCount = 1)
        {
            try
            {
                // Validierung
                if (width < 128 || width > 2048 || height < 128 || height > 2048)
                {
                    return new ImageResult
                    {
                        Success = false,
                        ErrorMessage = "Bildgröße muss zwischen 128x128 und 2048x2048 Pixeln liegen"
                    };
                }

                // Request Body für Imagen API
                var requestBody = new
                {
                    instances = new[]
                    {
                        new
                        {
                            prompt = prompt
                        }
                    },
                    parameters = new
                    {
                        sampleCount = sampleCount,
                        aspectRatio = $"{width}:{height}",
                        safetyFilterLevel = "block_some",
                        personGeneration = "allow_adult"
                    }
                };

                string jsonContent = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

                string url = $"{IMAGEN_API_URL}?key={_apiKey}";
                var response = await _httpClient.PostAsync(url, content);

                if (!response.IsSuccessStatusCode)
                {
                    string errorContent = await response.Content.ReadAsStringAsync();
                    return new ImageResult
                    {
                        Success = false,
                        ErrorMessage = $"API-Fehler {response.StatusCode}: {errorContent}"
                    };
                }

                string responseBody = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(responseBody);

                // Parse Response
                if (jsonDoc.RootElement.TryGetProperty("predictions", out var predictions) &&
                    predictions.GetArrayLength() > 0)
                {
                    var firstPrediction = predictions[0];
                    if (firstPrediction.TryGetProperty("bytesBase64Encoded", out var base64Element))
                    {
                        string base64Image = base64Element.GetString();
                        if (!string.IsNullOrEmpty(base64Image))
                        {
                            byte[] imageBytes = Convert.FromBase64String(base64Image);
                            
                            return new ImageResult
                            {
                                Success = true,
                                ImageData = imageBytes,
                                Base64Data = base64Image,
                                Prompt = prompt,
                                Width = width,
                                Height = height
                            };
                        }
                    }
                }

                return new ImageResult
                {
                    Success = false,
                    ErrorMessage = "Keine Bilddaten in API-Response gefunden"
                };
            }
            catch (Exception ex)
            {
                return new ImageResult
                {
                    Success = false,
                    ErrorMessage = $"Exception: {ex.Message}"
                };
            }
        }

        /// <summary>
        /// Speichert generiertes Bild als PNG-Datei
        /// </summary>
        public async Task<bool> SaveImage(ImageResult imageResult, string filePath)
        {
            try
            {
                if (!imageResult.Success || imageResult.ImageData == null)
                    return false;

                // Stelle sicher, dass Verzeichnis existiert
                string? directory = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }

                await File.WriteAllBytesAsync(filePath, imageResult.ImageData);
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Generiert Banner für Webshop
        /// </summary>
        public async Task<ImageResult> GenerateShopBanner(string shopName, string tagline)
        {
            string prompt = $"E-commerce banner for {shopName}, tagline: '{tagline}', professional web design, modern, clean, high quality, 1920x600 pixels";
            return await GenerateImage(prompt, 1920, 600);
        }

        /// <summary>
        /// Generiert Mockup (z.B. T-Shirt mit Design)
        /// </summary>
        public async Task<ImageResult> GenerateMockup(string productType, string designDescription)
        {
            string prompt = $"{productType} mockup with {designDescription}, professional product mockup, realistic, high quality, commercial photography";
            return await GenerateImage(prompt, 1024, 1024);
        }
    }

    /// <summary>
    /// Ergebnis-Klasse für Bildgenerierung
    /// </summary>
    public class ImageResult
    {
        public bool Success { get; set; }
        public byte[]? ImageData { get; set; }
        public string? Base64Data { get; set; }
        public string? ErrorMessage { get; set; }
        public string? Prompt { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
        public DateTime GeneratedAt { get; set; } = DateTime.Now;

        /// <summary>
        /// Speichert Bild als PNG-Datei
        /// </summary>
        public async Task<bool> SaveToFile(string filePath)
        {
            try
            {
                if (!Success || ImageData == null)
                    return false;

                string? directory = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }

                await File.WriteAllBytesAsync(filePath, ImageData);
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Gibt Data-URL für HTML/Web zurück
        /// </summary>
        public string GetDataUrl()
        {
            if (!Success || string.IsNullOrEmpty(Base64Data))
                return string.Empty;
            
            return $"data:image/png;base64,{Base64Data}";
        }
    }
}
