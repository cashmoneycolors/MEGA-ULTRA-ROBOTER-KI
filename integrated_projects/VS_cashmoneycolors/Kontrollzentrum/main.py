import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from core.zenith_controller import ZenithController
    st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")
controller = ZenithController()
controller.run()
import importlib
import os
import sys
def discover_modules():
    modules = []
    for fname in os.listdir(modules_path):
        if fname.endswith('.py') and not fname.startswith('__') and fname not in ['main.py', 'api_server.py']:
            modules.append(fname[:-3])
    return modules
modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
def get_capabilities(mod):
    caps = []
    for cap in ['run', 'install', 'to_svg', 'to_word', 'describe']:
        if hasattr(mod, cap):
            caps.append(cap)
    return caps


def main():
    print("=== Autonomes Kontrollzentrum ===")
    modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
    mods = []
    for module_name in discover_modules():
        try:
            mod = importlib.import_module(module_name)
            mods.append((module_name, mod, get_capabilities(mod)))
        except Exception as e:
            print(f"[WARN] Modul {module_name} konnte nicht geladen werden: {e}")
    # Kommandozeilenargumente prüfen
    args = sys.argv[1:]
        print("[🤖 MEGA ULTRA ROBOTER KI AUTONOM GENERIERUNG]")
        print("[11:36:42] 🤖 ROBOTER: Hallo! Ich bin dein autonomer Roboter KI wie Gemini. Ich steuere alles für dich.")
    if args:
        if args[0] == 'alle' and len(args) > 1:
            action = args[1]
            ok, fail = [], []
            for name, mod, caps in mods:
                if action in caps:
                    print(f"[INFO] {name}.{action}() wird ausgeführt...")
                    try:
                        getattr(mod, action)()
                        ok.append(name)
                    except Exception as e:
                        print(f"[ERROR] {name}.{action} fehlgeschlagen: {e}")
                        fail.append((name, str(e)))
            print("\n--- Zusammenfassung ---")
            print(f"Erfolgreich installiert: {', '.join(ok) if ok else 'keine'}")
        try:
            controller = ZenithController()
            controller.run()
        except Exception as e:
            print(f"[🤖 FEHLER] Mega Ultra Roboter KI: {e}")
            def main():
                import datetime
                parser = argparse.ArgumentParser(description="Kontrollzentrum Modul-Manager")
                parser.add_argument('module', nargs='?', help="Modulname oder 'alle' oder 'team'")
                parser.add_argument('action', nargs='?', help="Aktion: run, install, to_svg, ...")
                parser.add_argument('args', nargs=argparse.REMAINDER, help="Weitere Argumente für das Modul")
                args = parser.parse_args()

                modules = discover_modules()
                if not modules:
                    print("Keine Module gefunden.")
                    return

                # TEAM-MODUS: Wenn keine Argumente oder 'team' als Modul, führe alles vollautomatisch aus
                if (not args.module and not args.action) or (args.module and args.module.lower() == 'team'):
                    log_lines = []
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_lines.append(f"[TEAM-MODUS] Autostart am {now}\n")

                    # 1. Alle Module installieren
                    log_lines.append("[INSTALLATION]")
                    install_results = []
                    for m in modules:
                        if 'install' in m['capabilities']:
                            try:
                                m['module'].install()
                                msg = f"Modul: {m['name']:<20} Status: OK"
                                print(msg)
                                log_lines.append(msg)
                                install_results.append((m['name'], 'OK'))
                            except Exception as e:
                                msg = f"Modul: {m['name']:<20} Status: FEHLER ({e})"
                                print(msg)
                                log_lines.append(msg)
                                install_results.append((m['name'], f"FEHLER: {e}"))
                    ok_count = sum(1 for _, status in install_results if status == 'OK')
                    fail_count = len(install_results) - ok_count
                    log_lines.append(f"[ZUSAMMENFASSUNG] Erfolgreich installiert: {ok_count}  Fehlgeschlagen: {fail_count}\n")

                    # 2. Alle Module ausführen
                    log_lines.append("[RUN]")
                    run_results = []
                    for m in modules:
                        if 'run' in m['capabilities']:
                            try:
                                result = m['module'].run()
                                # Prüfe auf Demo-Modus oder spezielle Rückgabe
                                if isinstance(result, str) and 'demo' in result.lower():
                                    msg = f"Modul: {m['name']:<20} Status: DEMO-MODUS ({result})"
                                    print(msg)
                                    log_lines.append(msg)
                                    run_results.append((m['name'], f"DEMO-MODUS: {result}"))
                                else:
                                    msg = f"Modul: {m['name']:<20} Status: OK"
                                    print(msg)
                                    log_lines.append(msg)
                                    run_results.append((m['name'], 'OK'))
                            except Exception as e:
                                msg = f"Modul: {m['name']:<20} Status: FEHLER ({e})"
                                print(msg)
                                log_lines.append(msg)
                                run_results.append((m['name'], f"FEHLER: {e}"))
                    ok_count = sum(1 for _, status in run_results if status == 'OK')
                    demo_count = sum(1 for _, status in run_results if 'DEMO-MODUS' in status)
                    fail_count = len(run_results) - ok_count - demo_count
                    log_lines.append(f"[ZUSAMMENFASSUNG] Erfolgreich gestartet: {ok_count}  Demo-Modus: {demo_count}  Fehlgeschlagen: {fail_count}\n")

                    # 3. Logfile schreiben
                    with open('team_log.txt', 'a', encoding='utf-8') as f:
                        for line in log_lines:
                            f.write(line + '\n')
                    print("\n[TEAM-MODUS] Ablauf abgeschlossen. Details siehe team_log.txt.")
                    return

                # ...bestehende CLI-Logik...
            func(*params)
            return
        else:
            print("Ungültige Argumente. Beispiel: python main.py alle install | python main.py 3 to_svg out.svg")
            return
    # Interaktives CLI wie bisher
    print("Gefundene Module und Fähigkeiten:")
    for i, (name, mod, caps) in enumerate(mods):
        print(f"{i+1}. {name}: {', '.join(caps) if caps else 'keine speziellen Fähigkeiten'}")
    print("\nAktion wählen:")
    print("  [nummer] [aktion] [optional: parameter]")
    print("Beispiel: 2 to_svg out.svg")
    print("Oder 'alle install' für alle Module mit install().")
    inp = input("> ").strip()
    if inp.startswith('alle '):
        _, action = inp.split(' ', 1)
        for name, mod, caps in mods:
            if action in caps:
                print(f"[INFO] {name}.{action}() wird ausgeführt...")
                getattr(mod, action)()
        return
    parts = inp.split()
    if not parts or not parts[0].isdigit():
        print("Ungültige Eingabe.")
        return
    idx = int(parts[0]) - 1
    if idx < 0 or idx >= len(mods):
        print("Ungültige Modulnummer.")
        return
    action = parts[1] if len(parts) > 1 else 'run'
    params = parts[2:] if len(parts) > 2 else []
    name, mod, caps = mods[idx]
    if action not in caps:
        print(f"{name} unterstützt '{action}' nicht.")
        return
    print(f"[INFO] {name}.{action}({', '.join(params)}) wird ausgeführt...")
    func = getattr(mod, action)
    func(*params)

