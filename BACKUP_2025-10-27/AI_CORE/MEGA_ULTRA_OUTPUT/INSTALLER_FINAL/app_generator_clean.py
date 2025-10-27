#!/usr/bin/env python3
"""
SICHERHEITSHINWEIS: Kritische Secrets (z.B. JWT_SECRET, MAINTENANCE_KEY) werden ausschließlich über Umgebungsvariablen bezogen oder sicher zur Laufzeit generiert. Niemals hardcodieren!
Wenn ein Secret generiert wird, erscheint eine gelbe Warnung. Siehe Projektdoku und Copilot-Instructions.
"""
import os
import secrets

# --- Secret Handling (global) ---
def get_secret_env_or_generate(env_name, length=32):
    value = os.environ.get(env_name)
    if value:
        return value
    generated = secrets.token_urlsafe(length)
    print(f"\033[93mWARNUNG: {env_name} nicht gefunden, generiere zur Laufzeit! Niemals hardcodieren!\033[0m")
    return generated

# Beispiel für kritische Secrets
JWT_SECRET = get_secret_env_or_generate('JWT_SECRET', 32)
MAINTENANCE_KEY = get_secret_env_or_generate('MAINTENANCE_KEY', 32)

"""
MEGA ULTRA APP GENERATOR - COMPLETE APPLICATION SUITE
Erstellt vollstandige Apps auf Kommando - wie ein echter Entwickler!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Import aller Komponenten
sys.path.append('.')
try:
    from teil_1_core_engine import MegaUltraCoreEngine
    from optimierung_phase1 import MegaUltraOptimizedEngine
    from optimierung_phase2 import MegaUltraColorTheoryAI, MegaUltraTypographyAI
    from teil_4_ki_learning import MegaUltraKILearning
except ImportError as e:
    print(f"Warning: Could not import all AI components: {e}")

class MegaUltraAppGenerator:
    """Vollstandiger App Generator - erstellt echte Apps!"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEGA ULTRA APP GENERATOR - Professional Suite")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # App Templates
        self.app_templates = {
            'python_app': {
                'name': 'Python Desktop App',
                'description': 'Tkinter Desktop Application',
                'tech_stack': ['Python', 'Tkinter', 'SQLite'],
                'features': ['GUI Interface', 'Database', 'Cross-Platform'],
                'time_estimate': '5-10 minutes'
            },
            'web_app': {
                'name': 'Simple Web App',
                'description': 'HTML/CSS/JavaScript Web App',
                'tech_stack': ['HTML5', 'CSS3', 'JavaScript'],
                'features': ['Responsive Design', 'Modern UI'],
                'time_estimate': '10-15 minutes'
            },
            'utility_app': {
                'name': 'Utility Tool',
                'description': 'Command Line Utility',
                'tech_stack': ['Python', 'argparse'],
                'features': ['CLI Interface', 'File Processing'],
                'time_estimate': '5 minutes'
            }
        }
        
        # Initialize systems
        self.initialize_systems()
        self.create_interface()
        
        # Generation state
        self.generated_apps = []
        
        print("MEGA ULTRA APP GENERATOR READY!")
    
    def initialize_systems(self):
        """Initialize AI systems"""
        try:
            self.core_engine = MegaUltraCoreEngine()
            self.systems_ready = True
            print("All Systems Ready!")
        except Exception as e:
            print(f"System Error: {e}")
            self.systems_ready = False
    
    def create_interface(self):
        """Create main interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2b2b2b', height=80)
        header_frame.pack(fill='x', padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="MEGA ULTRA APP GENERATOR",
            font=('Arial', 20, 'bold'),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=10)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel
        left_frame = tk.Frame(main_frame, bg='#3b3b3b', width=400)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Command input
        cmd_label = tk.Label(
            left_frame,
            text="App Generation Command:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        cmd_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.app_command = tk.Text(
            left_frame,
            height=4,
            font=('Arial', 11),
            bg='#4b4b4b',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.app_command.pack(fill='x', padx=20, pady=5)
        
        # Quick commands
        quick_label = tk.Label(
            left_frame,
            text="Quick Commands:",
            font=('Arial', 10, 'bold'),
            bg='#3b3b3b',
            fg='#cccccc'
        )
        quick_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        quick_commands = [
            "Erstelle eine Todo-List Desktop App",
            "Mache einen Taschenrechner",
            "Generiere ein Notiz-Tool"
        ]
        
        for cmd in quick_commands:
            btn = tk.Button(
                left_frame,
                text=cmd,
                command=lambda c=cmd: self.set_command(c),
                bg='#5b5b5b',
                fg='#ffffff',
                font=('Arial', 9),
                relief='flat'
            )
            btn.pack(fill='x', padx=20, pady=2)
        
        # App type selection
        type_label = tk.Label(
            left_frame,
            text="App Type:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        type_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.app_type_var = tk.StringVar(value='python_app')
        type_frame = tk.Frame(left_frame, bg='#3b3b3b')
        type_frame.pack(fill='x', padx=20, pady=5)
        
        for app_type, template in self.app_templates.items():
            rb = tk.Radiobutton(
                type_frame,
                text=template['name'],
                variable=self.app_type_var,
                value=app_type,
                bg='#3b3b3b',
                fg='#ffffff',
                selectcolor='#5b5b5b',
                font=('Arial', 10),
                command=self.update_template_info
            )
            rb.pack(anchor='w', pady=2)
        
        # Project settings
        settings_label = tk.Label(
            left_frame,
            text="Project Settings:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        settings_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        # Project name
        name_frame = tk.Frame(left_frame, bg='#3b3b3b')
        name_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            name_frame,
            text="Project Name:",
            bg='#3b3b3b',
            fg='#cccccc',
            font=('Arial', 10)
        ).pack(side='left')
        
        self.project_name_var = tk.StringVar(value="MyApp")
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.project_name_var,
            bg='#4b4b4b',
            fg='#ffffff',
            font=('Arial', 10)
        )
        name_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Output directory
        dir_frame = tk.Frame(left_frame, bg='#3b3b3b')
        dir_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            dir_frame,
            text="Output Dir:",
            bg='#3b3b3b',
            fg='#cccccc',
            font=('Arial', 10)
        ).pack(side='left')
        
        self.output_dir_var = tk.StringVar(value="./GENERATED_APPS")
        dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.output_dir_var,
            bg='#4b4b4b',
            fg='#ffffff',
            font=('Arial', 9),
            width=20
        )
        dir_entry.pack(side='right', padx=(10, 5))
        
        browse_btn = tk.Button(
            dir_frame,
            text="Browse",
            command=self.browse_output_dir,
            bg='#5b5b5b',
            fg='#ffffff',
            font=('Arial', 8)
        )
        browse_btn.pack(side='right')
        
        # Generate button
        self.generate_btn = tk.Button(
            left_frame,
            text="GENERATE APP",
            command=self.start_generation,
            bg='#007acc',
            fg='#ffffff',
            font=('Arial', 14, 'bold'),
            height=2
        )
        self.generate_btn.pack(fill='x', padx=20, pady=20)
        
        # Right panel
        right_frame = tk.Frame(main_frame, bg='#3b3b3b', width=400)
        right_frame.pack(side='right', fill='both', expand=True)
        right_frame.pack_propagate(False)
        
        # Template info
        info_label = tk.Label(
            right_frame,
            text="Template Information:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        info_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.template_info = tk.Text(
            right_frame,
            height=8,
            font=('Arial', 10),
            bg='#4b4b4b',
            fg='#cccccc',
            state='disabled'
        )
        self.template_info.pack(fill='x', padx=20, pady=5)
        
        # Generation progress
        progress_label = tk.Label(
            right_frame,
            text="Generation Progress:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        progress_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.progress_text = tk.Text(
            right_frame,
            height=10,
            font=('Arial', 9),
            bg='#4b4b4b',
            fg='#00ff00',
            state='disabled'
        )
        self.progress_text.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            right_frame,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', padx=20, pady=10)
        
        # Generated apps list
        apps_label = tk.Label(
            right_frame,
            text="Generated Apps:",
            font=('Arial', 12, 'bold'),
            bg='#3b3b3b',
            fg='#ffffff'
        )
        apps_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        self.apps_listbox = tk.Listbox(
            right_frame,
            height=6,
            font=('Arial', 9),
            bg='#4b4b4b',
            fg='#ffffff',
            selectbackground='#007acc'
        )
        self.apps_listbox.pack(fill='x', padx=20, pady=5)
        
        # Control buttons
        controls_frame = tk.Frame(right_frame, bg='#3b3b3b')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        run_btn = tk.Button(
            controls_frame,
            text="Run App",
            command=self.run_selected_app,
            bg='#28a745',
            fg='#ffffff',
            font=('Arial', 9)
        )
        run_btn.pack(side='left', padx=(0, 5))
        
        open_btn = tk.Button(
            controls_frame,
            text="Open Folder",
            command=self.open_app_folder,
            bg='#6c757d',
            fg='#ffffff',
            font=('Arial', 9)
        )
        open_btn.pack(side='left', padx=(0, 5))
        
        delete_btn = tk.Button(
            controls_frame,
            text="Delete",
            command=self.delete_selected_app,
            bg='#dc3545',
            fg='#ffffff',
            font=('Arial', 9)
        )
        delete_btn.pack(side='right')
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#1b1b1b', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready for App Generation",
            bg='#1b1b1b',
            fg='#00ff00',
            font=('Arial', 10)
        )
        self.status_label.pack(side='left', padx=20, pady=5)
        
        # Initialize template info
        self.update_template_info()
    
    def set_command(self, command):
        """Set command in text area"""
        self.app_command.delete('1.0', 'end')
        self.app_command.insert('1.0', command)
    
    def update_template_info(self):
        """Update template information"""
        app_type = self.app_type_var.get()
        template = self.app_templates.get(app_type, {})
        
        info_text = f"""
