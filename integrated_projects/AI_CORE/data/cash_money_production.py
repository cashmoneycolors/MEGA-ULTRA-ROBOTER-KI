import sqlite3
import json
import time
import os
from datetime import datetime
from pathlib import Path

class AutonomousWealthSystem:
    def __init__(self, initial_capital=100):
        self.capital = initial_capital
        self.target = 10000
        self.db_path = "wealth_system.db"
        self.log_path = "system.log"
        self.setup_database()
        self.cycle_count = 0
        self.error_count = 0
        
    def setup_database(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, amount REAL, balance REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS art_portfolio
                     (id INTEGER PRIMARY KEY, timestamp TEXT, cost REAL, selling_price REAL, profit REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS trading_log
                     (id INTEGER PRIMARY KEY, timestamp TEXT, asset TEXT, action TEXT, amount REAL, price REAL, profit REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS clones
                     (id INTEGER PRIMARY KEY, created_at TEXT, status TEXT, profit_contribution REAL)''')
        
        conn.commit()
        conn.close()
        self.log("Database initialized")
    
    def log(self, message):
        """Log system events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_path, "a") as f:
            f.write(log_msg + "\n")
    
    def execute_production_cycle(self):
        """Main profit generation cycle"""
        try:
            self.cycle_count += 1
            cycle_profit = 0
            
            # 40% Art Production
            art_profit = self.generate_art_assets()
            cycle_profit += art_profit
            
            # 35% Trading
            trading_profit = self.execute_asset_trading()
            cycle_profit += trading_profit
            
            # 25% Vector Services
            vector_profit = self.generate_vector_services()
            cycle_profit += vector_profit
            
            # Apply clone multiplier
            clone_multiplier = 1 + (self.get_active_clones() * 0.03)
            clone_multiplier = min(clone_multiplier, 2.0)
            
            final_profit = cycle_profit * clone_multiplier
            self.capital += final_profit
            
            self.record_transaction("profit", final_profit)
            self.error_count = 0
            
            self.log(f"Cycle {self.cycle_count}: +{final_profit:.2f} CHF | Capital: {self.capital:.2f} CHF")
            
            # Check clone creation
            if self.capital > 500 and self.get_active_clones() < 25:
                self.evaluate_clone_creation()
            
            return final_profit
            
        except Exception as e:
            self.error_count += 1
            self.log(f"ERROR in cycle: {str(e)}")
            if self.error_count >= 5:
                self.log("Max errors reached. Pausing system.")
                return 0
    
    def generate_art_assets(self):
        """KI-Kunst production (40% allocation)"""
        try:
            budget = self.capital * 0.40
            production_cost = 8.50
            units = int(budget / production_cost)
            
            if units == 0:
                return 0
            
            profit = 0
            for _ in range(units):
                selling_price = 45 + (self.cycle_count % 155)
                item_profit = selling_price - production_cost
                profit += item_profit
                
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO art_portfolio (timestamp, cost, selling_price, profit) VALUES (?, ?, ?, ?)",
                         (datetime.now().isoformat(), production_cost, selling_price, item_profit))
                conn.commit()
                conn.close()
            
            return profit
        except Exception as e:
            self.log(f"Art generation error: {str(e)}")
            return 0
    
    def execute_asset_trading(self):
        """Multi-asset trading (35% allocation)"""
        try:
            budget = self.capital * 0.35
            max_risk = budget * 0.70
            
            assets = ["BTC", "ETH", "Gold", "Silver"]
            profit = 0
            
            for asset in assets:
                trade_amount = max_risk / len(assets)
                price_change = (self.cycle_count % 10) - 3
                trade_profit = trade_amount * (price_change / 100)
                profit += trade_profit
                
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO trading_log (timestamp, asset, action, amount, price, profit) VALUES (?, ?, ?, ?, ?, ?)",
                         (datetime.now().isoformat(), asset, "BUY/SELL", trade_amount, price_change, trade_profit))
                conn.commit()
                conn.close()
            
            return max(profit, 0)
        except Exception as e:
            self.log(f"Trading error: {str(e)}")
            return 0
    
    def generate_vector_services(self):
        """Vector services (25% allocation)"""
        try:
            budget = self.capital * 0.25
            service_cost = 35
            units = int(budget / service_cost)
            
            if units == 0:
                return 0
            
            profit = units * (85 - service_cost)
            return profit
        except Exception as e:
            self.log(f"Vector services error: {str(e)}")
            return 0
    
    def evaluate_clone_creation(self):
        """Create autonomous clones when conditions met"""
        try:
            clone_cost = 85
            if self.capital >= clone_cost:
                self.capital -= clone_cost
                
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO clones (created_at, status, profit_contribution) VALUES (?, ?, ?)",
                         (datetime.now().isoformat(), "active", 0))
                conn.commit()
                conn.close()
                
                self.log(f"Clone created! Total clones: {self.get_active_clones()}")
        except Exception as e:
            self.log(f"Clone creation error: {str(e)}")
    
    def get_active_clones(self):
        """Get number of active clones"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def record_transaction(self, trans_type, amount):
        """Record financial transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO transactions (timestamp, type, amount, balance) VALUES (?, ?, ?, ?)",
                     (datetime.now().isoformat(), trans_type, amount, self.capital))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"Transaction recording error: {str(e)}")
    
    def generate_report(self):
        """Generate system status report"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art_count = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trades = c.fetchone()[0]
            
            clones = self.get_active_clones()
            
            conn.close()
            
            progress = (self.capital/self.target*100)
            report = f"""\n=== AUTONOMOUS WEALTH SYSTEM REPORT ===
Capital:        {self.capital:.2f} CHF
Target:         {self.target:.2f} CHF
Progress:       {progress:.1f}%
Cycles:         {self.cycle_count}
Art Assets:     {art_count}
Trades:         {trades}
Active Clones:  {clones}
========================================\n"""
            return report
        except Exception as e:
            self.log(f"Report generation error: {str(e)}")
            return "Report generation failed"
    
    def run(self):
        """Main execution loop"""
        self.log("=== SYSTEM START ===")
        self.log(f"Initial Capital: {self.capital} CHF | Target: {self.target} CHF")
        
        while self.capital < self.target:
            self.execute_production_cycle()
            print(self.generate_report())
            time.sleep(2)  # 2 seconds between cycles for testing
        
        self.log(f"=== TARGET REACHED: {self.capital:.2f} CHF ===")
        print(self.generate_report())

if __name__ == "__main__":
    system = AutonomousWealthSystem(initial_capital=100)
    system.run()
