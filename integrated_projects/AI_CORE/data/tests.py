import unittest
import sqlite3
import os
from cash_money_production import AutonomousWealthSystem
from backup_manager import BackupManager
from analytics_engine import AnalyticsEngine
from error_recovery import ErrorRecovery

class TestWealthSystem(unittest.TestCase):
    def setUp(self):
        self.system = AutonomousWealthSystem(initial_capital=100)
        self.test_db = "test_wealth_system.db"
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_initial_capital(self):
        """Test initial capital"""
        self.assertEqual(self.system.capital, 100)
    
    def test_production_cycle(self):
        """Test production cycle"""
        initial = self.system.capital
        profit = self.system.execute_production_cycle()
        self.assertGreater(self.system.capital, initial)
        self.assertGreater(profit, 0)
    
    def test_art_generation(self):
        """Test art asset generation"""
        profit = self.system.generate_art_assets()
        self.assertGreaterEqual(profit, 0)
    
    def test_trading(self):
        """Test asset trading"""
        profit = self.system.execute_asset_trading()
        self.assertGreaterEqual(profit, 0)
    
    def test_vector_services(self):
        """Test vector services"""
        profit = self.system.generate_vector_services()
        self.assertGreaterEqual(profit, 0)
    
    def test_clone_creation(self):
        """Test clone creation"""
        self.system.capital = 500
        initial_clones = self.system.get_active_clones()
        self.system.evaluate_clone_creation()
        self.assertGreaterEqual(self.system.get_active_clones(), initial_clones)
    
    def test_database_integrity(self):
        """Test database integrity"""
        recovery = ErrorRecovery(self.test_db)
        self.assertTrue(recovery.verify_database_integrity())
    
    def test_backup_creation(self):
        """Test backup creation"""
        backup_mgr = BackupManager(self.test_db)
        backup_file = backup_mgr.create_backup()
        self.assertTrue(os.path.exists(backup_file))
    
    def test_analytics(self):
        """Test analytics engine"""
        analytics = AnalyticsEngine(self.test_db)
        report = analytics.generate_report()
        self.assertIn("timestamp", report)
    
    def test_capital_never_negative(self):
        """Test capital never goes negative"""
        for _ in range(10):
            self.system.execute_production_cycle()
        self.assertGreaterEqual(self.system.capital, 0)
    
    def test_cycle_count_increment(self):
        """Test cycle count increments"""
        initial = self.system.cycle_count
        self.system.execute_production_cycle()
        self.assertEqual(self.system.cycle_count, initial + 1)

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.backup_mgr = BackupManager("test_db.db")
    
    def tearDown(self):
        import shutil
        if os.path.exists("backups"):
            shutil.rmtree("backups")
    
    def test_backup_creation(self):
        """Test backup file creation"""
        backup = self.backup_mgr.create_backup()
        self.assertIsNotNone(backup)
    
    def test_json_export(self):
        """Test JSON export"""
        export_file = self.backup_mgr.export_json()
        self.assertIsNotNone(export_file)

class TestErrorRecovery(unittest.TestCase):
    def setUp(self):
        self.recovery = ErrorRecovery("test_recovery.db")
    
    def test_checkpoint_save_load(self):
        """Test checkpoint save and load"""
        state = {"capital": 1000, "cycle_count": 5}
        self.recovery.save_checkpoint(state)
        loaded = self.recovery.load_checkpoint()
        self.assertEqual(loaded["capital"], 1000)
    
    def test_database_integrity_check(self):
        """Test database integrity check"""
        result = self.recovery.verify_database_integrity()
        self.assertIsNotNone(result)

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    run_tests()
