using System;
using System.IO;

namespace MegaUltraRoboterKI
{
    public static class ConsoleHelper
    {
        public static void WriteInfo(string message)
        {
            System.Console.ForegroundColor = ConsoleColor.Cyan;
            System.Console.WriteLine($"[INFO] {message}");
            System.Console.ResetColor();
        }

        public static void WriteError(string message)
        {
            System.Console.ForegroundColor = ConsoleColor.Red;
            System.Console.WriteLine($"[ERROR] {message}");
            System.Console.ResetColor();
        }

        public static void WriteSuccess(string message)
        {
            System.Console.ForegroundColor = ConsoleColor.Green;
            System.Console.WriteLine($"[SUCCESS] {message}");
            System.Console.ResetColor();
        }

        public static void DisplayHeader()
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
        }
    }
}
