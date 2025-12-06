#!/usr/bin/env python3
import os
import sqlite3
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class QuickWealthSystem:
    def __init__(self):
        self.capital = 100
        self.target = 10000
        self.db = "wealth_system.db"
        self.cycle = 0
        self.setup_db()
    
    def setup_db(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, amount REAL, balance REAL)''')
        conn.commit()
        conn.close()
    
    def get_btc_price(self):
        try:
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=chf")
            return r.json()["bitcoin"]["chf"]
        except:
            return 50000
    
    def cycle_run(self):
        self.cycle += 1
        
        # 40% Art
        art = self.capital * 0.40 * 5
        
        # 35% Crypto
        btc_price = self.get_btc_price()
        crypto = self.capital * 0.35 * (btc_price / 50000)
        
        # 25% Services
        services = self.capital * 0.25 * 2
        
        profit = art + crypto + services
        self.capital += profit
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?)",
                 (datetime.now().isoformat(), "profit", profit, self.capital))
        conn.commit()
        conn.close()
        
        print(f"Cycle {self.cycle}: +{profit:.2f} CHF | Total: {self.capital:.2f} CHF | {(self.capital/self.target*100):.1f}%")
        
        return profit
    
    def run(self):
        print(f"Start: {self.capital} CHF → Target: {self.target} CHF\n")
        while self.capital < self.target:
            self.cycle_run()
            time.sleep(1)
        print(f"\n✓ TARGET REACHED: {self.capital:.2f} CHF")

if __name__ == "__main__":
    system = QuickWealthSystem()
    system.run()
