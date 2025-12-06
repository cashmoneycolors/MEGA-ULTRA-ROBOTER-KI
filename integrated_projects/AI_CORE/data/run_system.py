#!/usr/bin/env python3
import subprocess
import time
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

def start_system():
    """Start the autonomous wealth system"""
    print("🚀 Starting Autonomous Wealth System...")
    print("=" * 50)
    
    try:
        # Start main system
        print("▶ Starting wealth production engine...")
        proc = subprocess.Popen(
            [sys.executable, 'cash_money_production.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✓ System running!")
        print("=" * 50)
        print("\n📊 Monitor the system.log for details\n")
        
        # Keep process alive
        proc.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏹ Shutting down...")
        proc.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_system()
