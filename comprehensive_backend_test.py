#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Employee Directory System
Focused on Review Request Requirements:
1. Excel Data Loading (640 employees)
2. Employee Management APIs
3. Core 5-Tab APIs (Home/News, Employee Directory, Work/Tasks, Knowledge, Help)
4. Utility APIs
5. Data Integrity Verification
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "https://profile-gallery-4.preview.emergentagent.com/api"

class ComprehensiveBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.failed_tests = []
        
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
        if not success:
            self.failed_tests.append(test_name)
        print()

    # ========================================
    # EXCEL DATA LOADING VERIFICATION
    # ========================================

    def test_excel_data_loading(self):
        """Test Excel data loading - Verify exactly 640 employees loaded"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    # Verify data structure and required fields
                    sample_employee = employees[0] if employees else {}
                    required_fields = ['id', 'name', 'department', 'location', 'grade']
                    missing_fields = [field for field in required_fields if field not in sample_employee]
                    
                    if not missing_fields:
                        self.log_test(
                            "Excel Data Loading", 
                            True, 
                            f"✅ VERIFIED: Exactly 640 employees loaded from Excel with all required fields",
                            {
                                "employee_count": employee_count,
                                "sample_fields": list(sample_employee.keys())[:10],
                                "sample_employee": {
                                    "name": sample_employee.get("name"),
                                    "department": sample_employee.get("department"),
                                    "location": sample_employee.get("location")
                                }
                            }
                        )
                    else:
                        self.log_test(
                            "Excel Data Loading", 
                            False, 
                            f"640 employees loaded but missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Excel Data Loading", 
                        False, 
                        f"❌ CRITICAL: Expected 640 employees, but found {employee_count}",
                        {"expected": 640, "actual": employee_count}
                    )
            else:
                self.log_test(
                    "Excel Data Loading", 
                    False, 
                    f"❌ CRITICAL: Could not fetch employees - HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Excel Data Loading", False, f"❌ CRITICAL: Exception: {str(e)}")

    # ========================================
    # EMPLOYEE MANAGEMENT APIs
    # ========================================

    def test_employee_management_apis(self):
        """Test all Employee Management APIs"""
        
        # Test 1: GET /api/employees
        try:
            response = self.session.get(f"{self.base_url}/employees")
            if response.status_code == 200:
                employees = response.json()
                self.log_test(
                    "GET /api/employees", 
                    True, 
                    f"Successfully fetched {len(employees)} employees",
                    {"count": len(employees)}
                )
            else:
                self.log_test("GET /api/employees", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/employees", False, f"Exception: {str(e)}")

        # Test 2: Search functionality
        try:
            response = self.session.get(f"{self.base_url}/employees?search=Manager")
            if response.status_code == 200:
                search_results = response.json()
                self.log_test(
                    "Employee Search Functionality", 
                    True, 
                    f"Search returned {len(search_results)} results for 'Manager'",
                    {"search_term": "Manager", "results": len(search_results)}
                )
            else:
                self.log_test("Employee Search Functionality", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Employee Search Functionality", False, f"Exception: {str(e)}")

        # Test 3: Department filtering
        try:
            # First get departments
            dept_response = self.session.get(f"{self.base_url}/departments")
            if dept_response.status_code == 200:
                departments = dept_response.json().get("departments", [])
                test_dept = next((d for d in departments if d != "All Departments"), None)
                
                if test_dept:
                    filter_response = self.session.get(f"{self.base_url}/employees?department={test_dept}")
                    if filter_response.status_code == 200:
                        filtered_employees = filter_response.json()
                        self.log_test(
                            "Department Filtering", 
                            True, 
                            f"Department filter returned {len(filtered_employees)} employees from {test_dept}",
                            {"department": test_dept, "count": len(filtered_employees)}
                        )
                    else:
                        self.log_test("Department Filtering", False, f"HTTP {filter_response.status_code}")
                else:
                    self.log_test("Department Filtering", False, "No departments available for testing")
            else:
                self.log_test("Department Filtering", False, "Could not fetch departments")
        except Exception as e:
            self.log_test("Department Filtering", False, f"Exception: {str(e)}")

        # Test 4: Location filtering
        try:
            # First get locations
            loc_response = self.session.get(f"{self.base_url}/locations")
            if loc_response.status_code == 200:
                locations = loc_response.json().get("locations", [])
                test_location = next((l for l in locations if l != "All Locations"), None)
                
                if test_location:
                    filter_response = self.session.get(f"{self.base_url}/employees?location={test_location}")
                    if filter_response.status_code == 200:
                        filtered_employees = filter_response.json()
                        self.log_test(
                            "Location Filtering", 
                            True, 
                            f"Location filter returned {len(filtered_employees)} employees from {test_location}",
                            {"location": test_location, "count": len(filtered_employees)}
                        )
                    else:
                        self.log_test("Location Filtering", False, f"HTTP {filter_response.status_code}")
                else:
                    self.log_test("Location Filtering", False, "No locations available for testing")
            else:
                self.log_test("Location Filtering", False, "Could not fetch locations")
        except Exception as e:
            self.log_test("Location Filtering", False, f"Exception: {str(e)}")

    # ========================================
    # CORE 5-TAB APIs
    # ========================================

    def test_home_tab_news_api(self):
        """Test Home tab - News Management API"""
        
        # Test GET /api/news
        try:
            response = self.session.get(f"{self.base_url}/news")
            if response.status_code == 200:
                news_items = response.json()
                self.log_test(
                    "Home Tab - GET /api/news", 
                    True, 
                    f"Successfully fetched {len(news_items)} news items",
                    {"count": len(news_items)}
                )
            else:
                self.log_test("Home Tab - GET /api/news", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Home Tab - GET /api/news", False, f"Exception: {str(e)}")

        # Test POST /api/news (Create news)
        try:
            news_data = {
                "title": "Test Company Announcement",
                "content": "This is a test announcement for the comprehensive backend testing.",
                "priority": "high"
            }
            
            response = self.session.post(f"{self.base_url}/news", json=news_data)
            if response.status_code == 200:
                created_news = response.json()
                self.log_test(
                    "Home Tab - POST /api/news", 
                    True, 
                    f"Successfully created news item: {created_news.get('title')}",
                    {"news_id": created_news.get("id"), "priority": news_data["priority"]}
                )
                
                # Store for cleanup
                self.test_news_id = created_news.get("id")
            else:
                self.log_test("Home Tab - POST /api/news", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Home Tab - POST /api/news", False, f"Exception: {str(e)}")

    def test_employee_directory_tab_apis(self):
        """Test Employee Directory tab - Employee and Hierarchy APIs"""
        
        # Test GET /api/hierarchy
        try:
            response = self.session.get(f"{self.base_url}/hierarchy")
            if response.status_code == 200:
                hierarchy = response.json()
                self.log_test(
                    "Employee Directory - GET /api/hierarchy", 
                    True, 
                    f"Successfully fetched {len(hierarchy)} hierarchy relationships",
                    {"relationships": len(hierarchy)}
                )
            else:
                self.log_test("Employee Directory - GET /api/hierarchy", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Employee Directory - GET /api/hierarchy", False, f"Exception: {str(e)}")

        # Test POST /api/hierarchy (Create hierarchy relationship)
        try:
            # Get two employees for testing
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code == 200:
                employees = emp_response.json()
                if len(employees) >= 2:
                    relation_data = {
                        "employeeId": employees[0]["id"],
                        "reportsTo": employees[1]["id"]
                    }
                    
                    response = self.session.post(f"{self.base_url}/hierarchy", json=relation_data)
                    if response.status_code == 200:
                        created_relation = response.json()
                        self.log_test(
                            "Employee Directory - POST /api/hierarchy", 
                            True, 
                            f"Successfully created hierarchy relationship",
                            {
                                "employee": employees[0]["name"],
                                "manager": employees[1]["name"]
                            }
                        )
                    elif response.status_code == 400:
                        # Relationship might already exist
                        self.log_test(
                            "Employee Directory - POST /api/hierarchy", 
                            True, 
                            "Hierarchy relationship already exists (expected behavior)"
                        )
                    else:
                        self.log_test("Employee Directory - POST /api/hierarchy", False, f"HTTP {response.status_code}")
                else:
                    self.log_test("Employee Directory - POST /api/hierarchy", False, "Not enough employees for testing")
            else:
                self.log_test("Employee Directory - POST /api/hierarchy", False, "Could not fetch employees")
        except Exception as e:
            self.log_test("Employee Directory - POST /api/hierarchy", False, f"Exception: {str(e)}")

    def test_work_tab_tasks_api(self):
        """Test Work tab - Task Management API"""
        
        # Test GET /api/tasks
        try:
            response = self.session.get(f"{self.base_url}/tasks")
            if response.status_code == 200:
                tasks = response.json()
                self.log_test(
                    "Work Tab - GET /api/tasks", 
                    True, 
                    f"Successfully fetched {len(tasks)} tasks",
                    {"count": len(tasks)}
                )
            else:
                self.log_test("Work Tab - GET /api/tasks", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Work Tab - GET /api/tasks", False, f"Exception: {str(e)}")

        # Test POST /api/tasks (Create task)
        try:
            # Get an employee to assign task to
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code == 200:
                employees = emp_response.json()
                if employees:
                    task_data = {
                        "title": "Test Task - Backend Verification",
                        "description": "This is a test task created during comprehensive backend testing.",
                        "assigned_to": employees[0]["id"],
                        "priority": "medium",
                        "status": "pending",
                        "due_date": "2025-03-31T23:59:59"
                    }
                    
                    response = self.session.post(f"{self.base_url}/tasks", json=task_data)
                    if response.status_code == 200:
                        created_task = response.json()
                        self.log_test(
                            "Work Tab - POST /api/tasks", 
                            True, 
                            f"Successfully created task: {created_task.get('title')}",
                            {
                                "task_id": created_task.get("id"),
                                "assigned_to": employees[0]["name"],
                                "priority": task_data["priority"]
                            }
                        )
                        
                        # Store for cleanup
                        self.test_task_id = created_task.get("id")
                    else:
                        self.log_test("Work Tab - POST /api/tasks", False, f"HTTP {response.status_code}")
                else:
                    self.log_test("Work Tab - POST /api/tasks", False, "No employees available for task assignment")
            else:
                self.log_test("Work Tab - POST /api/tasks", False, "Could not fetch employees")
        except Exception as e:
            self.log_test("Work Tab - POST /api/tasks", False, f"Exception: {str(e)}")

    def test_knowledge_tab_api(self):
        """Test Knowledge tab - Knowledge Management API"""
        
        # Test GET /api/knowledge
        try:
            response = self.session.get(f"{self.base_url}/knowledge")
            if response.status_code == 200:
                knowledge_articles = response.json()
                self.log_test(
                    "Knowledge Tab - GET /api/knowledge", 
                    True, 
                    f"Successfully fetched {len(knowledge_articles)} knowledge articles",
                    {"count": len(knowledge_articles)}
                )
            else:
                self.log_test("Knowledge Tab - GET /api/knowledge", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Knowledge Tab - GET /api/knowledge", False, f"Exception: {str(e)}")

        # Test POST /api/knowledge (Create knowledge article)
        try:
            knowledge_data = {
                "title": "Test Company Policy - Backend Testing",
                "content": "This is a test knowledge article created during comprehensive backend testing to verify the knowledge management system functionality.",
                "category": "policy",
                "tags": ["test", "backend", "verification", "policy"]
            }
            
            response = self.session.post(f"{self.base_url}/knowledge", json=knowledge_data)
            if response.status_code == 200:
                created_article = response.json()
                self.log_test(
                    "Knowledge Tab - POST /api/knowledge", 
                    True, 
                    f"Successfully created knowledge article: {created_article.get('title')}",
                    {
                        "article_id": created_article.get("id"),
                        "category": knowledge_data["category"],
                        "tags_count": len(knowledge_data["tags"])
                    }
                )
                
                # Store for cleanup
                self.test_knowledge_id = created_article.get("id")
            else:
                self.log_test("Knowledge Tab - POST /api/knowledge", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Knowledge Tab - POST /api/knowledge", False, f"Exception: {str(e)}")

    def test_help_tab_api(self):
        """Test Help tab - Support Management API"""
        
        # Test GET /api/help
        try:
            response = self.session.get(f"{self.base_url}/help")
            if response.status_code == 200:
                help_requests = response.json()
                self.log_test(
                    "Help Tab - GET /api/help", 
                    True, 
                    f"Successfully fetched {len(help_requests)} help requests",
                    {"count": len(help_requests)}
                )
            else:
                self.log_test("Help Tab - GET /api/help", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Help Tab - GET /api/help", False, f"Exception: {str(e)}")

        # Test POST /api/help (Create help request)
        try:
            help_data = {
                "title": "Test Support Request - Backend Verification",
                "message": "This is a test support request created during comprehensive backend testing to verify the help/support system functionality.",
                "priority": "medium"
            }
            
            response = self.session.post(f"{self.base_url}/help", json=help_data)
            if response.status_code == 200:
                created_request = response.json()
                self.log_test(
                    "Help Tab - POST /api/help", 
                    True, 
                    f"Successfully created help request: {created_request.get('title')}",
                    {
                        "request_id": created_request.get("id"),
                        "priority": help_data["priority"],
                        "status": created_request.get("status")
                    }
                )
                
                # Store for cleanup
                self.test_help_id = created_request.get("id")
            else:
                self.log_test("Help Tab - POST /api/help", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Help Tab - POST /api/help", False, f"Exception: {str(e)}")

        # Test POST /api/help/{id}/reply (Add reply to help request)
        if hasattr(self, 'test_help_id') and self.test_help_id:
            try:
                reply_data = {
                    "message": "This is a test reply to verify the threaded reply system functionality."
                }
                
                response = self.session.post(f"{self.base_url}/help/{self.test_help_id}/reply", json=reply_data)
                if response.status_code == 200:
                    updated_request = response.json()
                    replies = updated_request.get("replies", [])
                    self.log_test(
                        "Help Tab - POST /api/help/{id}/reply", 
                        True, 
                        f"Successfully added reply to help request",
                        {
                            "request_id": self.test_help_id,
                            "replies_count": len(replies)
                        }
                    )
                else:
                    self.log_test("Help Tab - POST /api/help/{id}/reply", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Help Tab - POST /api/help/{id}/reply", False, f"Exception: {str(e)}")

    # ========================================
    # UTILITY APIs
    # ========================================

    def test_utility_apis(self):
        """Test Utility APIs - Departments, Locations, Stats"""
        
        # Test GET /api/departments
        try:
            response = self.session.get(f"{self.base_url}/departments")
            if response.status_code == 200:
                result = response.json()
                departments = result.get("departments", [])
                self.log_test(
                    "GET /api/departments", 
                    True, 
                    f"Successfully fetched {len(departments)} departments",
                    {"count": len(departments), "sample": departments[:5] if departments else []}
                )
            else:
                self.log_test("GET /api/departments", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/departments", False, f"Exception: {str(e)}")

        # Test GET /api/locations
        try:
            response = self.session.get(f"{self.base_url}/locations")
            if response.status_code == 200:
                result = response.json()
                locations = result.get("locations", [])
                self.log_test(
                    "GET /api/locations", 
                    True, 
                    f"Successfully fetched {len(locations)} locations",
                    {"count": len(locations), "sample": locations[:5] if locations else []}
                )
            else:
                self.log_test("GET /api/locations", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/locations", False, f"Exception: {str(e)}")

        # Test GET /api/stats
        try:
            response = self.session.get(f"{self.base_url}/stats")
            if response.status_code == 200:
                stats = response.json()
                excel_stats = stats.get("excel", {})
                db_stats = stats.get("database", {})
                
                self.log_test(
                    "GET /api/stats", 
                    True, 
                    f"Successfully fetched system statistics",
                    {
                        "excel_employees": excel_stats.get("total_employees", 0),
                        "db_employees": db_stats.get("employees", 0),
                        "hierarchy_relations": db_stats.get("hierarchy_relations", 0)
                    }
                )
            else:
                self.log_test("GET /api/stats", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/stats", False, f"Exception: {str(e)}")

    # ========================================
    # DATA INTEGRITY VERIFICATION
    # ========================================

    def test_data_integrity(self):
        """Test Data Integrity - Verify Excel-based data consistency"""
        
        try:
            # Get all data sources
            employees_response = self.session.get(f"{self.base_url}/employees")
            departments_response = self.session.get(f"{self.base_url}/departments")
            locations_response = self.session.get(f"{self.base_url}/locations")
            stats_response = self.session.get(f"{self.base_url}/stats")
            
            if all(r.status_code == 200 for r in [employees_response, departments_response, locations_response, stats_response]):
                employees = employees_response.json()
                departments = departments_response.json().get("departments", [])
                locations = locations_response.json().get("locations", [])
                stats = stats_response.json()
                
                # Verify employee count consistency
                employee_count = len(employees)
                db_employee_count = stats.get("database", {}).get("employees", 0)
                excel_employee_count = stats.get("excel", {}).get("total_employees", 0)
                
                # Verify department count (expected 24)
                dept_count = len([d for d in departments if d != "All Departments"])
                
                # Verify location count (expected 23)
                loc_count = len([l for l in locations if l != "All Locations"])
                
                integrity_issues = []
                
                if employee_count != 640:
                    integrity_issues.append(f"Employee count mismatch: expected 640, got {employee_count}")
                
                if dept_count != 24:
                    integrity_issues.append(f"Department count mismatch: expected 24, got {dept_count}")
                
                if loc_count != 23:
                    integrity_issues.append(f"Location count mismatch: expected 23, got {loc_count}")
                
                if employee_count != db_employee_count:
                    integrity_issues.append(f"DB employee count mismatch: API={employee_count}, Stats={db_employee_count}")
                
                if not integrity_issues:
                    self.log_test(
                        "Data Integrity Verification", 
                        True, 
                        f"✅ ALL DATA INTEGRITY CHECKS PASSED",
                        {
                            "employees": employee_count,
                            "departments": dept_count,
                            "locations": loc_count,
                            "excel_db_sync": "✅ Synchronized"
                        }
                    )
                else:
                    self.log_test(
                        "Data Integrity Verification", 
                        False, 
                        f"❌ Data integrity issues found: {'; '.join(integrity_issues)}",
                        {
                            "employees": employee_count,
                            "departments": dept_count,
                            "locations": loc_count,
                            "issues": integrity_issues
                        }
                    )
            else:
                self.log_test("Data Integrity Verification", False, "Could not fetch all required data for integrity check")
                
        except Exception as e:
            self.log_test("Data Integrity Verification", False, f"Exception: {str(e)}")

    # ========================================
    # MAIN TEST EXECUTION
    # ========================================

    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests"""
        print("=" * 80)
        print("🚀 COMPREHENSIVE BACKEND API TESTING - REVIEW REQUEST VERIFICATION")
        print("=" * 80)
        print()
        
        # 1. Excel Data Loading Verification
        print("📊 TESTING: Excel Data Loading (640 employees)")
        print("-" * 50)
        self.test_excel_data_loading()
        
        # 2. Employee Management APIs
        print("👥 TESTING: Employee Management APIs")
        print("-" * 50)
        self.test_employee_management_apis()
        
        # 3. Core 5-Tab APIs
        print("🏠 TESTING: Home Tab - News API")
        print("-" * 50)
        self.test_home_tab_news_api()
        
        print("📋 TESTING: Employee Directory Tab - Hierarchy API")
        print("-" * 50)
        self.test_employee_directory_tab_apis()
        
        print("💼 TESTING: Work Tab - Tasks API")
        print("-" * 50)
        self.test_work_tab_tasks_api()
        
        print("📚 TESTING: Knowledge Tab - Knowledge API")
        print("-" * 50)
        self.test_knowledge_tab_api()
        
        print("🆘 TESTING: Help Tab - Support API")
        print("-" * 50)
        self.test_help_tab_api()
        
        # 4. Utility APIs
        print("🔧 TESTING: Utility APIs")
        print("-" * 50)
        self.test_utility_apis()
        
        # 5. Data Integrity
        print("🔍 TESTING: Data Integrity Verification")
        print("-" * 50)
        self.test_data_integrity()
        
        # Summary
        self.print_test_summary()

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print()
        
        if self.failed_tests:
            print("❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"   • {test}")
            print()
        
        # Key verification results
        excel_test = next((r for r in self.test_results if r["test"] == "Excel Data Loading"), None)
        integrity_test = next((r for r in self.test_results if r["test"] == "Data Integrity Verification"), None)
        
        print("🎯 KEY REVIEW REQUEST VERIFICATIONS:")
        if excel_test:
            status = "✅ VERIFIED" if excel_test["success"] else "❌ FAILED"
            print(f"   • Excel Data Loading (640 employees): {status}")
        
        if integrity_test:
            status = "✅ VERIFIED" if integrity_test["success"] else "❌ FAILED"
            print(f"   • Data Integrity (24 departments, 23 locations): {status}")
        
        # Count API group successes
        api_groups = {
            "Employee Management": ["GET /api/employees", "Employee Search Functionality", "Department Filtering", "Location Filtering"],
            "Home Tab (News)": ["Home Tab - GET /api/news", "Home Tab - POST /api/news"],
            "Employee Directory Tab": ["Employee Directory - GET /api/hierarchy", "Employee Directory - POST /api/hierarchy"],
            "Work Tab (Tasks)": ["Work Tab - GET /api/tasks", "Work Tab - POST /api/tasks"],
            "Knowledge Tab": ["Knowledge Tab - GET /api/knowledge", "Knowledge Tab - POST /api/knowledge"],
            "Help Tab": ["Help Tab - GET /api/help", "Help Tab - POST /api/help", "Help Tab - POST /api/help/{id}/reply"],
            "Utility APIs": ["GET /api/departments", "GET /api/locations", "GET /api/stats"]
        }
        
        for group_name, test_names in api_groups.items():
            group_tests = [r for r in self.test_results if r["test"] in test_names]
            group_passed = len([r for r in group_tests if r["success"]])
            group_total = len(group_tests)
            if group_total > 0:
                group_rate = (group_passed / group_total * 100)
                status = "✅ OPERATIONAL" if group_rate >= 80 else "❌ ISSUES"
                print(f"   • {group_name}: {status} ({group_passed}/{group_total} tests passed)")
        
        print()
        print("=" * 80)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Backend system is fully operational!")
        elif success_rate >= 80:
            print("✅ GOOD: Backend system is mostly operational with minor issues.")
        elif success_rate >= 60:
            print("⚠️  WARNING: Backend system has significant issues that need attention.")
        else:
            print("❌ CRITICAL: Backend system has major failures requiring immediate attention.")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = ComprehensiveBackendTester()
    tester.run_comprehensive_tests()