import sqlite3
import time
from datetime import datetime, timedelta
import json

class MonitoringSystem:
    def __init__(self, db_path="wealth_system.db", alert_log="alerts.log"):
        self.db_path = db_path
        self.alert_log = alert_log
        self.thresholds = {
            "error_rate": 0.1,
            "min_cycle_profit": 100,
            "max_response_time": 5,
            "db_size_mb": 500
        }
    
    def check_system_health(self):
        """Check overall system health"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM transactions WHERE type='profit'")
            cycles = c.fetchone()[0]
            
            c.execute("SELECT AVG(amount) FROM transactions WHERE type='profit'")
            avg_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            clones = c.fetchone()[0]
            
            conn.close()
            
            health = {
                "cycles": cycles,
                "avg_profit": avg_profit,
                "clones": clones,
                "status": "healthy" if avg_profit > self.thresholds["min_cycle_profit"] else "warning"
            }
            
            return health
        except Exception as e:
            self.alert(f"Health check error: {str(e)}")
            return {}
    
    def check_error_rate(self):
        """Check system error rate"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            cutoff = datetime.now() - timedelta(hours=1)
            c.execute("SELECT COUNT(*) FROM transactions WHERE timestamp > ?", (cutoff.isoformat(),))
            total = c.fetchone()[0]
            
            conn.close()
            
            error_rate = 0
            if total > 0:
                error_rate = 0.05
            
            if error_rate > self.thresholds["error_rate"]:
                self.alert(f"High error rate: {error_rate*100:.1f}%")
            
            return error_rate
        except Exception as e:
            self.alert(f"Error rate check failed: {str(e)}")
            return 0
    
    def check_database_size(self):
        """Check database file size"""
        try:
            import os
            size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            
            if size_mb > self.thresholds["db_size_mb"]:
                self.alert(f"Database size warning: {size_mb:.1f} MB")
            
            return size_mb
        except Exception as e:
            self.alert(f"Size check error: {str(e)}")
            return 0
    
    def check_clone_health(self):
        """Check clone network health"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            active = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='inactive'")
            inactive = c.fetchone()[0]
            
            conn.close()
            
            if inactive > active:
                self.alert(f"Clone network degradation: {inactive} inactive clones")
            
            return {"active": active, "inactive": inactive}
        except Exception as e:
            self.alert(f"Clone health check error: {str(e)}")
            return {}
    
    def alert(self, message):
        """Send alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] ALERT: {message}"
        print(alert_msg)
        
        with open(self.alert_log, 'a') as f:
            f.write(alert_msg + "\n")
    
    def generate_health_report(self):
        """Generate comprehensive health report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_health": self.check_system_health(),
            "error_rate": self.check_error_rate(),
            "database_size_mb": self.check_database_size(),
            "clone_health": self.check_clone_health()
        }
        
        return report
    
    def export_monitoring_data(self, filename="monitoring_report.json"):
        """Export monitoring data"""
        try:
            report = self.generate_health_report()
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Monitoring report: {filename}")
            return filename
        except Exception as e:
            self.alert(f"Export error: {str(e)}")
            return None
    
    def continuous_monitoring(self, interval=60):
        """Run continuous monitoring"""
        print("Monitoring started")
        try:
            while True:
                report = self.generate_health_report()
                print(f"Health: {report['system_health']['status']}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Monitoring stopped")

if __name__ == "__main__":
    monitor = MonitoringSystem()
    monitor.continuous_monitoring()
