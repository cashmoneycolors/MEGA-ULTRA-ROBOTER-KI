#!/usr/bin/env python3
import subprocess
import sys
import shutil
from pathlib import Path

print("\n[BUILD] Creating Wealth System Pro EXE...\n")

# Clean
for folder in ["build", "dist"]:
    if Path(folder).exists():
        shutil.rmtree(folder)

# Build
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name=WealthSystemPro",
    "--hidden-import=tkinter",
    "--hidden-import=sqlite3",
    "--hidden-import=paypalrestsdk",
    "--collect-all=paypalrestsdk",
    "wealth_app_pro.py"
]

subprocess.run(cmd, check=True)

exe = Path("dist") / "WealthSystemPro.exe"
desktop = Path.home() / "Desktop" / "WealthSystemPro.exe"

if exe.exists():
    shutil.copy(exe, desktop)
    print(f"\n[OK] EXE ready: {desktop}")
    print(f"[OK] Size: {desktop.stat().st_size / 1024 / 1024:.1f} MB")
    print("\n[SUCCESS] Double-click to run!\n")
