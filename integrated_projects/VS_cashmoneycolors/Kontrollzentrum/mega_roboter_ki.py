
import os
import subprocess
import shutil
from pathlib import Path

def ensure_structure():
    for folder in ["modules", "core", "tests", ".github"]:
        Path(folder).mkdir(exist_ok=True)
    if not Path(".env").exists() and Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
    print("[OK] Projektstruktur geprüft und angelegt.")

def install_requirements():
    if Path("requirements.txt").exists():
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
        print("[OK] Abhängigkeiten installiert.")
    else:
        print("[WARN] requirements.txt fehlt.")

def test_modules():
    print("[INFO] Starte Unittests...")
    subprocess.run(["python", "-m", "unittest", "discover", "tests"])

def test_api():
    ki_sideboard = Path("modules/ki_sideboard.py")
    if ki_sideboard.exists():
        print("[INFO] Starte KI-Sideboard für API-Test...")
        subprocess.Popen(["python", str(ki_sideboard)])
        print("[HINWEIS] Teste Endpunkte z.B. mit Postman: http://localhost:8003/health")
    else:
        print("[WARN] modules/ki_sideboard.py nicht gefunden.")

def backup():
    backup_name = f"backup_{os.getpid()}.zip"
    shutil.make_archive(backup_name.replace('.zip',''), 'zip', '.')
    print(f"[OK] Backup erstellt: {backup_name}")

def main():
    print("""
    === MegaRoboterKI – Kontrollzentrum ===
    1. Struktur prüfen
    2. Abhängigkeiten installieren
    3. Module testen
    4. API-Integration testen
    5. Backup erstellen
    0. Beenden
    """)
    while True:
        wahl = input("Aktion wählen (0-5): ")
        if wahl == "1": ensure_structure()
        elif wahl == "2": install_requirements()
        elif wahl == "3": test_modules()
        elif wahl == "4": test_api()
        elif wahl == "5": backup()
        elif wahl == "0": break
        else: print("Ungültige Eingabe!")

if __name__ == "__main__":
    main()
