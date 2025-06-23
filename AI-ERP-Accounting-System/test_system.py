#!/usr/bin/env python3
"""
Test script for the ERP system without AI integration
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from accounting.core import AccountingEngine
        print("✓ AccountingEngine imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AccountingEngine: {e}")
        return False
    
    try:
        from security.encryption import AESEncryption
        print("✓ AESEncryption imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AESEncryption: {e}")
        return False
    
    try:
        from ui.dashboard import DashboardManager
        print("✓ DashboardManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import DashboardManager: {e}")
        return False
    
    return True

def test_accounting():
    """Test accounting functionality"""
    print("\nTesting accounting functionality...")
    
    try:
        from accounting.core import AccountingEngine
        engine = AccountingEngine()
        
        # Test adding transactions
        engine.add_transaction("2024-01-01", "Test expense", 100.0, "Cash", "expense")
        engine.add_transaction("2024-01-02", "Test income", 200.0, "Bank", "income")
        
        # Test reports
        balance_sheet = engine.get_balance_sheet()
        income_stmt = engine.get_income_statement()
        
        print(f"✓ Added {len(engine.transactions)} transactions")
        print(f"✓ Balance sheet has {len(balance_sheet)} accounts")
        print(f"✓ Income statement has {len(income_stmt)} types")
        
        return True
    except Exception as e:
        print(f"✗ Accounting test failed: {e}")
        return False

def test_encryption():
    """Test encryption functionality"""
    print("\nTesting encryption functionality...")
    
    try:
        from security.encryption import AESEncryption
        encryption = AESEncryption()
        encryption.initialize_keys()
        
        # Test encryption/decryption
        test_data = "Hello World"
        encrypted = encryption.encrypt_data(test_data)
        decrypted = encryption.decrypt_data(encrypted)
        
        if decrypted == test_data:
            print("✓ Encryption/decryption works correctly")
        else:
            print("✗ Encryption/decryption failed")
            return False
        
        # Test password hashing
        password = "test123"
        hashed = encryption.hash_password(password)
        print(f"✓ Password hashing works: {hashed[:20]}...")
        
        return True
    except Exception as e:
        print(f"✗ Encryption test failed: {e}")
        return False

def test_dashboard():
    """Test dashboard functionality"""
    print("\nTesting dashboard functionality...")
    
    try:
        import pandas as pd
        from ui.dashboard import DashboardManager
        
        dashboard = DashboardManager()
        
        # Create test data
        test_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'amount': [100, 200, 300]
        })
        
        # Test stats calculation
        stats = dashboard.display_summary_stats(test_data)
        print(f"✓ Dashboard stats calculated: {stats}")
        
        return True
    except Exception as e:
        print(f"✗ Dashboard test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("FINS ERP System - Component Tests")
    print("=" * 40)
    
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        test_imports,
        test_accounting,
        test_encryption,
        test_dashboard
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! System is ready to run.")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 