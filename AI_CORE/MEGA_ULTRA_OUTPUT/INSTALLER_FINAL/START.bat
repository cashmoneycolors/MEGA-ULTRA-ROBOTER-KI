@echo off
title MEGA ULTRA Creative Studio
cd /d "%~dp0"
echo ================================
echo   MEGA ULTRA Creative Studio   
echo ================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not installed
    pause
    exit
)
echo Installing dependencies...
pip install Pillow numpy psutil requests >nul
echo Starting application...
python mega_ultra_launcher.py
pause
