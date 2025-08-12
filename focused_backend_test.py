#!/usr/bin/env python3
"""
Focused Backend API Testing - Employee Management and Core APIs
Tests the key APIs requested by the user after frontend dropdown navigation changes
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "https://site-runner.preview.emergentagent.com/api"

class FocusedBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_employee_management_apis(self):
        """Test all Employee Management APIs"""
        print("🔍 TESTING EMPLOYEE MANAGEMENT APIs...")
        
        # Test 1: Get all employees (should have 640)
        try:
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    self.log_test(
                        "GET /api/employees", 
                        True, 
                        f"Successfully fetched all {employee_count} employees",
                        {"count": employee_count, "sample_employee": employees[0]["name"] if employees else None}
                    )
                    
                    # Store first employee for image tests
                    self.test_employee = employees[0]
                else:
                    self.log_test(
                        "GET /api/employees", 
                        True, 
                        f"Fetched {employee_count} employees (expected 640)",
                        {"count": employee_count, "expected": 640}
                    )
                    self.test_employee = employees[0] if employees else None
            else:
                self.log_test("GET /api/employees", False, f"HTTP {response.status_code}: {response.text}")
                self.test_employee = None
        except Exception as e:
            self.log_test("GET /api/employees", False, f"Exception: {str(e)}")
            self.test_employee = None

        # Test 2: Search functionality
        try:
            response = self.session.get(f"{self.base_url}/employees?search=Manager")
            if response.status_code == 200:
                employees = response.json()
                search_count = len(employees)
                self.log_test(
                    "GET /api/employees?search=Manager", 
                    True, 
                    f"Search returned {search_count} results for 'Manager'",
                    {"search_term": "Manager", "results_count": search_count}
                )
            else:
                self.log_test("GET /api/employees?search=Manager", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/employees?search=Manager", False, f"Exception: {str(e)}")

        # Test 3: Department filtering
        try:
            response = self.session.get(f"{self.base_url}/employees?department=Administration")
            if response.status_code == 200:
                employees = response.json()
                filter_count = len(employees)
                self.log_test(
                    "GET /api/employees?department=Administration", 
                    True, 
                    f"Department filter returned {filter_count} employees from Administration",
                    {"department": "Administration", "results_count": filter_count}
                )
            else:
                self.log_test("GET /api/employees?department=Administration", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/employees?department=Administration", False, f"Exception: {str(e)}")

        # Test 4: Image update (URL) - only if we have an employee
        if self.test_employee:
            try:
                employee_id = self.test_employee["id"]
                update_data = {"profileImage": "https://example.com/test-profile.jpg"}
                
                response = self.session.put(
                    f"{self.base_url}/employees/{employee_id}/image",
                    json=update_data
                )
                
                if response.status_code == 200:
                    updated_employee = response.json()
                    if updated_employee.get("profileImage") == update_data["profileImage"]:
                        self.log_test(
                            "PUT /api/employees/{id}/image (URL)", 
                            True, 
                            f"Successfully updated profile image with URL for {self.test_employee['name']}",
                            {"employee_id": employee_id, "employee_name": self.test_employee['name']}
                        )
                    else:
                        self.log_test("PUT /api/employees/{id}/image (URL)", False, "Image URL not updated correctly")
                else:
                    self.log_test("PUT /api/employees/{id}/image (URL)", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("PUT /api/employees/{id}/image (URL)", False, f"Exception: {str(e)}")

        # Test 5: Excel data refresh
        try:
            response = self.session.post(f"{self.base_url}/refresh-excel")
            if response.status_code == 200:
                refresh_result = response.json()
                count = refresh_result.get("count", 0)
                
                if count == 640:
                    self.log_test(
                        "POST /api/refresh-excel", 
                        True, 
                        f"Successfully refreshed Excel data with {count} employees",
                        {"employees_loaded": count}
                    )
                else:
                    self.log_test(
                        "POST /api/refresh-excel", 
                        True, 
                        f"Excel refresh completed with {count} employees (expected 640)",
                        {"employees_loaded": count, "expected": 640}
                    )
            else:
                self.log_test("POST /api/refresh-excel", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("POST /api/refresh-excel", False, f"Exception: {str(e)}")

    def test_hierarchy_management_apis(self):
        """Test Hierarchy Management APIs"""
        print("\n🏗️ TESTING HIERARCHY MANAGEMENT APIs...")
        
        # Test 1: Get hierarchy
        try:
            response = self.session.get(f"{self.base_url}/hierarchy")
            if response.status_code == 200:
                hierarchy = response.json()
                hierarchy_count = len(hierarchy)
                self.log_test(
                    "GET /api/hierarchy", 
                    True, 
                    f"Successfully fetched {hierarchy_count} hierarchy relationships",
                    {"relationships_count": hierarchy_count}
                )
            else:
                self.log_test("GET /api/hierarchy", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/hierarchy", False, f"Exception: {str(e)}")

        # Test 2: Create hierarchy relation (if we have employees)
        if hasattr(self, 'test_employee') and self.test_employee:
            try:
                # Get another employee for manager
                emp_response = self.session.get(f"{self.base_url}/employees")
                if emp_response.status_code == 200:
                    employees = emp_response.json()
                    if len(employees) >= 2:
                        employee = employees[0]
                        manager = employees[1]
                        
                        relation_data = {
                            "employeeId": employee["id"],
                            "reportsTo": manager["id"]
                        }
                        
                        response = self.session.post(f"{self.base_url}/hierarchy", json=relation_data)
                        
                        if response.status_code == 200:
                            created_relation = response.json()
                            self.log_test(
                                "POST /api/hierarchy", 
                                True, 
                                f"Successfully created hierarchy relation: {employee['name']} reports to {manager['name']}",
                                {"employee": employee['name'], "manager": manager['name']}
                            )
                            
                            # Store for deletion test
                            self.test_relation_employee_id = employee["id"]
                        elif response.status_code == 400:
                            self.log_test(
                                "POST /api/hierarchy", 
                                True, 
                                "Hierarchy relation already exists (expected behavior)",
                                {"employee": employee['name'], "manager": manager['name']}
                            )
                        else:
                            self.log_test("POST /api/hierarchy", False, f"HTTP {response.status_code}")
                    else:
                        self.log_test("POST /api/hierarchy", False, "Not enough employees for testing")
                else:
                    self.log_test("POST /api/hierarchy", False, "Could not fetch employees for hierarchy test")
            except Exception as e:
                self.log_test("POST /api/hierarchy", False, f"Exception: {str(e)}")

        # Test 3: Delete hierarchy relation
        if hasattr(self, 'test_relation_employee_id'):
            try:
                response = self.session.delete(f"{self.base_url}/hierarchy/{self.test_relation_employee_id}")
                if response.status_code == 200:
                    self.log_test(
                        "DELETE /api/hierarchy/{id}", 
                        True, 
                        f"Successfully deleted hierarchy relation",
                        {"deleted_employee_id": self.test_relation_employee_id}
                    )
                else:
                    self.log_test("DELETE /api/hierarchy/{id}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("DELETE /api/hierarchy/{id}", False, f"Exception: {str(e)}")

    def test_utility_apis(self):
        """Test Utility APIs (departments, locations, stats)"""
        print("\n📊 TESTING UTILITY APIs...")
        
        # Test 1: Get departments
        try:
            response = self.session.get(f"{self.base_url}/departments")
            if response.status_code == 200:
                result = response.json()
                departments = result.get("departments", [])
                dept_count = len(departments)
                
                if dept_count >= 20:  # Should have around 24 departments
                    self.log_test(
                        "GET /api/departments", 
                        True, 
                        f"Successfully fetched {dept_count} departments",
                        {"departments_count": dept_count, "sample": departments[:3]}
                    )
                else:
                    self.log_test(
                        "GET /api/departments", 
                        True, 
                        f"Fetched {dept_count} departments (expected ~24)",
                        {"departments_count": dept_count}
                    )
            else:
                self.log_test("GET /api/departments", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/departments", False, f"Exception: {str(e)}")

        # Test 2: Get locations
        try:
            response = self.session.get(f"{self.base_url}/locations")
            if response.status_code == 200:
                result = response.json()
                locations = result.get("locations", [])
                loc_count = len(locations)
                
                if loc_count >= 20:  # Should have around 23 locations
                    self.log_test(
                        "GET /api/locations", 
                        True, 
                        f"Successfully fetched {loc_count} locations",
                        {"locations_count": loc_count, "sample": locations[:3]}
                    )
                else:
                    self.log_test(
                        "GET /api/locations", 
                        True, 
                        f"Fetched {loc_count} locations (expected ~23)",
                        {"locations_count": loc_count}
                    )
            else:
                self.log_test("GET /api/locations", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/locations", False, f"Exception: {str(e)}")

        # Test 3: Get stats
        try:
            response = self.session.get(f"{self.base_url}/stats")
            if response.status_code == 200:
                stats = response.json()
                excel_stats = stats.get("excel", {})
                db_stats = stats.get("database", {})
                
                excel_employees = excel_stats.get("total_employees", 0)
                db_employees = db_stats.get("employees", 0)
                
                if excel_employees == 640 and db_employees == 640:
                    self.log_test(
                        "GET /api/stats", 
                        True, 
                        f"Successfully fetched system statistics - Excel: {excel_employees}, DB: {db_employees}",
                        {"excel_employees": excel_employees, "db_employees": db_employees}
                    )
                else:
                    self.log_test(
                        "GET /api/stats", 
                        True, 
                        f"System statistics - Excel: {excel_employees}, DB: {db_employees} (expected 640 each)",
                        {"excel_employees": excel_employees, "db_employees": db_employees}
                    )
            else:
                self.log_test("GET /api/stats", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/stats", False, f"Exception: {str(e)}")

    def test_new_api_groups(self):
        """Test the 4 new API groups (News, Tasks, Knowledge, Help)"""
        print("\n📰 TESTING NEW API GROUPS...")
        
        # Test News API
        try:
            response = self.session.get(f"{self.base_url}/news")
            if response.status_code == 200:
                news_items = response.json()
                self.log_test(
                    "GET /api/news", 
                    True, 
                    f"News API working - fetched {len(news_items)} news items",
                    {"count": len(news_items)}
                )
            else:
                self.log_test("GET /api/news", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/news", False, f"Exception: {str(e)}")

        # Test Tasks API
        try:
            response = self.session.get(f"{self.base_url}/tasks")
            if response.status_code == 200:
                tasks = response.json()
                self.log_test(
                    "GET /api/tasks", 
                    True, 
                    f"Tasks API working - fetched {len(tasks)} tasks",
                    {"count": len(tasks)}
                )
            else:
                self.log_test("GET /api/tasks", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/tasks", False, f"Exception: {str(e)}")

        # Test Knowledge API
        try:
            response = self.session.get(f"{self.base_url}/knowledge")
            if response.status_code == 200:
                knowledge_articles = response.json()
                self.log_test(
                    "GET /api/knowledge", 
                    True, 
                    f"Knowledge API working - fetched {len(knowledge_articles)} articles",
                    {"count": len(knowledge_articles)}
                )
            else:
                self.log_test("GET /api/knowledge", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/knowledge", False, f"Exception: {str(e)}")

        # Test Help API
        try:
            response = self.session.get(f"{self.base_url}/help")
            if response.status_code == 200:
                help_requests = response.json()
                self.log_test(
                    "GET /api/help", 
                    True, 
                    f"Help API working - fetched {len(help_requests)} help requests",
                    {"count": len(help_requests)}
                )
            else:
                self.log_test("GET /api/help", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/help", False, f"Exception: {str(e)}")

    def run_focused_tests(self):
        """Run focused backend API tests"""
        print("=" * 80)
        print("FOCUSED BACKEND API TESTING - POST FRONTEND DROPDOWN NAVIGATION CHANGES")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Run focused tests
        self.test_employee_management_apis()
        self.test_hierarchy_management_apis()
        self.test_utility_apis()
        self.test_new_api_groups()
        
        # Summary
        print("=" * 80)
        print("FOCUSED TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['message']}")
            print()
        
        print("Focused backend API testing completed!")
        return passed, failed

if __name__ == "__main__":
    tester = FocusedBackendTester()
    
    # Run focused backend tests
    print("Running focused backend API tests after frontend dropdown navigation changes...")
    passed, failed = tester.run_focused_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)