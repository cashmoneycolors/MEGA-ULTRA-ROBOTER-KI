import os

path = r"C:\Users\nazmi\Desktop\START_SHOP.bat"
content = r"""@echo off
TITLE MEGA-ULTRA-ROBOTER-KI - SHOP
COLOR 0A

cd /d "C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI"

echo ========================================================
echo  MEGA-ULTRA-ROBOTER-KI SHOP (LIVE)
echo ========================================================
echo.
echo Hier koennen Kunden deine Produkte kaufen.
echo Das Geld landet direkt auf deinem PayPal-Konto.
echo.

:: Use python -m streamlit to avoid PATH issues
python -m streamlit run shop_ui.py --server.port 8503 --server.headless true

if %errorlevel% neq 0 (
    echo.
    echo FEHLER: Konnte Shop nicht starten.
    echo Stelle sicher, dass Python und Streamlit installiert sind.
    pause
)
pause
"""

with open(path, "w") as f:
    f.write(content)

print("✅ START_SHOP.bat wurde repariert!")
