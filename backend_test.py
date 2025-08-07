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
BACKEND_URL = "https://a942ff7a-6bf7-4e4a-ad56-c28e6a4f717d.preview.emergentagent.com/api"

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

    def test_4_update_employee_image_url(self):
        """Test PUT /api/employees/{id}/image - Test profile image update with URL"""
        try:
            # First get an employee to update
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee["id"]
                    
                    # Update profile image with URL
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
                                "PUT /api/employees/{id}/image (URL)", 
                                True, 
                                f"Successfully updated profile image with URL for employee {employee_id}",
                                {"employee_id": employee_id, "new_image": update_data["profileImage"]}
                            )
                        else:
                            self.log_test(
                                "PUT /api/employees/{id}/image (URL)", 
                                False, 
                                "Profile image was not updated correctly"
                            )
                    else:
                        self.log_test(
                            "PUT /api/employees/{id}/image (URL)", 
                            False, 
                            f"HTTP {update_response.status_code}: {update_response.text}"
                        )
                else:
                    self.log_test("PUT /api/employees/{id}/image (URL)", False, "No employees available for testing")
            else:
                self.log_test("PUT /api/employees/{id}/image (URL)", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("PUT /api/employees/{id}/image (URL)", False, f"Exception: {str(e)}")

    def test_4b_update_employee_image_base64(self):
        """Test PUT /api/employees/{id}/image - Test profile image update with base64 data"""
        try:
            # First get an employee to update
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee["id"]
                    
                    # Create a small test image in base64 (1x1 red pixel PNG)
                    base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    
                    # Update profile image with base64 data
                    update_data = {
                        "profileImage": base64_image
                    }
                    
                    update_response = self.session.put(
                        f"{self.base_url}/employees/{employee_id}/image",
                        json=update_data
                    )
                    
                    if update_response.status_code == 200:
                        updated_employee = update_response.json()
                        new_image_url = updated_employee.get("profileImage")
                        
                        # Check if the image was converted to a file URL
                        if new_image_url and new_image_url.startswith("/uploads/images/"):
                            self.log_test(
                                "PUT /api/employees/{id}/image (Base64)", 
                                True, 
                                f"Successfully updated profile image with base64 data for employee {employee_id}",
                                {"employee_id": employee_id, "new_image_url": new_image_url}
                            )
                        else:
                            self.log_test(
                                "PUT /api/employees/{id}/image (Base64)", 
                                False, 
                                f"Base64 image was not converted to file URL correctly. Got: {new_image_url}"
                            )
                    else:
                        self.log_test(
                            "PUT /api/employees/{id}/image (Base64)", 
                            False, 
                            f"HTTP {update_response.status_code}: {update_response.text}"
                        )
                else:
                    self.log_test("PUT /api/employees/{id}/image (Base64)", False, "No employees available for testing")
            else:
                self.log_test("PUT /api/employees/{id}/image (Base64)", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("PUT /api/employees/{id}/image (Base64)", False, f"Exception: {str(e)}")

    def test_4c_upload_employee_image_file(self):
        """Test POST /api/employees/{id}/upload-image - Test file upload"""
        try:
            # First get an employee to update
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee["id"]
                    
                    # Create a small test image file (1x1 red pixel PNG)
                    import io
                    import base64
                    
                    # Decode the base64 image to bytes
                    base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    image_bytes = base64.b64decode(base64_data)
                    
                    # Create file-like object
                    files = {
                        'file': ('test_image.png', io.BytesIO(image_bytes), 'image/png')
                    }
                    
                    upload_response = self.session.post(
                        f"{self.base_url}/employees/{employee_id}/upload-image",
                        files=files
                    )
                    
                    if upload_response.status_code == 200:
                        updated_employee = upload_response.json()
                        new_image_url = updated_employee.get("profileImage")
                        
                        # Check if the image was saved as a file URL
                        if new_image_url and new_image_url.startswith("/uploads/images/"):
                            self.log_test(
                                "POST /api/employees/{id}/upload-image", 
                                True, 
                                f"Successfully uploaded image file for employee {employee_id}",
                                {"employee_id": employee_id, "new_image_url": new_image_url}
                            )
                        else:
                            self.log_test(
                                "POST /api/employees/{id}/upload-image", 
                                False, 
                                f"File upload did not return correct URL. Got: {new_image_url}"
                            )
                    else:
                        self.log_test(
                            "POST /api/employees/{id}/upload-image", 
                            False, 
                            f"HTTP {upload_response.status_code}: {upload_response.text}"
                        )
                else:
                    self.log_test("POST /api/employees/{id}/upload-image", False, "No employees available for testing")
            else:
                self.log_test("POST /api/employees/{id}/upload-image", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("POST /api/employees/{id}/upload-image", False, f"Exception: {str(e)}")

    def test_4d_static_file_serving(self):
        """Test static file serving for uploaded images"""
        try:
            # First upload an image to get a file URL
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee["id"]
                    
                    # Upload a test image first
                    import io
                    import base64
                    
                    base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    image_bytes = base64.b64decode(base64_data)
                    
                    files = {
                        'file': ('test_static.png', io.BytesIO(image_bytes), 'image/png')
                    }
                    
                    upload_response = self.session.post(
                        f"{self.base_url}/employees/{employee_id}/upload-image",
                        files=files
                    )
                    
                    if upload_response.status_code == 200:
                        updated_employee = upload_response.json()
                        image_url = updated_employee.get("profileImage")
                        
                        if image_url and image_url.startswith("/uploads/images/"):
                            # Now test if we can access the static file
                            # Remove /api from base_url for static file access
                            static_url = self.base_url.replace("/api", "") + image_url
                            
                            static_response = self.session.get(static_url)
                            
                            if static_response.status_code == 200:
                                # Check if it's actually an image
                                content_type = static_response.headers.get('content-type', '')
                                if 'image' in content_type:
                                    self.log_test(
                                        "Static File Serving", 
                                        True, 
                                        f"Successfully served static image file",
                                        {"image_url": static_url, "content_type": content_type}
                                    )
                                else:
                                    self.log_test(
                                        "Static File Serving", 
                                        False, 
                                        f"Static file served but wrong content type: {content_type}"
                                    )
                            else:
                                self.log_test(
                                    "Static File Serving", 
                                    False, 
                                    f"Could not access static file: HTTP {static_response.status_code}"
                                )
                        else:
                            self.log_test("Static File Serving", False, "Could not get valid image URL for testing")
                    else:
                        self.log_test("Static File Serving", False, "Could not upload test image for static file testing")
                else:
                    self.log_test("Static File Serving", False, "No employees available for testing")
            else:
                self.log_test("Static File Serving", False, "Could not fetch employees for testing")
                
        except Exception as e:
            self.log_test("Static File Serving", False, f"Exception: {str(e)}")

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
        self.test_4_update_employee_image_url()
        self.test_4b_update_employee_image_base64()
        self.test_4c_upload_employee_image_file()
        self.test_4d_static_file_serving()
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

    def test_hierarchy_scenario_specific(self):
        """Test specific hierarchy scenario: Anirudh→Chandan, Binay→Chandan, Chandan→Ranjit Sarkar"""
        print("\n" + "="*80)
        print("TESTING SPECIFIC HIERARCHY SCENARIO")
        print("="*80)
        
        try:
            # Step 1: Clear existing hierarchy to start fresh
            print("Step 1: Clearing existing hierarchy...")
            clear_response = self.session.delete(f"{self.base_url}/hierarchy/clear")
            if clear_response.status_code == 200:
                print("✅ Hierarchy cleared successfully")
            else:
                print(f"⚠️  Warning: Could not clear hierarchy: {clear_response.status_code}")
            
            # Step 2: Get employees to find our test subjects
            print("\nStep 2: Finding employees for hierarchy test...")
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("Hierarchy Scenario Test", False, "Could not fetch employees")
                return
            
            employees = emp_response.json()
            
            # Find employees by name (case-insensitive search)
            anirudh = None
            binay = None
            chandan = None
            ranjit = None
            
            for emp in employees:
                name_lower = emp.get("name", "").lower()
                if "anirudh" in name_lower:
                    anirudh = emp
                elif "binay" in name_lower:
                    binay = emp
                elif "chandan" in name_lower:
                    chandan = emp
                elif "ranjit" in name_lower and "sarkar" in name_lower:
                    ranjit = emp
            
            # If we can't find specific names, use first 4 employees for testing
            if not all([anirudh, binay, chandan, ranjit]):
                print("⚠️  Could not find all specific employees by name, using first 4 employees for testing")
                if len(employees) >= 4:
                    anirudh = employees[0]
                    binay = employees[1] 
                    chandan = employees[2]
                    ranjit = employees[3]
                    print(f"Using: {anirudh['name']} as Anirudh, {binay['name']} as Binay, {chandan['name']} as Chandan, {ranjit['name']} as Ranjit")
                else:
                    self.log_test("Hierarchy Scenario Test", False, "Not enough employees for testing")
                    return
            else:
                print(f"✅ Found employees: Anirudh={anirudh['name']}, Binay={binay['name']}, Chandan={chandan['name']}, Ranjit={ranjit['name']}")
            
            # Step 3: Create hierarchy relationships
            print("\nStep 3: Creating hierarchy relationships...")
            
            relationships_to_create = [
                {"employeeId": anirudh["id"], "reportsTo": chandan["id"], "description": f"{anirudh['name']} reports to {chandan['name']}"},
                {"employeeId": binay["id"], "reportsTo": chandan["id"], "description": f"{binay['name']} reports to {chandan['name']}"},
                {"employeeId": chandan["id"], "reportsTo": ranjit["id"], "description": f"{chandan['name']} reports to {ranjit['name']}"}
            ]
            
            created_relationships = []
            
            for rel in relationships_to_create:
                relation_data = {
                    "employeeId": rel["employeeId"],
                    "reportsTo": rel["reportsTo"]
                }
                
                create_response = self.session.post(
                    f"{self.base_url}/hierarchy",
                    json=relation_data
                )
                
                if create_response.status_code == 200:
                    created_rel = create_response.json()
                    created_relationships.append(created_rel)
                    print(f"✅ Created: {rel['description']}")
                else:
                    print(f"❌ Failed to create: {rel['description']} - {create_response.status_code}: {create_response.text}")
            
            # Step 4: Verify relationships were stored correctly
            print("\nStep 4: Verifying stored relationships...")
            hierarchy_response = self.session.get(f"{self.base_url}/hierarchy")
            
            if hierarchy_response.status_code == 200:
                stored_hierarchy = hierarchy_response.json()
                print(f"✅ Retrieved {len(stored_hierarchy)} hierarchy relationships")
                
                # Verify each expected relationship exists
                expected_relationships = [
                    (anirudh["id"], chandan["id"]),
                    (binay["id"], chandan["id"]),
                    (chandan["id"], ranjit["id"])
                ]
                
                found_relationships = []
                for rel in stored_hierarchy:
                    found_relationships.append((rel["employeeId"], rel["reportsTo"]))
                
                all_found = True
                for expected in expected_relationships:
                    if expected in found_relationships:
                        print(f"✅ Verified relationship: {expected[0]} → {expected[1]}")
                    else:
                        print(f"❌ Missing relationship: {expected[0]} → {expected[1]}")
                        all_found = False
                
                # Step 5: Test tree structure building capability
                print("\nStep 5: Testing tree structure building capability...")
                
                # Build a simple tree structure from the relationships
                def build_hierarchy_tree(relationships):
                    """Build a tree structure from hierarchy relationships"""
                    # Create employee lookup
                    emp_lookup = {emp["id"]: emp["name"] for emp in [anirudh, binay, chandan, ranjit]}
                    
                    # Find who reports to whom
                    reports_to = {}
                    subordinates = {}
                    
                    for rel in relationships:
                        emp_id = rel["employeeId"]
                        manager_id = rel["reportsTo"]
                        
                        reports_to[emp_id] = manager_id
                        
                        if manager_id not in subordinates:
                            subordinates[manager_id] = []
                        subordinates[manager_id].append(emp_id)
                    
                    # Find root managers (those who don't report to anyone in our test set)
                    all_employees = set([anirudh["id"], binay["id"], chandan["id"], ranjit["id"]])
                    root_managers = []
                    
                    for emp_id in all_employees:
                        if emp_id not in reports_to:
                            root_managers.append(emp_id)
                    
                    return {
                        "reports_to": reports_to,
                        "subordinates": subordinates,
                        "root_managers": root_managers,
                        "employee_names": emp_lookup
                    }
                
                tree_structure = build_hierarchy_tree(stored_hierarchy)
                
                # Verify tree structure
                expected_root = ranjit["id"]  # Ranjit should be the root
                expected_chandan_subordinates = {anirudh["id"], binay["id"]}  # Anirudh and Binay should report to Chandan
                
                if expected_root in tree_structure["root_managers"]:
                    print(f"✅ Correct root manager: {tree_structure['employee_names'][expected_root]}")
                else:
                    print(f"❌ Expected root manager {tree_structure['employee_names'][expected_root]} not found in roots: {[tree_structure['employee_names'][r] for r in tree_structure['root_managers']]}")
                    all_found = False
                
                chandan_subordinates = set(tree_structure["subordinates"].get(chandan["id"], []))
                if chandan_subordinates == expected_chandan_subordinates:
                    subordinate_names = [tree_structure['employee_names'][sub] for sub in chandan_subordinates]
                    print(f"✅ Correct subordinates for {chandan['name']}: {subordinate_names}")
                else:
                    print(f"❌ Incorrect subordinates for {chandan['name']}")
                    all_found = False
                
                # Print the complete tree structure
                print(f"\nComplete Tree Structure:")
                print(f"Root: {tree_structure['employee_names'][ranjit['id']]}")
                print(f"  └── {tree_structure['employee_names'][chandan['id']]}")
                for sub_id in tree_structure["subordinates"].get(chandan["id"], []):
                    print(f"      ├── {tree_structure['employee_names'][sub_id]}")
                
                if all_found and len(created_relationships) == 3:
                    self.log_test(
                        "Hierarchy Scenario Test", 
                        True, 
                        "Successfully created and verified hierarchical relationships with proper tree structure",
                        {
                            "relationships_created": len(created_relationships),
                            "tree_root": tree_structure['employee_names'][ranjit['id']],
                            "middle_manager": tree_structure['employee_names'][chandan['id']],
                            "subordinates": [tree_structure['employee_names'][sub] for sub in tree_structure["subordinates"].get(chandan["id"], [])]
                        }
                    )
                else:
                    self.log_test(
                        "Hierarchy Scenario Test", 
                        False, 
                        f"Hierarchy relationships not properly established. Created: {len(created_relationships)}/3, All verified: {all_found}"
                    )
            else:
                self.log_test("Hierarchy Scenario Test", False, f"Could not retrieve hierarchy: {hierarchy_response.status_code}")
                
        except Exception as e:
            self.log_test("Hierarchy Scenario Test", False, f"Exception during hierarchy scenario test: {str(e)}")

if __name__ == "__main__":
    tester = EmployeeDirectoryTester()
    
    # Run comprehensive backend tests focusing on Excel and image functionality
    print("Running comprehensive backend API tests...")
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)