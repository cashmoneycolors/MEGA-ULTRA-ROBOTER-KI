"""
PHASE_1_ERROR_SCAN.py
Syntaktischer Schnell-Scan aller Python-Dateien im Repo.
Ergebnis wird nach error_scan_report.txt geschrieben.
Exit-Code 0 = keine Fehler, >0 = Anzahl gefundener Fehler.
"""
import os, sys, py_compile, traceback

ROOT = os.path.abspath(os.path.dirname(__file__))
REPORT = os.path.join(ROOT, 'error_scan_report.txt')
EXCLUDE_DIRS = {'.venv', 'venv', '__pycache__'}
ERRORS = []

def iter_py_files():
    for base, dirs, files in os.walk(ROOT):
        # Filter excluded dirs in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(base, f)

def scan():
    for path in iter_py_files():
        rel = os.path.relpath(path, ROOT)
        try:
            py_compile.compile(path, doraise=True)
        except Exception as e:
            ERRORS.append((rel, f"{e.__class__.__name__}: {e}"))

if __name__ == '__main__':
    scan()
    with open(REPORT, 'w', encoding='utf-8') as fh:
        if not ERRORS:
            fh.write('SCAN OK - keine Syntaxfehler gefunden.\n')
        else:
            fh.write(f'SCAN FAIL - {len(ERRORS)} Fehler gefunden.\n')
            for rel, msg in ERRORS:
                fh.write(f'- {rel}: {msg}\n')
    print(open(REPORT, 'r', encoding='utf-8').read().strip())
    sys.exit(len(ERRORS))
