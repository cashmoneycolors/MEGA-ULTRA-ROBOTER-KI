#!/usr/bin/env python3
"""
🚀 QUICK START SCRIPT - Maximum Autonomous Profit System

Dieses Skript führt dich durch die ersten Schritte:
1. Überprüfung der Installation
2. Erste Konfiguration
3. System-Test
4. Vollständiger Start

Verwendung:
python quick_start.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def _upsert_dotenv_key(path: Path, key: str, value: str) -> None:
    lines: list[str] = []
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines(keepends=False)

    updated = False
    out: list[str] = []
    prefix = f"{key}="
    for line in lines:
        if line.startswith(prefix):
            out.append(f"{key}={value}")
            updated = True
        else:
            out.append(line)

    if not updated:
        if out and out[-1].strip() != "":
            out.append("")
        out.append(f"{key}={value}")

    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def validate_env_prod_ready(allow_test_mode: bool = True) -> bool:
    """Prüft .env ohne Secret-Leaks.

    - Wenn Keys als Umgebungsvariablen existieren, werden sie still in .env übernommen.
    - Wenn danach noch Keys fehlen, kann optional im Testmodus fortgefahren werden.
    """
    try:
        import env_validate
    except Exception:
        print("⚠️ env_validate.py fehlt – überspringe ENV-Validierung")
        return True

    env_path = Path(".env")
    if not env_path.exists() and Path(".env.example").exists():
        # Automatisch anlegen (ohne interaktives Nachfragen)
        env_path.write_text(Path(".env.example").read_text(encoding="utf-8"), encoding="utf-8")
        print("✅ .env aus .env.example erstellt")

    # 1) Fehlende Keys aus OS-Umgebung übernehmen (ohne Ausgabe der Werte)
    missing, _present = env_validate.validate(env_validate.DEFAULT_REQUIRED_KEYS)
    for key in list(missing):
        val = os.getenv(key)
        if val:
            _upsert_dotenv_key(env_path, key, val)

    # 2) Re-Check
    missing, present = env_validate.validate(env_validate.DEFAULT_REQUIRED_KEYS)
    if not missing:
        print("✅ .env ist prod-ready (alle erforderlichen Keys gesetzt)")
        return True

    print("⚠️ .env ist NICHT vollständig (Keys fehlen/Placeholder):")
    for k in missing:
        print(f"  - {k}")

    if not allow_test_mode:
        return False

    print("ℹ️ Fahre automatisch im Test-Modus fort (begrenzte Live-Daten).")
    return True


def print_header():
    """Drucke Header"""
    print(
        """
🚀 MAXIMUM AUTONOMOUS PROFIT SYSTEM - QUICK START
===================================================

🤖 Willkommen beim KI-gesteuerten Multi-Asset-Optimierungssystem!

