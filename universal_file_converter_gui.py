import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

# Import des Hauptmoduls
from universal_file_converter import (
    hauptprogramm,
    dateien_analysieren,
    kategorisiere_dateien_nach_typ,
    UniversalKonverter,
    ALLE_ENDUNGEN_SET,
    groesse_formatieren
)

class UniversalFileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔄 Universal Datei-Konverter & Analyse-Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')

        # Hauptframe
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfiguriere Grid-Layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Titel
        title_label = ttk.Label(main_frame, text="🔄 Universal Datei-Konverter & Analyse-Tool",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Verzeichnis-Auswahl
        ttk.Label(main_frame, text="📁 Verzeichnis:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dir_entry = ttk.Entry(main_frame, width=50)
        self.dir_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        self.dir_entry.insert(0, os.path.expanduser('~'))

        browse_btn = ttk.Button(main_frame, text="Durchsuchen", command=self.browse_directory)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)

        # Notebook für Tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))

        # Tab 1: Analyse
        analyze_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(analyze_frame, text="📊 Analyse")

        analyze_btn = ttk.Button(analyze_frame, text="🔍 Analyse starten", command=self.start_analysis)
        analyze_btn.grid(row=0, column=0, pady=(0, 10))

        # Analyse-Ergebnisse
        self.analyze_text = scrolledtext.ScrolledText(analyze_frame, wrap=tk.WORD, height=20)
        self.analyze_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        analyze_frame.columnconfigure(0, weight=1)
        analyze_frame.rowconfigure(1, weight=1)

        # Tab 2: Konvertierung
        convert_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(convert_frame, text="🔄 Konvertierung")

        # Konvertierungsoptionen
        ttk.Label(convert_frame, text="🎯 Konvertierungsoptionen:").grid(row=0, column=0, sticky=tk.W, pady=5)

        # Checkboxen für Kategorien
        self.category_vars = {}
        categories = ['Bilder', 'Dokumente', 'Daten', 'Archive']

        for i, category in enumerate(categories):
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            ttk.Checkbutton(convert_frame, text=category, variable=var).grid(
                row=i//2 + 1, column=i%2, sticky=tk.W, padx=(20, 0), pady=2)

        # Konvertierungs-Button
        convert_btn = ttk.Button(convert_frame, text="🔄 Konvertierung starten", command=self.start_conversion)
        convert_btn.grid(row=3, column=0, columnspan=2, pady=(20, 10))

        # Konvertierungs-Ergebnisse
        self.convert_text = scrolledtext.ScrolledText(convert_frame, wrap=tk.WORD, height=15)
        self.convert_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        convert_frame.columnconfigure(0, weight=1)
        convert_frame.columnconfigure(1, weight=1)
        convert_frame.rowconfigure(4, weight=1)

        # Tab 3: Info
        info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(info_frame, text="ℹ️ Info")

        info_text = """🔄 Universal Datei-Konverter & Analyse-Tool

Dieses Tool bietet umfassende Funktionen für:

📊 DATEIANALYSE:
• Automatische Erkennung von über 120 Dateiformaten
• Kategorisierung nach Dateityp und Größe
• Detaillierte Statistiken und Zusammenfassungen

🔄 UNIVERSALE KONVERTIERUNG:
• Unterstützt Bilder, Dokumente, Daten und Archive
• Batch-Konvertierung mehrerer Dateien
• Flexible Auswahl von Zielformaten

🎯 FUNKTIONEN:
• Rekursive Verzeichnisanalyse
• Intelligente Dateikategorisierung
• Sichere Dateinamensbereinigung
• Umfassende Fehlerbehandlung

📁 UNTERSTÜTZTE FORMATE:
• Bilder: JPEG, PNG, WEBP, BMP, TIFF, GIF
• Dokumente: TXT, PDF, DOCX, HTML, JSON
• Daten: CSV, JSON, XML, Excel
• Archive: ZIP, TAR, TAR.GZ

💡 TIPP: Wählen Sie ein Verzeichnis und starten Sie die Analyse,
um einen detaillierten Überblick über Ihre Dateien zu erhalten!"""

        info_scrolled = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD)
        info_scrolled.insert(tk.END, info_text)
        info_scrolled.config(state=tk.DISABLED)
        info_scrolled.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        # Statusleiste
        self.status_var = tk.StringVar()
        self.status_var.set("Bereit")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Fortschrittsbalken
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

    def browse_directory(self):
        """Verzeichnis-Browser öffnen"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def start_analysis(self):
        """Analyse in separatem Thread starten"""
        directory = self.dir_entry.get().strip()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Fehler", "Bitte wählen Sie ein gültiges Verzeichnis aus!")
            return

        self.status_var.set("Analysiere Dateien...")
        self.progress_var.set(0)
        self.analyze_text.delete(1.0, tk.END)

        # Thread für Analyse starten
        analysis_thread = threading.Thread(target=self.run_analysis, args=(directory,))
        analysis_thread.daemon = True
        analysis_thread.start()

    def run_analysis(self, directory):
        """Analyse durchführen"""
        try:
            self.progress_var.set(10)

            # Führe die Analyse durch
            ergebnisse_nach_endung = dateien_analysieren(directory, ALLE_ENDUNGEN_SET)
            self.progress_var.set(50)

            # Zusammenfassung nach Kategorie
            from collections import defaultdict
            zusammenfassung_kategorie = defaultdict(lambda: {'anzahl': 0, 'groesse': 0.0})
            gesamt_anzahl = 0
            gesamt_groesse = 0.0

            # Import für Kategorisierung
            from universal_file_converter import ENDUNG_ZU_KATEGORIE

            for endung, daten in ergebnisse_nach_endung.items():
                kategorie = ENDUNG_ZU_KATEGORIE.get(endung, "UNBEKANNT")
                zusammenfassung_kategorie[kategorie]['anzahl'] += daten['anzahl']
                zusammenfassung_kategorie[kategorie]['groesse'] += daten['groesse']
                gesamt_anzahl += daten['anzahl']
                gesamt_groesse += daten['groesse']

            self.progress_var.set(70)

            # Erweiterte Kategorisierung
            kategorisierte_dateien = kategorisiere_dateien_nach_typ(directory)
            self.progress_var.set(90)

            # Ergebnisse formatieren
            result_text = f"""================================================================================
🔍 Analyse-Ergebnisse für: {directory}
================================================================================

## 📊 Zusammenfassung nach Kategorie
"""

            if gesamt_anzahl > 0:
                sortierte_kategorien = sorted(
                    zusammenfassung_kategorie.items(),
                    key=lambda item: item[1]['groesse'],
                    reverse=True
                )

                result_text += "-" * 45 + "\n"
                for kategorie, daten in sortierte_kategorien:
                    groesse_str = groesse_formatieren(daten['groesse'])
                    anzahl = daten['anzahl']
                    result_text += f"**{kategorie:<25}**: {anzahl:>6} Dateien | **{groesse_str:>12}**\n"

                result_text += "-" * 45 + "\n"
                result_text += f"**GESAMT** (Gefunden): {gesamt_anzahl:>6} Dateien | **{groesse_formatieren(gesamt_groesse):>12}**\n"

            else:
                result_text += "\n⚠️ Es wurden keine Dateien mit den gesuchten Endungen gefunden.\n"

            result_text += "\n" + "=" * 80 + "\n"
            result_text += "\n## 🗂️  Erweiterte Datei-Kategorisierung\n"
            result_text += "-" * 40 + "\n"

            for kategorie, dateien in kategorisierte_dateien.items():
                if dateien:
                    gesamt_groesse_kategorie = sum(os.path.getsize(f) for f in dateien if os.path.exists(f))
                    result_text += f"📁 {kategorie:<15}: {len(dateien):>4} Dateien | {groesse_formatieren(gesamt_groesse_kategorie):>12}\n"

            self.progress_var.set(100)
            self.status_var.set("Analyse abgeschlossen")

            # Ergebnisse in Textfeld einfügen
            self.analyze_text.insert(tk.END, result_text)

        except Exception as e:
            self.status_var.set("Fehler bei der Analyse")
            messagebox.showerror("Fehler", f"Analyse fehlgeschlagen: {str(e)}")
            self.progress_var.set(0)

    def start_conversion(self):
        """Konvertierung starten"""
        directory = self.dir_entry.get().strip()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Fehler", "Bitte wählen Sie ein gültiges Verzeichnis aus!")
            return

        # Ausgewählte Kategorien sammeln
        selected_categories = [cat for cat, var in self.category_vars.items() if var.get()]

        if not selected_categories:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens eine Kategorie aus!")
            return

        # Zielformate definieren
        ziel_formate = {}
        from universal_file_converter import UNTERSTUETZTE_KONVERTIERUNGEN

        for category in selected_categories:
            if category in UNTERSTUETZTE_KONVERTIERUNGEN:
                ziel_formate[category] = list(UNTERSTUETZTE_KONVERTIERUNGEN[category].keys())

        if not ziel_formate:
            messagebox.showwarning("Warnung", "Keine gültigen Konvertierungsformate gefunden!")
            return

        self.status_var.set("Starte Konvertierung...")
        self.progress_var.set(0)
        self.convert_text.delete(1.0, tk.END)

        # Thread für Konvertierung starten
        convert_thread = threading.Thread(target=self.run_conversion, args=(directory, ziel_formate))
        convert_thread.daemon = True
        convert_thread.start()

    def run_conversion(self, directory, ziel_formate):
        """Konvertierung durchführen"""
        try:
            self.progress_var.set(10)

            # Konverter initialisieren
            konverter = UniversalKonverter()
            self.progress_var.set(20)

            # Batch-Konvertierung starten
            ergebnisse = konverter.batch_konvertierung(directory, ziel_formate)
            self.progress_var.set(80)

            # Ergebnisse formatieren
            result_text = f"""================================================================================
🔄 Konvertierungs-Ergebnisse
================================================================================

📁 Quelle: {directory}
🎯 Zielformate: {', '.join(ziel_formate.keys())}

✅ Erfolgreich konvertiert: {konverter.erfolgreiche_konvertierungen} Dateien
❌ Fehlgeschlagen: {konverter.fehlgeschlagene_konvertierungen} Dateien

📂 Ausgabeverzeichnis: {konverter.ausgabe_verzeichnis}

================================================================================
"""

            self.progress_var.set(100)
            self.status_var.set("Konvertierung abgeschlossen")

            # Ergebnisse in Textfeld einfügen
            self.convert_text.insert(tk.END, result_text)

            # Erfolgsmeldung
            messagebox.showinfo("Erfolg",
                              f"Konvertierung abgeschlossen!\n\n"
                              f"Erfolgreich: {konverter.erfolgreiche_konvertierungen}\n"
                              f"Fehlgeschlagen: {konverter.fehlgeschlagene_konvertierungen}\n\n"
                              f"Ausgabeverzeichnis: {konverter.ausgabe_verzeichnis}")

        except Exception as e:
            self.status_var.set("Fehler bei der Konvertierung")
            messagebox.showerror("Fehler", f"Konvertierung fehlgeschlagen: {str(e)}")
            self.progress_var.set(0)

def main():
    root = tk.Tk()
    app = UniversalFileConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
