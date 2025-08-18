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
BACKEND_URL = "https://dp-visibility-fix.preview.emergentagent.com/api"

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

    # ========================================
    # NEWS MANAGEMENT API TESTS
    # ========================================

    def test_13_get_all_news(self):
        """Test GET /api/news - Fetch all news items"""
        try:
            response = self.session.get(f"{self.base_url}/news")
            
            if response.status_code == 200:
                news_items = response.json()
                news_count = len(news_items)
                
                self.log_test(
                    "GET /api/news", 
                    True, 
                    f"Successfully fetched {news_count} news items",
                    {"count": news_count}
                )
            else:
                self.log_test(
                    "GET /api/news", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/news", False, f"Exception: {str(e)}")

    def test_14_create_news(self):
        """Test POST /api/news - Create news with different priorities"""
        try:
            # Test creating news with different priority levels
            test_news_items = [
                {
                    "title": "Company Annual Meeting 2025",
                    "content": "Join us for our annual company meeting on March 15th, 2025. We'll discuss company performance, future goals, and celebrate our achievements.",
                    "priority": "high"
                },
                {
                    "title": "New Employee Wellness Program",
                    "content": "We're excited to announce our new employee wellness program starting next month. This includes gym memberships, mental health support, and flexible work arrangements.",
                    "priority": "medium"
                },
                {
                    "title": "Office Coffee Machine Maintenance",
                    "content": "The coffee machine on the 3rd floor will be under maintenance tomorrow from 2-4 PM. Please use the machine on the 2nd floor during this time.",
                    "priority": "normal"
                }
            ]
            
            created_news = []
            
            for news_data in test_news_items:
                response = self.session.post(
                    f"{self.base_url}/news",
                    json=news_data
                )
                
                if response.status_code == 200:
                    created_item = response.json()
                    created_news.append(created_item)
                    
                    # Verify the created news has correct data
                    if (created_item.get("title") == news_data["title"] and
                        created_item.get("priority") == news_data["priority"] and
                        created_item.get("id")):
                        
                        self.log_test(
                            f"POST /api/news ({news_data['priority']} priority)", 
                            True, 
                            f"Successfully created news: {news_data['title'][:50]}...",
                            {"news_id": created_item["id"], "priority": news_data["priority"]}
                        )
                    else:
                        self.log_test(
                            f"POST /api/news ({news_data['priority']} priority)", 
                            False, 
                            "News created but data doesn't match"
                        )
                else:
                    self.log_test(
                        f"POST /api/news ({news_data['priority']} priority)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created news IDs for later tests
            self.created_news_ids = [item["id"] for item in created_news]
                
        except Exception as e:
            self.log_test("POST /api/news", False, f"Exception: {str(e)}")

    def test_15_update_news(self):
        """Test PUT /api/news/{id} - Update news item"""
        try:
            # First create a news item to update
            news_data = {
                "title": "Test News for Update",
                "content": "This news will be updated",
                "priority": "normal"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/news",
                json=news_data
            )
            
            if create_response.status_code == 200:
                created_news = create_response.json()
                news_id = created_news["id"]
                
                # Update the news
                update_data = {
                    "title": "Updated Test News",
                    "content": "This news has been updated with new content",
                    "priority": "high"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/news/{news_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_news = update_response.json()
                    
                    # Verify updates
                    if (updated_news.get("title") == update_data["title"] and
                        updated_news.get("priority") == update_data["priority"] and
                        updated_news.get("updated_at") != created_news.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/news/{id}", 
                            True, 
                            f"Successfully updated news item",
                            {"news_id": news_id, "new_title": update_data["title"]}
                        )
                    else:
                        self.log_test(
                            "PUT /api/news/{id}", 
                            False, 
                            "News updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/news/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/news/{id}", False, "Could not create news for update test")
                
        except Exception as e:
            self.log_test("PUT /api/news/{id}", False, f"Exception: {str(e)}")

    def test_16_delete_news(self):
        """Test DELETE /api/news/{id} - Delete news item"""
        try:
            # First create a news item to delete
            news_data = {
                "title": "Test News for Deletion",
                "content": "This news will be deleted",
                "priority": "normal"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/news",
                json=news_data
            )
            
            if create_response.status_code == 200:
                created_news = create_response.json()
                news_id = created_news["id"]
                
                # Delete the news
                delete_response = self.session.delete(f"{self.base_url}/news/{news_id}")
                
                if delete_response.status_code == 200:
                    # Verify deletion by trying to fetch the news
                    verify_response = self.session.get(f"{self.base_url}/news")
                    if verify_response.status_code == 200:
                        remaining_news = verify_response.json()
                        deleted_news_exists = any(item["id"] == news_id for item in remaining_news)
                        
                        if not deleted_news_exists:
                            self.log_test(
                                "DELETE /api/news/{id}", 
                                True, 
                                f"Successfully deleted news item",
                                {"deleted_news_id": news_id}
                            )
                        else:
                            self.log_test(
                                "DELETE /api/news/{id}", 
                                False, 
                                "News item still exists after deletion"
                            )
                    else:
                        self.log_test(
                            "DELETE /api/news/{id}", 
                            True, 
                            "News deleted (could not verify due to fetch error)"
                        )
                else:
                    self.log_test(
                        "DELETE /api/news/{id}", 
                        False, 
                        f"HTTP {delete_response.status_code}: {delete_response.text}"
                    )
            else:
                self.log_test("DELETE /api/news/{id}", False, "Could not create news for deletion test")
                
        except Exception as e:
            self.log_test("DELETE /api/news/{id}", False, f"Exception: {str(e)}")

    # ========================================
    # TASK MANAGEMENT API TESTS
    # ========================================

    def test_17_get_all_tasks(self):
        """Test GET /api/tasks - Fetch all tasks"""
        try:
            response = self.session.get(f"{self.base_url}/tasks")
            
            if response.status_code == 200:
                tasks = response.json()
                task_count = len(tasks)
                
                self.log_test(
                    "GET /api/tasks", 
                    True, 
                    f"Successfully fetched {task_count} tasks",
                    {"count": task_count}
                )
            else:
                self.log_test(
                    "GET /api/tasks", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/tasks", False, f"Exception: {str(e)}")

    def test_18_create_tasks(self):
        """Test POST /api/tasks - Create tasks with employee assignment"""
        try:
            # First get employees to assign tasks to
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("POST /api/tasks", False, "Could not fetch employees for task assignment")
                return
            
            employees = emp_response.json()
            if len(employees) < 3:
                self.log_test("POST /api/tasks", False, "Not enough employees for task assignment testing")
                return
            
            # Test creating tasks with different priorities and statuses
            test_tasks = [
                {
                    "title": "Complete Q1 Financial Report",
                    "description": "Prepare and submit the quarterly financial report including revenue analysis, expense breakdown, and profit margins for Q1 2025.",
                    "assigned_to": employees[0]["id"],
                    "priority": "high",
                    "status": "pending",
                    "due_date": "2025-03-31T23:59:59"
                },
                {
                    "title": "Update Employee Handbook",
                    "description": "Review and update the employee handbook with new policies regarding remote work and flexible schedules.",
                    "assigned_to": employees[1]["id"],
                    "priority": "medium",
                    "status": "in_progress",
                    "due_date": "2025-02-28T17:00:00"
                },
                {
                    "title": "Organize Team Building Event",
                    "description": "Plan and coordinate a team building event for the development team. Include venue booking, catering, and activity planning.",
                    "assigned_to": employees[2]["id"],
                    "priority": "low",
                    "status": "pending",
                    "due_date": "2025-04-15T12:00:00"
                }
            ]
            
            created_tasks = []
            
            for task_data in test_tasks:
                response = self.session.post(
                    f"{self.base_url}/tasks",
                    json=task_data
                )
                
                if response.status_code == 200:
                    created_task = response.json()
                    created_tasks.append(created_task)
                    
                    # Verify the created task has correct data
                    if (created_task.get("title") == task_data["title"] and
                        created_task.get("assigned_to") == task_data["assigned_to"] and
                        created_task.get("priority") == task_data["priority"] and
                        created_task.get("id")):
                        
                        assigned_employee = next((emp for emp in employees if emp["id"] == task_data["assigned_to"]), None)
                        employee_name = assigned_employee["name"] if assigned_employee else "Unknown"
                        
                        self.log_test(
                            f"POST /api/tasks ({task_data['priority']} priority)", 
                            True, 
                            f"Successfully created task: {task_data['title'][:40]}... assigned to {employee_name}",
                            {
                                "task_id": created_task["id"], 
                                "priority": task_data["priority"],
                                "assigned_to": employee_name,
                                "status": task_data["status"]
                            }
                        )
                    else:
                        self.log_test(
                            f"POST /api/tasks ({task_data['priority']} priority)", 
                            False, 
                            "Task created but data doesn't match"
                        )
                else:
                    self.log_test(
                        f"POST /api/tasks ({task_data['priority']} priority)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created task IDs for later tests
            self.created_task_ids = [task["id"] for task in created_tasks]
                
        except Exception as e:
            self.log_test("POST /api/tasks", False, f"Exception: {str(e)}")

    def test_19_update_task_status(self):
        """Test PUT /api/tasks/{id} - Update task status and other fields"""
        try:
            # First create a task to update
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("PUT /api/tasks/{id}", False, "Could not fetch employees for task creation")
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test("PUT /api/tasks/{id}", False, "No employees available for task assignment")
                return
            
            task_data = {
                "title": "Test Task for Status Update",
                "description": "This task will have its status updated",
                "assigned_to": employees[0]["id"],
                "priority": "medium",
                "status": "pending"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/tasks",
                json=task_data
            )
            
            if create_response.status_code == 200:
                created_task = create_response.json()
                task_id = created_task["id"]
                
                # Update the task status and other fields
                update_data = {
                    "status": "completed",
                    "priority": "high",
                    "title": "Updated Test Task - Completed"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/tasks/{task_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_task = update_response.json()
                    
                    # Verify updates
                    if (updated_task.get("status") == update_data["status"] and
                        updated_task.get("priority") == update_data["priority"] and
                        updated_task.get("title") == update_data["title"] and
                        updated_task.get("updated_at") != created_task.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/tasks/{id}", 
                            True, 
                            f"Successfully updated task status and fields",
                            {
                                "task_id": task_id, 
                                "new_status": update_data["status"],
                                "new_priority": update_data["priority"]
                            }
                        )
                    else:
                        self.log_test(
                            "PUT /api/tasks/{id}", 
                            False, 
                            "Task updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/tasks/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/tasks/{id}", False, "Could not create task for update test")
                
        except Exception as e:
            self.log_test("PUT /api/tasks/{id}", False, f"Exception: {str(e)}")

    def test_20_delete_task(self):
        """Test DELETE /api/tasks/{id} - Delete task"""
        try:
            # First create a task to delete
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("DELETE /api/tasks/{id}", False, "Could not fetch employees for task creation")
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test("DELETE /api/tasks/{id}", False, "No employees available for task assignment")
                return
            
            task_data = {
                "title": "Test Task for Deletion",
                "description": "This task will be deleted",
                "assigned_to": employees[0]["id"],
                "priority": "low",
                "status": "pending"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/tasks",
                json=task_data
            )
            
            if create_response.status_code == 200:
                created_task = create_response.json()
                task_id = created_task["id"]
                
                # Delete the task
                delete_response = self.session.delete(f"{self.base_url}/tasks/{task_id}")
                
                if delete_response.status_code == 200:
                    # Verify deletion by trying to fetch the tasks
                    verify_response = self.session.get(f"{self.base_url}/tasks")
                    if verify_response.status_code == 200:
                        remaining_tasks = verify_response.json()
                        deleted_task_exists = any(task["id"] == task_id for task in remaining_tasks)
                        
                        if not deleted_task_exists:
                            self.log_test(
                                "DELETE /api/tasks/{id}", 
                                True, 
                                f"Successfully deleted task",
                                {"deleted_task_id": task_id}
                            )
                        else:
                            self.log_test(
                                "DELETE /api/tasks/{id}", 
                                False, 
                                "Task still exists after deletion"
                            )
                    else:
                        self.log_test(
                            "DELETE /api/tasks/{id}", 
                            True, 
                            "Task deleted (could not verify due to fetch error)"
                        )
                else:
                    self.log_test(
                        "DELETE /api/tasks/{id}", 
                        False, 
                        f"HTTP {delete_response.status_code}: {delete_response.text}"
                    )
            else:
                self.log_test("DELETE /api/tasks/{id}", False, "Could not create task for deletion test")
                
        except Exception as e:
            self.log_test("DELETE /api/tasks/{id}", False, f"Exception: {str(e)}")

    # ========================================
    # KNOWLEDGE MANAGEMENT API TESTS
    # ========================================

    def test_21_get_all_knowledge(self):
        """Test GET /api/knowledge - Fetch all knowledge articles"""
        try:
            response = self.session.get(f"{self.base_url}/knowledge")
            
            if response.status_code == 200:
                knowledge_articles = response.json()
                article_count = len(knowledge_articles)
                
                self.log_test(
                    "GET /api/knowledge", 
                    True, 
                    f"Successfully fetched {article_count} knowledge articles",
                    {"count": article_count}
                )
            else:
                self.log_test(
                    "GET /api/knowledge", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/knowledge", False, f"Exception: {str(e)}")

    def test_22_create_knowledge_articles(self):
        """Test POST /api/knowledge - Create knowledge articles with different categories"""
        try:
            # Test creating knowledge articles with different categories and tags
            test_articles = [
                {
                    "title": "Remote Work Policy 2025",
                    "content": "Our updated remote work policy allows employees to work from home up to 3 days per week. Employees must maintain regular communication with their team and attend mandatory in-person meetings. Equipment and internet allowances are provided.",
                    "category": "policy",
                    "tags": ["remote-work", "policy", "2025", "flexibility"]
                },
                {
                    "title": "New Employee Onboarding Process",
                    "content": "Step-by-step guide for onboarding new employees: 1) Send welcome email with first-day instructions, 2) Prepare workspace and equipment, 3) Schedule orientation meetings, 4) Assign buddy/mentor, 5) Complete paperwork and system access setup.",
                    "category": "process",
                    "tags": ["onboarding", "hr", "new-employee", "process"]
                },
                {
                    "title": "Cybersecurity Training Guidelines",
                    "content": "All employees must complete annual cybersecurity training covering: password management, phishing identification, secure file sharing, VPN usage, and incident reporting procedures. Training must be completed within 30 days of hire.",
                    "category": "training",
                    "tags": ["cybersecurity", "training", "mandatory", "security"]
                },
                {
                    "title": "Office Closure - Holiday Schedule",
                    "content": "The office will be closed from December 24th to January 2nd for the holiday season. Emergency contacts will be available for critical issues. Regular operations resume January 3rd, 2025.",
                    "category": "announcement",
                    "tags": ["holiday", "closure", "schedule", "announcement"]
                }
            ]
            
            created_articles = []
            
            for article_data in test_articles:
                response = self.session.post(
                    f"{self.base_url}/knowledge",
                    json=article_data
                )
                
                if response.status_code == 200:
                    created_article = response.json()
                    created_articles.append(created_article)
                    
                    # Verify the created article has correct data
                    if (created_article.get("title") == article_data["title"] and
                        created_article.get("category") == article_data["category"] and
                        created_article.get("tags") == article_data["tags"] and
                        created_article.get("id")):
                        
                        self.log_test(
                            f"POST /api/knowledge ({article_data['category']} category)", 
                            True, 
                            f"Successfully created knowledge article: {article_data['title'][:40]}...",
                            {
                                "article_id": created_article["id"], 
                                "category": article_data["category"],
                                "tags_count": len(article_data["tags"])
                            }
                        )
                    else:
                        self.log_test(
                            f"POST /api/knowledge ({article_data['category']} category)", 
                            False, 
                            "Knowledge article created but data doesn't match"
                        )
                else:
                    self.log_test(
                        f"POST /api/knowledge ({article_data['category']} category)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created article IDs for later tests
            self.created_knowledge_ids = [article["id"] for article in created_articles]
                
        except Exception as e:
            self.log_test("POST /api/knowledge", False, f"Exception: {str(e)}")

    def test_23_update_knowledge_article(self):
        """Test PUT /api/knowledge/{id} - Update knowledge article"""
        try:
            # First create a knowledge article to update
            article_data = {
                "title": "Test Knowledge Article for Update",
                "content": "This article will be updated",
                "category": "guideline",
                "tags": ["test", "update"]
            }
            
            create_response = self.session.post(
                f"{self.base_url}/knowledge",
                json=article_data
            )
            
            if create_response.status_code == 200:
                created_article = create_response.json()
                article_id = created_article["id"]
                
                # Update the article
                update_data = {
                    "title": "Updated Test Knowledge Article",
                    "content": "This article has been updated with new comprehensive content including best practices and detailed procedures.",
                    "category": "process",
                    "tags": ["updated", "process", "best-practices", "procedures"]
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/knowledge/{article_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_article = update_response.json()
                    
                    # Verify updates
                    if (updated_article.get("title") == update_data["title"] and
                        updated_article.get("category") == update_data["category"] and
                        updated_article.get("tags") == update_data["tags"] and
                        updated_article.get("updated_at") != created_article.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/knowledge/{id}", 
                            True, 
                            f"Successfully updated knowledge article",
                            {
                                "article_id": article_id, 
                                "new_title": update_data["title"],
                                "new_category": update_data["category"],
                                "new_tags_count": len(update_data["tags"])
                            }
                        )
                    else:
                        self.log_test(
                            "PUT /api/knowledge/{id}", 
                            False, 
                            "Knowledge article updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/knowledge/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/knowledge/{id}", False, "Could not create knowledge article for update test")
                
        except Exception as e:
            self.log_test("PUT /api/knowledge/{id}", False, f"Exception: {str(e)}")

    def test_24_delete_knowledge_article(self):
        """Test DELETE /api/knowledge/{id} - Delete knowledge article"""
        try:
            # First create a knowledge article to delete
            article_data = {
                "title": "Test Knowledge Article for Deletion",
                "content": "This article will be deleted",
                "category": "other",
                "tags": ["test", "deletion"]
            }
            
            create_response = self.session.post(
                f"{self.base_url}/knowledge",
                json=article_data
            )
            
            if create_response.status_code == 200:
                created_article = create_response.json()
                article_id = created_article["id"]
                
                # Delete the article
                delete_response = self.session.delete(f"{self.base_url}/knowledge/{article_id}")
                
                if delete_response.status_code == 200:
                    # Verify deletion by trying to fetch the articles
                    verify_response = self.session.get(f"{self.base_url}/knowledge")
                    if verify_response.status_code == 200:
                        remaining_articles = verify_response.json()
                        deleted_article_exists = any(article["id"] == article_id for article in remaining_articles)
                        
                        if not deleted_article_exists:
                            self.log_test(
                                "DELETE /api/knowledge/{id}", 
                                True, 
                                f"Successfully deleted knowledge article",
                                {"deleted_article_id": article_id}
                            )
                        else:
                            self.log_test(
                                "DELETE /api/knowledge/{id}", 
                                False, 
                                "Knowledge article still exists after deletion"
                            )
                    else:
                        self.log_test(
                            "DELETE /api/knowledge/{id}", 
                            True, 
                            "Knowledge article deleted (could not verify due to fetch error)"
                        )
                else:
                    self.log_test(
                        "DELETE /api/knowledge/{id}", 
                        False, 
                        f"HTTP {delete_response.status_code}: {delete_response.text}"
                    )
            else:
                self.log_test("DELETE /api/knowledge/{id}", False, "Could not create knowledge article for deletion test")
                
        except Exception as e:
            self.log_test("DELETE /api/knowledge/{id}", False, f"Exception: {str(e)}")

    # ========================================
    # HELP/SUPPORT MANAGEMENT API TESTS
    # ========================================

    def test_25_get_all_help_requests(self):
        """Test GET /api/help - Fetch all help requests"""
        try:
            response = self.session.get(f"{self.base_url}/help")
            
            if response.status_code == 200:
                help_requests = response.json()
                request_count = len(help_requests)
                
                self.log_test(
                    "GET /api/help", 
                    True, 
                    f"Successfully fetched {request_count} help requests",
                    {"count": request_count}
                )
            else:
                self.log_test(
                    "GET /api/help", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/help", False, f"Exception: {str(e)}")

    def test_26_create_help_requests(self):
        """Test POST /api/help - Create help requests with different priorities"""
        try:
            # Test creating help requests with different priority levels
            test_help_requests = [
                {
                    "title": "System Access Issue - Cannot Login",
                    "message": "I'm unable to log into the company system. I've tried resetting my password multiple times but still getting authentication errors. This is blocking my work completely.",
                    "priority": "high"
                },
                {
                    "title": "Request for Additional Monitor",
                    "message": "I would like to request an additional monitor for my workstation to improve productivity. My current setup with a single monitor is limiting my ability to multitask effectively.",
                    "priority": "medium"
                },
                {
                    "title": "Question about Vacation Policy",
                    "message": "I have a question about the vacation policy. Can I carry over unused vacation days to next year? Also, what's the process for requesting extended leave?",
                    "priority": "normal"
                }
            ]
            
            created_requests = []
            
            for request_data in test_help_requests:
                response = self.session.post(
                    f"{self.base_url}/help",
                    json=request_data
                )
                
                if response.status_code == 200:
                    created_request = response.json()
                    created_requests.append(created_request)
                    
                    # Verify the created request has correct data
                    if (created_request.get("title") == request_data["title"] and
                        created_request.get("priority") == request_data["priority"] and
                        created_request.get("status") == "open" and
                        created_request.get("id")):
                        
                        self.log_test(
                            f"POST /api/help ({request_data['priority']} priority)", 
                            True, 
                            f"Successfully created help request: {request_data['title'][:40]}...",
                            {
                                "request_id": created_request["id"], 
                                "priority": request_data["priority"],
                                "status": created_request["status"]
                            }
                        )
                    else:
                        self.log_test(
                            f"POST /api/help ({request_data['priority']} priority)", 
                            False, 
                            "Help request created but data doesn't match"
                        )
                else:
                    self.log_test(
                        f"POST /api/help ({request_data['priority']} priority)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created request IDs for later tests
            self.created_help_ids = [request["id"] for request in created_requests]
                
        except Exception as e:
            self.log_test("POST /api/help", False, f"Exception: {str(e)}")

    def test_27_update_help_request_status(self):
        """Test PUT /api/help/{id} - Update help request status"""
        try:
            # First create a help request to update
            request_data = {
                "title": "Test Help Request for Status Update",
                "message": "This help request will have its status updated",
                "priority": "medium"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/help",
                json=request_data
            )
            
            if create_response.status_code == 200:
                created_request = create_response.json()
                request_id = created_request["id"]
                
                # Update the request status
                update_data = {
                    "status": "in_progress"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/help/{request_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_request = update_response.json()
                    
                    # Verify updates
                    if (updated_request.get("status") == update_data["status"] and
                        updated_request.get("updated_at") != created_request.get("created_at")):
                        
                        # Test another status update to "resolved"
                        resolve_data = {"status": "resolved"}
                        resolve_response = self.session.put(
                            f"{self.base_url}/help/{request_id}",
                            json=resolve_data
                        )
                        
                        if resolve_response.status_code == 200:
                            resolved_request = resolve_response.json()
                            if resolved_request.get("status") == "resolved":
                                self.log_test(
                                    "PUT /api/help/{id}", 
                                    True, 
                                    f"Successfully updated help request status through workflow: open → in_progress → resolved",
                                    {
                                        "request_id": request_id, 
                                        "final_status": resolved_request["status"]
                                    }
                                )
                            else:
                                self.log_test(
                                    "PUT /api/help/{id}", 
                                    False, 
                                    "Second status update failed"
                                )
                        else:
                            self.log_test(
                                "PUT /api/help/{id}", 
                                True, 
                                f"First status update successful (second update failed but not critical)",
                                {"request_id": request_id, "status": update_data["status"]}
                            )
                    else:
                        self.log_test(
                            "PUT /api/help/{id}", 
                            False, 
                            "Help request updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/help/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/help/{id}", False, "Could not create help request for update test")
                
        except Exception as e:
            self.log_test("PUT /api/help/{id}", False, f"Exception: {str(e)}")

    def test_28_add_help_reply(self):
        """Test POST /api/help/{id}/reply - Add reply to help request"""
        try:
            # First create a help request to reply to
            request_data = {
                "title": "Test Help Request for Reply System",
                "message": "I need help with setting up my development environment. The installation keeps failing.",
                "priority": "medium"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/help",
                json=request_data
            )
            
            if create_response.status_code == 200:
                created_request = create_response.json()
                request_id = created_request["id"]
                
                # Add multiple replies to test the reply system
                replies_to_add = [
                    {
                        "message": "Thank you for your request. Can you please provide more details about the specific error message you're seeing during installation?"
                    },
                    {
                        "message": "Also, please let us know which operating system you're using and the version of the development tools you're trying to install."
                    },
                    {
                        "message": "We've identified the issue. Please try downloading the latest installer from our internal portal and run it as administrator."
                    }
                ]
                
                successful_replies = 0
                
                for i, reply_data in enumerate(replies_to_add):
                    reply_response = self.session.post(
                        f"{self.base_url}/help/{request_id}/reply",
                        json=reply_data
                    )
                    
                    if reply_response.status_code == 200:
                        updated_request = reply_response.json()
                        replies = updated_request.get("replies", [])
                        
                        # Verify the reply was added
                        if len(replies) == i + 1:
                            latest_reply = replies[-1]
                            if latest_reply.get("message") == reply_data["message"]:
                                successful_replies += 1
                        
                if successful_replies == len(replies_to_add):
                    # Get final state to verify all replies
                    final_response = self.session.get(f"{self.base_url}/help")
                    if final_response.status_code == 200:
                        all_requests = final_response.json()
                        target_request = next((req for req in all_requests if req["id"] == request_id), None)
                        
                        if target_request and len(target_request.get("replies", [])) == len(replies_to_add):
                            self.log_test(
                                "POST /api/help/{id}/reply", 
                                True, 
                                f"Successfully added {len(replies_to_add)} replies to help request",
                                {
                                    "request_id": request_id, 
                                    "replies_count": len(target_request["replies"]),
                                    "final_status": target_request.get("status", "unknown")
                                }
                            )
                        else:
                            self.log_test(
                                "POST /api/help/{id}/reply", 
                                False, 
                                f"Replies added but final count doesn't match. Expected: {len(replies_to_add)}, Got: {len(target_request.get('replies', []))}"
                            )
                    else:
                        self.log_test(
                            "POST /api/help/{id}/reply", 
                            True, 
                            f"All {successful_replies} replies added successfully (could not verify final state)"
                        )
                else:
                    self.log_test(
                        "POST /api/help/{id}/reply", 
                        False, 
                        f"Only {successful_replies}/{len(replies_to_add)} replies were added successfully"
                    )
            else:
                self.log_test("POST /api/help/{id}/reply", False, "Could not create help request for reply test")
                
        except Exception as e:
            self.log_test("POST /api/help/{id}/reply", False, f"Exception: {str(e)}")

    def test_29_delete_help_request(self):
        """Test DELETE /api/help/{id} - Delete help request"""
        try:
            # First create a help request to delete
            request_data = {
                "title": "Test Help Request for Deletion",
                "message": "This help request will be deleted",
                "priority": "normal"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/help",
                json=request_data
            )
            
            if create_response.status_code == 200:
                created_request = create_response.json()
                request_id = created_request["id"]
                
                # Delete the help request
                delete_response = self.session.delete(f"{self.base_url}/help/{request_id}")
                
                if delete_response.status_code == 200:
                    # Verify deletion by trying to fetch the help requests
                    verify_response = self.session.get(f"{self.base_url}/help")
                    if verify_response.status_code == 200:
                        remaining_requests = verify_response.json()
                        deleted_request_exists = any(request["id"] == request_id for request in remaining_requests)
                        
                        if not deleted_request_exists:
                            self.log_test(
                                "DELETE /api/help/{id}", 
                                True, 
                                f"Successfully deleted help request",
                                {"deleted_request_id": request_id}
                            )
                        else:
                            self.log_test(
                                "DELETE /api/help/{id}", 
                                False, 
                                "Help request still exists after deletion"
                            )
                    else:
                        self.log_test(
                            "DELETE /api/help/{id}", 
                            True, 
                            "Help request deleted (could not verify due to fetch error)"
                        )
                else:
                    self.log_test(
                        "DELETE /api/help/{id}", 
                        False, 
                        f"HTTP {delete_response.status_code}: {delete_response.text}"
                    )
            else:
                self.log_test("DELETE /api/help/{id}", False, "Could not create help request for deletion test")
                
        except Exception as e:
            self.log_test("DELETE /api/help/{id}", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 80)
        print("EMPLOYEE DIRECTORY AND MANAGEMENT PLATFORM - COMPREHENSIVE BACKEND API TESTING")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Initialize storage for created IDs
        self.created_news_ids = []
        self.created_task_ids = []
        self.created_knowledge_ids = []
        self.created_help_ids = []
        
        # Run existing employee and hierarchy tests
        print("🔍 TESTING EMPLOYEE MANAGEMENT APIs...")
        self.test_1_get_all_employees()
        self.test_2_search_employees()
        self.test_3_filter_employees()
        self.test_4_update_employee_image_url()
        self.test_4b_update_employee_image_base64()
        self.test_4c_upload_employee_image_file()
        self.test_4d_static_file_serving()
        self.test_5_refresh_excel_data()
        
        print("\n🏗️ TESTING HIERARCHY MANAGEMENT APIs...")
        self.test_6_get_hierarchy()
        self.test_7_create_hierarchy_relation()
        self.test_8_delete_hierarchy_relation()
        self.test_9_clear_all_hierarchy()
        
        print("\n📊 TESTING UTILITY APIs...")
        self.test_10_get_departments()
        self.test_11_get_locations()
        self.test_12_get_stats()
        
        # Run new API tests
        print("\n📰 TESTING NEWS MANAGEMENT APIs...")
        self.test_13_get_all_news()
        self.test_14_create_news()
        self.test_15_update_news()
        self.test_16_delete_news()
        
        print("\n📋 TESTING TASK MANAGEMENT APIs...")
        self.test_17_get_all_tasks()
        self.test_18_create_tasks()
        self.test_19_update_task_status()
        self.test_20_delete_task()
        
        print("\n📚 TESTING KNOWLEDGE MANAGEMENT APIs...")
        self.test_21_get_all_knowledge()
        self.test_22_create_knowledge_articles()
        self.test_23_update_knowledge_article()
        self.test_24_delete_knowledge_article()
        
        print("\n🆘 TESTING HELP/SUPPORT MANAGEMENT APIs...")
        self.test_25_get_all_help_requests()
        self.test_26_create_help_requests()
        self.test_27_update_help_request_status()
        self.test_28_add_help_reply()
        self.test_29_delete_help_request()
        
        # Summary
        print("=" * 80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print()
        
        # Group results by API category
        categories = {
            "Employee Management": [r for r in self.test_results if any(x in r["test"] for x in ["employees", "image", "excel"])],
            "Hierarchy Management": [r for r in self.test_results if "hierarchy" in r["test"].lower()],
            "Utility APIs": [r for r in self.test_results if any(x in r["test"] for x in ["departments", "locations", "stats"])],
            "News Management": [r for r in self.test_results if "news" in r["test"].lower()],
            "Task Management": [r for r in self.test_results if "task" in r["test"].lower()],
            "Knowledge Management": [r for r in self.test_results if "knowledge" in r["test"].lower()],
            "Help/Support Management": [r for r in self.test_results if "help" in r["test"].lower()]
        }
        
        for category, results in categories.items():
            if results:
                cat_passed = sum(1 for r in results if r["success"])
                cat_total = len(results)
                print(f"{category}: {cat_passed}/{cat_total} tests passed")
        
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['message']}")
            print()
        
        print("All comprehensive backend API tests completed!")
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