Template: {template.get('name', 'Unknown')}

Description:
{template.get('description', 'No description available')}

Tech Stack:
{', '.join(template.get('tech_stack', []))}

Features:
{chr(10).join(['* ' + feature for feature in template.get('features', [])])}

Estimated Time:
{template.get('time_estimate', 'Unknown')}
        """.strip()
        
        self.template_info.config(state='normal')
        self.template_info.delete('1.0', 'end')
        self.template_info.insert('1.0', info_text)
        self.template_info.config(state='disabled')
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
    
    def start_generation(self):
        """Start app generation"""
        command = self.app_command.get('1.0', 'end').strip()
        
        if not command:
            messagebox.showwarning("Warning", "Please enter an app generation command!")
            return
        
        # Disable button and start progress
        self.generate_btn.config(state='disabled', text="GENERATING...")
        self.progress_bar['value'] = 0
        self.status_label.config(text="Generating application...", fg='#ffaa00')
        
        # Start generation thread
        threading.Thread(
            target=self.generate_app,
            args=(command,),
            daemon=True
        ).start()
    
    def generate_app(self, command):
        """Generate complete application"""
        try:
            self.log_progress("Starting app generation...")
            self.update_progress(10)
            
            # Get settings
            app_type = self.app_type_var.get()
            project_name = self.project_name_var.get()
            output_dir = self.output_dir_var.get()
            
            self.log_progress(f"Creating {app_type}: {project_name}")
            self.update_progress(25)
            
            # Create project directory
            project_path = os.path.join(output_dir, project_name)
            os.makedirs(project_path, exist_ok=True)
            
            self.log_progress("Setting up project structure...")
            self.update_progress(40)
            
            # Generate based on type
            if app_type == 'python_app':
                self.generate_python_app(project_path, project_name, command)
            elif app_type == 'web_app':
                self.generate_web_app(project_path, project_name, command)
            elif app_type == 'utility_app':
                self.generate_utility_app(project_path, project_name, command)
            
            self.update_progress(80)
            
            # Create documentation
            self.create_readme(project_path, project_name, command, app_type)
            
            self.log_progress("Finalizing project...")
            self.update_progress(95)
            
            # Add to generated apps list
            app_info = {
                'name': project_name,
                'type': app_type,
                'path': project_path,
                'command': command,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.update_progress(100)
            self.root.after(0, self.generation_complete, app_info)
            
        except Exception as e:
            self.root.after(0, self.generation_error, str(e))
    
    def generate_python_app(self, project_path, project_name, command):
        """Generate Python desktop app"""
        
        # Main application file
        main_content = f'''#!/usr/bin/env python3
"""
{project_name} - Generated by MEGA ULTRA App Generator
Command: {command}
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import json

