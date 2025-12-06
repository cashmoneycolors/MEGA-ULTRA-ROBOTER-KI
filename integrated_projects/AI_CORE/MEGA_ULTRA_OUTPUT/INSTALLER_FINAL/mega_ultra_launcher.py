#!/usr/bin/env python3
"""
MEGA ULTRA CREATIVE STUDIO - Windows Store Launcher
Professioneller Launcher für Microsoft Store App
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pathlib import Path

class MegaUltraLauncher:
    """Microsoft Store kompatible Launcher App"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEGA ULTRA Creative Studio")
        self.root.geometry("800x600")
        self.root.configure(bg='#0078d4')  # Microsoft Blue
        
        # App-Pfade
        self.app_directory = Path(__file__).parent
        self.apps = {
            'creative_studio': 'creative_studio_app.py',
            'app_generator': 'app_generator_clean.py', 
            'system_tools': 'system_check.py'
        }
        
        self.create_launcher_ui()
        
    def create_launcher_ui(self):
        """Erstelle Microsoft Store-style UI"""
        
        # Header mit Windows 11 Style
        header_frame = tk.Frame(self.root, bg='#0078d4', height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # App Icon und Titel
        title_frame = tk.Frame(header_frame, bg='#0078d4')
        title_frame.pack(expand=True, fill='both')
        
        # Haupttitel
        title_label = tk.Label(
            title_frame,
            text="MEGA ULTRA",
            font=('Segoe UI', 28, 'bold'),
            bg='#0078d4',
            fg='white'
        )
        title_label.pack(pady=(20, 0))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Creative Studio Professional",
            font=('Segoe UI', 14),
            bg='#0078d4',
            fg='#e1e1e1'
        )
        subtitle_label.pack()
        
        # Main Content Area mit Fluent Design
        main_frame = tk.Frame(self.root, bg='#f3f2f1')
        main_frame.pack(fill='both', expand=True)
        
        # Apps Grid
        apps_frame = tk.Frame(main_frame, bg='#f3f2f1')
        apps_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # App Cards im Fluent Design Style
        self.create_app_card(
            apps_frame, 
            "Creative Studio",
            "AI-powered design generation\nLogos, banners, icons & more",
            "#6264a7",
            lambda: self.launch_app('creative_studio'),
            row=0, col=0
        )
        
        self.create_app_card(
            apps_frame,
            "App Generator", 
            "Generate complete applications\nPython, Web, Utility tools",
            "#16537e",
            lambda: self.launch_app('app_generator'),
            row=0, col=1
        )
        
        self.create_app_card(
            apps_frame,
            "System Tools",
            "Performance monitoring\nSystem analysis & reports", 
            "#00bcf2",
            lambda: self.launch_app('system_tools'),
            row=1, col=0
        )
        
        # Info Card
        self.create_info_card(apps_frame, row=1, col=1)
        
        # Status Bar
        status_frame = tk.Frame(self.root, bg='#e1dfdd', height=40)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready • All AI systems online",
            font=('Segoe UI', 10),
            bg='#e1dfdd',
            fg='#323130'
        )
        self.status_label.pack(side='left', padx=20, pady=10)
        
        # Version Info
        version_label = tk.Label(
            status_frame,
            text="Version 1.0.0 • Microsoft Store Edition",
            font=('Segoe UI', 9),
            bg='#e1dfdd',
            fg='#605e5c'
        )
        version_label.pack(side='right', padx=20, pady=10)
    
    def create_app_card(self, parent, title, description, color, command, row, col):
        """Erstelle Fluent Design App Card"""
        
        card_frame = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            bd=0
        )
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Card Header mit Farbe
        header_frame = tk.Frame(card_frame, bg=color, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        card_title = tk.Label(
            header_frame,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            bg=color,
            fg='white'
        )
        card_title.pack(pady=15)
        
        # Card Body
        body_frame = tk.Frame(card_frame, bg='white')
        body_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        desc_label = tk.Label(
            body_frame,
            text=description,
            font=('Segoe UI', 11),
            bg='white',
            fg='#323130',
            justify='left',
            wraplength=200
        )
        desc_label.pack(anchor='w')
        
        # Launch Button
        launch_btn = tk.Button(
            body_frame,
            text="Launch",
            command=command,
            font=('Segoe UI', 11, 'bold'),
            bg=color,
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        launch_btn.pack(anchor='w', pady=(15, 0))
        
        # Hover Effects
        def on_enter(event):
            launch_btn.config(bg=self.darken_color(color))
        
        def on_leave(event):
            launch_btn.config(bg=color)
        
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
        # Card Shadow Effect (simulate with border)
        card_frame.config(highlightbackground='#e1dfdd', highlightthickness=1)
    
    def create_info_card(self, parent, row, col):
        """Erstelle Info Card"""
        
        card_frame = tk.Frame(parent, bg='#faf9f8', relief='flat', bd=0)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Header
        header_frame = tk.Frame(card_frame, bg='#8764b8', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        info_title = tk.Label(
            header_frame,
            text="System Info",
            font=('Segoe UI', 16, 'bold'),
            bg='#8764b8',
            fg='white'
        )
        info_title.pack(pady=15)
        
        # Body
        body_frame = tk.Frame(card_frame, bg='#faf9f8')
        body_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        info_text = """• 5 AI Engines Active
• GPU Acceleration Ready
• Multi-format Export
• Real-time Generation
• Auto-learning System"""
        
        info_label = tk.Label(
            body_frame,
            text=info_text,
            font=('Segoe UI', 11),
            bg='#faf9f8',
            fg='#323130',
            justify='left'
        )
        info_label.pack(anchor='w')
        
        # Settings Button
        settings_btn = tk.Button(
            body_frame,
            text="Settings",
            command=self.open_settings,
            font=('Segoe UI', 11),
            bg='#8764b8',
            fg='white',
            relief='flat',
            padx=20,
            pady=8
        )
        settings_btn.pack(anchor='w', pady=(15, 0))
    
    def darken_color(self, color):
        """Verdunkle Farbe für Hover-Effekt"""
        color_map = {
            '#6264a7': '#4f5185',
            '#16537e': '#0f3f5f', 
            '#00bcf2': '#0095c7',
            '#8764b8': '#6b4d93'
        }
        return color_map.get(color, color)
    
    def launch_app(self, app_name):
        """Starte ausgewählte App"""
        app_file = self.apps.get(app_name)
        
        if not app_file:
            messagebox.showerror("Error", f"App {app_name} not found!")
            return
        
        app_path = self.app_directory / app_file
        
        if not app_path.exists():
            messagebox.showerror("Error", f"App file not found: {app_file}")
            return
        
        try:
            # Update Status
            self.status_label.config(text=f"Launching {app_name}...")
            
            # Starte App in separatem Prozess
            subprocess.Popen([
                sys.executable, 
                str(app_path)
            ], cwd=str(self.app_directory))
            
            # Reset Status nach kurzer Zeit
            threading.Timer(2.0, lambda: self.status_label.config(
                text="Ready • All AI systems online"
            )).start()
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {app_name}:\n{e}")
            self.status_label.config(text="Ready • All AI systems online")
    
    def open_settings(self):
        """Öffne Einstellungen"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg='#f3f2f1')
        
        # Settings Header
        header = tk.Label(
            settings_window,
            text="MEGA ULTRA Settings",
            font=('Segoe UI', 18, 'bold'),
            bg='#f3f2f1',
            fg='#323130'
        )
        header.pack(pady=20)
        
        # Settings Content
        content_frame = tk.Frame(settings_window, bg='#f3f2f1')
        content_frame.pack(fill='both', expand=True, padx=30)
        
        # Theme Settings
        theme_frame = tk.LabelFrame(content_frame, text="Appearance", bg='#f3f2f1')
        theme_frame.pack(fill='x', pady=10)
        
        tk.Checkbutton(
            theme_frame,
            text="Dark Mode",
            bg='#f3f2f1',
            font=('Segoe UI', 11)
        ).pack(anchor='w', padx=10, pady=5)
        
        tk.Checkbutton(
            theme_frame,
            text="High Contrast",
            bg='#f3f2f1',
            font=('Segoe UI', 11)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Performance Settings
        perf_frame = tk.LabelFrame(content_frame, text="Performance", bg='#f3f2f1')
        perf_frame.pack(fill='x', pady=10)
        
        tk.Checkbutton(
            perf_frame,
            text="GPU Acceleration",
            bg='#f3f2f1',
            font=('Segoe UI', 11)
        ).pack(anchor='w', padx=10, pady=5)
        
        tk.Checkbutton(
            perf_frame,
            text="Auto-optimize Memory",
            bg='#f3f2f1',
            font=('Segoe UI', 11)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Close Button
        close_btn = tk.Button(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            font=('Segoe UI', 11),
            bg='#0078d4',
            fg='white',
            relief='flat',
            padx=30,
            pady=10
        )
        close_btn.pack(pady=20)
    
    def run(self):
        """Starte Launcher"""
        # Setze Windows-spezifische Eigenschaften
        try:
            # Windows 11 Stil
            self.root.wm_attributes('-alpha', 0.98)
        except:
            pass
        
        self.root.mainloop()

if __name__ == "__main__":
    launcher = MegaUltraLauncher()
    launcher.run()