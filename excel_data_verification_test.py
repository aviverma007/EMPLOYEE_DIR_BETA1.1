#!/usr/bin/env python3
"""
Excel Data Loading and Employee Directory Verification Test
Focused testing for the review request requirements:
1. Verify exactly 640 employees are loaded from Excel file
2. Test GET /api/employees endpoint functionality
3. Verify departments and locations are correctly extracted
4. Test search functionality by name, ID, department, location
5. Confirm data integrity of employee details
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "http://localhost:8001/api"

class ExcelDataVerificationTester:
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

    def test_1_excel_data_loading_640_employees(self):
        """Test 1: Verify exactly 640 employees are loaded from Excel file"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    # Verify sample employee has all required fields
                    sample_employee = employees[0] if employees else {}
                    required_fields = ['id', 'name', 'department', 'location', 'grade', 'mobile', 'email']
                    missing_fields = [field for field in required_fields if field not in sample_employee]
                    
                    if not missing_fields:
                        self.log_test(
                            "Excel Data Loading - 640 Employees", 
                            True, 
                            f"✅ VERIFIED: Exactly 640 employees loaded from Excel file with all required fields",
                            {
                                "employee_count": employee_count,
                                "sample_employee_fields": list(sample_employee.keys()),
                                "sample_employee_name": sample_employee.get('name', 'N/A'),
                                "sample_employee_id": sample_employee.get('id', 'N/A')
                            }
                        )
                    else:
                        self.log_test(
                            "Excel Data Loading - 640 Employees", 
                            False, 
                            f"640 employees loaded but missing required fields: {missing_fields}",
                            {"missing_fields": missing_fields}
                        )
                else:
                    self.log_test(
                        "Excel Data Loading - 640 Employees", 
                        False, 
                        f"❌ CRITICAL: Expected exactly 640 employees, but found {employee_count}",
                        {"expected": 640, "actual": employee_count}
                    )
            else:
                self.log_test(
                    "Excel Data Loading - 640 Employees", 
                    False, 
                    f"❌ CRITICAL: Could not fetch employees - HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Excel Data Loading - 640 Employees", False, f"❌ EXCEPTION: {str(e)}")

    def test_2_employee_api_endpoint_functionality(self):
        """Test 2: Test GET /api/employees endpoint comprehensive functionality"""
        try:
            # Test basic endpoint
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                
                # Verify response structure
                if employees and isinstance(employees, list):
                    sample_employee = employees[0]
                    
                    # Check for essential employee data fields
                    essential_fields = ['id', 'name', 'department', 'location']
                    has_essential_fields = all(field in sample_employee for field in essential_fields)
                    
                    if has_essential_fields:
                        # Test with different query parameters
                        test_cases = [
                            ("No parameters", f"{self.base_url}/employees"),
                            ("With search parameter", f"{self.base_url}/employees?search=Manager"),
                            ("With department filter", f"{self.base_url}/employees?department=Administration"),
                            ("With location filter", f"{self.base_url}/employees?location=IFC")
                        ]
                        
                        all_tests_passed = True
                        test_details = {}
                        
                        for test_name, url in test_cases:
                            test_response = self.session.get(url)
                            if test_response.status_code == 200:
                                test_employees = test_response.json()
                                test_details[test_name] = {
                                    "status": "✅ PASS",
                                    "count": len(test_employees)
                                }
                            else:
                                test_details[test_name] = {
                                    "status": "❌ FAIL",
                                    "error": f"HTTP {test_response.status_code}"
                                }
                                all_tests_passed = False
                        
                        self.log_test(
                            "Employee API Endpoint Functionality", 
                            all_tests_passed, 
                            f"Employee API endpoint functionality {'✅ VERIFIED' if all_tests_passed else '❌ PARTIAL FAILURE'}",
                            {
                                "base_employee_count": len(employees),
                                "test_results": test_details,
                                "sample_employee_structure": list(sample_employee.keys())
                            }
                        )
                    else:
                        self.log_test(
                            "Employee API Endpoint Functionality", 
                            False, 
                            f"❌ Employee data missing essential fields: {essential_fields}"
                        )
                else:
                    self.log_test(
                        "Employee API Endpoint Functionality", 
                        False, 
                        "❌ Invalid response format - expected list of employees"
                    )
            else:
                self.log_test(
                    "Employee API Endpoint Functionality", 
                    False, 
                    f"❌ API endpoint failed - HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Employee API Endpoint Functionality", False, f"❌ EXCEPTION: {str(e)}")

    def test_3_departments_and_locations_extraction(self):
        """Test 3: Verify departments and locations are correctly extracted from Excel"""
        try:
            # Test departments endpoint
            dept_response = self.session.get(f"{self.base_url}/departments")
            loc_response = self.session.get(f"{self.base_url}/locations")
            
            dept_success = dept_response.status_code == 200
            loc_success = loc_response.status_code == 200
            
            if dept_success and loc_success:
                departments = dept_response.json().get("departments", [])
                locations = loc_response.json().get("locations", [])
                
                # Remove "All Departments" and "All Locations" if present
                actual_departments = [d for d in departments if d not in ["All Departments", ""]]
                actual_locations = [l for l in locations if l not in ["All Locations", ""]]
                
                # Verify we have reasonable number of departments and locations
                dept_count = len(actual_departments)
                loc_count = len(actual_locations)
                
                # Expected ranges based on typical organizational structure
                dept_valid = 10 <= dept_count <= 50  # Reasonable range for departments
                loc_valid = 5 <= loc_count <= 30     # Reasonable range for locations
                
                if dept_valid and loc_valid:
                    self.log_test(
                        "Departments and Locations Extraction", 
                        True, 
                        f"✅ VERIFIED: Departments and locations correctly extracted from Excel",
                        {
                            "departments_count": dept_count,
                            "locations_count": loc_count,
                            "sample_departments": actual_departments[:5],
                            "sample_locations": actual_locations[:5]
                        }
                    )
                else:
                    self.log_test(
                        "Departments and Locations Extraction", 
                        False, 
                        f"❌ Unexpected counts - Departments: {dept_count}, Locations: {loc_count}",
                        {
                            "departments_count": dept_count,
                            "locations_count": loc_count,
                            "departments_valid": dept_valid,
                            "locations_valid": loc_valid
                        }
                    )
            else:
                error_details = {}
                if not dept_success:
                    error_details["departments_error"] = f"HTTP {dept_response.status_code}"
                if not loc_success:
                    error_details["locations_error"] = f"HTTP {loc_response.status_code}"
                
                self.log_test(
                    "Departments and Locations Extraction", 
                    False, 
                    f"❌ Failed to fetch departments/locations data",
                    error_details
                )
                
        except Exception as e:
            self.log_test("Departments and Locations Extraction", False, f"❌ EXCEPTION: {str(e)}")

    def test_4_search_functionality_comprehensive(self):
        """Test 4: Test employee search by name, ID, department, and location"""
        try:
            search_tests = [
                {
                    "name": "Search by Name (starts with 'Am')",
                    "url": f"{self.base_url}/employees?search=Am",
                    "expected_field": "name",
                    "search_term": "Am"
                },
                {
                    "name": "Search by Name (starts with 'Ra')",
                    "url": f"{self.base_url}/employees?search=Ra",
                    "expected_field": "name",
                    "search_term": "Ra"
                },
                {
                    "name": "Search by ID (starts with 'EMP')",
                    "url": f"{self.base_url}/employees?search=EMP",
                    "expected_field": "id",
                    "search_term": "EMP"
                },
                {
                    "name": "Search by Department (starts with 'Admin')",
                    "url": f"{self.base_url}/employees?search=Admin",
                    "expected_field": "department",
                    "search_term": "Admin"
                },
                {
                    "name": "Search by Location (starts with 'IFC')",
                    "url": f"{self.base_url}/employees?search=IFC",
                    "expected_field": "location",
                    "search_term": "IFC"
                }
            ]
            
            all_search_tests_passed = True
            search_results = {}
            
            for test in search_tests:
                try:
                    response = self.session.get(test["url"])
                    
                    if response.status_code == 200:
                        employees = response.json()
                        result_count = len(employees)
                        
                        # Verify results start with search term (case insensitive)
                        if employees:
                            # Check if at least some results match the expected pattern
                            matching_results = 0
                            for emp in employees[:10]:  # Check first 10 results
                                field_value = str(emp.get(test["expected_field"], "")).lower()
                                if field_value.startswith(test["search_term"].lower()):
                                    matching_results += 1
                            
                            match_percentage = (matching_results / min(len(employees), 10)) * 100
                            
                            search_results[test["name"]] = {
                                "status": "✅ PASS" if match_percentage >= 50 else "⚠️ PARTIAL",
                                "result_count": result_count,
                                "match_percentage": f"{match_percentage:.1f}%",
                                "sample_matches": matching_results
                            }
                            
                            if match_percentage < 50:
                                all_search_tests_passed = False
                        else:
                            search_results[test["name"]] = {
                                "status": "⚠️ NO RESULTS",
                                "result_count": 0,
                                "note": "No results found for search term"
                            }
                    else:
                        search_results[test["name"]] = {
                            "status": "❌ FAIL",
                            "error": f"HTTP {response.status_code}"
                        }
                        all_search_tests_passed = False
                        
                except Exception as search_error:
                    search_results[test["name"]] = {
                        "status": "❌ ERROR",
                        "error": str(search_error)
                    }
                    all_search_tests_passed = False
            
            self.log_test(
                "Search Functionality Comprehensive", 
                all_search_tests_passed, 
                f"Search functionality {'✅ VERIFIED' if all_search_tests_passed else '❌ ISSUES FOUND'}",
                {"search_test_results": search_results}
            )
                
        except Exception as e:
            self.log_test("Search Functionality Comprehensive", False, f"❌ EXCEPTION: {str(e)}")

    def test_5_data_integrity_verification(self):
        """Test 5: Confirm employee details data integrity from Excel parsing"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                
                if len(employees) >= 10:  # Test with first 10 employees
                    test_employees = employees[:10]
                    
                    integrity_checks = {
                        "has_valid_ids": 0,
                        "has_valid_names": 0,
                        "has_valid_departments": 0,
                        "has_valid_locations": 0,
                        "has_valid_grades": 0,
                        "has_valid_mobile": 0,
                        "has_valid_email": 0,
                        "has_profile_image_field": 0
                    }
                    
                    for emp in test_employees:
                        # Check ID format (should not be empty)
                        if emp.get('id') and len(str(emp.get('id'))) > 0:
                            integrity_checks["has_valid_ids"] += 1
                        
                        # Check name (should not be empty)
                        if emp.get('name') and len(str(emp.get('name'))) > 0:
                            integrity_checks["has_valid_names"] += 1
                        
                        # Check department (should not be empty)
                        if emp.get('department') and len(str(emp.get('department'))) > 0:
                            integrity_checks["has_valid_departments"] += 1
                        
                        # Check location (should not be empty)
                        if emp.get('location') and len(str(emp.get('location'))) > 0:
                            integrity_checks["has_valid_locations"] += 1
                        
                        # Check grade (should exist)
                        if emp.get('grade') is not None:
                            integrity_checks["has_valid_grades"] += 1
                        
                        # Check mobile (should exist, can be empty)
                        if 'mobile' in emp:
                            integrity_checks["has_valid_mobile"] += 1
                        
                        # Check email (should exist, can be empty)
                        if 'email' in emp:
                            integrity_checks["has_valid_email"] += 1
                        
                        # Check profile image field exists
                        if 'profileImage' in emp:
                            integrity_checks["has_profile_image_field"] += 1
                    
                    # Calculate integrity percentages
                    total_employees = len(test_employees)
                    integrity_percentages = {
                        key: (count / total_employees) * 100 
                        for key, count in integrity_checks.items()
                    }
                    
                    # Check if integrity is acceptable (>= 90% for critical fields)
                    critical_fields = ["has_valid_ids", "has_valid_names", "has_valid_departments", "has_valid_locations"]
                    critical_integrity = all(
                        integrity_percentages[field] >= 90.0 
                        for field in critical_fields
                    )
                    
                    # Check if optional fields are present (>= 80%)
                    optional_fields = ["has_valid_grades", "has_valid_mobile", "has_valid_email", "has_profile_image_field"]
                    optional_integrity = all(
                        integrity_percentages[field] >= 80.0 
                        for field in optional_fields
                    )
                    
                    overall_integrity = critical_integrity and optional_integrity
                    
                    self.log_test(
                        "Data Integrity Verification", 
                        overall_integrity, 
                        f"Data integrity {'✅ VERIFIED' if overall_integrity else '❌ ISSUES FOUND'}",
                        {
                            "tested_employees": total_employees,
                            "integrity_percentages": integrity_percentages,
                            "critical_fields_ok": critical_integrity,
                            "optional_fields_ok": optional_integrity,
                            "sample_employee": test_employees[0] if test_employees else {}
                        }
                    )
                else:
                    self.log_test(
                        "Data Integrity Verification", 
                        False, 
                        f"❌ Insufficient employees for integrity testing (found {len(employees)}, need >= 10)"
                    )
            else:
                self.log_test(
                    "Data Integrity Verification", 
                    False, 
                    f"❌ Could not fetch employees for integrity testing - HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Data Integrity Verification", False, f"❌ EXCEPTION: {str(e)}")

    def test_6_excel_to_api_pipeline_verification(self):
        """Test 6: Verify the complete Excel-to-API pipeline is working"""
        try:
            # Test the complete pipeline by checking stats endpoint
            stats_response = self.session.get(f"{self.base_url}/stats")
            
            if stats_response.status_code == 200:
                stats = stats_response.json()
                excel_stats = stats.get("excel", {})
                db_stats = stats.get("database", {})
                
                excel_employees = excel_stats.get("total_employees", 0)
                db_employees = db_stats.get("employees", 0)
                
                # Verify Excel and database are in sync
                if excel_employees == db_employees == 640:
                    # Test refresh functionality
                    refresh_response = self.session.post(f"{self.base_url}/refresh-excel")
                    
                    if refresh_response.status_code == 200:
                        refresh_result = refresh_response.json()
                        refreshed_count = refresh_result.get("count", 0)
                        
                        if refreshed_count == 640:
                            self.log_test(
                                "Excel-to-API Pipeline Verification", 
                                True, 
                                f"✅ VERIFIED: Complete Excel-to-API pipeline working perfectly",
                                {
                                    "excel_employees": excel_employees,
                                    "database_employees": db_employees,
                                    "refresh_count": refreshed_count,
                                    "pipeline_status": "✅ FULLY OPERATIONAL"
                                }
                            )
                        else:
                            self.log_test(
                                "Excel-to-API Pipeline Verification", 
                                False, 
                                f"❌ Excel refresh returned {refreshed_count} employees, expected 640"
                            )
                    else:
                        self.log_test(
                            "Excel-to-API Pipeline Verification", 
                            False, 
                            f"❌ Excel refresh failed - HTTP {refresh_response.status_code}"
                        )
                else:
                    self.log_test(
                        "Excel-to-API Pipeline Verification", 
                        False, 
                        f"❌ Excel/Database sync issue - Excel: {excel_employees}, DB: {db_employees}, Expected: 640"
                    )
            else:
                self.log_test(
                    "Excel-to-API Pipeline Verification", 
                    False, 
                    f"❌ Could not fetch stats - HTTP {stats_response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Excel-to-API Pipeline Verification", False, f"❌ EXCEPTION: {str(e)}")

    def run_all_tests(self):
        """Run all Excel data verification tests"""
        print("=" * 80)
        print("EXCEL DATA LOADING AND EMPLOYEE DIRECTORY VERIFICATION TEST")
        print("=" * 80)
        print(f"Testing backend API at: {self.base_url}")
        print("=" * 80)
        print()
        
        # Run all tests in sequence
        test_methods = [
            self.test_1_excel_data_loading_640_employees,
            self.test_2_employee_api_endpoint_functionality,
            self.test_3_departments_and_locations_extraction,
            self.test_4_search_functionality_comprehensive,
            self.test_5_data_integrity_verification,
            self.test_6_excel_to_api_pipeline_verification
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                print()
        
        # Print summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate == 100:
            print("🎉 ALL TESTS PASSED - Excel data loading and employee directory functionality verified!")
        elif success_rate >= 80:
            print("⚠️  MOSTLY SUCCESSFUL - Minor issues found, but core functionality working")
        else:
            print("❌ CRITICAL ISSUES FOUND - Excel data loading or employee directory has problems")
        
        print("=" * 80)
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = ExcelDataVerificationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)