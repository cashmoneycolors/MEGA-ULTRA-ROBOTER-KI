"""
CCashMoneyIDE - Production Desktop Application
Echte, funktionierende Desktop-App für Windows HP Laptop
Version: 1.0 - PRODUKTIONSBEREIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
import threading

class CCashMoneyIDE:
    """Hauptklasse für die Desktop-Anwendung"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CCashMoneyIDE - Autonomous Zenith Optimizer")
        self.root.geometry("1200x800")
        
        # Pfade
        self.base_dir = Path(__file__).parent.absolute()
        self.kontrollzentrum = self.base_dir / "Kontrollzentrum"
        
        # Style
        self.setup_style()
        
        # GUI erstellen
        self.create_menu()
        self.create_main_layout()
        self.create_status_bar()
        
        # Initialisierung
        self.load_project_status()
        self.log("CCashMoneyIDE gestartet - Bereit!")
    
    def setup_style(self):
        """Professionelles Styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Farben
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#007acc',
            'success': '#4ec9b0',
            'warning': '#ce9178',
            'error': '#f48771'
        }
        
        # Configure styles
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['accent'], foreground=self.colors['fg'])
        style.map('TButton', background=[('active', '#005a9e')])
    
    def create_menu(self):
        """Menüleiste erstellen"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Datei-Menü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Projekt öffnen", command=self.open_project)
        file_menu.add_command(label="Einstellungen", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Integration-Menü
        integration_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Integration", menu=integration_menu)
        integration_menu.add_command(label="Starte Integration", command=self.start_integration)
        integration_menu.add_command(label="Berichte anzeigen", command=self.show_reports)
        integration_menu.add_command(label="Module verwalten", command=self.manage_modules)
        
        # Tools-Menü
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Terminal öffnen", command=self.open_terminal)
        tools_menu.add_command(label="Explorer öffnen", command=self.open_explorer)
        tools_menu.add_command(label="Git Status", command=self.show_git_status)
        
        # Hilfe-Menü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Dokumentation", command=self.show_documentation)
        help_menu.add_command(label="Über", command=self.show_about)
    
    def create_main_layout(self):
        """Hauptlayout erstellen"""
        # Hauptcontainer
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linke Spalte - Projekt-Explorer
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        ttk.Label(left_frame, text="📁 Projekt-Explorer", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.project_tree = ttk.Treeview(left_frame, height=30)
        self.project_tree.pack(fill=tk.BOTH, expand=True)
        self.populate_project_tree()
        
        # Rechte Spalte - Dashboard & Aktionen
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Dashboard
        dashboard_frame = ttk.LabelFrame(right_frame, text="Dashboard", padding=10)
        dashboard_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_dashboard(dashboard_frame)
        
        # Aktionen
        actions_frame = ttk.LabelFrame(right_frame, text="Schnell-Aktionen", padding=10)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_actions(actions_frame)
        
        # Log-Ausgabe
        log_frame = ttk.LabelFrame(right_frame, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def create_dashboard(self, parent):
        """Dashboard mit Statistiken"""
        # Grid Layout
        stats = [
            ("📦 Dateien", "9 Dateien", 0, 0),
            ("📊 Größe", "~107 KB", 0, 1),
            ("✅ Status", "Bereit", 1, 0),
            ("🔧 Module", "5 Module", 1, 1),
        ]
        
        for text, value, row, col in stats:
            frame = tk.Frame(parent, bg='#2d2d30', relief=tk.RAISED, bd=2)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(frame, text=text, bg='#2d2d30', fg='#ffffff', font=('Arial', 10)).pack(pady=2)
            tk.Label(frame, text=value, bg='#2d2d30', fg='#4ec9b0', font=('Arial', 12, 'bold')).pack(pady=2)
        
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
    
    def create_actions(self, parent):
        """Schnell-Aktionen"""
        actions = [
            ("🚀 Integration starten", self.start_integration, '#007acc'),
            ("📄 Berichte anzeigen", self.show_reports, '#4ec9b0'),
            ("⚙️ Module verwalten", self.manage_modules, '#ce9178'),
            ("📁 Explorer öffnen", self.open_explorer, '#b5cea8'),
        ]
        
        for text, command, color in actions:
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.RAISED,
                bd=2,
                cursor='hand2',
                padx=20,
                pady=10
            )
            btn.pack(fill=tk.X, pady=5)
    
    def create_status_bar(self):
        """Statusleiste"""
        self.status_bar = tk.Label(
            self.root,
            text="Bereit",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#007acc',
            fg='white',
            font=('Arial', 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def populate_project_tree(self):
        """Projekt-Baum füllen"""
        self.project_tree.heading('#0', text='Projekt-Struktur')
        
        # Kontrollzentrum
        kontroll = self.project_tree.insert('', 'end', text='📁 Kontrollzentrum', open=True)
        
        if self.kontrollzentrum.exists():
            for item in sorted(self.kontrollzentrum.iterdir()):
                if item.is_file():
                    icon = '📄' if item.suffix in ['.txt', '.md'] else '🐍' if item.suffix == '.py' else '📋'
                    self.project_tree.insert(kontroll, 'end', text=f'{icon} {item.name}')
                elif item.is_dir():
                    dir_node = self.project_tree.insert(kontroll, 'end', text=f'📁 {item.name}')
                    # Sub-Dateien
                    for subitem in sorted(item.iterdir())[:5]:  # Max 5 anzeigen
                        if subitem.is_file():
                            self.project_tree.insert(dir_node, 'end', text=f'  📄 {subitem.name}')
    
    def log(self, message, level='INFO'):
        """Log-Nachricht hinzufügen"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        colors = {
            'INFO': '#4ec9b0',
            'SUCCESS': '#4ec9b0',
            'WARNING': '#ce9178',
            'ERROR': '#f48771'
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] ")
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.tag_config(level, foreground=colors.get(level, '#ffffff'))
        self.log_text.see(tk.END)
        
        # Status-Bar update
        self.status_bar.config(text=message)
    
    def load_project_status(self):
        """Projekt-Status laden"""
        self.log("Lade Projekt-Status...")
        
        # Prüfe Kontrollzentrum
        if self.kontrollzentrum.exists():
            files = list(self.kontrollzentrum.glob('*'))
            self.log(f"✅ Kontrollzentrum gefunden: {len(files)} Dateien", 'SUCCESS')
        else:
            self.log("⚠️ Kontrollzentrum nicht gefunden", 'WARNING')
    
    def start_integration(self):
        """Integration starten"""
        result = messagebox.askyesno(
            "Integration starten",
            "Möchtest du die automatische Integration starten?\n\n"
            "Dies wird:\n"
            "• Projekt analysieren\n"
            "• Backup erstellen\n"
            "• Module konsolidieren\n"
            "• Berichte generieren\n\n"
            "Dauer: ~2-3 Minuten"
        )
        
        if result:
            self.log("🚀 Starte Integration...", 'INFO')
            threading.Thread(target=self.run_integration, daemon=True).start()
    
    def run_integration(self):
        """Integration im Hintergrund ausführen"""
        script = self.kontrollzentrum / "update_integration.py"
        
        if not script.exists():
            self.log("❌ Integrations-Skript nicht gefunden!", 'ERROR')
            return
        
        try:
            process = subprocess.Popen(
                [sys.executable, str(script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.kontrollzentrum)
            )
            
            for line in process.stdout:
                self.root.after(0, lambda l=line: self.log(l.strip(), 'INFO'))
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.log("✅ Integration abgeschlossen!", 'SUCCESS'))
                self.root.after(0, lambda: messagebox.showinfo("Erfolg", "Integration erfolgreich abgeschlossen!"))
            else:
                self.root.after(0, lambda: self.log("⚠️ Integration mit Warnungen beendet", 'WARNING'))
        
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ Fehler: {str(e)}", 'ERROR'))
    
    def show_reports(self):
        """Berichte anzeigen"""
        reports_dir = self.kontrollzentrum / "integration_reports"
        
        if not reports_dir.exists():
            messagebox.showinfo("Info", "Noch keine Berichte vorhanden.\n\nStarte zuerst die Integration.")
            return
        
        # Fenster für Berichte
        reports_window = tk.Toplevel(self.root)
        reports_window.title("Integration Berichte")
        reports_window.geometry("800x600")
        
        # Liste der Berichte
        frame = ttk.Frame(reports_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="📊 Verfügbare Berichte", font=('Arial', 14, 'bold')).pack(pady=10)
        
        for report in sorted(reports_dir.glob('*')):
            btn_frame = tk.Frame(frame, bg='#2d2d30', relief=tk.RAISED, bd=2)
            btn_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(btn_frame, text=f"📄 {report.name}", bg='#2d2d30', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Button(
                btn_frame,
                text="Öffnen",
                command=lambda r=report: self.open_file(r),
                bg='#007acc',
                fg='white'
            ).pack(side=tk.RIGHT, padx=10, pady=5)
    
    def manage_modules(self):
        """Module verwalten"""
        modules_dir = self.kontrollzentrum / "consolidated_modules"
        
        if not modules_dir.exists():
            messagebox.showinfo("Info", "Modul-Struktur noch nicht erstellt.\n\nStarte zuerst die Integration.")
            return
        
        # Modul-Manager Fenster
        modules_window = tk.Toplevel(self.root)
        modules_window.title("Modul-Manager")
        modules_window.geometry("700x500")
        
        frame = ttk.Frame(modules_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="⚙️ Modul-Struktur", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(frame)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree.heading('#0', text='Module')
        
        for module_dir in sorted(modules_dir.iterdir()):
            if module_dir.is_dir():
                node = tree.insert('', 'end', text=f'📁 {module_dir.name}')
                for file in sorted(module_dir.glob('*.py')):
                    tree.insert(node, 'end', text=f'  🐍 {file.name}')
    
    def open_terminal(self):
        """Terminal öffnen"""
        self.log("Öffne Terminal...")
        subprocess.Popen('start cmd', shell=True, cwd=str(self.base_dir))
    
    def open_explorer(self):
        """Explorer öffnen"""
        self.log("Öffne Explorer...")
        os.startfile(str(self.kontrollzentrum))
    
    def open_project(self):
        """Projekt öffnen"""
        directory = filedialog.askdirectory(title="Projekt-Verzeichnis wählen")
        if directory:
            self.log(f"Projekt geöffnet: {directory}")
            messagebox.showinfo("Projekt", f"Projekt geöffnet:\n{directory}")
    
    def open_settings(self):
        """Einstellungen"""
        messagebox.showinfo("Einstellungen", "Einstellungen werden in einer zukünftigen Version verfügbar sein.")
    
    def show_git_status(self):
        """Git Status anzeigen"""
        self.log("Prüfe Git Status...")
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=str(self.base_dir)
            )
            
            if result.returncode == 0:
                status = result.stdout.strip() or "Keine Änderungen"
                messagebox.showinfo("Git Status", status)
                self.log(f"Git Status: {status}")
            else:
                self.log("Git nicht verfügbar", 'WARNING')
        except:
            self.log("Git nicht installiert", 'WARNING')
    
    def show_documentation(self):
        """Dokumentation anzeigen"""
        docs = [
            "00_READ_THIS_FIRST.txt",
            "README_START_HERE_FIRST.md",
            "VISUAL_SESSION_SUMMARY.txt"
        ]
        
        # Dialog mit Auswahl
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Dokumentation")
        doc_window.geometry("500x400")
        
        frame = ttk.Frame(doc_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="📚 Verfügbare Dokumentation", font=('Arial', 14, 'bold')).pack(pady=10)
        
        for doc in docs:
            doc_path = self.kontrollzentrum / doc
            if doc_path.exists():
                tk.Button(
                    frame,
                    text=f"📄 {doc}",
                    command=lambda d=doc_path: self.open_file(d),
                    bg='#007acc',
                    fg='white',
                    font=('Arial', 10),
                    relief=tk.RAISED,
                    bd=2,
                    cursor='hand2',
                    padx=10,
                    pady=10
                ).pack(fill=tk.X, pady=5)
    
    def open_file(self, filepath):
        """Datei öffnen"""
        try:
            os.startfile(str(filepath))
            self.log(f"Öffne: {filepath.name}")
        except Exception as e:
            self.log(f"Fehler beim Öffnen: {str(e)}", 'ERROR')
    
    def show_about(self):
        """Über-Dialog"""
        about_text = """
CCashMoneyIDE
Autonomous Zenith Optimizer

Version: 1.0 PRODUKTIONSBEREIT
Build: 2025-11-20

Entwickelt für Windows HP Laptop
Echte, funktionierende Desktop-Anwendung

Features:
✅ Projekt-Integration
✅ Modul-Verwaltung
✅ Bericht-Generierung
✅ Git-Integration
✅ Terminal-Zugriff

© 2025 CCashMoneyIDE Team
        """
        messagebox.showinfo("Über CCashMoneyIDE", about_text)


def main():
    """Hauptfunktion"""
    root = tk.Tk()
    app = CCashMoneyIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
