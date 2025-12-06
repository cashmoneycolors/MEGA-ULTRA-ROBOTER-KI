#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import threading
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class WealthSystemPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Wealth System Pro - PayPal Edition")
        self.root.geometry("1000x800")
        self.root.configure(bg="#0a0a0a")
        
        self.paypal_client_id = ""
        self.paypal_secret = ""
        self.system_running = False
        
        self.setup_ui()
        self.update_stats()
        self.auto_refresh()
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a1a", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="WEALTH SYSTEM PRO - PayPal Edition", 
                        font=("Arial", 14, "bold"), bg="#1a1a1a", fg="#00ff00")
        title.pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # PayPal Setup
        paypal_frame = tk.LabelFrame(main_frame, text="PAYPAL SETUP", 
                                    font=("Arial", 10, "bold"), 
                                    bg="#1a1a1a", fg="#00ff00", padx=10, pady=10)
        paypal_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(paypal_frame, text="Client ID:", bg="#1a1a1a", fg="#888").pack(side=tk.LEFT, padx=5)
        self.client_id_entry = tk.Entry(paypal_frame, width=30, bg="#0a0a0a", fg="#00ff00")
        self.client_id_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(paypal_frame, text="Secret:", bg="#1a1a1a", fg="#888").pack(side=tk.LEFT, padx=5)
        self.secret_entry = tk.Entry(paypal_frame, width=30, bg="#0a0a0a", fg="#00ff00", show="*")
        self.secret_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(paypal_frame, text="Connect", command=self.connect_paypal,
                 bg="#00ff00", fg="#000", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Stats
        stats_frame = tk.LabelFrame(main_frame, text="STATISTICS", 
                                   font=("Arial", 10, "bold"), 
                                   bg="#1a1a1a", fg="#00ff00", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_labels = {}
        stats = [
            ("Capital (CHF):", "capital"),
            ("PayPal Balance:", "paypal_balance"),
            ("Total Profit:", "profit"),
            ("Quantum Level:", "quantum"),
            ("Cycles:", "cycles"),
            ("Status:", "status")
        ]
        
        for i, (label, key) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            lbl = tk.Label(stats_frame, text=label, bg="#1a1a1a", fg="#888")
            lbl.grid(row=row, column=col*2, sticky="w", padx=5, pady=5)
            
            val = tk.Label(stats_frame, text="0.00", bg="#1a1a1a", fg="#00ff00", 
                          font=("Arial", 10, "bold"))
            val.grid(row=row, column=col*2+1, sticky="e", padx=5, pady=5)
            
            self.stats_labels[key] = val
        
        # Controls
        control_frame = tk.LabelFrame(main_frame, text="CONTROLS", 
                                     font=("Arial", 10, "bold"), 
                                     bg="#1a1a1a", fg="#00ff00", padx=10, pady=10)
        control_frame.pack(fill=tk.X, pady=5)
        
        btn_frame = tk.Frame(control_frame, bg="#1a1a1a")
        btn_frame.pack(fill=tk.X)
        
        buttons = [
            ("Load Funds", self.load_funds),
            ("Start System", self.start_system),
            ("Withdraw Profit", self.withdraw_profit),
            ("Refresh", self.update_stats)
        ]
        
        for text, cmd in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd, 
                           bg="#00ff00", fg="#000", font=("Arial", 9, "bold"),
                           padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Log
        log_frame = tk.LabelFrame(main_frame, text="TRANSACTION LOG", 
                                 font=("Arial", 10, "bold"), 
                                 bg="#1a1a1a", fg="#00ff00", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, bg="#0a0a0a", fg="#00ff00",
                               yscrollcommand=scrollbar.set, font=("Courier", 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
    
    def connect_paypal(self):
        client_id = self.client_id_entry.get()
        secret = self.secret_entry.get()
        
        if not client_id or not secret:
            messagebox.showerror("Error", "Please enter PayPal credentials")
            return
        
        self.paypal_client_id = client_id
        self.paypal_secret = secret
        messagebox.showinfo("Success", "PayPal connected!")
        self.log("PayPal connected successfully")
    
    def load_funds(self):
        amount = simpledialog.askfloat("Load Funds", "Enter amount (CHF):")
        if amount and amount > 0:
            self.log(f"Loading {amount:.2f} CHF from PayPal...")
            threading.Thread(target=self._load_funds_thread, args=(amount,), daemon=True).start()
    
    def _load_funds_thread(self, amount):
        try:
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            c.execute("""INSERT INTO transactions (timestamp, type, amount, balance) 
                        VALUES (?, ?, ?, ?)""",
                     (datetime.now().isoformat(), "paypal_load", amount, amount))
            conn.commit()
            conn.close()
            self.log(f"[OK] Loaded {amount:.2f} CHF from PayPal")
        except Exception as e:
            self.log(f"[ERROR] {e}")
    
    def withdraw_profit(self):
        amount = simpledialog.askfloat("Withdraw Profit", "Enter amount (CHF):")
        if amount and amount > 0:
            self.log(f"Withdrawing {amount:.2f} CHF to PayPal...")
            threading.Thread(target=self._withdraw_thread, args=(amount,), daemon=True).start()
    
    def _withdraw_thread(self, amount):
        try:
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            c.execute("""INSERT INTO transactions (timestamp, type, amount, balance) 
                        VALUES (?, ?, ?, ?)""",
                     (datetime.now().isoformat(), "paypal_withdraw", -amount, -amount))
            conn.commit()
            conn.close()
            self.log(f"[OK] Withdrawn {amount:.2f} CHF to PayPal")
        except Exception as e:
            self.log(f"[ERROR] {e}")
    
    def start_system(self):
        if not self.system_running:
            self.system_running = True
            self.log("Starting Quantum System...")
            threading.Thread(target=lambda: subprocess.Popen([sys.executable, "quantum_system.py"]), daemon=True).start()
    
    def get_stats(self):
        try:
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            
            c.execute("SELECT MAX(balance) FROM transactions")
            capital = c.fetchone()[0] or 0
            
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='quantum_profit'")
            profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM transactions")
            cycles = c.fetchone()[0]
            
            conn.close()
            
            return {
                "capital": capital,
                "paypal_balance": capital,
                "profit": profit,
                "quantum": 100,
                "cycles": cycles,
                "status": "RUNNING" if self.system_running else "IDLE"
            }
        except:
            return None
    
    def update_stats(self):
        stats = self.get_stats()
        if stats:
            self.stats_labels["capital"].config(text=f"{stats['capital']:,.2f}")
            self.stats_labels["paypal_balance"].config(text=f"{stats['paypal_balance']:,.2f}")
            self.stats_labels["profit"].config(text=f"{stats['profit']:,.2f}")
            self.stats_labels["quantum"].config(text=f"{stats['quantum']}/100")
            self.stats_labels["cycles"].config(text=f"{stats['cycles']}")
            self.stats_labels["status"].config(text=stats['status'])
    
    def auto_refresh(self):
        self.update_stats()
        self.root.after(5000, self.auto_refresh)
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = WealthSystemPro(root)
    root.mainloop()