class {project_name.replace(' ', '').replace('-', '')}App:
    """Main Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("{project_name}")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize data
        self.data_file = "app_data.json"
        self.load_data()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="{project_name}",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.LabelFrame(main_frame, text="Welcome", font=('Arial', 12, 'bold'))
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        welcome_text = f"""
Welcome to {project_name}!

This application was generated based on your request:
"{command}"

Generated on: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}

You can now customize this application to fit your specific needs.
The source code is fully editable and well-documented.
        """.strip()
        
        welcome_label = tk.Label(
            welcome_frame,
            text=welcome_text,
            font=('Arial', 10),
            justify='left',
            wraplength=700
        )
        welcome_label.pack(padx=20, pady=15)
        
        # Feature showcase area
        features_frame = tk.LabelFrame(main_frame, text="Features", font=('Arial', 12, 'bold'))
        features_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Feature list
        features_list = [
            "Modern GUI with tkinter",
            "Data persistence with JSON",
            "Error handling and validation",
            "Responsive layout design",
            "Cross-platform compatibility",
            "Easy to extend and customize"
        ]
        
        for i, feature in enumerate(features_list):
            feature_label = tk.Label(
                features_frame,
                text=f"• {{feature}}",
                font=('Arial', 10),
                anchor='w'
            )
            feature_label.pack(fill='x', padx=20, pady=2)
        
        # Control buttons
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill='x', pady=10)
        
        # Sample functionality buttons
        tk.Button(
            controls_frame,
            text="Show Info",
            command=self.show_info,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            padx=20
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            controls_frame,
            text="Save Data",
            command=self.save_data,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            padx=20
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            controls_frame,
            text="Load Data",
            command=self.load_data,
            bg='#e67e22',
            fg='white',
            font=('Arial', 10),
            padx=20
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            controls_frame,
            text="Exit",
            command=self.root.quit,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            padx=20
        ).pack(side='right')
    
    def show_info(self):
        """Show application information"""
        info_text = f"""
{project_name}
Version 1.0.0

