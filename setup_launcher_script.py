#!/usr/bin/env python3
"""Temporary setup script to create the launcher installation script"""

import os
from pathlib import Path

# Create directory structure
script_dir = Path(r"C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI\scripts\windows")
script_dir.mkdir(parents=True, exist_ok=True)

# Create __init__.py files
(script_dir.parent / "__init__.py").write_text("# Scripts package\n", encoding='utf-8')
(script_dir / "__init__.py").write_text("# Windows scripts package\n", encoding='utf-8')

# Create the main installation script
install_script = script_dir / "install_and_create_desktop_launchers.py"

script_content = '''#!/usr/bin/env python3
"""
Desktop and Start Menu Launcher Installation Script
Creates shortcuts for MEGA-ULTRA-ROBOTER-KI Dashboard and API
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

try:
    import win32com.client
    PYWIN32_AVAILABLE = True
except ImportError:
    PYWIN32_AVAILABLE = False
    print("⚠️  pywin32 not available - installing...")

def install_pywin32():
    """Install pywin32 if not available"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "--quiet"])
        print("✅ pywin32 installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install pywin32")
        return False

def create_shortcut(target_path, shortcut_path, arguments="", working_dir="", description="", icon_path=""):
    """Create a Windows shortcut (.lnk) file"""
    if not PYWIN32_AVAILABLE:
        if not install_pywin32():
            return False
        # Reload the module after installation
        try:
            import win32com.client
        except ImportError:
            return False
    
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.TargetPath = str(target_path)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(working_dir) if working_dir else str(Path(target_path).parent)
    shortcut.Description = description
    if icon_path:
        shortcut.IconLocation = icon_path
    shortcut.save()
    return True

def create_bat_file(bat_path, content):
    """Create a .bat file"""
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return bat_path

def get_python_path():
    """Get the current Python executable path"""
    return sys.executable

def get_project_root():
    """Get project root directory"""
    script_path = Path(__file__).resolve()
    return script_path.parent.parent.parent

def create_dashboard_launcher(desktop_path, start_menu_path, project_root, python_exe):
    """Create Dashboard launcher"""
    print("\\n📊 Creating Dashboard Launcher...")
    
    # Create .bat file
    bat_content = f"""@echo off
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
"{python_exe}" -m streamlit run paypal_maximizer.py --server.port=8501
pause
"""
    
    bat_name = "MEGA-ULTRA-ROBOTER-KI - Dashboard.bat"
    desktop_bat = desktop_path / bat_name
    start_menu_bat = start_menu_path / bat_name
    
    create_bat_file(desktop_bat, bat_content)
    create_bat_file(start_menu_bat, bat_content)
    
    print(f"  ✅ Desktop .bat: {desktop_bat}")
    print(f"  ✅ Start Menu .bat: {start_menu_bat}")
    
    # Create .lnk shortcut for Start Menu
    lnk_name = "Dashboard.lnk"
    start_menu_lnk = start_menu_path / lnk_name
    desktop_lnk = desktop_path / lnk_name
    
    cmd_exe = os.environ.get('COMSPEC', 'C:\\\\Windows\\\\System32\\\\cmd.exe')
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=start_menu_lnk,
        arguments=f'/c "{start_menu_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI Dashboard - PayPal Revenue Maximization System"
    ):
        print(f"  ✅ Start Menu .lnk: {start_menu_lnk}")
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=desktop_lnk,
        arguments=f'/c "{desktop_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI Dashboard"
    ):
        print(f"  ✅ Desktop .lnk: {desktop_lnk}")
    
    return True

def create_api_launcher(desktop_path, start_menu_path, project_root, python_exe):
    """Create API launcher"""
    print("\\n🚀 Creating API Launcher...")
    
    # Create .bat file
    bat_content = f"""@echo off
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
    
    bat_name = "MEGA-ULTRA-ROBOTER-KI - API.bat"
    desktop_bat = desktop_path / bat_name
    start_menu_bat = start_menu_path / bat_name
    
    create_bat_file(desktop_bat, bat_content)
    create_bat_file(start_menu_bat, bat_content)
    
    print(f"  ✅ Desktop .bat: {desktop_bat}")
    print(f"  ✅ Start Menu .bat: {start_menu_bat}")
    
    # Create .lnk shortcut for Start Menu
    lnk_name = "API Server.lnk"
    start_menu_lnk = start_menu_path / lnk_name
    desktop_lnk = desktop_path / lnk_name
    
    cmd_exe = os.environ.get('COMSPEC', 'C:\\\\Windows\\\\System32\\\\cmd.exe')
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=start_menu_lnk,
        arguments=f'/c "{start_menu_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI API Server - FastAPI Backend"
    ):
        print(f"  ✅ Start Menu .lnk: {start_menu_lnk}")
    
    if create_shortcut(
        target_path=cmd_exe,
        shortcut_path=desktop_lnk,
        arguments=f'/c "{desktop_bat}"',
        working_dir=project_root,
        description="MEGA-ULTRA-ROBOTER-KI API Server"
    ):
        print(f"  ✅ Desktop .lnk: {desktop_lnk}")
    
    return True

def open_folder_in_explorer(folder_path):
    """Open folder in Windows Explorer"""
    try:
        subprocess.Popen(f'explorer "{folder_path}"')
        return True
    except Exception as e:
        print(f"  ⚠️  Could not open folder: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create desktop and Start Menu launchers')
    parser.add_argument('--with-dashboard', action='store_true', help='Create Dashboard launcher')
    parser.add_argument('--with-api', action='store_true', help='Create API launcher')
    parser.add_argument('--open-folders', action='store_true', help='Open Desktop and Start Menu folders in Explorer')
    args = parser.parse_args()
    
    # If no specific launcher selected, create both
    if not args.with_dashboard and not args.with_api:
        args.with_dashboard = True
        args.with_api = True
    
    print("=" * 70)
    print("  MEGA-ULTRA-ROBOTER-KI - Launcher Installation")
    print("=" * 70)
    
    # Get paths
    project_root = get_project_root()
    python_exe = get_python_path()
    desktop_path = Path.home() / "Desktop"
    start_menu_path = Path(os.environ.get('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "MEGA-ULTRA-ROBOTER-KI"
    
    # Create Start Menu folder
    start_menu_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\\n📁 Project Root: {project_root}")
    print(f"🐍 Python: {python_exe}")
    print(f"🖥️  Desktop: {desktop_path}")
    print(f"📂 Start Menu: {start_menu_path}")
    
    # Create launchers
    if args.with_dashboard:
        create_dashboard_launcher(desktop_path, start_menu_path, project_root, python_exe)
    
    if args.with_api:
        create_api_launcher(desktop_path, start_menu_path, project_root, python_exe)
    
    print("\\n" + "=" * 70)
    print("✅ INSTALLATION COMPLETE!")
    print("=" * 70)
    print(f"\\n📍 Desktop Path: {desktop_path}")
    print(f"📍 Start Menu Path: {start_menu_path}")
    
    # Open folders if requested
    if args.open_folders:
        print("\\n🗂️  Opening folders in Explorer...")
        open_folder_in_explorer(desktop_path)
        open_folder_in_explorer(start_menu_path)
    
    print("\\n💡 TIP: You can now find the launchers:")
    print("   • On your Desktop")
    print("   • In Start Menu > All Apps > MEGA-ULTRA-ROBOTER-KI")
    print("\\n" + "=" * 70)

if __name__ == "__main__":
    main()
'''

install_script.write_text(script_content, encoding='utf-8')

print(f"✅ Created: {install_script}")
print(f"✅ Script is ready at: scripts\\windows\\install_and_create_desktop_launchers.py")
print("\\nNow run:")
print('python scripts\\windows\\install_and_create_desktop_launchers.py --with-dashboard --open-folders')
