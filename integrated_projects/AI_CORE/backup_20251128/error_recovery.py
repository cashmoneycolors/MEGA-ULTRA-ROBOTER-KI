import sqlite3
import os
import json
from datetime import datetime

class ErrorRecovery:
    def __init__(self, db_path="wealth_system.db", recovery_log="recovery.log"):
        self.db_path = db_path
        self.recovery_log = recovery_log
        self.checkpoint_file = "checkpoint.json"
    
    def save_checkpoint(self, system_state):
        """Save system state for recovery"""
        try:
            checkpoint = {
                "timestamp": datetime.now().isoformat(),
                "capital": system_state.get("capital", 0),
                "cycle_count": system_state.get("cycle_count", 0),
                "error_count": system_state.get("error_count", 0)
            }
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f)
            self.log("Checkpoint saved")
            return True
        except Exception as e:
            self.log(f"Checkpoint save error: {str(e)}")
            return False
    
    def load_checkpoint(self):
        """Load last checkpoint"""
        try:
            if os.path.exists(self.checkpoint_file):
                with open(self.checkpoint_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            self.log(f"Checkpoint load error: {str(e)}")
            return None
    
    def verify_database_integrity(self):
        """Check database integrity"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("PRAGMA integrity_check")
            result = c.fetchone()[0]
            conn.close()
            
            if result == "ok":
                self.log("Database integrity: OK")
                return True
            else:
                self.log(f"Database integrity issue: {result}")
                return False
        except Exception as e:
            self.log(f"Integrity check error: {str(e)}")
            return False
    
    def repair_database(self):
        """Attempt database repair"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("VACUUM")
            c.execute("REINDEX")
            conn.commit()
            conn.close()
            self.log("Database repair completed")
            return True
        except Exception as e:
            self.log(f"Repair error: {str(e)}")
            return False
    
    def rollback_transaction(self):
        """Rollback failed transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.rollback()
            conn.close()
            self.log("Transaction rolled back")
            return True
        except Exception as e:
            self.log(f"Rollback error: {str(e)}")
            return False
    
    def handle_crash_recovery(self):
        """Handle system crash recovery"""
        try:
            self.log("=== CRASH RECOVERY INITIATED ===")
            
            if not self.verify_database_integrity():
                self.log("Database corrupted, attempting repair...")
                if self.repair_database():
                    self.log("Database repaired successfully")
                else:
                    self.log("Database repair failed")
                    return False
            
            checkpoint = self.load_checkpoint()
            if checkpoint:
                self.log(f"Recovered state: Capital={checkpoint['capital']}, Cycles={checkpoint['cycle_count']}")
                return checkpoint
            
            return None
        except Exception as e:
            self.log(f"Recovery error: {str(e)}")
            return None
    
    def log(self, message):
        """Log recovery events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.recovery_log, 'a') as f:
            f.write(log_msg + "\n")
    
    def get_recovery_status(self):
        """Get recovery status"""
        try:
            checkpoint = self.load_checkpoint()
            integrity = self.verify_database_integrity()
            
            return {
                "last_checkpoint": checkpoint,
                "database_integrity": integrity,
                "recovery_log_exists": os.path.exists(self.recovery_log)
            }
        except Exception as e:
            self.log(f"Status error: {str(e)}")
            return {}
