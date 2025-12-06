import shutil
import os
from datetime import datetime
import sqlite3

class BackupManager:
    def __init__(self, db_path="wealth_system.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self):
        """Create database backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"wealth_system_{timestamp}.db")
            shutil.copy2(self.db_path, backup_file)
            print(f"Backup created: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"Backup error: {str(e)}")
            return None
    
    def restore_backup(self, backup_file):
        """Restore from backup"""
        try:
            shutil.copy2(backup_file, self.db_path)
            print(f"Restored from: {backup_file}")
            return True
        except Exception as e:
            print(f"Restore error: {str(e)}")
            return False
    
    def cleanup_old_backups(self, keep_count=10):
        """Keep only latest backups"""
        try:
            backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("wealth_system_")])
            if len(backups) > keep_count:
                for old_backup in backups[:-keep_count]:
                    os.remove(os.path.join(self.backup_dir, old_backup))
                    print(f"Deleted old backup: {old_backup}")
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
    
    def export_json(self, output_file="export.json"):
        """Export database to JSON"""
        try:
            import json
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            data = {}
            for table in ["transactions", "art_portfolio", "trading_log", "clones"]:
                c.execute(f"SELECT * FROM {table}")
                data[table] = [dict(row) for row in c.fetchall()]
            
            conn.close()
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Exported to: {output_file}")
            return output_file
        except Exception as e:
            print(f"Export error: {str(e)}")
            return None
    
    def export_csv(self, output_dir="exports"):
        """Export tables to CSV"""
        try:
            import csv
            os.makedirs(output_dir, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            for table in ["transactions", "art_portfolio", "trading_log", "clones"]:
                c.execute(f"SELECT * FROM {table}")
                rows = c.fetchall()
                cols = [description[0] for description in c.description]
                
                csv_file = os.path.join(output_dir, f"{table}.csv")
                with open(csv_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(cols)
                    writer.writerows(rows)
                print(f"Exported: {csv_file}")
            
            conn.close()
            return output_dir
        except Exception as e:
            print(f"CSV export error: {str(e)}")
            return None
