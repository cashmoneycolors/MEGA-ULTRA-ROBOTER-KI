import schedule
import time
import threading
from datetime import datetime
from cash_money_production import AutonomousWealthSystem
from backup_manager import BackupManager
from analytics_engine import AnalyticsEngine
from error_recovery import ErrorRecovery

class SystemScheduler:
    def __init__(self):
        self.system = AutonomousWealthSystem(initial_capital=100)
        self.backup_manager = BackupManager()
        self.analytics = AnalyticsEngine()
        self.recovery = ErrorRecovery()
        self.running = False
    
    def schedule_tasks(self):
        """Schedule all background tasks"""
        schedule.every(2).seconds.do(self.run_production_cycle)
        schedule.every(1).minutes.do(self.save_checkpoint)
        schedule.every(5).minutes.do(self.create_backup)
        schedule.every(10).minutes.do(self.generate_analytics)
        schedule.every(1).hours.do(self.cleanup_backups)
        schedule.every(1).hours.do(self.verify_integrity)
    
    def run_production_cycle(self):
        """Execute production cycle"""
        try:
            profit = self.system.execute_production_cycle()
            print(f"[{datetime.now()}] Cycle profit: {profit:.2f} CHF")
        except Exception as e:
            print(f"Cycle error: {str(e)}")
    
    def save_checkpoint(self):
        """Save system checkpoint"""
        try:
            state = {
                "capital": self.system.capital,
                "cycle_count": self.system.cycle_count,
                "error_count": self.system.error_count
            }
            self.recovery.save_checkpoint(state)
        except Exception as e:
            print(f"Checkpoint error: {str(e)}")
    
    def create_backup(self):
        """Create database backup"""
        try:
            self.backup_manager.create_backup()
        except Exception as e:
            print(f"Backup error: {str(e)}")
    
    def generate_analytics(self):
        """Generate analytics report"""
        try:
            report = self.analytics.generate_report()
            print(f"Analytics: {report}")
        except Exception as e:
            print(f"Analytics error: {str(e)}")
    
    def cleanup_backups(self):
        """Cleanup old backups"""
        try:
            self.backup_manager.cleanup_old_backups(keep_count=10)
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
    
    def verify_integrity(self):
        """Verify database integrity"""
        try:
            if not self.recovery.verify_database_integrity():
                print("Database integrity issue detected, attempting repair...")
                self.recovery.repair_database()
        except Exception as e:
            print(f"Integrity check error: {str(e)}")
    
    def run_scheduler(self):
        """Run scheduler loop"""
        self.running = True
        print("Scheduler started")
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """Start scheduler in background thread"""
        self.schedule_tasks()
        thread = threading.Thread(target=self.run_scheduler, daemon=True)
        thread.start()
        print("Background scheduler started")
        return thread
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        print("Scheduler stopped")

if __name__ == "__main__":
    scheduler = SystemScheduler()
    scheduler.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
