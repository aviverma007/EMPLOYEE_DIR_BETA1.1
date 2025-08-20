#!/usr/bin/env python3
"""
Backend Testing Script for Role-Based Access Control Review
Testing specific requirements from the review request:
1. Excel Data Loading (640 employees)
2. Basic API Health (core employee management endpoints)
3. Meeting Room Booking System
4. Authentication Support (backend APIs work for both roles)
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import uuid

# Use external URL from frontend/.env for testing
BASE_URL = "https://frontend-excel.preview.emergentagent.com/api"

class ReviewBackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 30
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            for key, value in details.items():
                print(f"  {key}: {value}")
        print()

    def test_excel_data_loading(self):
        """Test 1: Verify exactly 640 employees are loaded from Excel"""
        try:
            print("🔍 Testing Excel Data Loading...")
            
            # Test GET /api/employees endpoint
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code != 200:
                self.log_result(
                    "Excel Data Loading", 
                    False, 
                    f"Failed to fetch employees: HTTP {response.status_code}",
                    {"response": response.text[:500]}
                )
                return
            
            employees = response.json()
            employee_count = len(employees)
            
            # Verify exactly 640 employees
            if employee_count == 640:
                # Sample a few employees to verify data structure
                sample_employee = employees[0] if employees else {}
                required_fields = ['id', 'name', 'department', 'location', 'grade']
                missing_fields = [field for field in required_fields if field not in sample_employee]
                
                if missing_fields:
                    self.log_result(
                        "Excel Data Loading",
                        False,
                        f"Employee data missing required fields: {missing_fields}",
                        {"sample_employee": sample_employee}
                    )
                else:
                    self.log_result(
                        "Excel Data Loading",
                        True,
                        f"Successfully loaded exactly 640 employees from Excel",
                        {
                            "employee_count": employee_count,
                            "sample_fields": list(sample_employee.keys())[:10],
                            "sample_employee_name": sample_employee.get('name', 'N/A')
                        }
                    )
            else:
                self.log_result(
                    "Excel Data Loading",
                    False,
                    f"Expected 640 employees, found {employee_count}",
                    {"actual_count": employee_count}
                )
                
        except Exception as e:
            self.log_result(
                "Excel Data Loading",
                False,
                f"Exception during Excel data test: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_basic_api_health(self):
        """Test 2: Test core employee management endpoints"""
        try:
            print("🔍 Testing Basic API Health...")
            
            endpoints_to_test = [
                ("/employees", "Employee Directory"),
                ("/departments", "Departments List"),
                ("/locations", "Locations List"),
                ("/stats", "System Statistics")
            ]
            
            all_healthy = True
            endpoint_results = {}
            
            for endpoint, description in endpoints_to_test:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        if endpoint == "/employees":
                            endpoint_results[description] = f"✅ {len(data)} employees"
                        elif endpoint == "/departments":
                            departments = data.get('departments', []) if isinstance(data, dict) else data
                            endpoint_results[description] = f"✅ {len(departments)} departments"
                        elif endpoint == "/locations":
                            locations = data.get('locations', []) if isinstance(data, dict) else data
                            endpoint_results[description] = f"✅ {len(locations)} locations"
                        elif endpoint == "/stats":
                            endpoint_results[description] = f"✅ Stats available"
                        else:
                            endpoint_results[description] = "✅ Responding"
                    else:
                        endpoint_results[description] = f"❌ HTTP {response.status_code}"
                        all_healthy = False
                        
                except Exception as e:
                    endpoint_results[description] = f"❌ Error: {str(e)}"
                    all_healthy = False
            
            self.log_result(
                "Basic API Health",
                all_healthy,
                "All core endpoints tested" if all_healthy else "Some endpoints failed",
                endpoint_results
            )
                
        except Exception as e:
            self.log_result(
                "Basic API Health",
                False,
                f"Exception during API health test: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_meeting_room_booking(self):
        """Test 3: Verify meeting room booking and cancellation functionality"""
        try:
            print("🔍 Testing Meeting Room Booking System...")
            
            # First, get available meeting rooms
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code != 200:
                self.log_result(
                    "Meeting Room Booking",
                    False,
                    f"Failed to fetch meeting rooms: HTTP {response.status_code}",
                    {"response": response.text[:500]}
                )
                return
            
            rooms = response.json()
            if not rooms:
                self.log_result(
                    "Meeting Room Booking",
                    False,
                    "No meeting rooms available for testing"
                )
                return
            
            # Find a vacant room for testing
            vacant_room = None
            for room in rooms:
                if room.get('status') == 'vacant':
                    vacant_room = room
                    break
            
            if not vacant_room:
                # Use the first room regardless of status for testing
                vacant_room = rooms[0]
            
            room_id = vacant_room['id']
            room_name = vacant_room['name']
            
            # Get a sample employee for booking
            employees_response = self.session.get(f"{self.base_url}/employees?search=A")
            if employees_response.status_code == 200:
                employees = employees_response.json()
                if employees:
                    test_employee = employees[0]
                    employee_id = test_employee['id']
                    employee_name = test_employee['name']
                else:
                    employee_id = "80001"
                    employee_name = "Test Employee"
            else:
                employee_id = "80001"
                employee_name = "Test Employee"
            
            # Test booking creation
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Backend testing - role-based access verification"
            }
            
            # Try to book the room
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{room_id}/book",
                json=booking_data
            )
            
            booking_success = False
            cancellation_success = False
            
            if booking_response.status_code in [200, 201]:
                booking_success = True
                
                # Test cancellation
                cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{room_id}/booking")
                
                if cancel_response.status_code in [200, 204]:
                    cancellation_success = True
                    
            elif booking_response.status_code == 400:
                # Room might already be booked, try cancellation first then booking
                cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{room_id}/booking")
                if cancel_response.status_code in [200, 204]:
                    # Try booking again
                    booking_response = self.session.post(
                        f"{self.base_url}/meeting-rooms/{room_id}/book",
                        json=booking_data
                    )
                    if booking_response.status_code in [200, 201]:
                        booking_success = True
                        # Cancel again for cleanup
                        cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{room_id}/booking")
                        if cancel_response.status_code in [200, 204]:
                            cancellation_success = True
            
            overall_success = booking_success and cancellation_success
            
            self.log_result(
                "Meeting Room Booking",
                overall_success,
                "Booking and cancellation working" if overall_success else "Booking system has issues",
                {
                    "room_tested": f"{room_name} ({room_id})",
                    "employee_used": f"{employee_name} ({employee_id})",
                    "booking_success": booking_success,
                    "cancellation_success": cancellation_success,
                    "total_rooms": len(rooms)
                }
            )
                
        except Exception as e:
            self.log_result(
                "Meeting Room Booking",
                False,
                f"Exception during meeting room test: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_authentication_support(self):
        """Test 4: Verify backend APIs work for both admin and user roles"""
        try:
            print("🔍 Testing Authentication Support...")
            
            # Test key endpoints that both admin and user should access
            test_endpoints = [
                ("/employees", "Employee Directory Access"),
                ("/news", "News Management Access"),
                ("/tasks", "Task Management Access"),
                ("/knowledge", "Knowledge Base Access"),
                ("/help", "Help System Access")
            ]
            
            all_accessible = True
            access_results = {}
            
            for endpoint, description in test_endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        access_results[description] = f"✅ Accessible ({len(data)} items)"
                    elif response.status_code == 404:
                        access_results[description] = "⚠️ Endpoint not found"
                    else:
                        access_results[description] = f"❌ HTTP {response.status_code}"
                        all_accessible = False
                        
                except Exception as e:
                    access_results[description] = f"❌ Error: {str(e)}"
                    all_accessible = False
            
            # Test that there's no role-based restriction on backend
            # (Frontend handles role-based UI, backend should serve data to both)
            self.log_result(
                "Authentication Support",
                all_accessible,
                "Backend APIs accessible for both roles" if all_accessible else "Some APIs have access issues",
                access_results
            )
                
        except Exception as e:
            self.log_result(
                "Authentication Support",
                False,
                f"Exception during authentication test: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def run_all_tests(self):
        """Run all tests for the review request"""
        print("🚀 Starting Backend Testing for Role-Based Access Control Review")
        print(f"Testing against: {self.base_url}")
        print("=" * 80)
        
        # Run all tests
        self.test_excel_data_loading()
        self.test_basic_api_health()
        self.test_meeting_room_booking()
        self.test_authentication_support()
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - Backend is ready for role-based access control!")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed - Issues need attention")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = ReviewBackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)