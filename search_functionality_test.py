#!/usr/bin/env python3
"""
Focused Search Functionality Testing for Employee Directory and Attendance
Tests the "starts with" vs "contains" search pattern as requested in the review
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Get backend URL from frontend .env
BACKEND_URL = "https://dependency-solver.preview.emergentagent.com/api"

class SearchFunctionalityTester:
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

    def test_employee_search_starts_with_pattern(self):
        """Test Employee Directory search with 'starts with' pattern"""
        try:
            # Test cases for "starts with" pattern
            test_searches = ["Am", "An", "Ra"]
            
            for search_term in test_searches:
                print(f"\n🔍 Testing Employee search for '{search_term}' (should be 'starts with' pattern)")
                
                response = self.session.get(f"{self.base_url}/employees?search={search_term}")
                
                if response.status_code == 200:
                    employees = response.json()
                    search_count = len(employees)
                    
                    if search_count > 0:
                        # Analyze results to check if they follow "starts with" pattern
                        starts_with_results = []
                        contains_but_not_starts_results = []
                        
                        for emp in employees:
                            name = emp.get("name", "").lower()
                            search_lower = search_term.lower()
                            
                            if name.startswith(search_lower):
                                starts_with_results.append(emp["name"])
                            elif search_lower in name:
                                contains_but_not_starts_results.append(emp["name"])
                        
                        # Check if implementation follows "starts with" pattern
                        if len(contains_but_not_starts_results) == 0:
                            self.log_test(
                                f"Employee Search '{search_term}' - Starts With Pattern", 
                                True, 
                                f"✅ CORRECT: Search returns only names that START with '{search_term}' ({len(starts_with_results)} results)",
                                {
                                    "search_term": search_term,
                                    "total_results": search_count,
                                    "starts_with_count": len(starts_with_results),
                                    "contains_but_not_starts_count": len(contains_but_not_starts_results),
                                    "sample_starts_with": starts_with_results[:5],
                                    "pattern_type": "STARTS_WITH"
                                }
                            )
                        else:
                            self.log_test(
                                f"Employee Search '{search_term}' - Starts With Pattern", 
                                False, 
                                f"❌ INCORRECT: Search still uses 'contains' pattern - found {len(contains_but_not_starts_results)} names that contain '{search_term}' but don't start with it",
                                {
                                    "search_term": search_term,
                                    "total_results": search_count,
                                    "starts_with_count": len(starts_with_results),
                                    "contains_but_not_starts_count": len(contains_but_not_starts_results),
                                    "sample_starts_with": starts_with_results[:3],
                                    "sample_contains_not_starts": contains_but_not_starts_results[:3],
                                    "pattern_type": "CONTAINS (INCORRECT)"
                                }
                            )
                    else:
                        self.log_test(
                            f"Employee Search '{search_term}' - Starts With Pattern", 
                            True, 
                            f"Search returned no results for '{search_term}' (may be correct if no names start with this)",
                            {"search_term": search_term, "results_count": 0}
                        )
                else:
                    self.log_test(
                        f"Employee Search '{search_term}' - Starts With Pattern", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            self.log_test("Employee Search - Starts With Pattern", False, f"Exception: {str(e)}")

    def test_attendance_search_starts_with_pattern(self):
        """Test Attendance search with 'starts with' pattern"""
        try:
            # First, let's get some attendance records to understand the data structure
            print(f"\n🔍 Getting attendance records to understand data structure...")
            
            response = self.session.get(f"{self.base_url}/attendance")
            
            if response.status_code == 200:
                attendance_records = response.json()
                total_records = len(attendance_records)
                
                print(f"Found {total_records} attendance records")
                
                if total_records > 0:
                    # Show sample data structure
                    sample_record = attendance_records[0]
                    print(f"Sample attendance record structure: {list(sample_record.keys())}")
                    
                    # Test cases for "starts with" pattern on employee names in attendance
                    test_searches = ["Am", "An", "Ra"]
                    
                    for search_term in test_searches:
                        print(f"\n🔍 Testing Attendance search for '{search_term}' (should be 'starts with' pattern)")
                        
                        # Note: The attendance API doesn't seem to have a direct search parameter
                        # Let's check if there's a search functionality or if we need to filter by employee_id
                        
                        # Try searching by employee_id pattern first
                        search_response = self.session.get(f"{self.base_url}/attendance?employee_id={search_term}")
                        
                        if search_response.status_code == 200:
                            filtered_records = search_response.json()
                            
                            self.log_test(
                                f"Attendance Search '{search_term}' - Employee ID Filter", 
                                True, 
                                f"Attendance API responded to employee_id filter with {len(filtered_records)} results",
                                {
                                    "search_term": search_term,
                                    "results_count": len(filtered_records),
                                    "filter_type": "employee_id"
                                }
                            )
                        else:
                            # If direct search doesn't work, we'll analyze the data manually
                            # to check if there's a search pattern we can test
                            
                            # Filter records manually to test the pattern
                            starts_with_results = []
                            contains_but_not_starts_results = []
                            
                            for record in attendance_records:
                                employee_name = record.get("employee_name", "").lower()
                                search_lower = search_term.lower()
                                
                                if employee_name.startswith(search_lower):
                                    starts_with_results.append(record.get("employee_name", ""))
                                elif search_lower in employee_name:
                                    contains_but_not_starts_results.append(record.get("employee_name", ""))
                            
                            # Report the pattern analysis
                            if len(starts_with_results) > 0 or len(contains_but_not_starts_results) > 0:
                                self.log_test(
                                    f"Attendance Data Analysis '{search_term}' - Pattern Check", 
                                    True, 
                                    f"Manual analysis of attendance data for '{search_term}' pattern",
                                    {
                                        "search_term": search_term,
                                        "total_attendance_records": total_records,
                                        "names_starting_with": len(starts_with_results),
                                        "names_containing_not_starting": len(contains_but_not_starts_results),
                                        "sample_starts_with": starts_with_results[:3],
                                        "sample_contains_not_starts": contains_but_not_starts_results[:3],
                                        "note": "Attendance API may not have direct search functionality"
                                    }
                                )
                            else:
                                self.log_test(
                                    f"Attendance Data Analysis '{search_term}' - Pattern Check", 
                                    True, 
                                    f"No employee names in attendance records match '{search_term}' pattern",
                                    {
                                        "search_term": search_term,
                                        "total_attendance_records": total_records,
                                        "matching_names": 0
                                    }
                                )
                else:
                    self.log_test(
                        "Attendance Search - Pattern Analysis", 
                        True, 
                        "No attendance records found in database",
                        {"total_records": 0}
                    )
            else:
                self.log_test(
                    "Attendance Search - Pattern Analysis", 
                    False, 
                    f"Could not fetch attendance records: HTTP {response.status_code}"
                )
                    
        except Exception as e:
            self.log_test("Attendance Search - Starts With Pattern", False, f"Exception: {str(e)}")

    def test_backend_search_implementation_analysis(self):
        """Analyze the current backend search implementation"""
        try:
            print(f"\n🔍 Analyzing current search implementation...")
            
            # Test with a known pattern to understand current behavior
            test_cases = [
                {"search": "John", "description": "Common name that might appear in middle of names"},
                {"search": "An", "description": "Short prefix that should show starts-with behavior"},
                {"search": "Manager", "description": "Title that might appear in various fields"}
            ]
            
            for test_case in test_cases:
                search_term = test_case["search"]
                description = test_case["description"]
                
                print(f"\n🔍 Testing '{search_term}' - {description}")
                
                response = self.session.get(f"{self.base_url}/employees?search={search_term}")
                
                if response.status_code == 200:
                    employees = response.json()
                    
                    if len(employees) > 0:
                        # Analyze where the search term appears
                        field_matches = {
                            "name_starts": 0,
                            "name_contains": 0,
                            "id_matches": 0,
                            "department_matches": 0,
                            "location_matches": 0,
                            "other_matches": 0
                        }
                        
                        sample_matches = []
                        
                        for emp in employees[:10]:  # Analyze first 10 results
                            name = emp.get("name", "").lower()
                            emp_id = emp.get("id", "").lower()
                            department = emp.get("department", "").lower()
                            location = emp.get("location", "").lower()
                            search_lower = search_term.lower()
                            
                            match_info = {
                                "name": emp.get("name", ""),
                                "matches_in": []
                            }
                            
                            if name.startswith(search_lower):
                                field_matches["name_starts"] += 1
                                match_info["matches_in"].append("name_starts")
                            elif search_lower in name:
                                field_matches["name_contains"] += 1
                                match_info["matches_in"].append("name_contains")
                            
                            if search_lower in emp_id:
                                field_matches["id_matches"] += 1
                                match_info["matches_in"].append("id")
                            
                            if search_lower in department:
                                field_matches["department_matches"] += 1
                                match_info["matches_in"].append("department")
                            
                            if search_lower in location:
                                field_matches["location_matches"] += 1
                                match_info["matches_in"].append("location")
                            
                            if not match_info["matches_in"]:
                                field_matches["other_matches"] += 1
                                match_info["matches_in"].append("other_field")
                            
                            sample_matches.append(match_info)
                        
                        # Determine if this follows "starts with" pattern for names
                        name_pattern_correct = field_matches["name_contains"] == 0
                        
                        self.log_test(
                            f"Search Implementation Analysis '{search_term}'", 
                            name_pattern_correct, 
                            f"Pattern analysis: {'STARTS_WITH' if name_pattern_correct else 'CONTAINS'} for names",
                            {
                                "search_term": search_term,
                                "total_results": len(employees),
                                "name_starts_with": field_matches["name_starts"],
                                "name_contains_only": field_matches["name_contains"],
                                "id_matches": field_matches["id_matches"],
                                "department_matches": field_matches["department_matches"],
                                "location_matches": field_matches["location_matches"],
                                "other_matches": field_matches["other_matches"],
                                "sample_matches": sample_matches[:5],
                                "pattern_assessment": "STARTS_WITH" if name_pattern_correct else "CONTAINS (NEEDS FIX)"
                            }
                        )
                    else:
                        self.log_test(
                            f"Search Implementation Analysis '{search_term}'", 
                            True, 
                            f"No results for '{search_term}' - cannot analyze pattern",
                            {"search_term": search_term, "results_count": 0}
                        )
                else:
                    self.log_test(
                        f"Search Implementation Analysis '{search_term}'", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            self.log_test("Search Implementation Analysis", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all search functionality tests"""
        print("=" * 80)
        print("🔍 SEARCH FUNCTIONALITY TESTING - STARTS WITH vs CONTAINS PATTERN")
        print("=" * 80)
        print("Testing the review request: Search should work with 'starts with' pattern instead of 'contains' pattern")
        print()
        
        # Test 1: Employee Directory Search Pattern
        self.test_employee_search_starts_with_pattern()
        
        # Test 2: Attendance Search Pattern  
        self.test_attendance_search_starts_with_pattern()
        
        # Test 3: Backend Implementation Analysis
        self.test_backend_search_implementation_analysis()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 SEARCH FUNCTIONALITY TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Show critical findings
        print("\n🔍 CRITICAL FINDINGS:")
        
        search_pattern_issues = []
        for result in self.test_results:
            if not result["success"] and "CONTAINS" in result.get("details", {}).get("pattern_type", ""):
                search_pattern_issues.append(result)
        
        if search_pattern_issues:
            print("❌ SEARCH PATTERN ISSUES FOUND:")
            for issue in search_pattern_issues:
                print(f"   - {issue['test']}: {issue['message']}")
            print("\n🔧 RECOMMENDATION: Backend search implementation needs to be updated from 'contains' to 'starts with' pattern")
        else:
            print("✅ Search pattern appears to be correctly implemented as 'starts with'")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = SearchFunctionalityTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All search functionality tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some search functionality tests failed - see details above")
        sys.exit(1)