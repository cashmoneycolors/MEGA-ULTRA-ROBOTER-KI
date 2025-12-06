@echo off
setlocal ENABLEDELAYEDEXPANSION
echo === MASTER_PHASES_RUN START ===
where python >nul 2>nul || (echo Python nicht gefunden & exit /b 1)
python PHASE_1_ERROR_SCAN.py
if errorlevel 1 (
  echo [FAIL] Phase 1 Error Scan meldet Fehler. Siehe error_scan_report.txt
  exit /b 1
) else (
  echo [OK] Phase 1 abgeschlossen.
)
rem Platzhalter fuer weitere Phasen:
rem python PHASE_2_SOMETHING.py
rem python PHASE_3_SOMETHING.py
echo === MASTER_PHASES_RUN ENDE ===
endlocal
