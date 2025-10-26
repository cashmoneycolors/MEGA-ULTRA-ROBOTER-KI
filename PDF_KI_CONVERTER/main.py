# PDF KI-Konverter – MEGA ULTRA ROBOTER KI
# Analysiert PDF-Dateien, extrahiert Text und exportiert als JSON/CSV
import os
import sys
import json
import csv
from pathlib import Path
try:
    from PyPDF2 import PdfReader
except ImportError:
    print("[ERROR] PyPDF2 nicht installiert. Bitte requirements.txt beachten.")
    sys.exit(1)

PDF_PATH = os.environ.get("PDF_PATH", "../_EXAMPLES/beispiel.pdf")
EXPORT_JSON = os.environ.get("EXPORT_JSON", "output.json")
EXPORT_CSV = os.environ.get("EXPORT_CSV", "output.csv")

if not Path(PDF_PATH).exists():
    print(f"[ERROR] PDF nicht gefunden: {PDF_PATH}")
    sys.exit(1)

reader = PdfReader(PDF_PATH)
text = "\n".join(page.extract_text() or "" for page in reader.pages)

# Export als JSON
with open(EXPORT_JSON, "w", encoding="utf-8") as f:
    json.dump({"text": text}, f, ensure_ascii=False, indent=2)
print(f"[OK] Text als JSON exportiert: {EXPORT_JSON}")

# Export als CSV
with open(EXPORT_CSV, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["text"])
    writer.writerow([text])
print(f"[OK] Text als CSV exportiert: {EXPORT_CSV}")
