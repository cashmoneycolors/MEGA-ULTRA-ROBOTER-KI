#!/usr/bin/env python3
"""
Startup script for Autonomous Wealth System
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    required = ['flask', 'requests', 'sqlite3']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_config():
    """Ensure config.json exists"""
    if not Path("config.json").exists():
        default_config = {
            "initial_capital": 100,
            "target_capital": 10000,
            "cycle_interval": 2,
            "art_allocation": 0.40,
            "trading_allocation": 0.35,
            "vector_allocation": 0.25,
            "art_production_cost": 8.50,
            "art_min_price": 45,
            "art_max_price": 199,
            "vector_service_cost": 35,
            "vector_service_price": 85,
            "clone_creation_cost": 85,
            "max_clones": 25,
            "paypal": {
                "client_id": "",
                "client_secret": "",
                "sandbox_mode": True
            }
        }
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=2)
        print("✓ config.json created")

def main():
    print("=" * 50)
    print("Autonomous Wealth System - Startup")
    print("=" * 50)
    
    check_dependencies()
    setup_config()
    
    print("\n✓ All systems ready!")
    print("Starting application...\n")
    
    try:
        from app_complete import main as app_main
        app_main()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
