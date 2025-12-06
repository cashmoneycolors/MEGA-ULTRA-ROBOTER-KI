@echo off
REM MEGA ULTRA ROBOTER KI APP - DIREKTER START
REM Startet die reparierte Python-Version direkt

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  🤖 MEGA ULTRA ROBOTER KI – QUANTUM PRODUCTION EDITION 🚀            ║
echo ║  Vollständig integriert: OpenAI + Stripe + PayPal + AWS + NFT + More ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Prüfe Python 3.11
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.11 nicht gefunden!
    echo    Bitte installiere Python 3.11 oder verwende: py -3.11
    pause
    exit /b 1
)

echo ✅ Python 3.11 gefunden
echo.

REM Wechsle zum Projekt-Verzeichnis
cd /d "C:\Users\Laptop\Kontrollzentrum-1"

REM Starte die App
echo 🚀 Starte MEGA ULTRA ROBOTER KI APP...
echo.
py -3.11 mega_roboter_ki.py

pause
