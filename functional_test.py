#!/usr/bin/env python3
"""
🔥 HYPERLOCAL MARKETPLACE - COMPREHENSIVE FUNCTIONAL TEST
Simulates real-world usage of the platform by testing all user roles and features.
"""

import asyncio
import json
import httpx
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Test Configuration
BASE_URL = "http://localhost:12000"
TIMEOUT = 30.0

class HyperlocalTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=TIMEOUT)
        self.test_results = []
        self.tokens = {}
        self.test_data = {}
        
    async def log_test(self, test_name: str, status: str, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
        print()

    async def test_authentication(self):
        """Test authentication module"""
        print("🔐 TESTING AUTHENTICATION MODULE")
        print("=" * 50)
        
        # Test 1: User Registration (Customer)
        try:
            customer_data = {
                "phone": "+1234567890",
                "email": "customer@test.com",
                "password": "testpass123",
                "full_name": "Test Customer",
                "role": "customer"
            }
            
            response = await self.client.post(f"{BASE_URL}/auth/register", json=customer_data)
            
            if response.status_code == 200:
                result = response.json()
                # Extract token from nested data structure
                if result.get("data") and result["data"].get("token"):
                    self.tokens["customer"] = result["data"]["token"]
                elif result.get("token"):
                    self.tokens["customer"] = result["token"]
                
                user_id = result.get("data", {}).get("id") if result.get("data") else result.get("user_id")
                self.test_data["customer_id"] = user_id
                await self.log_test("Customer Registration", "PASS", 
                                  f"Customer registered with ID: {user_id}", result)
            else:
                await self.log_test("Customer Registration", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Customer Registration", "FAIL", f"Exception: {str(e)}")

        # Test 2: User Registration (Seller)
        try:
            seller_data = {
                "phone": "+1234567891",
                "email": "seller@test.com", 
                "password": "testpass123",
                "full_name": "Test Seller",
                "role": "seller"
            }
            
            response = await self.client.post(f"{BASE_URL}/auth/register", json=seller_data)
            
            if response.status_code == 200:
                result = response.json()
                user_id = result.get("data", {}).get("id") if result.get("data") else result.get("user_id")
                self.test_data["seller_id"] = user_id
                await self.log_test("Seller Registration", "PASS", 
                                  f"Seller registered with ID: {user_id}", result)
                
                # Login to get token
                login_response = await self.client.post(f"{BASE_URL}/auth/login", json={
                    "phone": "+1234567891",
                    "password": "testpass123"
                })
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    if login_result.get("data") and login_result["data"].get("token"):
                        self.tokens["seller"] = login_result["data"]["token"]
                    elif login_result.get("token"):
                        self.tokens["seller"] = login_result["token"]
            else:
                await self.log_test("Seller Registration", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Seller Registration", "FAIL", f"Exception: {str(e)}")

        # Test 3: User Registration (Admin)
        try:
            admin_data = {
                "phone": "+1234567892",
                "email": "admin@test.com",
                "password": "testpass123", 
                "full_name": "Test Admin",
                "role": "admin"
            }
            
            response = await self.client.post(f"{BASE_URL}/auth/register", json=admin_data)
            
            if response.status_code == 200:
                result = response.json()
                user_id = result.get("data", {}).get("id") if result.get("data") else result.get("user_id")
                self.test_data["admin_id"] = user_id
                await self.log_test("Admin Registration", "PASS", 
                                  f"Admin registered with ID: {user_id}", result)
                
                # Login to get token
                login_response = await self.client.post(f"{BASE_URL}/auth/login", json={
                    "phone": "+1234567892",
                    "password": "testpass123"
                })
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    if login_result.get("data") and login_result["data"].get("token"):
                        self.tokens["admin"] = login_result["data"]["token"]
                    elif login_result.get("token"):
                        self.tokens["admin"] = login_result["token"]
            else:
                await self.log_test("Admin Registration", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Admin Registration", "FAIL", f"Exception: {str(e)}")

        # Test 4: Login Test
        try:
            login_data = {
                "phone": "+1234567890",
                "password": "testpass123"
            }
            
            response = await self.client.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                result = response.json()
                # Update customer token from login
                if result.get("data") and result["data"].get("token"):
                    self.tokens["customer"] = result["data"]["token"]
                elif result.get("token"):
                    self.tokens["customer"] = result["token"]
                await self.log_test("User Login", "PASS", 
                                  f"Login successful for customer", result)
            else:
                await self.log_test("User Login", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("User Login", "FAIL", f"Exception: {str(e)}")

    async def test_seller_module(self):
        """Test seller functionality"""
        print("🏪 TESTING SELLER MODULE")
        print("=" * 50)
        
        if not self.tokens.get("seller"):
            await self.log_test("Seller Module", "SKIP", "No seller token available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['seller']}"}
        
        # Test 1: Create Shop
        try:
            shop_data = {
                "name": "Fresh Mart Demo",
                "description": "Your neighborhood grocery store for testing",
                "address": "123 Test Street, Demo City, DC 12345",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "category": "Grocery",
                "phone": "+1234567890",
                "email": "freshmart@demo.com"
            }
            
            response = await self.client.post(f"{BASE_URL}/shops", 
                                            json=shop_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                self.test_data["shop_id"] = result.get("id")
                await self.log_test("Create Shop", "PASS", 
                                  f"Shop created with ID: {result.get('id')}", result)
            else:
                await self.log_test("Create Shop", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Create Shop", "FAIL", f"Exception: {str(e)}")

        # Test 2: Add Products
        if self.test_data.get("shop_id"):
            products = [
                {
                    "name": "Fresh Apples",
                    "description": "Crisp and sweet red apples",
                    "price": 3.99,
                    "category": "Fruits",
                    "quantity": 100,
                    "unit": "kg",
                    "in_stock": True
                },
                {
                    "name": "Organic Bananas", 
                    "description": "Fresh organic bananas",
                    "price": 2.49,
                    "category": "Fruits",
                    "quantity": 50,
                    "unit": "kg",
                    "in_stock": True
                },
                {
                    "name": "Whole Wheat Bread",
                    "description": "Fresh baked whole wheat bread",
                    "price": 4.99,
                    "category": "Bakery",
                    "quantity": 20,
                    "unit": "loaf",
                    "in_stock": True
                }
            ]
            
            for i, product_data in enumerate(products):
                try:
                    response = await self.client.post(f"{BASE_URL}/shops/{self.test_data['shop_id']}/products", 
                                                    json=product_data, headers=headers)
                    
                    if response.status_code == 200:
                        result = response.json()
                        await self.log_test(f"Add Product {i+1}", "PASS", 
                                          f"Product '{product_data['name']}' added", result)
                    else:
                        await self.log_test(f"Add Product {i+1}", "FAIL", 
                                          f"Status: {response.status_code}, Response: {response.text}")
                        
                except Exception as e:
                    await self.log_test(f"Add Product {i+1}", "FAIL", f"Exception: {str(e)}")

        # Test 3: Get Shop Dashboard
        try:
            response = await self.client.get(f"{BASE_URL}/vendor/shop", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("Seller Dashboard", "PASS", 
                                  f"Dashboard data retrieved", result)
            else:
                await self.log_test("Seller Dashboard", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Seller Dashboard", "FAIL", f"Exception: {str(e)}")

    async def test_customer_module(self):
        """Test customer functionality"""
        print("🛒 TESTING CUSTOMER MODULE")
        print("=" * 50)
        
        if not self.tokens.get("customer"):
            await self.log_test("Customer Module", "SKIP", "No customer token available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['customer']}"}
        
        # Test 1: Discover Shops by Location
        try:
            params = {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "radius": 10
            }
            
            response = await self.client.get(f"{BASE_URL}/shops", 
                                           params=params, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("Discover Nearby Shops", "PASS", 
                                  f"Found {len(result.get('shops', []))} shops", result)
            else:
                await self.log_test("Discover Nearby Shops", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Discover Nearby Shops", "FAIL", f"Exception: {str(e)}")

        # Test 2: Browse Products by Category
        try:
            response = await self.client.get(f"{BASE_URL}/catalog", 
                                           params={"category": "Fruits"}, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("Browse Products by Category", "PASS", 
                                  f"Found {len(result.get('products', []))} products", result)
            else:
                await self.log_test("Browse Products by Category", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Browse Products by Category", "FAIL", f"Exception: {str(e)}")

        # Test 3: Search Products
        try:
            response = await self.client.get(f"{BASE_URL}/catalog", 
                                           params={"search": "apple"}, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("Search Products", "PASS", 
                                  f"Search returned {len(result.get('products', []))} results", result)
            else:
                await self.log_test("Search Products", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Search Products", "FAIL", f"Exception: {str(e)}")

        # Test 4: Get User Profile
        try:
            response = await self.client.get(f"{BASE_URL}/users/me", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("Get User Profile", "PASS", 
                                  f"Profile retrieved successfully", result)
            else:
                await self.log_test("Get User Profile", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("Get User Profile", "FAIL", f"Exception: {str(e)}")

    async def test_admin_module(self):
        """Test admin functionality"""
        print("🛠️ TESTING ADMIN MODULE")
        print("=" * 50)
        
        if not self.tokens.get("admin"):
            await self.log_test("Admin Module", "SKIP", "No admin token available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        # Test 1: View All Shops (Admin perspective)
        try:
            response = await self.client.get(f"{BASE_URL}/shops", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("View All Shops", "PASS", 
                                  f"Retrieved shops data", result)
            else:
                await self.log_test("View All Shops", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("View All Shops", "FAIL", f"Exception: {str(e)}")

        # Test 2: Update Shop (Admin perspective)
        if self.test_data.get("shop_id"):
            try:
                update_data = {"status": "approved", "notes": "Shop approved for testing"}
                response = await self.client.put(f"{BASE_URL}/shops/{self.test_data['shop_id']}", 
                                               json=update_data, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    await self.log_test("Update Shop", "PASS", 
                                      f"Shop updated successfully", result)
                else:
                    await self.log_test("Update Shop", "FAIL", 
                                      f"Status: {response.status_code}, Response: {response.text}")
                    
            except Exception as e:
                await self.log_test("Update Shop", "FAIL", f"Exception: {str(e)}")

        # Test 3: View Catalog Categories
        try:
            response = await self.client.get(f"{BASE_URL}/catalog/categories", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                await self.log_test("View Categories", "PASS", 
                                  f"Retrieved categories data", result)
            else:
                await self.log_test("View Categories", "FAIL", 
                                  f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            await self.log_test("View Categories", "FAIL", f"Exception: {str(e)}")

    async def test_error_handling(self):
        """Test error handling and edge cases"""
        print("⚠️ TESTING ERROR HANDLING")
        print("=" * 50)
        
        # Test 1: Invalid Authentication
        try:
            headers = {"Authorization": "Bearer invalid_token"}
            response = await self.client.get(f"{BASE_URL}/vendor/shop", headers=headers)
            
            if response.status_code == 401:
                await self.log_test("Invalid Token Handling", "PASS", 
                                  "Correctly rejected invalid token")
            else:
                await self.log_test("Invalid Token Handling", "FAIL", 
                                  f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            await self.log_test("Invalid Token Handling", "FAIL", f"Exception: {str(e)}")

        # Test 2: Duplicate Registration
        try:
            duplicate_data = {
                "phone": "+1234567890",  # Same as customer
                "email": "duplicate@test.com",
                "password": "testpass123",
                "full_name": "Duplicate User",
                "role": "customer"
            }
            
            response = await self.client.post(f"{BASE_URL}/auth/register", json=duplicate_data)
            
            if response.status_code == 400:
                await self.log_test("Duplicate Registration Handling", "PASS", 
                                  "Correctly rejected duplicate phone number")
            else:
                await self.log_test("Duplicate Registration Handling", "FAIL", 
                                  f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            await self.log_test("Duplicate Registration Handling", "FAIL", f"Exception: {str(e)}")

        # Test 3: Invalid Data Validation
        try:
            invalid_shop_data = {
                "name": "",  # Empty name
                "description": "Test shop",
                "address": "123 Test St",
                "latitude": "invalid",  # Invalid latitude
                "longitude": -74.0060,
                "category": "Grocery"
            }
            
            headers = {"Authorization": f"Bearer {self.tokens.get('seller', '')}"}
            response = await self.client.post(f"{BASE_URL}/shops", 
                                            json=invalid_shop_data, headers=headers)
            
            if response.status_code == 422:
                await self.log_test("Data Validation", "PASS", 
                                  "Correctly rejected invalid data")
            else:
                await self.log_test("Data Validation", "FAIL", 
                                  f"Expected 422, got {response.status_code}")
                
        except Exception as e:
            await self.log_test("Data Validation", "FAIL", f"Exception: {str(e)}")

    async def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 FINAL TEST REPORT")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print(f"📋 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⏭️ Skipped: {skipped_tests}")
        print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📝 DETAILED RESULTS:")
        for result in self.test_results:
            status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⏭️"
            print(f"   {status_emoji} {result['test_name']}: {result['status']}")
            if result["details"]:
                print(f"      └─ {result['details']}")
        
        # Save detailed report
        report_data = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "skipped_tests": skipped_tests,
                "success_rate": (passed_tests/total_tests)*100,
                "test_date": datetime.now().isoformat()
            },
            "test_results": self.test_results,
            "test_data": self.test_data,
            "tokens": {k: "***REDACTED***" for k in self.tokens.keys()}
        }
        
        with open("/workspace/FUNCTIONAL_TEST_RESULTS.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: /workspace/FUNCTIONAL_TEST_RESULTS.json")
        
        # Determine overall status
        if failed_tests == 0:
            print(f"\n🎉 ALL TESTS PASSED! Platform is ready for production.")
            return True
        else:
            print(f"\n⚠️ {failed_tests} tests failed. Review issues before production deployment.")
            return False

    async def run_all_tests(self):
        """Run all functional tests"""
        print("🚀 STARTING COMPREHENSIVE FUNCTIONAL TESTING")
        print("="*80)
        print(f"🕐 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Backend URL: {BASE_URL}")
        print("="*80)
        
        try:
            # Run all test modules
            await self.test_authentication()
            await self.test_seller_module()
            await self.test_customer_module()
            await self.test_admin_module()
            await self.test_error_handling()
            
            # Generate final report
            success = await self.generate_report()
            
            return success
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR during testing: {str(e)}")
            return False
        finally:
            await self.client.aclose()

async def main():
    """Main test execution"""
    tester = HyperlocalTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🔥 FUNCTIONAL TESTING COMPLETED SUCCESSFULLY!")
        exit(0)
    else:
        print("\n💥 FUNCTIONAL TESTING COMPLETED WITH ISSUES!")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())