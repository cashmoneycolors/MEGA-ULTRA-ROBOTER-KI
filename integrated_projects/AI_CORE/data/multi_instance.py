import sqlite3
import json
import os
from datetime import datetime
from cash_money_production import AutonomousWealthSystem

class MultiInstanceManager:
    def __init__(self, num_instances=3):
        self.num_instances = num_instances
        self.instances = []
        self.master_db = "master_wealth_system.db"
        self.setup_master_db()
    
    def setup_master_db(self):
        """Setup master database for aggregation"""
        try:
            conn = sqlite3.connect(self.master_db)
            c = conn.cursor()
            
            c.execute('''CREATE TABLE IF NOT EXISTS instance_stats
                         (id INTEGER PRIMARY KEY, instance_id INTEGER, timestamp TEXT, capital REAL, cycles INTEGER)''')
            c.execute('''CREATE TABLE IF NOT EXISTS aggregated_profit
                         (id INTEGER PRIMARY KEY, timestamp TEXT, total_profit REAL, num_instances INTEGER)''')
            
            conn.commit()
            conn.close()
            print("Master database initialized")
        except Exception as e:
            print(f"Master DB error: {str(e)}")
    
    def create_instance(self, instance_id, initial_capital=100):
        """Create new system instance"""
        try:
            db_path = f"wealth_system_instance_{instance_id}.db"
            system = AutonomousWealthSystem(initial_capital=initial_capital)
            system.db_path = db_path
            
            self.instances.append({
                "id": instance_id,
                "system": system,
                "db_path": db_path,
                "created_at": datetime.now().isoformat()
            })
            
            print(f"Instance {instance_id} created")
            return system
        except Exception as e:
            print(f"Instance creation error: {str(e)}")
            return None
    
    def initialize_all_instances(self):
        """Initialize all instances"""
        for i in range(self.num_instances):
            self.create_instance(i, initial_capital=100)
    
    def execute_all_cycles(self):
        """Execute cycle on all instances"""
        try:
            total_profit = 0
            for instance in self.instances:
                profit = instance["system"].execute_production_cycle()
                total_profit += profit
            
            self.record_aggregated_profit(total_profit)
            return total_profit
        except Exception as e:
            print(f"Cycle execution error: {str(e)}")
            return 0
    
    def record_aggregated_profit(self, total_profit):
        """Record aggregated profit"""
        try:
            conn = sqlite3.connect(self.master_db)
            c = conn.cursor()
            
            c.execute("INSERT INTO aggregated_profit (timestamp, total_profit, num_instances) VALUES (?, ?, ?)",
                     (datetime.now().isoformat(), total_profit, len(self.instances)))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Recording error: {str(e)}")
    
    def get_instance_stats(self):
        """Get stats for all instances"""
        try:
            stats = []
            for instance in self.instances:
                stat = {
                    "id": instance["id"],
                    "capital": instance["system"].capital,
                    "cycles": instance["system"].cycle_count,
                    "clones": instance["system"].get_active_clones()
                }
                stats.append(stat)
            
            return stats
        except Exception as e:
            print(f"Stats error: {str(e)}")
            return []
    
    def get_total_capital(self):
        """Get total capital across all instances"""
        total = sum(instance["system"].capital for instance in self.instances)
        return total
    
    def get_aggregated_report(self):
        """Get aggregated report"""
        try:
            stats = self.get_instance_stats()
            total_capital = self.get_total_capital()
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "num_instances": len(self.instances),
                "total_capital": total_capital,
                "instances": stats
            }
            
            return report
        except Exception as e:
            print(f"Report error: {str(e)}")
            return {}
    
    def export_aggregated_report(self, filename="aggregated_report.json"):
        """Export aggregated report"""
        try:
            report = self.get_aggregated_report()
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Aggregated report: {filename}")
            return filename
        except Exception as e:
            print(f"Export error: {str(e)}")
            return None
    
    def run_multi_instance(self, cycles=10):
        """Run multi-instance system"""
        print(f"=== MULTI-INSTANCE SYSTEM ({self.num_instances} instances) ===")
        self.initialize_all_instances()
        
        for cycle in range(cycles):
            total_profit = self.execute_all_cycles()
            report = self.get_aggregated_report()
            print(f"Cycle {cycle+1}: Total profit: {total_profit:.2f} CHF | Total capital: {report['total_capital']:.2f} CHF")

if __name__ == "__main__":
    manager = MultiInstanceManager(num_instances=3)
    manager.run_multi_instance(cycles=5)
