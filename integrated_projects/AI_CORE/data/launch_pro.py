#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

print("\n" + "="*60)
print("[LAUNCH] Wealth System Pro - PayPal Edition")
print("="*60 + "\n")

# Check PayPal config
if not Path("paypal_config.json").exists():
    print("[SETUP] First time setup required\n")
    subprocess.run([sys.executable, "setup_paypal.py"])

# Start app
print("[START] Launching Wealth System Pro...\n")
subprocess.run([sys.executable, "wealth_app_pro.py"])