if __name__ == '__main__':
    main()
import streamlit as st
# Adjust the import path if 'zenith_controller.py' is in the same directory
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Ensure 'zenith_controller.py' exists in the same directory as this file
# Ensure 'zenith_controller.py' exists in the same directory as this file
try:
    from core.zenith_controller import ZenithController
except ModuleNotFoundError:
    st.error("Fehler: 'core/zenith_controller.py' wurde nicht gefunden. Bitte stellen Sie sicher, dass sich die Datei im Unterverzeichnis 'core/' befindet.")
    st.stop()
except ImportError as e:
    st.error(f"Fehler beim Importieren von 'ZenithController': {e}")
    st.stop()

st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")

controller = ZenithController()
controller.run()
import importlib
import os
import sys

# Liste aller produktiven Plug-and-Play-Module
MODULES = [
    'data_import',
    'nft_modul',
    'dropshipping_modul',
    'ki_modul',
    'grafik_design_modul',
]

modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

for module_name in MODULES:
    try:
        mod = importlib.import_module(module_name)
        print(f"Modul '{module_name}' erfolgreich importiert.")
        if hasattr(mod, 'run'):
            print(f"Starte {module_name}.run() ...")
            mod.run()
        else:
            print(f"Modul '{module_name}' hat keine run()-Funktion.")
    except Exception as e:
        print(f"Fehler beim Importieren/Ausführen von '{module_name}': {e}")