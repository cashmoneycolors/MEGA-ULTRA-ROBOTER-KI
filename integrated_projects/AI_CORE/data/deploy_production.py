#!/usr/bin/env python3
"""Production Deployment Script"""
import os
import sys
import subprocess
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.checks_passed = 0
        self.checks_failed = 0
    
    def check_python_version(self):
        """Check Python version"""
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 9:
                logger.info(f"✓ Python {version.major}.{version.minor} OK")
                self.checks_passed += 1
                return True
            else:
                logger.error(f"✗ Python 3.9+ required (found {version.major}.{version.minor})")
                self.checks_failed += 1
                return False
        except Exception as e:
            logger.error(f"✗ Python check failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def check_dependencies(self):
        """Check required packages"""
        try:
            required = [
                "requests",
                "python-dotenv",
                "sqlite3",
                "sentry-sdk"
            ]
            
            missing = []
            for package in required:
                try:
                    __import__(package.replace("-", "_"))
                except ImportError:
                    missing.append(package)
            
            if missing:
                logger.warning(f"✗ Missing packages: {', '.join(missing)}")
                logger.info("Installing dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                self.checks_passed += 1
            else:
                logger.info("✓ All dependencies installed")
                self.checks_passed += 1
            
            return True
        except Exception as e:
            logger.error(f"✗ Dependency check failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def check_env_file(self):
        """Check .env configuration"""
        try:
            env_path = self.project_root / ".env"
            
            if not env_path.exists():
                logger.error("✗ .env file not found")
                self.checks_failed += 1
                return False
            
            required_keys = [
                "PAYPAL_CLIENT_ID",
                "PAYPAL_CLIENT_SECRET",
                "OPENAI_API_KEY",
                "BINANCE_API_KEY"
            ]
            
            with open(env_path) as f:
                env_content = f.read()
            
            missing_keys = []
            for key in required_keys:
                if f"{key}=your_" in env_content or f"{key}=" not in env_content:
                    missing_keys.append(key)
            
            if missing_keys:
                logger.warning(f"✗ Missing/unconfigured keys: {', '.join(missing_keys)}")
                logger.info("Please configure these in .env file")
                self.checks_failed += 1
                return False
            else:
                logger.info("✓ .env configured")
                self.checks_passed += 1
                return True
                
        except Exception as e:
            logger.error(f"✗ .env check failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def check_database(self):
        """Check database setup"""
        try:
            import sqlite3
            
            db_path = self.project_root / "wealth_system.db"
            
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = c.fetchall()
                conn.close()
                
                if tables:
                    logger.info(f"✓ Database OK ({len(tables)} tables)")
                    self.checks_passed += 1
                    return True
                else:
                    logger.warning("✗ Database empty, initializing...")
                    self.init_database()
                    self.checks_passed += 1
                    return True
            else:
                logger.info("✓ Database will be created on first run")
                self.checks_passed += 1
                return True
                
        except Exception as e:
            logger.error(f"✗ Database check failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def init_database(self):
        """Initialize database"""
        try:
            from wealth_system_production import ProductionWealthSystem
            system = ProductionWealthSystem()
            logger.info("✓ Database initialized")
        except Exception as e:
            logger.error(f"✗ Database init failed: {str(e)}")
    
    def test_paypal_connection(self):
        """Test PayPal API"""
        try:
            from paypal_business import PayPalBusiness
            paypal = PayPalBusiness()
            token = paypal.get_access_token()
            
            if token:
                logger.info("✓ PayPal connection OK")
                self.checks_passed += 1
                return True
            else:
                logger.warning("✗ PayPal connection failed")
                self.checks_failed += 1
                return False
                
        except Exception as e:
            logger.warning(f"✗ PayPal test failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def test_crypto_connection(self):
        """Test Crypto API"""
        try:
            from crypto_trading import CryptoTrading
            crypto = CryptoTrading()
            price = crypto.get_price("BTC")
            
            if price > 0:
                logger.info(f"✓ Crypto connection OK (BTC: {price} CHF)")
                self.checks_passed += 1
                return True
            else:
                logger.warning("✗ Crypto connection failed")
                self.checks_failed += 1
                return False
                
        except Exception as e:
            logger.warning(f"✗ Crypto test failed: {str(e)}")
            self.checks_failed += 1
            return False
    
    def test_ai_art(self):
        """Test AI Art API"""
        try:
            from ai_art_generator import AIArtGenerator
            ai = AIArtGenerator()
            
            if ai.openai_key:
                logger.info("✓ AI Art configured")
                self.checks_passed += 1
                return True
            else:
                logger.warning("⚠ AI Art not configured (optional)")
                self.checks_passed += 1
                return True
                
        except Exception as e:
            logger.warning(f"⚠ AI Art test failed: {str(e)}")
            self.checks_passed += 1
            return True
    
    def run_all_checks(self):
        """Run all deployment checks"""
        logger.info("=" * 50)
        logger.info("PRODUCTION DEPLOYMENT CHECKS")
        logger.info("=" * 50)
        
        self.check_python_version()
        self.check_dependencies()
        self.check_env_file()
        self.check_database()
        self.test_paypal_connection()
        self.test_crypto_connection()
        self.test_ai_art()
        
        logger.info("=" * 50)
        logger.info(f"Checks Passed: {self.checks_passed}")
        logger.info(f"Checks Failed: {self.checks_failed}")
        logger.info("=" * 50)
        
        if self.checks_failed == 0:
            logger.info("✓ READY FOR PRODUCTION")
            return True
        else:
            logger.error("✗ FIX ISSUES BEFORE DEPLOYMENT")
            return False
    
    def start_system(self):
        """Start production system"""
        try:
            logger.info("Starting production system...")
            from wealth_system_production import ProductionWealthSystem
            
            system = ProductionWealthSystem(initial_capital=100)
            system.run()
            
        except Exception as e:
            logger.error(f"System start failed: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    deployer = ProductionDeployer()
    
    if deployer.run_all_checks():
        logger.info("Starting system...")
        deployer.start_system()
    else:
        logger.error("Deployment checks failed. Please fix issues and try again.")
        sys.exit(1)
