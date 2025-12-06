using System;
using System.Runtime.Versioning;

namespace MegaUltraRoboterKI.AI_CORE
{
    public class MegaUltraAIIntegratorEnhanced
    {
        // Main-Methode entfernt - StartupObject ist RoboterKIMaxUltraApp
        
        public static void Initialize()
        {
            Console.WriteLine("Willkommen beim MegaUltraAIIntegratorEnhanced!");
            Console.WriteLine("AI_CORE Modul initialisiert.");
        }

        public static string ProcessInput(string? eingabe)
        {
            if (string.IsNullOrWhiteSpace(eingabe))
            {
                return "Leere Eingabe erkannt.";
            }
            return VerarbeiteEingabe(eingabe);
        }

        // Beispiel-Algorithmus: Dreht den Text um und gibt ihn in Großbuchstaben zurück
        public static string VerarbeiteEingabe(string eingabe)
        {
            char[] arr = eingabe.ToCharArray();
            Array.Reverse(arr);
            return new string(arr).ToUpper();
        }
    }
}
