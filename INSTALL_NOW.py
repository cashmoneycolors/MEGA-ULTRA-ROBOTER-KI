#!/usr/bin/env python3
"""
MEGA-ULTRA-ROBOTER-KI - Complete Launcher Installation
This script does EVERYTHING in one go - no other files needed!
"""

import os
import sys
import subprocess
from pathlib import Path

def install_pywin32():
    """Install pywin32 if not available"""
    print("📦 Checking pywin32...")
    try:
        import win32com.client
        print("✅ pywin32 already installed")
        return True
    except ImportError:
        print("⚠️  Installing pywin32...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "--quiet"])
            print("✅ pywin32 installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pywin32")
            return False

def create_shortcut(target_path, shortcut_path, arguments="", working_dir="", description=""):
    """Create a Windows shortcut (.lnk) file"""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(target_path)
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = str(working_dir) if working_dir else str(Path(target_path).parent)
        shortcut.Description = description
        shortcut.save()
        return True
    except Exception as e:
        print(f"  ⚠️  Could not create shortcut: {e}")
        return False

def create_bat_file(bat_path, content):
    """Create a .bat file"""
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return bat_path

def open_folder_in_explorer(folder_path):
    """Open folder in Windows Explorer"""
    try:
        subprocess.Popen(f'explorer "{folder_path}"')
        return True
    except Exception as e:
        print(f"  ⚠️  Could not open folder: {e}")
        return False

def main():
    print("=" * 70)
    print("  MEGA-ULTRA-ROBOTER-KI - Complete Launcher Installation")
    print("=" * 70)
    
    # Get paths
    project_root = Path(r"C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI")
    python_exe = sys.executable
    desktop_path = Path.home() / "Desktop"
    start_menu_path = Path(os.environ.get('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "MEGA-ULTRA-ROBOTER-KI"
    
    print(f"\n📁 Project Root: {project_root}")
    print(f"🐍 Python: {python_exe}")
    print(f"🖥️  Desktop: {desktop_path}")
    print(f"📂 Start Menu: {start_menu_path}")
    
    # Create Start Menu folder
    start_menu_path.mkdir(parents=True, exist_ok=True)
    print(f"\n✅ Created Start Menu folder: {start_menu_path}")

    # Create requirements.txt
    req_path = project_root / "requirements.txt"
    if not req_path.exists():
        print("📝 Creating requirements.txt...")
        req_content = "streamlit\nfastapi\nuvicorn\npython-dotenv\nrequests\npandas\n"
        with open(req_path, "w", encoding="utf-8") as f:
            f.write(req_content)
        print(f"✅ Created: {req_path}")
    
    # Install pywin32
    if not install_pywin32():
        print("\n❌ Cannot continue without pywin32")
        input("\nPress Enter to exit...")
        return
    
    # ========================================================================
    # CREATE DASHBOARD LAUNCHER
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 CREATING DASHBOARD LAUNCHER")
    print("=" * 70)
    
    dashboard_bat_content = f"""@echo off
title MEGA-ULTRA-ROBOTER-KI Dashboard
cd /d "{project_root}"

echo ===============================================
echo   MEGA-ULTRA-ROBOTER-KI - Dashboard
echo ===============================================
echo.
echo Installing/checking dependencies...
"{python_exe}" -m pip install -q -r requirements.txt
echo.
echo Starting Streamlit Dashboard...
echo Dashboard will open in your browser automatically.
echo.
"{python_exe}" -m streamlit run dashboard_ui.py --server.port=8502 --server.address=localhost
pause
"""
    
    # Create Dashboard .bat files
    bat_name = "MEGA-ULTRA-ROBOTER-KI - Dashboard.bat"
    desktop_bat = desktop_path / bat_name
    start_menu_bat = start_menu_path / bat_name
    
    create_bat_file(desktop_bat, dashboard_bat_content)
    create_bat_file(start_menu_bat, dashboard_bat_content)
    
    print(f"✅ Desktop .bat: {desktop_bat}")
    print(f"✅ Start Menu .bat: {start_menu_bat}")
    
    # Create Dashboard .lnk shortcuts
    cmd_exe = os.environ.get('COMSPEC', 'C:\\Windows\\System32\\cmd.exe')
    
    dashboard_lnk_desktop = desktop_path / "Dashboard.lnk"
    dashboard_lnk_startmenu = start_menu_path / "Dashboard.lnk"
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=dashboard_lnk_startmenu,
        arguments=f'/c "{start_menu_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI Dashboard - PayPal Revenue Maximization"
    ):
        print(f"✅ Start Menu .lnk: {dashboard_lnk_startmenu}")
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=dashboard_lnk_desktop,
        arguments=f'/c "{desktop_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI Dashboard"
    ):
        print(f"✅ Desktop .lnk: {dashboard_lnk_desktop}")
    
    # ========================================================================
    # CREATE API LAUNCHER
    # ========================================================================
    print("\n" + "=" * 70)
    print("🚀 CREATING API SERVER LAUNCHER")
    print("=" * 70)
    
    api_bat_content = f"""@echo off
title MEGA-ULTRA-ROBOTER-KI API Server
cd /d "{project_root}"

echo ===============================================
echo   MEGA-ULTRA-ROBOTER-KI - API Server
echo ===============================================
echo.
echo Installing/checking dependencies...
"{python_exe}" -m pip install -q -r requirements.txt
echo.
echo Starting FastAPI Server...
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
"{python_exe}" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
"""
    
    # Create API .bat files
    api_bat_name = "MEGA-ULTRA-ROBOTER-KI - API.bat"
    api_desktop_bat = desktop_path / api_bat_name
    api_start_menu_bat = start_menu_path / api_bat_name
    
    create_bat_file(api_desktop_bat, api_bat_content)
    create_bat_file(api_start_menu_bat, api_bat_content)
    
    print(f"✅ Desktop .bat: {api_desktop_bat}")
    print(f"✅ Start Menu .bat: {api_start_menu_bat}")
    
    # Create API .lnk shortcuts
    api_lnk_desktop = desktop_path / "API Server.lnk"
    api_lnk_startmenu = start_menu_path / "API Server.lnk"
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=api_lnk_startmenu,
        arguments=f'/c "{api_start_menu_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI API Server - FastAPI Backend"
    ):
        print(f"✅ Start Menu .lnk: {api_lnk_startmenu}")
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=api_lnk_desktop,
        arguments=f'/c "{api_desktop_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI API Server"
    ):
        print(f"✅ Desktop .lnk: {api_lnk_desktop}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ INSTALLATION COMPLETE!")
    print("=" * 70)
    print(f"\n📍 Desktop Path: {desktop_path}")
    print(f"📍 Start Menu Path: {start_menu_path}")
    
    print("\n🗂️  Opening folders in Explorer...")
    open_folder_in_explorer(desktop_path)
    open_folder_in_explorer(start_menu_path)
    
    print("\n💡 LAUNCHERS CREATED:")
    print("\n   ON DESKTOP:")
    print(f"   • {dashboard_lnk_desktop.name}")
    print(f"   • {api_lnk_desktop.name}")
    print(f"   • {bat_name}")
    print(f"   • {api_bat_name}")
    
    print("\n   IN START MENU (All Apps > MEGA-ULTRA-ROBOTER-KI):")
    print(f"   • Dashboard.lnk")
    print(f"   • API Server.lnk")
    print(f"   • {bat_name}")
    print(f"   • {api_bat_name}")
    
    print("\n" + "=" * 70)
    print("🎉 You can now start the Dashboard or API from Desktop or Start Menu!")
    print("=" * 70)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
