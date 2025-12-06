#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import threading
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class WealthSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autonomous Wealth System")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.update_stats()
        self.auto_refresh()
    
    def setup_ui(self):
        """Setup UI components"""
        header = tk.Frame(self.root, bg="#1a1a1a", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="AUTONOMOUS WEALTH SYSTEM", 
                        font=("Arial", 16, "bold"), bg="#1a1a1a", fg="#00ff00")
        title.pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats_frame = tk.LabelFrame(main_frame, text="STATISTICS", 
                                   font=("Arial", 10, "bold"), 
                                   bg="#1a1a1a", fg="#00ff00", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_labels = {}
        stats = [
            ("Capital (CHF):", "capital"),
            ("Total Profit (CHF):", "profit"),
            ("Art Assets:", "art"),
            ("Trades:", "trades"),
            ("Active Clones:", "clones"),
            ("Avg Profit/Cycle:", "avg_profit")
        ]
        
        for i, (label, key) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            lbl = tk.Label(stats_frame, text=label, bg="#1a1a1a", fg="#888888")
            lbl.grid(row=row, column=col*2, sticky="w", padx=5, pady=5)
            
            val = tk.Label(stats_frame, text="0.00", bg="#1a1a1a", fg="#00ff00", 
                          font=("Arial", 10, "bold"))
            val.grid(row=row, column=col*2+1, sticky="e", padx=5, pady=5)
            
            self.stats_labels[key] = val
        
        control_frame = tk.LabelFrame(main_frame, text="CONTROLS", 
                                     font=("Arial", 10, "bold"), 
                                     bg="#1a1a1a", fg="#00ff00", padx=10, pady=10)
        control_frame.pack(fill=tk.X, pady=5)
        
        btn_frame = tk.Frame(control_frame, bg="#1a1a1a")
        btn_frame.pack(fill=tk.X)
        
        buttons = [
            ("Start System", self.start_system),
            ("Refresh", self.update_stats),
            ("Export Data", self.export_data),
            ("Config", self.open_config)
        ]
        
        for text, cmd in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd, 
                           bg="#00ff00", fg="#000000", font=("Arial", 9, "bold"),
                           padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
        
        log_frame = tk.LabelFrame(main_frame, text="SYSTEM LOG", 
                                 font=("Arial", 10, "bold"), 
                                 bg="#1a1a1a", fg="#00ff00", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=15, bg="#0a0a0a", fg="#00ff00",
                               yscrollcommand=scrollbar.set, font=("Courier", 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.load_log()
    
    def get_stats(self):
        """Get system statistics"""
        try:
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            
            c.execute("SELECT MAX(balance) FROM transactions")
            capital = c.fetchone()[0] or 0
            
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
            profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trades = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            clones = c.fetchone()[0]
            
            c.execute("SELECT AVG(amount) FROM transactions WHERE type='profit'")
            avg_profit = c.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "capital": capital,
                "profit": profit,
                "art": art,
                "trades": trades,
                "clones": clones,
                "avg_profit": avg_profit
            }
        except:
            return None
    
    def update_stats(self):
        """Update statistics display"""
        stats = self.get_stats()
        if stats:
            self.stats_labels["capital"].config(text=f"{stats['capital']:,.2f}")
            self.stats_labels["profit"].config(text=f"{stats['profit']:,.2f}")
            self.stats_labels["art"].config(text=f"{stats['art']:,}")
            self.stats_labels["trades"].config(text=f"{stats['trades']:,}")
            self.stats_labels["clones"].config(text=f"{stats['clones']}")
            self.stats_labels["avg_profit"].config(text=f"{stats['avg_profit']:,.2f}")
    
    def auto_refresh(self):
        """Auto refresh every 5 seconds"""
        self.update_stats()
        self.root.after(5000, self.auto_refresh)
    
    def load_log(self):
        """Load system log"""
        try:
            with open("system.log", "r") as f:
                lines = f.readlines()
                for line in lines[-30:]:
                    self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
        except:
            pass
    
    def start_system(self):
        """Start production system"""
        threading.Thread(target=lambda: subprocess.Popen([sys.executable, "cash_money_production.py"]), daemon=True).start()
        messagebox.showinfo("Info", "Production system started in background!")
    
    def export_data(self):
        """Export data"""
        threading.Thread(target=lambda: subprocess.run([sys.executable, "export_data.py"]), daemon=True).start()
        messagebox.showinfo("Info", "Data export started!")
    
    def open_config(self):
        """Open config manager"""
        threading.Thread(target=lambda: subprocess.run([sys.executable, "config_manager.py"]), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = WealthSystemApp(root)
    root.mainloop()