Generated by MEGA ULTRA App Generator
Based on command: "{command}"

This is a fully functional Python desktop application
that you can customize and extend as needed.
        """.strip()
        
        messagebox.showinfo("Application Info", info_text)
    
    def save_data(self):
        """Save application data"""
        data = {{
            "last_saved": datetime.now().isoformat(),
            "app_name": "{project_name}",
            "version": "1.0.0"
        }}
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {{e}}")
    
    def load_data(self):
        """Load application data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                last_saved = data.get('last_saved', 'Never')
                messagebox.showinfo("Data Loaded", f"Last saved: {{last_saved}}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {{e}}")
        else:
            messagebox.showinfo("Info", "No saved data found.")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = {project_name.replace(' ', '').replace('-', '')}App()
    app.run()
'''
        
        with open(os.path.join(project_path, 'main.py'), 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        # Requirements file
        requirements = '''# Application dependencies
# Install with: pip install -r requirements.txt

# GUI framework (built into Python)
# tkinter is included with Python

# For JSON data handling (built into Python)
# json is included with Python

# Optional: For advanced features
# pillow>=9.0.0  # For image handling
# requests>=2.28.0  # For web requests
'''
        
        with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
            f.write(requirements)
        
        # Batch file for Windows
        batch_content = f'''@echo off
echo Starting {project_name}...
python main.py
pause
'''
        
        with open(os.path.join(project_path, 'run.bat'), 'w') as f:
            f.write(batch_content)
        
        # Shell script for Unix/Linux
        shell_content = f'''#!/bin/bash
