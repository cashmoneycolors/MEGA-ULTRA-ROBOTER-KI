import importlib
import os
import sys
import glob

MODULES_DIR = os.path.join(os.path.dirname(__file__), 'modules')
CORE_DIR = os.path.join(os.path.dirname(__file__), 'core')
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

def list_module_files():
    return [os.path.basename(f) for f in glob.glob(os.path.join(MODULES_DIR, '*.py')) if not f.endswith('__init__.py')]

def test_all_modules():
    print("--- Kontrollzentrum Modul-Test-Runner ---")
    for mod_file in list_module_files():
        mod_name = mod_file[:-3]
        print(f"\nTeste Modul: {mod_name}")
        try:
            mod = importlib.import_module(f"modules.{mod_name}")
            if hasattr(mod, 'run'):
                result = mod.run()
                print(f"run() Rückgabe: {result}")
            else:
                print("Kein run()-Entry-Point gefunden.")
        except Exception as e:
            print(f"Fehler beim Laden/Ausführen von {mod_name}: {e}")

if __name__ == "__main__":
    test_all_modules()
