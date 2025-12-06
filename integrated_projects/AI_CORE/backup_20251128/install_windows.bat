@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo [INSTALL] Autonomous Wealth System - Windows
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies
echo [INSTALL] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Create shortcuts
echo [CREATE] Creating desktop shortcuts...

REM Desktop path
set DESKTOP=%USERPROFILE%\Desktop

REM Create app shortcut
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Wealth System.lnk'); $Shortcut.TargetPath = 'python.exe'; $Shortcut.Arguments = '%CD%\wealth_app.py'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Save()"

echo [OK] Desktop shortcut created
echo.

echo ============================================================
echo [SUCCESS] Installation complete!
echo ============================================================
echo.
echo You can now:
echo   1. Double-click "Wealth System.lnk" on your desktop
echo   2. Or run: python wealth_app.py
echo.
pause