echo "Starting {project_name}..."
python3 main.py
'''
        
        with open(os.path.join(project_path, 'run.sh'), 'w') as f:
            f.write(shell_content)
    
    def generate_web_app(self, project_path, project_name, command):
        """Generate simple web app"""
        
        # HTML file
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{project_name}</h1>
        <p>Generated by MEGA ULTRA App Generator</p>
    </header>
    
    <main>
        <section class="welcome">
            <h2>Welcome!</h2>
            <p>This web application was generated based on your request:</p>
            <blockquote>"{command}"</blockquote>
        </section>
        
        <section class="features">
            <h2>Features</h2>
            <ul>
                <li>Responsive design</li>
                <li>Modern CSS styling</li>
                <li>Interactive JavaScript</li>
                <li>Cross-browser compatibility</li>
            </ul>
        </section>
        
        <section class="demo">
            <h2>Interactive Demo</h2>
            <button id="demo-btn" onclick="showDemo()">Click Me!</button>
            <div id="demo-result"></div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 {project_name} - Generated by MEGA ULTRA App Generator</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>'''
        
        with open(os.path.join(project_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # CSS file
        css_content = '''/* Modern CSS for generated web app */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 2rem 0;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

header p {
    font-size: 1.1rem;
    opacity: 0.9;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

section {
    background: rgba(255, 255, 255, 0.95);
    margin: 2rem 0;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

h2 {
    color: #4a5568;
    margin-bottom: 1rem;
    font-size: 1.8rem;
}

blockquote {
    background: #f7fafc;
    border-left: 4px solid #667eea;
    padding: 1rem;
    margin: 1rem 0;
    font-style: italic;
    color: #2d3748;
}

ul {
    list-style: none;
    padding-left: 0;
}

li {
    padding: 0.5rem 0;
    position: relative;
    padding-left: 1.5rem;
}

li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #48bb78;
    font-weight: bold;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

button:active {
    transform: translateY(0);
}

#demo-result {
    margin-top: 1rem;
    padding: 1rem;
    background: #f0fff4;
    border: 2px solid #48bb78;
    border-radius: 6px;
    display: none;
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

footer {
    text-align: center;
    padding: 2rem;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 2rem;
}

/* Responsive design */
@media (max-width: 768px) {
    main {
        padding: 0 1rem;
    }
    
    section {
        padding: 1.5rem;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    h2 {
        font-size: 1.5rem;
    }
}
'''
        
        with open(os.path.join(project_path, 'style.css'), 'w') as f:
            f.write(css_content)
        
        # JavaScript file
        js_content = '''// JavaScript for generated web app

document.addEventListener('DOMContentLoaded', function() {
    console.log('Web app loaded successfully!');
    
    // Add some interactivity
    const demoBtn = document.getElementById('demo-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', showDemo);
    }
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

function showDemo() {
    const result = document.getElementById('demo-result');
    const messages = [
        'Hello from your generated web app!',
        'This is a fully functional web application.',
        'You can customize and extend it as needed.',
        'Great job on creating your first app!',
        'The possibilities are endless!'
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    const currentTime = new Date().toLocaleTimeString();
    
    result.innerHTML = `
        <h3>Demo Result</h3>
        <p><strong>Message:</strong> ${randomMessage}</p>
        <p><strong>Time:</strong> ${currentTime}</p>
        <p><strong>Random Number:</strong> ${Math.floor(Math.random() * 1000)}</p>
    `;
    
    result.style.display = 'block';
    
    // Change button text
    const btn = document.getElementById('demo-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Click Again!';
    
    setTimeout(() => {
        btn.textContent = originalText;
    }, 2000);
}

// Add some dynamic effects
function addSparkles() {
    // Simple animation effect
    console.log('✨ Adding some magic to your web app!');
}

// Call sparkles effect
setTimeout(addSparkles, 1000);
'''
        
        with open(os.path.join(project_path, 'script.js'), 'w') as f:
            f.write(js_content)
    
    def generate_utility_app(self, project_path, project_name, command):
        """Generate command line utility"""
        
        utility_content = f'''#!/usr/bin/env python3
"""
{project_name} - Command Line Utility
Generated by MEGA ULTRA App Generator
Command: {command}
"""

import argparse
import os
import sys
from datetime import datetime

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='{project_name} - Generated utility tool'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='{project_name} 1.0.0'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show application information'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demonstration'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input file or text'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file'
    )
    
    args = parser.parse_args()
    
    if args.info:
        show_info()
    elif args.demo:
        run_demo()
    elif args.input:
        process_input(args.input, args.output)
    else:
        parser.print_help()

def show_info():
    """Show application information"""
    print(f"""
{project_name}
Version: 1.0.0
Generated: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}

Description:
This utility was generated based on the command:
"{command}"

Usage:
  python {{os.path.basename(__file__)}} --help     Show this help
  python {{os.path.basename(__file__)}} --info     Show information
  python {{os.path.basename(__file__)}} --demo     Run demonstration
  python {{os.path.basename(__file__)}} --input <file>  Process input file

Generated by MEGA ULTRA App Generator
    """.strip())

def run_demo():
    """Run demonstration"""
    print("Running {project_name} demonstration...")
    print()
    
    # Demo functionality
    print("1. Processing sample data...")
    import time
    time.sleep(1)
    
    print("2. Performing calculations...")
    result = sum(range(1, 101))  # Sum 1 to 100
    print(f"   Result: {{result}}")
    time.sleep(1)
    
    print("3. Generating output...")
    output = f"Demo completed at {{datetime.now().strftime('%H:%M:%S')}}"
    print(f"   {{output}}")
    
    print()
    print("Demo completed successfully!")

def process_input(input_data, output_file=None):
    """Process input data"""
    print(f"Processing input: {{input_data}}")
    
    # Check if input is a file
    if os.path.isfile(input_data):
        print("Reading from file...")
        try:
            with open(input_data, 'r') as f:
                content = f.read()
            
            # Process the content (example: count lines)
            lines = content.split('\\n')
            words = content.split()
            chars = len(content)
            
            result = f"""
File Analysis Report
===================
File: {{input_data}}
Lines: {{len(lines)}}
Words: {{len(words)}}
Characters: {{chars}}
Processed: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
            """.strip()
            
            print(result)
            
            # Save to output file if specified
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(result)
                print(f"Results saved to: {{output_file}}")
            
        except Exception as e:
            print(f"Error reading file: {{e}}", file=sys.stderr)
            sys.exit(1)
    
    else:
        # Treat as text input
        print(f"Processing text input: {{input_data[:50]}}...")
        
        # Simple text processing
        result = f"""
Text Analysis
=============
Input: {{input_data}}
Length: {{len(input_data)}}
Words: {{len(input_data.split())}}
Uppercase: {{input_data.upper()}}
Processed: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
        """.strip()
        
        print(result)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"Results saved to: {{output_file}}")

if __name__ == "__main__":
    main()
'''
        
        with open(os.path.join(project_path, 'utility.py'), 'w', encoding='utf-8') as f:
            f.write(utility_content)
        
        # Batch file for Windows
        batch_content = f'''@echo off
echo {project_name} Utility
echo ==================
python utility.py %*
'''
        
        with open(os.path.join(project_path, 'run.bat'), 'w') as f:
            f.write(batch_content)
    
    def create_readme(self, project_path, project_name, command, app_type):
        """Create README file"""
        
        readme_content = f'''# {project_name}

Generated by **MEGA ULTRA App Generator** 

## Description

This {app_type.replace('_', ' ')} was automatically generated based on your request:

> {command}

## Installation

### Prerequisites
- Python 3.7 or higher (for Python apps)
- Modern web browser (for web apps)

### Setup
1. Download or clone this project
2. For Python apps: Install dependencies (if any):
   ```
   pip install -r requirements.txt
   ```

## Running the Application

### Python Desktop App
```bash
python main.py
```

Or double-click `run.bat` (Windows) or `run.sh` (Unix/Linux)

### Web App
Simply open `index.html` in your web browser

### Utility App
```bash
python utility.py --help
python utility.py --demo
```

## Features

- ✅ Modern, clean interface
- ✅ Cross-platform compatibility  
- ✅ Well-documented code
- ✅ Easy to customize and extend
- ✅ Ready for immediate use

## Customization

This generated application provides a solid foundation that you can build upon:

1. **Modify the UI**: Update the interface to match your needs
2. **Add Features**: Extend functionality as required
3. **Integrate APIs**: Connect to external services
4. **Add Database**: Implement data persistence
5. **Deploy**: Package for distribution

## Project Structure

```
{project_name}/
├── main.py          # Main application (Python apps)
├── index.html       # Main page (Web apps)
├── style.css        # Styling (Web apps)
├── script.js        # JavaScript (Web apps)
├── utility.py       # Utility script (Utility apps)
├── requirements.txt # Dependencies
├── run.bat         # Windows launcher
├── run.sh          # Unix/Linux launcher
└── README.md       # This file
```

## Support

This application was generated automatically. For customization help:

1. Check the inline code comments
2. Refer to the relevant technology documentation
3. Use online resources and tutorials

## Generated Information

- **Generated on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Generator**: MEGA ULTRA App Generator v1.0
- **App Type**: {app_type.replace('_', ' ').title()}
- **Original Command**: {command}

---

**Happy coding!** 🚀

*This project was created using AI-powered app generation technology.*
'''
        
        with open(os.path.join(project_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def log_progress(self, message):
        """Log progress message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\\n"
        
        def update():
            self.progress_text.config(state='normal')
            self.progress_text.insert('end', log_entry)
            self.progress_text.see('end')
            self.progress_text.config(state='disabled')
        
        self.root.after(0, update)
    
    def update_progress(self, value):
        """Update progress bar"""
        def update():
            self.progress_bar['value'] = value
        
        self.root.after(0, update)
    
    def generation_complete(self, app_info):
        """Handle successful generation"""
        self.generate_btn.config(state='normal', text="GENERATE APP")
        self.status_label.config(text="App generated successfully!", fg='#00ff00')
        
        # Add to list
        self.generated_apps.append(app_info)
        self.update_apps_list()
        
        self.log_progress(f"SUCCESS: {app_info['name']} generated!")
        
        messagebox.showinfo(
            "Success!",
            f"Application '{app_info['name']}' generated successfully!\\n\\n"
            f"Location: {app_info['path']}\\n\\n"
            f"You can now run and customize your application."
        )
    
    def generation_error(self, error_message):
        """Handle generation error"""
        self.generate_btn.config(state='normal', text="GENERATE APP")
        self.status_label.config(text="Generation failed!", fg='#ff0000')
        
        self.log_progress(f"ERROR: {error_message}")
        
        messagebox.showerror("Generation Error", f"Failed to generate app:\\n\\n{error_message}")
    
    def update_apps_list(self):
        """Update generated apps list"""
        self.apps_listbox.delete(0, 'end')
        
        for app in self.generated_apps:
            display_text = f"{app['name']} ({app['type']}) - {app['timestamp']}"
            self.apps_listbox.insert('end', display_text)
    
    def run_selected_app(self):
        """Run selected application"""
        selection = self.apps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application!")
            return
        
        app = self.generated_apps[selection[0]]
        app_path = app['path']
        
        try:
            if app['type'] == 'python_app':
                main_py = os.path.join(app_path, 'main.py')
                if os.path.exists(main_py):
                    subprocess.Popen([sys.executable, main_py], cwd=app_path)
                    messagebox.showinfo("Running", f"Started {app['name']}!")
            
            elif app['type'] == 'web_app':
                index_html = os.path.join(app_path, 'index.html')
                if os.path.exists(index_html):
                    import webbrowser
                    webbrowser.open(f'file://{index_html}')
                    messagebox.showinfo("Running", f"Opened {app['name']} in browser!")
            
            elif app['type'] == 'utility_app':
                utility_py = os.path.join(app_path, 'utility.py')
                if os.path.exists(utility_py):
                    subprocess.Popen([sys.executable, utility_py, '--demo'], cwd=app_path)
                    messagebox.showinfo("Running", f"Started {app['name']} demo!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run app: {e}")
    
    def open_app_folder(self):
        """Open application folder"""
        selection = self.apps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application!")
            return
        
        app = self.generated_apps[selection[0]]
        
        try:
            if sys.platform == "win32":
                os.startfile(app['path'])
            else:
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", app['path']])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def delete_selected_app(self):
        """Delete selected application"""
        selection = self.apps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application!")
            return
        
        app = self.generated_apps[selection[0]]
        
        if messagebox.askyesno("Confirm", f"Delete '{app['name']}'?\\n\\nThis will permanently delete all files."):
            try:
                import shutil
                shutil.rmtree(app['path'])
                
                self.generated_apps.pop(selection[0])
                self.update_apps_list()
                
                messagebox.showinfo("Deleted", f"Successfully deleted '{app['name']}'!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MegaUltraAppGenerator()
    app.run()