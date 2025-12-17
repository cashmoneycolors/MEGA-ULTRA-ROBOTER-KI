@echo off
cd /d C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI
echo ===============================================
echo   Setting up launcher installation...
echo ===============================================
python setup_launcher_script.py
echo.
echo ===============================================
echo   Creating desktop and Start Menu launchers...
echo ===============================================
python scripts\windows\install_and_create_desktop_launchers.py --with-dashboard --open-folders
pause
