#!/usr/bin/env python3
"""Direct execution of launcher installation"""

import os
import sys
import subprocess
from pathlib import Path

# Step 1: Run setup_launcher_script.py
print("=" * 70)
print("STEP 1: Running setup_launcher_script.py")
print("=" * 70)
exec(open(r"C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI\setup_launcher_script.py").read())

print("\n" + "=" * 70)
print("STEP 2: Running install_and_create_desktop_launchers.py")
print("=" * 70)

# Step 2: Run the installation script
os.chdir(r"C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI")
sys.argv = ["install_and_create_desktop_launchers.py", "--with-dashboard", "--open-folders"]
exec(open(r"C:\cashmoneycolors\-MEGA-ULTRA-ROBOTER-KI\scripts\windows\install_and_create_desktop_launchers.py").read())
