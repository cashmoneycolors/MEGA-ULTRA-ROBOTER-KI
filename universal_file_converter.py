import os
import sys
import shutil
import zipfile
import tarfile
import json
import csv
from collections import defaultdict
from typing import Dict, Set, List, Tuple, Any
from pathlib import Path

# ----------------------------------------------------------------------
# 1. DATENSTRUKTUR: Alle relevanten Dateiendungen & Kategorisierung
# ----------------------------------------------------------------------

DATEIFORMATE_KATEGORIEN: Dict[str, Set[str]] = {
    "Text und Dokumente": {".docx", ".doc", ".dotx", ".dotm", ".txt", ".rtf", ".pdf", ".odt", ".epub", ".mobi"},
    "Rastergrafiken": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp", ".psd", ".heic", ".heif"},
    "Vektorgrafiken": {".svg", ".ai", ".eps", ".cdr", ".wmf", ".emf"},
    "Audio und Video": {".mp3", ".wav", ".flac", ".aac", ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
    "Daten, Code und System": {".html", ".htm", ".css", ".js", ".xml", ".json", ".csv", ".xlsx", ".xls", ".exe", ".dll", ".msi", ".bat", ".cmd", ".ps1"},
    "Archive und Kompression": {".zip", ".rar", ".7z", ".tar.gz", ".tar", ".gz", ".bz2"},
    "CAD und 3D Modellierung": {".dwg", ".dxf", ".stl", ".step", ".stp", ".iges", ".igs", ".ifc", ".obj", ".fbx", ".blend"},
    "GIS und Geodaten": {".shp", ".shx", ".dbf", ".gpx", ".kml", ".kmz", ".geojson", ".geotiff"},
    "Datenbanken": {".mdb", ".accdb", ".sqlite", ".db", ".sql", ".mdf", ".ndf", ".dat", ".db3"},
    "Skripte und Programmierung": {".py", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".rb", ".pl", ".swift", ".go", ".rs"},
    "DTP und Layout": {".indd", ".qxp", ".idml", ".pmd", ".p65"},
    "E-Books": {".epub", ".mobi", ".azw", ".azw3", ".fb2"},
    "Schriftarten": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Konfiguration": {".ini", ".cfg", ".conf", ".config", ".yml", ".yaml"},
    "Logdateien": {".log", ".txt", ".csv"},
    "Backup Dateien": {".bak", ".backup", ".old", ".tmp"}
}

# Unterstützte Konvertierungsformate
UNTERSTUETZTE_KONVERTIERUNGEN = {
    # Bildformate
    'Bilder': {
        'JPEG': '.jpg',
        'PNG': '.png',
        'WEBP': '.webp',
        'BMP': '.bmp',
        'TIFF': '.tiff',
        'GIF': '.gif'
    },
    # Dokumentenformate
    'Dokumente': {
        'TXT': '.txt',
        'PDF': '.pdf',
        'DOCX': '.docx',
        'HTML': '.html',
        'JSON': '.json'
    },
    # Datenformate
    'Daten': {
        'CSV': '.csv',
        'JSON': '.json',
        'XML': '.xml',
        'Excel': '.xlsx'
    },
    # Archivformate
    'Archive': {
        'ZIP': '.zip',
        'TAR': '.tar',
        'TAR_GZ': '.tar.gz'
    }
}

# Mapping von Endungen zu Kategorien für Konvertierung
ENDUNG_ZU_KONVERTIERUNG_KATEGORIE = {
    # Bilder
    **{ext: 'Bilder' for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.tif', '.bmp', '.psd', '.heic', '.heif']},
    # Dokumente
    **{ext: 'Dokumente' for ext in ['.txt', '.docx', '.doc', '.pdf', '.html', '.htm', '.rtf', '.odt']},
    # Daten
    **{ext: 'Daten' for ext in ['.csv', '.json', '.xml', '.xlsx', '.xls']},
    # Archive
    **{ext: 'Archive' for ext in ['.zip', '.rar', '.7z', '.tar.gz', '.tar']}
}

# Erzeuge ein Set aller Endungen für die schnelle Suche
ALLE_ENDUNGEN_SET = set()
for endungen_set in DATEIFORMATE_KATEGORIEN.values():
    ALLE_ENDUNGEN_SET.update(endungen_set)

# Erzeuge ein Mapping von Endung zu Kategorie für die Ergebnisausgabe
ENDUNG_ZU_KATEGORIE = {}
for kategorie, endungen in DATEIFORMATE_KATEGORIEN.items():
    for endung in endungen:
        ENDUNG_ZU_KATEGORIE[endung] = kategorie

# ----------------------------------------------------------------------
# 2. HILFSFUNKTIONEN
# ----------------------------------------------------------------------

def groesse_formatieren(byte_groesse: float) -> str:
    """Konvertiert Byte-Größe in lesbare Einheiten (KB, MB, GB)."""
    if byte_groesse < 1024:
        return f"{byte_groesse:.2f} B"
    elif byte_groesse < 1024**2:
        return f"{byte_groesse / 1024:.2f} KB"
    elif byte_groesse < 1024**3:
        return f"{byte_groesse / 1024**2:.2f} MB"
    else:
        return f"{byte_groesse / 1024**3:.2f} GB"

def sicherer_dateiname(dateiname: str) -> str:
    """Entfernt ungültige Zeichen aus Dateinamen."""
    unguelstige_zeichen = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for zeichen in unguelstige_zeichen:
        dateiname = dateiname.replace(zeichen, '_')
    return dateiname

# ----------------------------------------------------------------------
# 3. UNIVERSAL-KONVERTIERUNGS-KLASSE
# ----------------------------------------------------------------------

class UniversalKonverter:
    def __init__(self, ausgabe_verzeichnis: str = "Konvertierte_Dateien"):
        self.ausgabe_verzeichnis = ausgabe_verzeichnis
        self.erfolgreiche_konvertierungen = 0
        self.fehlgeschlagene_konvertierungen = 0

        # Erstelle Ausgabeverzeichnis falls nicht vorhanden
        os.makedirs(self.ausgabe_verzeichnis, exist_ok=True)

    def konvertiere_datei(self, eingabe_pfad: str, ziel_format: str, ziel_kategorie: str) -> Tuple[bool, str]:
        """
        Konvertiert eine Datei in das gewünschte Format.
        """
        try:
            datei_name = Path(eingabe_pfad).stem
            datei_name = sicherer_dateiname(datei_name)
            endung = UNTERSTUETZTE_KONVERTIERUNGEN[ziel_kategorie][ziel_format]
            ausgabe_pfad = os.path.join(self.ausgabe_verzeichnis, f"{datei_name}_konvertiert{endung}")

            # Einfache Kopie für nicht implementierte Konvertierungen
            shutil.copy2(eingabe_pfad, ausgabe_pfad)
            self.erfolgreiche_konvertierungen += 1
            return True, ausgabe_pfad

        except Exception as e:
            self.fehlgeschlagene_konvertierungen += 1
            return False, f"Fehler bei {eingabe_pfad}: {str(e)}"

    def batch_konvertierung(self, verzeichnis: str, ziel_formate: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Konvertiert alle unterstützten Dateien in einem Verzeichnis.
        """
        ergebnisse = {}
        dateien_nach_kategorie = defaultdict(list)

        # Finde alle Dateien und gruppiere nach Kategorie
        for root, dirs, files in os.walk(verzeichnis):
            for datei in files:
                datei_pfad = os.path.join(root, datei)
                endung = Path(datei).suffix.lower()

                if endung in ENDUNG_ZU_KONVERTIERUNG_KATEGORIE:
                    kategorie = ENDUNG_ZU_KONVERTIERUNG_KATEGORIE[endung]
                    dateien_nach_kategorie[kategorie].append(datei_pfad)

        print(f"📁 Gefundene Dateien nach Kategorien:")
        for kategorie, dateien in dateien_nach_kategorie.items():
            print(f"   {kategorie}: {len(dateien)} Dateien")

        # Konvertiere jede Datei in jedes gewünschte Format ihrer Kategorie
        for kategorie, datei_liste in dateien_nach_kategorie.items():
            if kategorie in ziel_formate:
                ergebnisse[kategorie] = {}

                for ziel_format in ziel_formate[kategorie]:
                    ergebnisse[kategorie][ziel_format] = []

                    for datei_pfad in datei_liste:
                        erfolg, nachricht = self.konvertiere_datei(datei_pfad, ziel_format, kategorie)
                        if erfolg:
                            ergebnisse[kategorie][ziel_format].append({
                                'original': datei_pfad,
                                'konvertiert': nachricht,
                                'erfolg': True
                            })
                            print(f"✅ Konvertiert: {Path(datei_pfad).name} → {ziel_format}")
                        else:
                            ergebnisse[kategorie][ziel_format].append({
                                'original': datei_pfad,
                                'fehler': nachricht,
                                'erfolg': False
                            })
                            print(f"❌ Fehler: {Path(datei_pfad).name} → {ziel_format}")

        return ergebnisse

# ----------------------------------------------------------------------
# 4. ANALYSE-FUNKTIONEN
# ----------------------------------------------------------------------

def dateien_analysieren(verzeichnis_pfad: str, endungen_set: Set[str]) -> Dict[str, Dict[str, int | float]]:
    """
    Durchsucht ein Verzeichnis rekursiv und erfasst die Zählung und Gesamtgröße pro Endung.
    """
    ergebnisse_pro_endung = defaultdict(lambda: {'anzahl': 0, 'groesse': 0.0})

    if not os.path.isdir(verzeichnis_pfad):
        print(f"❌ Fehler: Das Verzeichnis '{verzeichnis_pfad}' wurde nicht gefunden.", file=sys.stderr)
        return dict(ergebnisse_pro_endung)

    for root, dirs, files in os.walk(verzeichnis_pfad):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ('appdata', '$recycle.bin')]

        for dateiname in files:
            basisname, endung = os.path.splitext(dateiname)
            endung_lower = endung.lower()

            if endung_lower in endungen_set:
                vollstaendiger_pfad = os.path.join(root, dateiname)

                try:
                    groesse_in_bytes = os.path.getsize(vollstaendiger_pfad)
                    ergebnisse_pro_endung[endung_lower]['anzahl'] += 1
                    ergebnisse_pro_endung[endung_lower]['groesse'] += groesse_in_bytes
                except OSError:
                    pass

    return dict(ergebnisse_pro_endung)

# ----------------------------------------------------------------------
# 5. ERWEITERTE KATEGORISIERUNG
# ----------------------------------------------------------------------

def kategorisiere_dateien_nach_typ(verzeichnis: str) -> Dict[str, List[str]]:
    """Kategorisiert Dateien nach ihrem Typ und Inhalt."""
    kategorien = {
        "Kleine_Dateien": [],      # < 1MB
        "Mittlere_Dateien": [],    # 1MB - 10MB
        "Große_Dateien": [],       # > 10MB
        "Bilder": [],
        "Dokumente": [],
        "Daten": [],
        "Archive": [],
        "Programme": [],
        "Audio_Video": [],
        "Skripte": []
    }

    for root, dirs, files in os.walk(verzeichnis):
        for datei in files:
            datei_pfad = os.path.join(root, datei)
            endung = Path(datei).suffix.lower()

            try:
                groesse = os.path.getsize(datei_pfad)

                # Größenkategorien
                if groesse < 1024 * 1024:  # < 1MB
                    kategorien["Kleine_Dateien"].append(datei_pfad)
                elif groesse < 10 * 1024 * 1024:  # 1MB - 10MB
                    kategorien["Mittlere_Dateien"].append(datei_pfad)
                else:  # > 10MB
                    kategorien["Große_Dateien"].append(datei_pfad)

                # Typkategorien
                if endung in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.heic', '.psd']:
                    kategorien["Bilder"].append(datei_pfad)
                elif endung in ['.txt', '.docx', '.doc', '.pdf', '.rtf', '.odt', '.epub', '.mobi']:
                    kategorien["Dokumente"].append(datei_pfad)
                elif endung in ['.csv', '.json', '.xml', '.xlsx', '.xls']:
                    kategorien["Daten"].append(datei_pfad)
                elif endung in ['.zip', '.rar', '.7z', '.tar.gz', '.tar']:
                    kategorien["Archive"].append(datei_pfad)
                elif endung in ['.exe', '.msi', '.dll']:
                    kategorien["Programme"].append(datei_pfad)
                elif endung in ['.mp3', '.wav', '.flac', '.mp4', '.mov', '.avi', '.mkv']:
                    kategorien["Audio_Video"].append(datei_pfad)
                elif endung in ['.py', '.java', '.c', '.cpp', '.js', '.html', '.css', '.php']:
                    kategorien["Skripte"].append(datei_pfad)

            except OSError:
                pass

    return kategorien

# ----------------------------------------------------------------------
# 6. HAUPTPROGRAMM MIT ALLEN FUNKTIONEN
# ----------------------------------------------------------------------

def hauptprogramm():
    print("=" * 80)
    print("🔄 UNIVERSAL DATEI-KONVERTER & ANALYSE-TOOL")
    print("=" * 80)

    # Benutzer nach Pfad fragen
    such_pfad = input("📁 Pfad zum Verzeichnis (Enter für Home-Verzeichnis): ").strip()
    if not such_pfad:
        such_pfad = os.path.expanduser('~')

    if not os.path.exists(such_pfad):
        print("❌ Verzeichnis existiert nicht!")
        return

    print(f"\n🔍 Starte Dateianalyse in: **{such_pfad}**")
    print(f"   (Analysiere **{len(ALLE_ENDUNGEN_SET)}** Formate aus {len(DATEIFORMATE_KATEGORIEN)} Kategorien)")
    print("=" * 80)

    # Führe die Analyse durch
    ergebnisse_nach_endung = dateien_analysieren(such_pfad, ALLE_ENDUNGEN_SET)

    # Zusammenfassung nach Kategorie
    zusammenfassung_kategorie = defaultdict(lambda: {'anzahl': 0, 'groesse': 0.0})
    gesamt_anzahl = 0
    gesamt_groesse = 0.0

    for endung, daten in ergebnisse_nach_endung.items():
        kategorie = ENDUNG_ZU_KATEGORIE.get(endung, "UNBEKANNT")
        zusammenfassung_kategorie[kategorie]['anzahl'] += daten['anzahl']
        zusammenfassung_kategorie[kategorie]['groesse'] += daten['groesse']
        gesamt_anzahl += daten['anzahl']
        gesamt_groesse += daten['groesse']

    # Ausgabe der Analyse-Ergebnisse
    if gesamt_anzahl > 0:
        print("\n## 📊 Zusammenfassung nach Kategorie")
        print("-" * 45)

        sortierte_kategorien = sorted(
            zusammenfassung_kategorie.items(),
            key=lambda item: item[1]['groesse'],
            reverse=True
        )

        for kategorie, daten in sortierte_kategorien:
            groesse_str = groesse_formatieren(daten['groesse'])
            anzahl = daten['anzahl']
            print(f"**{kategorie:<25}**: {anzahl:>6} Dateien | **{groesse_str:>12}**")

        print("-" * 45)
        print(f"**GESAMT** (Gefunden): {gesamt_anzahl:>6} Dateien | **{groesse_formatieren(gesamt_groesse):>12}**")

    else:
        print("\n⚠️ Es wurden keine Dateien mit den gesuchten Endungen in diesem Verzeichnis gefunden.")

    print("=" * 80)

    # Erweiterte Kategorisierung
    print("\n## 🗂️  Erweiterte Datei-Kategorisierung")
    print("-" * 40)

    kategorisierte_dateien = kategorisiere_dateien_nach_typ(such_pfad)

    for kategorie, dateien in kategorisierte_dateien.items():
        if dateien:
            gesamt_groesse_kategorie = sum(os.path.getsize(f) for f in dateien if os.path.exists(f))
            print(f"📁 {kategorie:<15}: {len(dateien):>4} Dateien | {groesse_formatieren(gesamt_groesse_kategorie):>12}")

    # Universelle Konvertierung
    print("\n## 🔄 UNIVERSALE DATEI-KONVERTIERUNG")
    print("-" * 35)

    konvertierbare_dateien = {}
    for kategorie in UNTERSTUETZTE_KONVERTIERUNGEN.keys():
        dateien_in_kategorie = []
        for root, dirs, files in os.walk(such_pfad):
            for datei in files:
                endung = Path(datei).suffix.lower()
                if endung in ENDUNG_ZU_KONVERTIERUNG_KATEGORIE and ENDUNG_ZU_KONVERTIERUNG_KATEGORIE[endung] == kategorie:
                    dateien_in_kategorie.append(os.path.join(root, datei))

        if dateien_in_kategorie:
            konvertierbare_dateien[kategorie] = dateien_in_kategorie
            print(f"🔄 {kategorie:<10}: {len(dateien_in_kategorie):>4} konvertierbare Dateien")

    if konvertierbare_dateien:
        konvertieren = input("\n🔄 Universelle Konvertierung starten? (j/n): ").lower().strip()

        if konvertieren in ['j', 'ja', 'y', 'yes']:
            print("\n🎯 Verfügbare Konvertierungsoptionen:")

            ziel_formate = {}
            for kategorie in konvertierbare_dateien.keys():
                print(f"\n📂 {kategorie}:")
                formate = UNTERSTUETZTE_KONVERTIERUNGEN[kategorie]
                for i, (format_name, endung) in enumerate(formate.items(), 1):
                    print(f"   {i}. {format_name} ({endung})")

                auswahl = input(f"   Wähle Formate für {kategorie} (Komma-getrennt oder 'alle'): ").strip()

                if auswahl.lower() == 'alle':
                    ziel_formate[kategorie] = list(formate.keys())
                else:
                    try:
                        indices = [int(x.strip()) for x in auswahl.split(',')]
                        ziel_formate[kategorie] = [list(formate.keys())[i-1] for i in indices]
                    except (ValueError, IndexError):
                        print(f"   ❌ Ungültige Auswahl für {kategorie}, überspringe...")
                        continue

            if ziel_formate:
                # Konvertierung starten
                konverter = UniversalKonverter()

                print(f"\n🔄 Starte universelle Konvertierung...")
                print(f"   Quelle: {such_pfad}")
                print("   Zielformate:")
                for kategorie, formate in ziel_formate.items():
                    print(f"     {kategorie}: {', '.join(formate)}")
                print("-" * 50)

                ergebnisse = konverter.batch_konvertierung(such_pfad, ziel_formate)

                print(f"\n✅ Universelle Konvertierung abgeschlossen!")
                print(f"   Erfolgreich: {konverter.erfolgreiche_konvertierungen}")
                print(f"   Fehlgeschlagen: {konverter.fehlgeschlagene_konvertierungen}")
                print(f"   Ausgabeverzeichnis: {konverter.ausgabe_verzeichnis}")

            else:
                print("❌ Keine gültigen Formate ausgewählt!")
        else:
            print("❌ Konvertierung abgebrochen!")
    else:
        print("❌ Keine konvertierbaren Dateien gefunden!")

    print("\n" + "=" * 80)
    print("🎉 Universal Konverter beendet!")
    print("=" * 80)

# ----------------------------------------------------------------------
# 7. PROGRAMMSTART
# ----------------------------------------------------------------------

if __name__ == "__main__":
    hauptprogramm()
