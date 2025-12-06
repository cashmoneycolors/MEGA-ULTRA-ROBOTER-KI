#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Build Windows EXE with PyInstaller"""
    print("\n" + "="*60)
    print("[BUILD] Creating Windows EXE")
    print("="*60 + "\n")
    
    # Install PyInstaller
    print("[INSTALL] PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"], check=True)
    
    # Build EXE
    print("[BUILD] Compiling wealth_app.py to EXE...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=WealthSystem",
        "--icon=NONE",
        "--add-data=wealth_system.db:.",
        "--add-data=config.json:.",
        "--add-data=system.log:.",
        "wealth_app.py"
    ], check=True)
    
    exe_path = Path("dist") / "WealthSystem.exe"
    
    if exe_path.exists():
        print(f"\n[OK] EXE created: {exe_path}")
        print(f"[OK] Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Copy to Desktop
        desktop = Path.home() / "Desktop"
        dest = desktop / "WealthSystem.exe"
        
        import shutil
        shutil.copy(exe_path, dest)
        print(f"[OK] Copied to Desktop: {dest}")
        
        print("\n" + "="*60)
        print("[SUCCESS] App ready!")
        print("="*60)
        print(f"\nDouble-click: {dest}")
        print("Or search 'WealthSystem' in Start Menu\n")
    else:
        print("[ERROR] Build failed")

if __name__ == "__main__":
    build_exe()
