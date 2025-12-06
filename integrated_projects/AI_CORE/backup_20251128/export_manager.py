
import sqlite3
import csv
import json
import os
from datetime import datetime

class ExportManager:
    def __init__(self, db_path="wealth_system.db", export_dir="exports"):
        self.db_path = db_path
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)
    
    def export_to_json(self, filename=None):
        """Export all data to JSON"""
        try:
            if not filename:
                filename = os.path.join(self.export_dir, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            data = {}
            for table in ["transactions", "art_portfolio", "trading_log", "clones"]:
                c.execute(f"SELECT * FROM {table}")
                data[table] = [dict(row) for row in c.fetchall()]
            
            conn.close()
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"Exported to JSON: {filename}")
            return filename
        except Exception as e:
            print(f"JSON export error: {str(e)}")
            return None
    
    def export_to_csv(self, table_name=None):
        """Export table to CSV"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            tables = [table_name] if table_name else ["transactions", "art_portfolio", "trading_log", "clones"]
            
            for table in tables:
                c.execute(f"SELECT * FROM {table}")
                rows = c.fetchall()
                cols = [description[0] for description in c.description]
                
                filename = os.path.join(self.export_dir, f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(cols)
                    writer.writerows(rows)
                
                print(f"Exported to CSV: {filename}")
            
            conn.close()
            return True
        except Exception as e:
            print(f"CSV export error: {str(e)}")
            return False
    
    def export_summary_report(self):
        """Export summary report"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM transactions")
            total_transactions = c.fetchone()[0]
            
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
            total_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art_count = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit) FROM art_portfolio")
            art_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trade_count = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit) FROM trading_log")
            trading_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            active_clones = c.fetchone()[0]
            
            conn.close()
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_transactions": total_transactions,
                    "total_profit": total_profit,
                    "art_assets": art_count,
                    "art_profit": art_profit,
                    "trades": trade_count,
                    "trading_profit": trading_profit,
                    "active_clones": active_clones
                }
            }
            
            filename = os.path.join(self.export_dir, f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"Summary report exported: {filename}")
            return filename
        except Exception as e:
            print(f"Summary export error: {str(e)}")
            return None
    
    def export_html_report(self):
        """Export HTML report"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
            total_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            clones = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art = c.fetchone()[0]
            
            conn.close()
            
            html = f"""
<html>
<head>
    <title>Wealth System Report</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        .header {{ color: #00ff00; font-size: 24px; }}
        .stat {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="header">Autonomous Wealth System Report</div>
    <div class="stat">Generated: {datetime.now().isoformat()}</div>
    <div class="stat">Total Profit: {total_profit:.2f} CHF</div>
    <div class="stat">Active Clones: {clones}</div>
    <div class="stat">Art Assets: {art}</div>
</body>
</html>
"""
            
            filename = os.path.join(self.export_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            with open(filename, 'w') as f:
                f.write(html)
            
            print(f"HTML report exported: {filename}")
            return filename
        except Exception as e:
            print(f"HTML export error: {str(e)}")
            return None