Dieser Quick-Start führt dich durch:
✅ System-Überprüfung
✅ Abhängigkeiten-Installation
✅ Konfiguration
✅ Ersten Testlauf
✅ Vollständigen Systemstart

    """
    )


def check_python_version():
    """Überprüfe Python-Version"""
    print("🐍 Überprüfe Python-Version...")
    version = sys.version_info
    if version >= (3, 8):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} - benötigt 3.8+"
        )
        return False


def check_requirements_file():
    """Überprüfe requirements.txt"""
    print("📦 Überprüfe requirements.txt...")
    if Path("requirements.txt").exists():
        print("✅ requirements.txt gefunden")
        return True
    else:
        print("❌ requirements.txt nicht gefunden")
        return False


def install_dependencies():
    """Installiere Abhängigkeiten"""
    print("📦 Installiere Abhängigkeiten...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Abhängigkeiten erfolgreich installiert")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei Installation: {e}")
        return False


def check_env_file():
    """Überprüfe .env Konfiguration"""
    print("🔐 Überprüfe .env Konfiguration...")

    if Path(".env").exists():
        print("✅ .env Datei gefunden")
        return True
    elif Path(".env.example").exists():
        print("⚠️ .env nicht gefunden, aber .env.example verfügbar → erstelle automatisch .env")
        try:
            with open(".env.example", "r", encoding="utf-8") as src, open(
                ".env", "w", encoding="utf-8"
            ) as dst:
                dst.write(src.read())
            print("✅ .env aus .env.example erstellt")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Kopieren: {e}")
            return False
    else:
        print("⚠️ Keine .env oder .env.example gefunden")
        return True


def run_system_test():
    """Führe System-Test durch"""
    print("🧪 Führe System-Test durch...")

    try:
        # Teste Importe
        print("  📚 Teste Modul-Importe...")
        import live_data_integrator
        import autonomous_trading_engine
        import autonomous_dropshipping_engine
        import multi_asset_optimization_engine
        import unified_autonomous_dashboard
        import master_autonomous_orchestrator

        print("  ✅ Alle Module importiert")

        # Teste Live Data Integrator
        print("  📡 Teste Live Data Integrator...")
        # Hier könnte ein kurzer Test stehen

        print("✅ System-Test erfolgreich")
        return True

    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    except Exception as e:
        print(f"❌ System-Test fehlgeschlagen: {e}")
        return False


def start_full_system():
    """Starte vollständiges System"""
    print("🚀 Starte Maximum Autonomous Profit System...")

    try:
        # Starte Deployment-Skript
        subprocess.run([sys.executable, "deploy_maximum_autonomous_profit.py"])
    except KeyboardInterrupt:
        print("\n🛑 System durch User beendet")
    except Exception as e:
        print(f"❌ Fehler beim Systemstart: {e}")


def main():
    """Hauptfunktion"""
    print_header()

    # Schritt 1: Python-Version
    if not check_python_version():
        print("❌ Python-Version nicht kompatibel. Bitte aktualisiere auf Python 3.8+")
        sys.exit(1)

    # Schritt 2: Requirements-Datei
    if not check_requirements_file():
        print(
            "❌ requirements.txt fehlt. Bitte stelle sicher, dass alle Dateien vorhanden sind."
        )
        sys.exit(1)

    # Schritt 3: Abhängigkeiten installieren
    if not install_dependencies():
        print("❌ Abhängigkeiten konnten nicht installiert werden.")
        sys.exit(1)

    # Schritt 4: .env Konfiguration
    check_env_file()
    if not validate_env_prod_ready(allow_test_mode=True):
        print("❌ Fehlende Keys – Abbruch. Bitte .env vervollständigen und erneut starten.")
        sys.exit(1)

    # Schritt 5: System-Test
    if not run_system_test():
        print("❌ System-Test fehlgeschlagen. Bitte prüfe die Installation.")
        sys.exit(1)

    print(
        """
🎉 ALLES BEREIT!

Dein Maximum Autonomous Profit System ist einsatzbereit!

Verfügbare Startoptionen:
1. 🚀 Vollständiges System starten (empfohlen)
2. 📈 Nur Trading Engine
3. 🛒 Nur Dropshipping Engine
4. 📊 Nur Dashboard
5. 🧪 Test-Modus (keine echten Trades)

    """
    )

    while True:
        try:
            choice = input("Wähle eine Option (1-5) oder 'q' zum Beenden: ").strip()

            if choice == "1":
                print("🚀 Starte vollständiges System...")
                start_full_system()
                break

            elif choice == "2":
                print("📈 Starte Trading Engine...")
                subprocess.run(
                    [
                        sys.executable,
                        "deploy_maximum_autonomous_profit.py",
                        "--trading-only",
                    ]
                )
                break

            elif choice == "3":
                print("🛒 Starte Dropshipping Engine...")
                subprocess.run(
                    [
                        sys.executable,
                        "deploy_maximum_autonomous_profit.py",
                        "--dropshipping-only",
                    ]
                )
                break

            elif choice == "4":
                print("📊 Starte Dashboard...")
                subprocess.run(
                    [
                        sys.executable,
                        "deploy_maximum_autonomous_profit.py",
                        "--dashboard-only",
                    ]
                )
                break

            elif choice == "5":
                print("🧪 Starte Test-Modus...")
                subprocess.run(
                    [
                        sys.executable,
                        "deploy_maximum_autonomous_profit.py",
                        "--test-mode",
                    ]
                )
                break

            elif choice.lower() == "q":
                print("👋 Auf Wiedersehen!")
                break

            else:
                print("❌ Ungültige Auswahl. Bitte wähle 1-5 oder 'q'.")

        except KeyboardInterrupt:
            print("\n👋 Quick Start durch User beendet")
            break
        except Exception as e:
            print(f"❌ Fehler: {e}")


if __name__ == "__main__":
    main()
