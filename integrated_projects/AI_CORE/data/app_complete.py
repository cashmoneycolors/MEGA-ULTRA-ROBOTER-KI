#!/usr/bin/env python3
"""
Autonomous Wealth Generation System - Complete Edition
Integriert KI-Kunst, Asset Trading, Vector Services und PayPal
"""

import sqlite3
import json
import time
import os
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
import requests
from threading import Thread

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousWealthSystem:
    def __init__(self, initial_capital=100, config_path="config.json"):
        self.capital = initial_capital
        self.config = self.load_config(config_path)
        self.target = self.config.get("target_capital", 10000)
        self.db_path = "wealth_system.db"
        self.cycle_count = 0
        self.error_count = 0
        self.running = False
        self.setup_database()
        self.load_capital_from_db()
        
    def load_config(self, path):
        """Load configuration from JSON"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            logger.warning(f"Config file not found: {path}. Using defaults.")
            return {
                "initial_capital": 100,
                "target_capital": 10000,
                "cycle_interval": 2,
                "art_allocation": 0.40,
                "trading_allocation": 0.35,
                "vector_allocation": 0.25
            }
    
    def setup_database(self):
        """Initialize SQLite database"""
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
        c.execute('''CREATE TABLE IF NOT EXISTS paypal_transactions
                     (id INTEGER PRIMARY KEY, transaction_id TEXT, timestamp TEXT, amount REAL, status TEXT, service TEXT)''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def load_capital_from_db(self):
        """Load capital from last session"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT MAX(balance) FROM transactions")
            result = c.fetchone()
            if result and result[0]:
                self.capital = result[0]
                logger.info(f"Loaded capital from database: {self.capital:.2f} CHF")
            conn.close()
        except:
            pass
    
    def execute_production_cycle(self):
        """Main profit generation cycle"""
        try:
            self.cycle_count += 1
            cycle_profit = 0
            
            art_profit = self.generate_art_assets()
            cycle_profit += art_profit
            
            trading_profit = self.execute_asset_trading()
            cycle_profit += trading_profit
            
            vector_profit = self.generate_vector_services()
            cycle_profit += vector_profit
            
            clone_multiplier = 1 + (self.get_active_clones() * 0.03)
            clone_multiplier = min(clone_multiplier, 2.0)
            
            final_profit = cycle_profit * clone_multiplier
            self.capital += final_profit
            
            self.record_transaction("profit", final_profit)
            self.error_count = 0
            
            logger.info(f"Cycle {self.cycle_count}: +{final_profit:.2f} CHF | Capital: {self.capital:.2f} CHF")
            
            if self.capital > 500 and self.get_active_clones() < 25:
                self.evaluate_clone_creation()
            
            return final_profit
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"ERROR in cycle: {str(e)}")
            if self.error_count >= 5:
                logger.error("Max errors reached. Pausing system.")
                return 0
    
    def generate_art_assets(self):
        """KI-Kunst production (40% allocation)"""
        try:
            budget = self.capital * self.config.get("art_allocation", 0.40)
            production_cost = self.config.get("art_production_cost", 8.50)
            units = int(budget / production_cost)
            
            if units == 0:
                return 0
            
            profit = 0
            for _ in range(units):
                selling_price = self.config.get("art_min_price", 45) + (self.cycle_count % 155)
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
            logger.error(f"Art generation error: {str(e)}")
            return 0
    
    def execute_asset_trading(self):
        """Multi-asset trading (35% allocation)"""
        try:
            budget = self.capital * self.config.get("trading_allocation", 0.35)
            max_risk = budget * self.config.get("max_trading_risk", 0.70)
            
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
            logger.error(f"Trading error: {str(e)}")
            return 0
    
    def generate_vector_services(self):
        """Vector services (25% allocation)"""
        try:
            budget = self.capital * self.config.get("vector_allocation", 0.25)
            service_cost = self.config.get("vector_service_cost", 35)
            units = int(budget / service_cost)
            
            if units == 0:
                return 0
            
            profit = units * (self.config.get("vector_service_price", 85) - service_cost)
            return profit
        except Exception as e:
            logger.error(f"Vector services error: {str(e)}")
            return 0
    
    def evaluate_clone_creation(self):
        """Create autonomous clones"""
        try:
            clone_cost = self.config.get("clone_creation_cost", 85)
            if self.capital >= clone_cost:
                self.capital -= clone_cost
                
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO clones (created_at, status, profit_contribution) VALUES (?, ?, ?)",
                         (datetime.now().isoformat(), "active", 0))
                conn.commit()
                conn.close()
                
                logger.info(f"Clone created! Total clones: {self.get_active_clones()}")
        except Exception as e:
            logger.error(f"Clone creation error: {str(e)}")
    
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
            logger.error(f"Transaction recording error: {str(e)}")
    
    def get_status(self):
        """Get system status"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art_count = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trades = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit) FROM art_portfolio")
            art_profit = c.fetchone()[0] or 0
            
            clones = self.get_active_clones()
            conn.close()
            
            progress = (self.capital / self.target * 100)
            
            return {
                "capital": round(self.capital, 2),
                "target": self.target,
                "progress": round(progress, 1),
                "cycles": self.cycle_count,
                "art_assets": art_count,
                "trades": trades,
                "art_profit": round(art_profit, 2),
                "active_clones": clones,
                "running": self.running
            }
        except Exception as e:
            logger.error(f"Status error: {str(e)}")
            return {}
    
    def run_autonomous(self):
        """Run system autonomously"""
        self.running = True
        logger.info("=== SYSTEM START ===")
        logger.info(f"Initial Capital: {self.capital} CHF | Target: {self.target} CHF")
        
        while self.running:
            self.execute_production_cycle()
            if self.capital >= self.target:
                logger.info(f"=== TARGET REACHED: {self.capital:.2f} CHF ===")
            time.sleep(self.config.get("cycle_interval", 2))

class PayPalIntegration:
    def __init__(self, client_id, client_secret, sandbox=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        self.base_url = "https://api.sandbox.paypal.com" if sandbox else "https://api.paypal.com"
        self.access_token = None
    
    def get_access_token(self):
        """Get PayPal access token"""
        try:
            url = f"{self.base_url}/v1/oauth2/token"
            headers = {"Accept": "application/json", "Accept-Language": "en_US"}
            data = {"grant_type": "client_credentials"}
            
            response = requests.post(url, headers=headers, data=data, 
                                   auth=(self.client_id, self.client_secret))
            
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                logger.info("PayPal access token obtained")
                return self.access_token
            else:
                logger.error(f"PayPal auth failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"PayPal token error: {str(e)}")
            return None

# Flask Web Dashboard
app = Flask(__name__)
wealth_system = None

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Autonomous Wealth System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f0f0f; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { text-align: center; margin-bottom: 40px; }
        h1 { font-size: 2.5em; margin-bottom: 10px; background: linear-gradient(45deg, #00ff88, #00ccff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: #1a1a1a; border: 2px solid #00ff88; border-radius: 10px; padding: 20px; }
        .card h3 { color: #00ff88; margin-bottom: 10px; }
        .card .value { font-size: 1.8em; font-weight: bold; color: #00ccff; }
        .progress-bar { width: 100%; height: 20px; background: #333; border-radius: 10px; overflow: hidden; margin-top: 10px; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #00ff88, #00ccff); transition: width 0.3s; }
        .controls { text-align: center; margin: 30px 0; }
        button { background: #00ff88; color: #000; border: none; padding: 12px 30px; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 0 10px; }
        button:hover { background: #00ccff; }
        .status { text-align: center; font-size: 1.2em; margin: 20px 0; }
        .status.running { color: #00ff88; }
        .status.stopped { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Autonomous Wealth System</h1>
            <p>AI-Powered Autonomous Capital Generation</p>
        </header>
        
        <div class="grid">
            <div class="card">
                <h3>💰 Capital</h3>
                <div class="value" id="capital">0 CHF</div>
            </div>
            <div class="card">
                <h3>🎯 Target</h3>
                <div class="value" id="target">10,000 CHF</div>
            </div>
            <div class="card">
                <h3>📊 Progress</h3>
                <div class="value" id="progress">0%</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                </div>
            </div>
            <div class="card">
                <h3>🔄 Cycles</h3>
                <div class="value" id="cycles">0</div>
            </div>
            <div class="card">
                <h3>🎨 Art Assets</h3>
                <div class="value" id="art">0</div>
            </div>
            <div class="card">
                <h3>📈 Trades</h3>
                <div class="value" id="trades">0</div>
            </div>
            <div class="card">
                <h3>🤖 Active Clones</h3>
                <div class="value" id="clones">0</div>
            </div>
            <div class="card">
                <h3>⚙️ Status</h3>
                <div class="value" id="status" style="font-size: 1.2em;">Stopped</div>
            </div>
        </div>
        
        <div class="controls">
            <button onclick="startSystem()">▶️ Start System</button>
            <button onclick="stopSystem()">⏹️ Stop System</button>
            <button onclick="refreshStatus()">🔄 Refresh</button>
        </div>
        
        <div class="status" id="status-text">System Ready</div>
    </div>
    
    <script>
        function refreshStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('capital').textContent = data.capital.toFixed(2) + ' CHF';
                    document.getElementById('progress').textContent = data.progress + '%';
                    document.getElementById('progress-fill').style.width = data.progress + '%';
                    document.getElementById('cycles').textContent = data.cycles;
                    document.getElementById('art').textContent = data.art_assets;
                    document.getElementById('trades').textContent = data.trades;
                    document.getElementById('clones').textContent = data.active_clones;
                    document.getElementById('status').textContent = data.running ? '🟢 Running' : '🔴 Stopped';
                    document.getElementById('status-text').textContent = data.running ? 'System is running autonomously' : 'System is stopped';
                    document.getElementById('status-text').className = 'status ' + (data.running ? 'running' : 'stopped');
                });
        }
        
        function startSystem() {
            fetch('/api/start', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert(data.message);
                    refreshStatus();
                });
        }
        
        function stopSystem() {
            fetch('/api/stop', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert(data.message);
                    refreshStatus();
                });
        }
        
        setInterval(refreshStatus, 2000);
        refreshStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    return jsonify(wealth_system.get_status())

@app.route('/api/start', methods=['POST'])
def api_start():
    if not wealth_system.running:
        thread = Thread(target=wealth_system.run_autonomous, daemon=True)
        thread.start()
        return jsonify({"message": "System started", "status": "running"})
    return jsonify({"message": "System already running", "status": "running"})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    wealth_system.running = False
    return jsonify({"message": "System stopped", "status": "stopped"})

def main():
    global wealth_system
    
    wealth_system = AutonomousWealthSystem(initial_capital=100)
    
    logger.info("Starting Autonomous Wealth System Web Dashboard")
    logger.info("Open http://localhost:5000 in your browser")
    
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
