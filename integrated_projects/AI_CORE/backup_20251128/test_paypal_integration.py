"""
PayPal Integration Test Script
Tests all PayPal functionality for the Autonomous Wealth Generation System
"""

import sys
import os
import json
from datetime import datetime

def test_config_loading():
    """Test configuration loading"""
    print("🔧 Testing configuration loading...")
    
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        paypal_config = config.get('paypal', {})
        required_fields = ['client_id', 'client_secret', 'currency']
        
        missing_fields = [field for field in required_fields if not paypal_config.get(field)]
        
        if missing_fields:
            print(f"❌ Missing PayPal configuration fields: {missing_fields}")
            print("   Please update config.json with your PayPal credentials")
            return False
        
        print("✅ Configuration loaded successfully")
        print(f"   Currency: {paypal_config.get('currency')}")
        print(f"   Sandbox Mode: {paypal_config.get('sandbox_mode')}")
        print(f"   Payments Enabled: {paypal_config.get('enable_payments')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading error: {str(e)}")
        return False

def test_paypal_import():
    """Test PayPal SDK import"""
    print("\n🔧 Testing PayPal SDK import...")
    
    try:
        from paypal_integration import PayPalBusinessManager
        print("✅ PayPal integration module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ PayPal SDK import failed: {str(e)}")
        print("   Run: pip install paypal-checkout-sdk")
        return False
    except Exception as e:
        print(f"❌ PayPal module error: {str(e)}")
        return False

def test_paypal_initialization():
    """Test PayPal client initialization"""
    print("\n🔧 Testing PayPal client initialization...")
    
    try:
        from paypal_integration import PayPalBusinessManager
        
        paypal_manager = PayPalBusinessManager("config.json")
        
        if paypal_manager.paypal_client:
            print("✅ PayPal client initialized successfully")
            return True
        else:
            print("❌ PayPal client initialization failed")
            print("   Check your client_id and client_secret in config.json")
            return False
            
    except Exception as e:
        print(f"❌ PayPal initialization error: {str(e)}")
        return False

def test_service_configuration():
    """Test service configuration"""
    print("\n🔧 Testing service configuration...")
    
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        services = config.get('paypal', {}).get('services', {})
        
        if not services:
            print("❌ No services configured")
            return False
        
        enabled_services = [name for name, config in services.items() if config.get('enabled')]
        
        if not enabled_services:
            print("❌ No services enabled")
            return False
        
        print(f"✅ Found {len(enabled_services)} enabled services:")
        for service in enabled_services:
            price = services[service].get('price_usd', 0)
            desc = services[service].get('description', 'No description')
            print(f"   - {service}: ${price:.2f} - {desc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Service configuration error: {str(e)}")
        return False

def test_enhanced_wealth_system():
    """Test enhanced wealth system"""
    print("\n🔧 Testing enhanced wealth system...")
    
    try:
        # Import the enhanced system
        sys.path.append(os.getcwd())
        from enhanced_wealth_system import EnhancedWealthSystem
        
        # Initialize with payments disabled for testing
        system = EnhancedWealthSystem(initial_capital=100, enable_payments=False)
        
        print("✅ Enhanced wealth system initialized")
        print(f"   Initial capital: {system.capital} CHF")
        print(f"   Target: {system.target} CHF")
        print(f"   Database path: {system.db_path}")
        
        # Test basic functionality
        profit = system.execute_production_cycle()
        print(f"   Test cycle profit: {profit:.2f} CHF")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced wealth system error: {str(e)}")
        return False

def test_api_server_imports():
    """Test API server imports"""
    print("\n🔧 Testing API server imports...")
    
    try:
        # Test basic imports
        from flask import Flask
        from flask_cors import CORS
        import sqlite3
        print("✅ Basic Flask imports successful")
        
        # Test PayPal imports in API context
        try:
            from paypal_integration import PayPalBusinessManager
            print("✅ PayPal integration available in API context")
        except ImportError:
            print("⚠️  PayPal integration not available in API context")
        
        return True
        
    except Exception as e:
        print(f"❌ API server import error: {str(e)}")
        return False

def test_database_integration():
    """Test database tables"""
    print("\n🔧 Testing database integration...")
    
    try:
        from enhanced_wealth_system import EnhancedWealthSystem
        
        system = EnhancedWealthSystem(initial_capital=100, enable_payments=False)
        
        # Check if database exists
        if not os.path.exists(system.db_path):
            print("❌ Database file not created")
            return False
        
        # Test database connection and tables
        conn = sqlite3.connect(system.db_path)
        c = conn.cursor()
        
        # Check for PayPal tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        
        required_tables = ['transactions', 'paypal_payments']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing database tables: {missing_tables}")
            return False
        
        print(f"✅ Database integration successful")
        print(f"   Found {len(tables)} tables: {', '.join(tables)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database integration error: {str(e)}")
        return False

def run_integration_test():
    """Run complete integration test"""
    print("🚀 Starting PayPal Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("PayPal SDK Import", test_paypal_import),
        ("PayPal Initialization", test_paypal_initialization),
        ("Service Configuration", test_service_configuration),
        ("Enhanced Wealth System", test_enhanced_wealth_system),
        ("API Server Imports", test_api_server_imports),
        ("Database Integration", test_database_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! PayPal integration is ready.")
        print("\nNext steps:")
        print("1. Configure your PayPal credentials in config.json")
        print("2. Run: python enhanced_wealth_system.py")
        print("3. Start API server: python api_server.py")
        print("4. Test payment endpoints with your PayPal account")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    run_integration_test()