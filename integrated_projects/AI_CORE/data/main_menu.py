#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

def show_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("[SYSTEM] AUTONOMOUS WEALTH GENERATION")
    print("="*60)
    print("\n1. [START] Production System")
    print("2. [API] Server (Port 5000)")
    print("3. [WEB] Dashboard (Port 8000)")
    print("4. [MONITOR] System Stats")
    print("5. [EXPORT] Data")
    print("6. [CONFIG] Manager")
    print("7. [LOG] View System Log")
    print("8. [CLEAR] Database")
    print("9. [EXIT] Quit")
    print("\n" + "="*60)

def run_option(choice):
    """Execute selected option"""
    if choice == "1":
        print("\n[START] Production system...")
        subprocess.Popen([sys.executable, "cash_money_production.py"])
    
    elif choice == "2":
        print("\n[START] API server on port 5000...")
        subprocess.Popen([sys.executable, "api_server.py"])
    
    elif choice == "3":
        print("\n[START] Web dashboard on port 8000...")
        subprocess.Popen([sys.executable, "web_server.py"])
    
    elif choice == "4":
        print("\n[START] Monitor...")
        subprocess.run([sys.executable, "monitor.py"])
    
    elif choice == "5":
        print("\n[START] Exporting data...")
        subprocess.run([sys.executable, "export_data.py"])
    
    elif choice == "6":
        print("\n[START] Configuration Manager...")
        subprocess.run([sys.executable, "config_manager.py"])
    
    elif choice == "7":
        print("\n[LOG] System Log:")
        print("="*60)
        try:
            with open("system.log", "r") as f:
                lines = f.readlines()
                for line in lines[-50:]:
                    print(line.rstrip())
        except:
            print("No log file found")
        print("="*60)
    
    elif choice == "8":
        confirm = input("\n[WARN] Clear database? (yes/no): ")
        if confirm.lower() == "yes":
            import sqlite3
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            c.execute("DELETE FROM transactions")
            c.execute("DELETE FROM art_portfolio")
            c.execute("DELETE FROM trading_log")
            c.execute("DELETE FROM clones")
            conn.commit()
            conn.close()
            print("[OK] Database cleared")
    
    elif choice == "9":
        print("\n[EXIT] Goodbye!")
        sys.exit(0)
    
    else:
        print("\n[ERROR] Invalid option")

def main():
    """Main menu loop"""
    while True:
        show_menu()
        choice = input("Select option (1-9): ").strip()
        run_option(choice)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
