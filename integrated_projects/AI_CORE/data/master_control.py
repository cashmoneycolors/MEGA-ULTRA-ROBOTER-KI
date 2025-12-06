#!/usr/bin/env python3
import subprocess
import sys
import time
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

print("\n" + "="*70)
print("[MASTER CONTROL] Autonomous Wealth System - Full Deployment")
print("="*70 + "\n")

processes = []

try:
    # Start Quantum System
    print("[1/3] Starting Quantum System...")
    p1 = subprocess.Popen([sys.executable, "quantum_system.py"])
    processes.append(("Quantum System", p1))
    time.sleep(2)
    
    # Start Auto Withdraw
    print("[2/3] Starting Auto Withdraw...")
    p2 = subprocess.Popen([sys.executable, "auto_withdraw.py"])
    processes.append(("Auto Withdraw", p2))
    time.sleep(2)
    
    # Start GUI App
    print("[3/3] Starting GUI App...")
    p3 = subprocess.Popen([sys.executable, "wealth_app_final.py"])
    processes.append(("GUI App", p3))
    
    print("\n" + "="*70)
    print("[OK] All systems running!")
    print("="*70 + "\n")
    
    for name, proc in processes:
        print(f"  {name}: PID {proc.pid}")
    
    print("\n[RUNNING] Press Ctrl+C to stop\n")
    
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n\n[STOP] Shutting down all systems...")
    for name, proc in processes:
        proc.terminate()
        print(f"  Stopped: {name}")
    print("\n[OK] All systems stopped\n")
