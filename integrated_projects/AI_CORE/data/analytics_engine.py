import sqlite3
from datetime import datetime, timedelta
import json

class AnalyticsEngine:
    def __init__(self, db_path="wealth_system.db"):
        self.db_path = db_path
    
    def get_profit_by_source(self):
        """Get profit breakdown by source"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT SUM(profit) FROM art_portfolio")
            art = c.fetchone()[0] or 0
            
            c.execute("SELECT SUM(profit) FROM trading_log")
            trading = c.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "art": art,
                "trading": trading,
                "total": art + trading
            }
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def get_cycle_statistics(self):
        """Get cycle performance stats"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*), AVG(amount), MAX(amount), MIN(amount) FROM transactions WHERE type='profit'")
            count, avg, max_val, min_val = c.fetchone()
            
            conn.close()
            
            return {
                "total_cycles": count or 0,
                "avg_profit": avg or 0,
                "max_profit": max_val or 0,
                "min_profit": min_val or 0
            }
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def get_clone_performance(self):
        """Get clone network performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            active = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit_contribution) FROM clones")
            total_profit = c.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "active_clones": active,
                "total_profit": total_profit,
                "avg_per_clone": total_profit / active if active > 0 else 0
            }
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def get_hourly_performance(self, hours=24):
        """Get performance over last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            cutoff = datetime.now() - timedelta(hours=hours)
            c.execute("SELECT strftime('%Y-%m-%d %H:00:00', timestamp) as hour, SUM(amount) FROM transactions WHERE timestamp > ? AND type='profit' GROUP BY hour ORDER BY hour",
                     (cutoff.isoformat(),))
            
            data = [{"hour": row[0], "profit": row[1]} for row in c.fetchall()]
            conn.close()
            
            return data
        except Exception as e:
            print(f"Error: {str(e)}")
            return []
    
    def generate_report(self):
        """Generate comprehensive analytics report"""
        try:
            profit_source = self.get_profit_by_source()
            cycle_stats = self.get_cycle_statistics()
            clone_perf = self.get_clone_performance()
            hourly = self.get_hourly_performance()
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "profit_by_source": profit_source,
                "cycle_statistics": cycle_stats,
                "clone_performance": clone_perf,
                "hourly_performance": hourly
            }
            
            return report
        except Exception as e:
            print(f"Report error: {str(e)}")
            return {}
    
    def export_report(self, filename="analytics_report.json"):
        """Export report to JSON"""
        try:
            report = self.generate_report()
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report exported: {filename}")
            return filename
        except Exception as e:
            print(f"Export error: {str(e)}")
            return None
