using System;

namespace MegaUltraRoboterKI.AI_CORE
{
    public class MegaUltraAIIntegratorEnhanced
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Willkommen beim MegaUltraAIIntegratorEnhanced!");
            Console.WriteLine("Bitte gib einen beliebigen Text ein (oder 'exit' zum Beenden):");

            while (true)
            {
                Console.Write("> ");
                string input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine("Leere Eingabe erkannt. Bitte gib etwas ein.");
                    continue;
                }

                if (input.Trim().ToLower() == "exit")
                {
                    Console.WriteLine("Programm wird beendet. Auf Wiedersehen!");
                    break;
                }

                // Hier kannst du beliebige Verarbeitung einbauen:
                string output = VerarbeiteEingabe(input);

                Console.WriteLine($"Verarbeitetes Ergebnis: {output}");
            }
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