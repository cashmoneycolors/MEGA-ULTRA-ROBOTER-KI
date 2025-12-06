#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def deploy():
    """Deploy and start all services"""
    os.chdir(Path(__file__).parent)
    
    print("\n" + "="*60)
    print("[DEPLOY] Autonomous Wealth System")
    print("="*60 + "\n")
    
    # Check dependencies
    print("[CHECK] Verifying dependencies...")
    try:
        import flask
        import flask_cors
        print("[OK] Flask installed")
    except ImportError:
        print("[INSTALL] Installing Flask...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start services
    print("\n[START] Starting services...\n")
    
    services = [
        ("Production System", "cash_money_production.py"),
        ("API Server (5000)", "api_server.py"),
        ("Web Dashboard (8000)", "web_server.py"),
    ]
    
    processes = []
    for name, script in services:
        print(f"[START] {name}...")
        proc = subprocess.Popen([sys.executable, script])
        processes.append((name, proc))
    
    print("\n" + "="*60)
    print("[OK] All services started!")
    print("="*60)
    print("\nAccess points:")
    print("  - Web Dashboard: http://localhost:8000")
    print("  - API: http://localhost:5000/api")
    print("  - Mobile: http://localhost:8000/mobile_dashboard.html")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        for name, proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\n[STOP] Stopping all services...")
        for name, proc in processes:
            proc.terminate()
        print("[OK] All services stopped")

if __name__ == "__main__":
    deploy()
