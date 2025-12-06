@echo off
REM Deinstalliere Python 3.14 und installiere Python 3.11

echo Deinstalliere Python 3.14...
wmic product where name="Python 3.14" call uninstall /nointeractive

echo.
echo Bitte lade Python 3.11 herunter von:
echo https://www.python.org/downloads/release/python-3110/
echo.
echo WICHTIG: Bei Installation "Add Python to PATH" ankreuzen!
echo.
pause
