@echo off
REM ============================================
REM ROBOTER KI APP Starter
REM L?dt .env und startet die App
REM ============================================

echo Lade Umgebungsvariablen aus .env...
for /f "tokens=1,2 delims==" %%a in ('type .env ^| findstr /v "^#" ^| findstr "="') do (
    set "%%a=%%b"
)

echo Starte ROBOTER KI APP...
start "" "??ROBOTER_KI_APP.exe"
