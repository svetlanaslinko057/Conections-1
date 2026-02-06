#!/usr/bin/env python3
"""
Backend API Testing for Connections Module
Tests all endpoints mentioned in the review request
"""

import requests
import sys
import json
from datetime import datetime

# Use the public endpoint from frontend/.env
BACKEND_URL = "https://influencer-eval.preview.emergentagent.com"

class ConnectionsAPITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            self.failed_tests.append({"name": name, "details": details})
            print(f"❌ {name} - {details}")
    
    def test_health_check(self):
        """Test main backend health check"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True
                details = f"Status: {response.status_code}, Data: {data}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Backend Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Health Check", False, str(e))
            return False
    
    def test_connections_health(self):
        """Test connections module health"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/health", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True and data.get('module') == 'connections'
                details = f"Status: {response.status_code}, Module: {data.get('module')}, Enabled: {data.get('enabled')}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Connections Module Health", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Module Health", False, str(e))
            return False
    
    def test_connections_score_mock(self):
        """Test connections scoring mock API"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/score/mock", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True and 'data' in data
                details = f"Status: {response.status_code}, Has mock data: {'data' in data}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Connections Score Mock API", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Score Mock API", False, str(e))
            return False
    
    def test_connections_accounts(self):
        """Test connections accounts list API"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/accounts", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True
                accounts_count = len(data.get('data', {}).get('items', []))
                details = f"Status: {response.status_code}, Accounts found: {accounts_count}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Connections Accounts List", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Accounts List", False, str(e))
            return False
    
    def test_connections_compare(self):
        """Test connections compare API with mock data"""
        try:
            # First try to get some accounts to compare
            accounts_response = requests.get(f"{BACKEND_URL}/api/connections/accounts?limit=2", timeout=10)
            
            if accounts_response.status_code == 200:
                accounts_data = accounts_response.json()
                accounts = accounts_data.get('data', {}).get('items', [])
                
                if len(accounts) >= 2:
                    # Use real accounts for comparison
                    compare_data = {
                        "left": accounts[0].get('handle', 'test1'),
                        "right": accounts[1].get('handle', 'test2')
                    }
                else:
                    # Use mock handles
                    compare_data = {
                        "left": "mock_user_1",
                        "right": "mock_user_2"
                    }
            else:
                # Use mock handles
                compare_data = {
                    "left": "mock_user_1", 
                    "right": "mock_user_2"
                }
            
            response = requests.post(
                f"{BACKEND_URL}/api/connections/compare",
                json=compare_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            # Accept both 200 (success) and 404 (profiles not found) as valid responses
            success = response.status_code in [200, 404]
            if response.status_code == 200:
                data = response.json()
                success = data.get('ok') == True
                details = f"Status: {response.status_code}, Comparison successful"
            elif response.status_code == 404:
                details = f"Status: {response.status_code}, Profiles not found (expected for mock data)"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("Connections Compare API", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Compare API", False, str(e))
            return False
    
    def test_connections_stats(self):
        """Test connections stats API"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/stats", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True and 'data' in data
                total_profiles = data.get('data', {}).get('total_profiles', 0)
                details = f"Status: {response.status_code}, Total profiles: {total_profiles}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Connections Stats API", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Stats API", False, str(e))
            return False
    
    def test_connections_config(self):
        """Test connections config API"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/config", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True and 'data' in data
                details = f"Status: {response.status_code}, Has config data: {'data' in data}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Connections Config API", success, details)
            return success
        except Exception as e:
            self.log_test("Connections Config API", False, str(e))
            return False
    
    def test_early_signal_mock(self):
        """Test early signal mock API"""
        try:
            response = requests.get(f"{BACKEND_URL}/api/connections/early-signal/mock", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get('ok') == True and 'data' in data
                details = f"Status: {response.status_code}, Has early signal data: {'data' in data}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Early Signal Mock API", success, details)
            return success
        except Exception as e:
            self.log_test("Early Signal Mock API", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🔍 Starting Connections Module Backend Tests...")
        print(f"📡 Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        # Core health checks
        self.test_health_check()
        self.test_connections_health()
        
        # Main APIs from review request
        self.test_connections_score_mock()
        self.test_connections_accounts()
        self.test_connections_compare()
        
        # Additional APIs
        self.test_connections_stats()
        self.test_connections_config()
        self.test_early_signal_mock()
        
        # Summary
        print("=" * 60)
        print(f"📊 Tests Summary: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test['name']}: {test['details']}")
        
        return self.tests_passed == self.tests_run

def main():
    tester = ConnectionsAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())