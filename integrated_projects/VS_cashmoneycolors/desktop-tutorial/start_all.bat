@echo off
REM Stabiles Startskript: Startet REST-API und Web-Frontend nacheinander im selben Fenster

echo Starte Python REST-API (Uvicorn)...
cd /d %~dp0AethelosGAZI
python -m uvicorn api.rest:app --reload --host 127.0.0.1 --port 8000
if %errorlevel% neq 0 (
	echo Fehler beim Starten der Python REST-API!
	pause
	exit /b %errorlevel%
)

echo Starte Flask Web-Frontend...
cd /d %~dp0AethelosGAZI\webapp
python app.py
if %errorlevel% neq 0 (
	echo Fehler beim Starten des Web-Frontends!
	pause
	exit /b %errorlevel%
)

echo Hinweis: Die C#-API muss separat in Visual Studio als ASP.NET Core Projekt gestartet werden.
pause
REM Warte auf Benutzereingabe, um das Fenster offen zu halten
exit /b 0