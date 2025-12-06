@echo off
cd /d c:\Users\Laptop\Desktop\AI_CORE\data

echo Starting Autonomous Wealth System Services...
echo.

start "API Server" cmd /k python api_server.py
timeout /t 2 /nobreak

start "Web Dashboard" cmd /k python web_server.py
timeout /t 2 /nobreak

echo.
echo Services started!
echo Dashboard: http://localhost:8000
echo API: http://localhost:5000
echo.
pause
