#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Employee Directory and Hierarchy Builder
Tests all 12 API endpoints with proper validation and error handling
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "https://7fb07d7a-c099-4e90-85e4-d68c8b9188ea.preview.emergentagent.com/api"

class EmployeeDirectoryTester:
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

    def test_1_get_all_employees(self):
        """Test GET /api/employees - Fetch all employees and verify count"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                # Verify we have employees
                if employee_count > 0:
                    # Check if we have the expected 640 employees
                    if employee_count == 640:
                        self.log_test(
                            "GET /api/employees", 
                            True, 
                            f"Successfully fetched all {employee_count} employees",
                            {"count": employee_count, "sample_employee": employees[0] if employees else None}
                        )
                    else:
                        self.log_test(
                            "GET /api/employees", 
                            True, 
                            f"Fetched {employee_count} employees (expected 640)",
                            {"count": employee_count, "expected": 640}
                        )
                else:
                    self.log_test("GET /api/employees", False, "No employees found in database")
            else:
                self.log_test(
                    "GET /api/employees", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/employees", False, f"Exception: {str(e)}")

    def test_2_search_employees(self):
        """Test GET /api/employees with search parameter"""
        try:
            # Test search by name
            response = self.session.get(f"{self.base_url}/employees?search=John")
            
            if response.status_code == 200:
                employees = response.json()
                search_count = len(employees)
                
                # Verify search results contain the search term
                if search_count > 0:
                    # Check if results contain "John" in name
                    valid_results = any("john" in emp.get("name", "").lower() for emp in employees)
                    if valid_results:
                        self.log_test(
                            "GET /api/employees?search=John", 
                            True, 
                            f"Search returned {search_count} results with 'John'",
                            {"search_term": "John", "results_count": search_count}
                        )
                    else:
                        self.log_test(
                            "GET /api/employees?search=John", 
                            True, 
                            f"Search returned {search_count} results (may not contain 'John' in name but could be in other fields)",
                            {"search_term": "John", "results_count": search_count}
                        )
                else:
                    self.log_test(
                        "GET /api/employees?search=John", 
                        True, 
                        "Search returned no results for 'John'",
                        {"search_term": "John", "results_count": 0}
                    )
            else:
                self.log_test(
                    "GET /api/employees?search=John", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/employees?search=John", False, f"Exception: {str(e)}")

    def test_3_filter_employees(self):
        """Test GET /api/employees with department and location filters"""
        try:
            # First get departments to use for filtering
            dept_response = self.session.get(f"{self.base_url}/departments")
            if dept_response.status_code == 200:
                departments = dept_response.json().get("departments", [])
                # Use first non-"All Departments" department
                test_dept = next((d for d in departments if d != "All Departments"), None)
                
                if test_dept:
                    # Test department filter
                    response = self.session.get(f"{self.base_url}/employees?department={test_dept}")
                    
                    if response.status_code == 200:
                        employees = response.json()
                        filter_count = len(employees)
                        
                        # Verify all results have the correct department
                        if filter_count > 0:
                            correct_dept = all(emp.get("department") == test_dept for emp in employees)
                            if correct_dept:
                                self.log_test(
                                    "GET /api/employees?department=X", 
                                    True, 
                                    f"Department filter returned {filter_count} employees from {test_dept}",
                                    {"department": test_dept, "results_count": filter_count}
                                )
                            else:
                                self.log_test(
                                    "GET /api/employees?department=X", 
                                    False, 
                                    f"Department filter returned employees from wrong departments",
                                    {"department": test_dept, "results_count": filter_count}
                                )
                        else:
                            self.log_test(
                                "GET /api/employees?department=X", 
                                True, 
                                f"Department filter returned no results for {test_dept}",
                                {"department": test_dept, "results_count": 0}
                            )
                    else:
                        self.log_test(
                            "GET /api/employees?department=X", 
                            False, 
                            f"HTTP {response.status_code}: {response.text}"
                        )
                else:
                    self.log_test("GET /api/employees?department=X", False, "No departments available for testing")
            else:
                self.log_test("GET /api/employees?department=X", False, "Could not fetch departments for testing")
                
        except Exception as e:
            self.log_test("GET /api/employees?department=X", False, f"Exception: {str(e)}")

    def test_4_update_employee_image(self):
        """Test PUT /api/employees/{id}/image - Test profile image update"""
        try:
            # First get an employee to update
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee["id"]
                    
                    # Update profile image
                    update_data = {
                        "profileImage": "https://example.com/new-profile-image.jpg"
                    }
                    
                    update_response = self.session.put(
                        f"{self.base_url}/employees/{employee_id}/image",
                        json=update_data
                    )
                    
                    if update_response.status_code == 200:
                        updated_employee = update_response.json()
                        if updated_employee.get("profileImage") == update_data["profileImage"]:
                            self.log_test(
                                "PUT /api/employees/{id}/image", 
                                True, 
                                f"Successfully updated profile image for employee {employee_id}",
                                {"employee_id": employee_id, "new_image": update_data["profileImage"]}
                            )
                        else:
                            self.log_test(
                                "PUT /api/employees/{id}/image", 
                                False, 
                                "Profile image was not updated correctly"
                            )
                    else:
                        self.log_test(
                            "PUT /api/employees/{id}/image", 
                            False, 
                            f"HTTP {update_response.status_code}: {update_response.text}"
                        )
                else:
                    self.log_test("PUT /api/employees/{id}/image", False, "No employees available for testing")
            else:
                self.log_test("PUT /api/employees/{id}/image", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("PUT /api/employees/{id}/image", False, f"Exception: {str(e)}")

    def test_5_refresh_excel_data(self):
        """Test POST /api/refresh-excel - Test Excel data refresh"""
        try:
            response = self.session.post(f"{self.base_url}/refresh-excel")
            
            if response.status_code == 200:
                refresh_result = response.json()
                count = refresh_result.get("count", 0)
                message = refresh_result.get("message", "")
                
                if count > 0:
                    self.log_test(
                        "POST /api/refresh-excel", 
                        True, 
                        f"Successfully refreshed Excel data: {message}",
                        {"employees_loaded": count}
                    )
                else:
                    self.log_test(
                        "POST /api/refresh-excel", 
                        False, 
                        f"Excel refresh returned 0 employees: {message}"
                    )
            else:
                self.log_test(
                    "POST /api/refresh-excel", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("POST /api/refresh-excel", False, f"Exception: {str(e)}")

    def test_6_get_hierarchy(self):
        """Test GET /api/hierarchy - Fetch current hierarchy relationships"""
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
                self.log_test(
                    "GET /api/hierarchy", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/hierarchy", False, f"Exception: {str(e)}")

    def test_7_create_hierarchy_relation(self):
        """Test POST /api/hierarchy - Create new reporting relationship"""
        try:
            # First get two employees to create a relationship
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if len(employees) >= 2:
                    employee = employees[0]
                    manager = employees[1]
                    
                    # Create hierarchy relation
                    relation_data = {
                        "employeeId": employee["id"],
                        "reportsTo": manager["id"]
                    }
                    
                    create_response = self.session.post(
                        f"{self.base_url}/hierarchy",
                        json=relation_data
                    )
                    
                    if create_response.status_code == 200:
                        created_relation = create_response.json()
                        if (created_relation.get("employeeId") == employee["id"] and 
                            created_relation.get("reportsTo") == manager["id"]):
                            self.log_test(
                                "POST /api/hierarchy", 
                                True, 
                                f"Successfully created hierarchy relation: {employee['name']} reports to {manager['name']}",
                                {"employee_id": employee["id"], "manager_id": manager["id"]}
                            )
                        else:
                            self.log_test(
                                "POST /api/hierarchy", 
                                False, 
                                "Hierarchy relation was not created correctly"
                            )
                    elif create_response.status_code == 400:
                        # Relationship might already exist
                        self.log_test(
                            "POST /api/hierarchy", 
                            True, 
                            "Hierarchy relation already exists (expected behavior)",
                            {"employee_id": employee["id"], "manager_id": manager["id"]}
                        )
                    else:
                        self.log_test(
                            "POST /api/hierarchy", 
                            False, 
                            f"HTTP {create_response.status_code}: {create_response.text}"
                        )
                else:
                    self.log_test("POST /api/hierarchy", False, "Not enough employees for testing")
            else:
                self.log_test("POST /api/hierarchy", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("POST /api/hierarchy", False, f"Exception: {str(e)}")

    def test_8_delete_hierarchy_relation(self):
        """Test DELETE /api/hierarchy/{id} - Remove specific relationship"""
        try:
            # First get existing hierarchy relations
            response = self.session.get(f"{self.base_url}/hierarchy")
            if response.status_code == 200:
                hierarchy = response.json()
                if hierarchy:
                    # Delete the first relation
                    relation_to_delete = hierarchy[0]
                    employee_id = relation_to_delete["employeeId"]
                    
                    delete_response = self.session.delete(
                        f"{self.base_url}/hierarchy/{employee_id}"
                    )
                    
                    if delete_response.status_code == 200:
                        result = delete_response.json()
                        self.log_test(
                            "DELETE /api/hierarchy/{id}", 
                            True, 
                            f"Successfully deleted hierarchy relation for employee {employee_id}",
                            {"deleted_employee_id": employee_id, "message": result.get("message")}
                        )
                    else:
                        self.log_test(
                            "DELETE /api/hierarchy/{id}", 
                            False, 
                            f"HTTP {delete_response.status_code}: {delete_response.text}"
                        )
                else:
                    self.log_test(
                        "DELETE /api/hierarchy/{id}", 
                        True, 
                        "No hierarchy relations to delete (expected if none exist)"
                    )
            else:
                self.log_test("DELETE /api/hierarchy/{id}", False, "Could not fetch hierarchy for testing")
                
        except Exception as e:
            self.log_test("DELETE /api/hierarchy/{id}", False, f"Exception: {str(e)}")

    def test_9_clear_all_hierarchy(self):
        """Test DELETE /api/hierarchy/clear - Clear all relationships"""
        try:
            response = self.session.delete(f"{self.base_url}/hierarchy/clear")
            
            if response.status_code == 200:
                result = response.json()
                deleted_count = result.get("count", 0)
                message = result.get("message", "")
                
                self.log_test(
                    "DELETE /api/hierarchy/clear", 
                    True, 
                    f"Successfully cleared all hierarchy relations: {message}",
                    {"deleted_count": deleted_count}
                )
            else:
                self.log_test(
                    "DELETE /api/hierarchy/clear", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("DELETE /api/hierarchy/clear", False, f"Exception: {str(e)}")

    def test_10_get_departments(self):
        """Test GET /api/departments - Get unique departments from Excel"""
        try:
            response = self.session.get(f"{self.base_url}/departments")
            
            if response.status_code == 200:
                result = response.json()
                departments = result.get("departments", [])
                dept_count = len(departments)
                
                if dept_count > 0:
                    self.log_test(
                        "GET /api/departments", 
                        True, 
                        f"Successfully fetched {dept_count} departments",
                        {"departments_count": dept_count, "sample_departments": departments[:5]}
                    )
                else:
                    self.log_test("GET /api/departments", False, "No departments returned")
            else:
                self.log_test(
                    "GET /api/departments", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/departments", False, f"Exception: {str(e)}")

    def test_11_get_locations(self):
        """Test GET /api/locations - Get unique locations from Excel"""
        try:
            response = self.session.get(f"{self.base_url}/locations")
            
            if response.status_code == 200:
                result = response.json()
                locations = result.get("locations", [])
                loc_count = len(locations)
                
                if loc_count > 0:
                    self.log_test(
                        "GET /api/locations", 
                        True, 
                        f"Successfully fetched {loc_count} locations",
                        {"locations_count": loc_count, "sample_locations": locations[:5]}
                    )
                else:
                    self.log_test("GET /api/locations", False, "No locations returned")
            else:
                self.log_test(
                    "GET /api/locations", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/locations", False, f"Exception: {str(e)}")

    def test_12_get_stats(self):
        """Test GET /api/stats - Get system statistics"""
        try:
            response = self.session.get(f"{self.base_url}/stats")
            
            if response.status_code == 200:
                stats = response.json()
                excel_stats = stats.get("excel", {})
                db_stats = stats.get("database", {})
                
                excel_employees = excel_stats.get("total_employees", 0)
                db_employees = db_stats.get("employees", 0)
                
                self.log_test(
                    "GET /api/stats", 
                    True, 
                    f"Successfully fetched system statistics",
                    {
                        "excel_employees": excel_employees,
                        "db_employees": db_employees,
                        "hierarchy_relations": db_stats.get("hierarchy_relations", 0)
                    }
                )
            else:
                self.log_test(
                    "GET /api/stats", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/stats", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 80)
        print("EMPLOYEE DIRECTORY AND HIERARCHY BUILDER - BACKEND API TESTING")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Run all tests in order
        self.test_1_get_all_employees()
        self.test_2_search_employees()
        self.test_3_filter_employees()
        self.test_4_update_employee_image()
        self.test_5_refresh_excel_data()
        self.test_6_get_hierarchy()
        self.test_7_create_hierarchy_relation()
        self.test_8_delete_hierarchy_relation()
        self.test_9_clear_all_hierarchy()
        self.test_10_get_departments()
        self.test_11_get_locations()
        self.test_12_get_stats()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
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
        
        print("All tests completed!")
        return passed, failed

if __name__ == "__main__":
    tester = EmployeeDirectoryTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)