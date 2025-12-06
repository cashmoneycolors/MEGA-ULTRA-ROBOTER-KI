"""
Enhanced Autonomous Wealth Generation System with PayPal Business Integration
Combines simulated profit generation with real payment processing
"""

import sqlite3
import json
import time
import os
from datetime import datetime
from pathlib import Path

# Import PayPal integration
try:
    from paypal_integration import PayPalBusinessManager
    PAYPAL_AVAILABLE = True
except ImportError:
    PAYPAL_AVAILABLE = False
    print("PayPal integration not available")

class EnhancedWealthSystem:
    def __init__(self, initial_capital=100, enable_payments=True):
        self.capital = initial_capital
        self.target = 10000
        self.db_path = "wealth_system.db"
        self.log_path = "system.log"
        self.config_path = "config.json"
        self.enable_payments = enable_payments
        self.paypal_manager = None
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize PayPal if enabled
        if self.enable_payments and PAYPAL_AVAILABLE:
            self.paypal_manager = PayPalBusinessManager(self.config_path)
            if self.paypal_manager.paypal_client:
                self.log("PayPal integration initialized successfully")
            else:
                self.log("PayPal integration failed - continuing without payments")
        
        self.setup_database()
        self.cycle_count = 0
        self.error_count = 0
        self.payment_history = []
        
    def load_config(self):
        """Load system configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Config loading error: {str(e)}")
            return {}
    
    def setup_database(self):
        """Initialize SQLite database with enhanced schema"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Original tables
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, amount REAL, balance REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS art_portfolio
                     (id INTEGER PRIMARY KEY, timestamp TEXT, cost REAL, selling_price REAL, profit REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS trading_log
                     (id INTEGER PRIMARY KEY, timestamp TEXT, asset TEXT, action TEXT, amount REAL, price REAL, profit REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS clones
                     (id INTEGER PRIMARY KEY, created_at TEXT, status TEXT, profit_contribution REAL)''')
        
        # New PayPal payment tables
        c.execute('''CREATE TABLE IF NOT EXISTS paypal_payments
                     (id INTEGER PRIMARY KEY, order_id TEXT UNIQUE, service_type TEXT, amount REAL, 
                      currency TEXT, status TEXT, created_at TEXT, captured_at TEXT, customer_id TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS payment_transactions
                     (id INTEGER PRIMARY KEY, payment_id INTEGER, transaction_type TEXT, 
                      amount REAL, currency TEXT, paypal_transaction_id TEXT, timestamp TEXT,
                      FOREIGN KEY (payment_id) REFERENCES paypal_payments (id))''')
        
        conn.commit()
        conn.close()
        self.log("Enhanced database initialized with PayPal support")
    
    def log(self, message):
        """Log system events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_path, "a") as f:
            f.write(log_msg + "\n")
    
    def execute_production_cycle(self):
        """Main profit generation cycle with optional payments"""
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
            
            # Offer payment processing for services
            if self.enable_payments and self.paypal_manager:
                self.process_service_payments()
            
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
        """Enhanced art production with payment integration"""
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
        """Enhanced trading with payment integration"""
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
        """Enhanced vector services with payment integration"""
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
    
    def process_service_payments(self):
        """Process PayPal payments for services"""
        if not self.paypal_manager or not self.config.get('paypal', {}).get('enable_payments'):
            return
        
        try:
            paypal_config = self.config.get('paypal', {})
            services = paypal_config.get('services', {})
            
            # Process payments for enabled services
            for service_type, service_config in services.items():
                if service_config.get('enabled'):
                    self.process_single_service_payment(service_type, service_config)
                    
        except Exception as e:
            self.log(f"Service payment processing error: {str(e)}")
    
    def process_single_service_payment(self, service_type, service_config):
        """Process payment for a single service"""
        try:
            price_usd = service_config.get('price_usd', 0)
            if price_usd <= 0:
                return
            
            # Create PayPal order for this service
            result = self.paypal_manager.process_wealth_system_payment(
                service_type=service_type,
                amount=price_usd,
                customer_info={"system_cycle": self.cycle_count}
            )
            
            if 'error' not in result:
                # Store payment in database
                self.store_paypal_payment(
                    order_id=result['order_id'],
                    service_type=service_type,
                    amount=price_usd,
                    currency=result['currency']
                )
                self.log(f"PayPal payment initiated for {service_type}: ${price_usd}")
            
        except Exception as e:
            self.log(f"Single service payment error: {str(e)}")
    
    def store_paypal_payment(self, order_id, service_type, amount, currency):
        """Store PayPal payment in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""INSERT INTO paypal_payments 
                        (order_id, service_type, amount, currency, status, created_at) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                     (order_id, service_type, amount, currency, "CREATED", datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"PayPal payment storage error: {str(e)}")
    
    def capture_paypal_payment(self, order_id):
        """Capture completed PayPal payment"""
        try:
            if not self.paypal_manager:
                return {"error": "PayPal manager not available"}
            
            result = self.paypal_manager.capture_order(order_id)
            
            if 'error' not in result:
                # Update payment status in database
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("""UPDATE paypal_payments 
                            SET status = ?, captured_at = ? 
                            WHERE order_id = ?""",
                         ("CAPTURED", datetime.now().isoformat(), order_id))
                conn.commit()
                conn.close()
                
                self.log(f"PayPal payment captured: {order_id}")
                return {"success": True, "capture_id": result["capture_id"]}
            
            return result
            
        except Exception as e:
            self.log(f"Payment capture error: {str(e)}")
            return {"error": str(e)}
    
    def get_payment_statistics(self):
        """Get payment processing statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Get payment counts and amounts
            c.execute("SELECT COUNT(*), SUM(amount) FROM paypal_payments WHERE status = 'CAPTURED'")
            captured_stats = c.fetchone()
            
            c.execute("SELECT COUNT(*), SUM(amount) FROM paypal_payments WHERE status = 'CREATED'")
            pending_stats = c.fetchone()
            
            # Get service breakdown
            c.execute("""SELECT service_type, COUNT(*), SUM(amount) 
                        FROM paypal_payments 
                        WHERE status = 'CAPTURED' 
                        GROUP BY service_type""")
            service_stats = c.fetchall()
            
            conn.close()
            
            return {
                "captured_payments": captured_stats[0] or 0,
                "captured_amount": captured_stats[1] or 0,
                "pending_payments": pending_stats[0] or 0,
                "pending_amount": pending_stats[1] or 0,
                "service_breakdown": service_stats
            }
            
        except Exception as e:
            self.log(f"Payment statistics error: {str(e)}")
            return {}
    
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
        """Generate enhanced system status report"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art_count = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trades = c.fetchone()[0]
            
            clones = self.get_active_clones()
            
            conn.close()
            
            # Get payment statistics
            payment_stats = self.get_payment_statistics()
            
            progress = (self.capital/self.target*100)
            
            report = f"""\n=== ENHANCED WEALTH SYSTEM REPORT ===
Capital:        {self.capital:.2f} CHF
Target:         {self.target:.2f} CHF
Progress:       {progress:.1f}%
Cycles:         {self.cycle_count}
Art Assets:     {art_count}
Trades:         {trades}
Active Clones:  {clones}

--- PAYPAL PAYMENTS ---
Captured:       {payment_stats.get('captured_payments', 0)} payments
Captured Amt:   ${payment_stats.get('captured_amount', 0):.2f} USD
Pending:        {payment_stats.get('pending_payments', 0)} payments
Pending Amt:    ${payment_stats.get('pending_amount', 0):.2f} USD
====================================\n"""
            
            return report
        except Exception as e:
            self.log(f"Report generation error: {str(e)}")
            return "Report generation failed"
    
    def run(self):
        """Main execution loop with payment processing"""
        self.log("=== ENHANCED SYSTEM START ===")
        self.log(f"Initial Capital: {self.capital} CHF | Target: {self.target} CHF")
        
        if self.enable_payments:
            self.log("PayPal payment processing: ENABLED")
        else:
            self.log("PayPal payment processing: DISABLED")
        
        while self.capital < self.target:
            self.execute_production_cycle()
            print(self.generate_report())
            time.sleep(2)  # 2 seconds between cycles for testing
        
        self.log(f"=== TARGET REACHED: {self.capital:.2f} CHF ===")
        print(self.generate_report())

if __name__ == "__main__":
    # Initialize enhanced system with PayPal integration
    system = EnhancedWealthSystem(initial_capital=100, enable_payments=True)
    system.run()