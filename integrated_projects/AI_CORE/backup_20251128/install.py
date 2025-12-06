#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
from pathlib import Path

def install():
    """Install Autonomous Wealth System on Windows"""
    print("\n" + "="*60)
    print("[INSTALL] Autonomous Wealth System - Windows")
    print("="*60 + "\n")
    
    # Check Python
    print("[CHECK] Verifying Python...")
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8+ required")
        return False
    print("[OK] Python 3.8+ found\n")
    
    # Install dependencies
    print("[INSTALL] Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("[OK] Dependencies installed\n")
    except:
        print("[ERROR] Failed to install dependencies")
        return False
    
    # Create desktop shortcut
    print("[CREATE] Creating desktop shortcut...")
    try:
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Wealth System.lnk"
        
        # Create VBS script for shortcut
        vbs_script = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{sys.executable}"
oLink.Arguments = "{Path.cwd() / 'wealth_app.py'}"
oLink.WorkingDirectory = "{Path.cwd()}"
oLink.Description = "Autonomous Wealth System"
oLink.Save
"""
        vbs_file = Path.cwd() / "create_shortcut.vbs"
        vbs_file.write_text(vbs_script)
        
        subprocess.run(["cscript.exe", str(vbs_file)], capture_output=True)
        vbs_file.unlink()
        
        print(f"[OK] Shortcut created: {shortcut_path}\n")
    except Exception as e:
        print(f"[WARN] Could not create shortcut: {e}\n")
    
    # Create start menu shortcut
    print("[CREATE] Creating Start Menu shortcut...")
    try:
        start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        if start_menu.exists():
            shortcut_path = start_menu / "Wealth System.lnk"
            
            vbs_script = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{sys.executable}"
oLink.Arguments = "{Path.cwd() / 'wealth_app.py'}"
oLink.WorkingDirectory = "{Path.cwd()}"
oLink.Description = "Autonomous Wealth System"
oLink.Save
"""
            vbs_file = Path.cwd() / "create_shortcut.vbs"
            vbs_file.write_text(vbs_script)
            
            subprocess.run(["cscript.exe", str(vbs_file)], capture_output=True)
            vbs_file.unlink()
            
            print(f"[OK] Start Menu shortcut created\n")
    except Exception as e:
        print(f"[WARN] Could not create Start Menu shortcut: {e}\n")
    
    # Summary
    print("="*60)
    print("[SUCCESS] Installation complete!")
    print("="*60)
    print("\nYou can now:")
    print("  1. Double-click 'Wealth System' on your desktop")
    print("  2. Or search 'Wealth System' in Start Menu")
    print("  3. Or run: python wealth_app.py")
    print("\n")

if __name__ == "__main__":
    install()
