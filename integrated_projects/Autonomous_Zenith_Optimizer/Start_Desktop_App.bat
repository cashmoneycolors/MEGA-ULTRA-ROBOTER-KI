@echo off
REM CCashMoneyIDE Desktop App Starter
REM Echte funktionierende Desktop-Anwendung für Windows HP Laptop

echo.
echo ========================================================
echo     CCashMoneyIDE - Desktop Application
echo     Version 1.0 - PRODUKTIONSBEREIT
echo ========================================================
echo.

REM Prüfe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python nicht gefunden!
    echo Bitte installiere Python 3.8+ von python.org
    pause
    exit /b 1
)

echo [OK] Python gefunden
echo.
echo Starte CCashMoneyIDE Desktop App...
echo.

REM Starte Desktop-App
python CCashMoneyIDE_Desktop.py

if errorlevel 1 (
    echo.
    echo FEHLER beim Starten der Anwendung!
    pause
)
