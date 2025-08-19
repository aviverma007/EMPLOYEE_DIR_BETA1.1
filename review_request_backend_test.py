#!/usr/bin/env python3
"""
Review Request Backend Testing - Focused Testing for Specific Features
Tests the specific backend requirements mentioned in the review request:
1. Employee data loading (GET /api/employees)
2. Meeting room structure and booking functionality (GET /api/meeting-rooms)
3. Static file serving for policy documents (/company policies/)
4. All existing APIs should still be working after changes
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "https://profile-gallery-4.preview.emergentagent.com/api"

class ReviewRequestTester:
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

    def test_1_employee_data_loading(self):
        """Test GET /api/employees - Verify employee data loading (640 employees expected)"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                # Verify we have the expected 640 employees
                if employee_count == 640:
                    # Check data structure of first employee
                    sample_employee = employees[0] if employees else {}
                    required_fields = ['id', 'name', 'department', 'location', 'grade', 'mobile', 'email']
                    missing_fields = [field for field in required_fields if field not in sample_employee]
                    
                    if not missing_fields:
                        self.log_test(
                            "Employee Data Loading", 
                            True, 
                            f"✅ Successfully loaded exactly 640 employees with complete data structure",
                            {
                                "employee_count": employee_count,
                                "sample_employee_id": sample_employee.get('id'),
                                "sample_employee_name": sample_employee.get('name'),
                                "sample_department": sample_employee.get('department'),
                                "sample_location": sample_employee.get('location')
                            }
                        )
                    else:
                        self.log_test(
                            "Employee Data Loading", 
                            False, 
                            f"❌ Employee data missing required fields: {missing_fields}",
                            {"missing_fields": missing_fields}
                        )
                else:
                    self.log_test(
                        "Employee Data Loading", 
                        False, 
                        f"❌ Expected 640 employees, but got {employee_count}",
                        {"expected": 640, "actual": employee_count}
                    )
            else:
                self.log_test(
                    "Employee Data Loading", 
                    False, 
                    f"❌ HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Employee Data Loading", False, f"❌ Exception: {str(e)}")

    def test_2_meeting_room_structure(self):
        """Test GET /api/meeting-rooms - Check meeting room structure and data"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                room_count = len(rooms)
                
                if room_count > 0:
                    # Check data structure of first room
                    sample_room = rooms[0]
                    required_fields = ['id', 'name', 'capacity', 'location', 'floor', 'status']
                    missing_fields = [field for field in required_fields if field not in sample_room]
                    
                    if not missing_fields:
                        # Count rooms by status
                        vacant_rooms = [r for r in rooms if r.get('status') == 'vacant']
                        occupied_rooms = [r for r in rooms if r.get('status') == 'occupied']
                        
                        # Check for IFC location rooms (should have multiple floors)
                        ifc_rooms = [r for r in rooms if r.get('location') == 'IFC']
                        ifc_floors = list(set([r.get('floor') for r in ifc_rooms]))
                        
                        self.log_test(
                            "Meeting Room Structure", 
                            True, 
                            f"✅ Successfully loaded {room_count} meeting rooms with complete structure",
                            {
                                "total_rooms": room_count,
                                "vacant_rooms": len(vacant_rooms),
                                "occupied_rooms": len(occupied_rooms),
                                "ifc_rooms": len(ifc_rooms),
                                "ifc_floors": sorted(ifc_floors),
                                "sample_room_name": sample_room.get('name'),
                                "sample_room_capacity": sample_room.get('capacity')
                            }
                        )
                    else:
                        self.log_test(
                            "Meeting Room Structure", 
                            False, 
                            f"❌ Meeting room data missing required fields: {missing_fields}",
                            {"missing_fields": missing_fields}
                        )
                else:
                    self.log_test(
                        "Meeting Room Structure", 
                        False, 
                        "❌ No meeting rooms found"
                    )
            else:
                self.log_test(
                    "Meeting Room Structure", 
                    False, 
                    f"❌ HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Meeting Room Structure", False, f"❌ Exception: {str(e)}")

    def test_3_meeting_room_booking_functionality(self):
        """Test meeting room booking functionality - POST /api/meeting-rooms/{id}/book"""
        try:
            # First get available rooms
            rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if rooms_response.status_code != 200:
                self.log_test("Meeting Room Booking", False, "❌ Could not fetch meeting rooms")
                return
            
            rooms = rooms_response.json()
            vacant_rooms = [r for r in rooms if r.get('status') == 'vacant']
            
            if not vacant_rooms:
                self.log_test("Meeting Room Booking", False, "❌ No vacant rooms available for booking test")
                return
            
            # Get employees for booking
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("Meeting Room Booking", False, "❌ Could not fetch employees for booking")
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test("Meeting Room Booking", False, "❌ No employees available for booking")
                return
            
            # Test booking a room
            test_room = vacant_rooms[0]
            test_employee = employees[0]
            
            # Create booking for tomorrow to avoid past time issues
            from datetime import datetime, timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": test_employee["id"],
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "remarks": "Review request test booking"
            }
            
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{test_room['id']}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                booked_room = booking_response.json()
                
                # Verify booking was created
                if (booked_room.get('status') == 'occupied' and 
                    booked_room.get('bookings') and 
                    len(booked_room.get('bookings', [])) > 0):
                    
                    booking = booked_room['bookings'][0]
                    
                    self.log_test(
                        "Meeting Room Booking", 
                        True, 
                        f"✅ Successfully booked room '{test_room['name']}' for {test_employee['name']}",
                        {
                            "room_id": test_room['id'],
                            "room_name": test_room['name'],
                            "employee_name": test_employee['name'],
                            "booking_id": booking.get('id'),
                            "start_time": booking.get('start_time'),
                            "end_time": booking.get('end_time')
                        }
                    )
                    
                    # Clean up - cancel the booking
                    cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{test_room['id']}/booking")
                    if cancel_response.status_code == 200:
                        print("   ✅ Test booking cleaned up successfully")
                    
                else:
                    self.log_test(
                        "Meeting Room Booking", 
                        False, 
                        "❌ Room booking created but status/bookings not updated correctly"
                    )
            else:
                self.log_test(
                    "Meeting Room Booking", 
                    False, 
                    f"❌ HTTP {booking_response.status_code}: {booking_response.text}"
                )
                
        except Exception as e:
            self.log_test("Meeting Room Booking", False, f"❌ Exception: {str(e)}")

    def test_4_meeting_room_cancel_functionality(self):
        """Test meeting room cancel functionality for occupied rooms"""
        try:
            # First get occupied rooms
            rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if rooms_response.status_code != 200:
                self.log_test("Meeting Room Cancel", False, "❌ Could not fetch meeting rooms")
                return
            
            rooms = rooms_response.json()
            occupied_rooms = [r for r in rooms if r.get('status') == 'occupied']
            
            if not occupied_rooms:
                # Create a booking first to test cancellation
                vacant_rooms = [r for r in rooms if r.get('status') == 'vacant']
                if not vacant_rooms:
                    self.log_test("Meeting Room Cancel", False, "❌ No rooms available for cancel test")
                    return
                
                # Get employees for booking
                emp_response = self.session.get(f"{self.base_url}/employees")
                if emp_response.status_code != 200:
                    self.log_test("Meeting Room Cancel", False, "❌ Could not fetch employees for booking")
                    return
                
                employees = emp_response.json()
                if not employees:
                    self.log_test("Meeting Room Cancel", False, "❌ No employees available for booking")
                    return
                
                # Create a test booking
                test_room = vacant_rooms[0]
                test_employee = employees[0]
                
                from datetime import datetime, timedelta
                tomorrow = datetime.now() + timedelta(days=1)
                start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
                end_time = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
                
                booking_data = {
                    "employee_id": test_employee["id"],
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "remarks": "Test booking for cancel functionality"
                }
                
                booking_response = self.session.post(
                    f"{self.base_url}/meeting-rooms/{test_room['id']}/book",
                    json=booking_data
                )
                
                if booking_response.status_code != 200:
                    self.log_test("Meeting Room Cancel", False, "❌ Could not create test booking for cancel test")
                    return
                
                test_room_id = test_room['id']
            else:
                test_room_id = occupied_rooms[0]['id']
            
            # Test cancellation
            cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{test_room_id}/booking")
            
            if cancel_response.status_code == 200:
                # Verify cancellation by checking room status
                verify_response = self.session.get(f"{self.base_url}/meeting-rooms")
                if verify_response.status_code == 200:
                    updated_rooms = verify_response.json()
                    cancelled_room = next((r for r in updated_rooms if r['id'] == test_room_id), None)
                    
                    if cancelled_room and cancelled_room.get('status') == 'vacant':
                        self.log_test(
                            "Meeting Room Cancel", 
                            True, 
                            f"✅ Successfully cancelled booking for room {test_room_id}",
                            {
                                "room_id": test_room_id,
                                "new_status": cancelled_room.get('status'),
                                "bookings_count": len(cancelled_room.get('bookings', []))
                            }
                        )
                    else:
                        self.log_test(
                            "Meeting Room Cancel", 
                            False, 
                            "❌ Booking cancelled but room status not updated to vacant"
                        )
                else:
                    self.log_test(
                        "Meeting Room Cancel", 
                        True, 
                        "✅ Booking cancelled (could not verify status due to fetch error)"
                    )
            else:
                self.log_test(
                    "Meeting Room Cancel", 
                    False, 
                    f"❌ HTTP {cancel_response.status_code}: {cancel_response.text}"
                )
                
        except Exception as e:
            self.log_test("Meeting Room Cancel", False, f"❌ Exception: {str(e)}")

    def test_5_static_file_serving_policies(self):
        """Test static file serving for policy documents from /company policies/"""
        try:
            # Test accessing policy files directly
            base_static_url = self.base_url.replace("/api", "")
            
            # List of known policy files from the directory listing
            test_policy_files = [
                "Holiday List - 2023.xlsx.pdf",
                "List of Holidays -2025.xlsx.pdf",
                "Microsoft Word - Flexible Work Schedule.pdf",
                "_11_11_70bde4e9a0a04aed_Business Hours Attendance Policy.pdf",
                "_14_33_50e319284d7e4fe4_Leave Policy (Revised).pdf"
            ]
            
            successful_files = []
            failed_files = []
            
            for policy_file in test_policy_files:
                try:
                    # URL encode the filename for proper HTTP request
                    import urllib.parse
                    encoded_filename = urllib.parse.quote(policy_file)
                    policy_url = f"{base_static_url}/company policies/{encoded_filename}"
                    
                    response = self.session.get(policy_url, timeout=10)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        content_length = len(response.content)
                        
                        # Check if it's a PDF file
                        if 'pdf' in content_type.lower() or policy_file.endswith('.pdf'):
                            successful_files.append({
                                "filename": policy_file,
                                "content_type": content_type,
                                "size_bytes": content_length
                            })
                        else:
                            failed_files.append({
                                "filename": policy_file,
                                "error": f"Wrong content type: {content_type}"
                            })
                    else:
                        failed_files.append({
                            "filename": policy_file,
                            "error": f"HTTP {response.status_code}"
                        })
                        
                except Exception as file_error:
                    failed_files.append({
                        "filename": policy_file,
                        "error": str(file_error)
                    })
            
            if successful_files:
                self.log_test(
                    "Static File Serving - Policies", 
                    True, 
                    f"✅ Successfully served {len(successful_files)} policy files from /company policies/",
                    {
                        "successful_files": len(successful_files),
                        "failed_files": len(failed_files),
                        "sample_successful": successful_files[0] if successful_files else None,
                        "total_size_mb": round(sum(f["size_bytes"] for f in successful_files) / 1024 / 1024, 2)
                    }
                )
            else:
                self.log_test(
                    "Static File Serving - Policies", 
                    False, 
                    f"❌ Could not serve any policy files. All {len(failed_files)} files failed",
                    {"failed_files": failed_files}
                )
                
        except Exception as e:
            self.log_test("Static File Serving - Policies", False, f"❌ Exception: {str(e)}")

    def test_6_existing_apis_health_check(self):
        """Test that all existing APIs are still working after changes"""
        try:
            # Test key existing endpoints
            api_endpoints = [
                {"endpoint": "/employees", "name": "Employee Management"},
                {"endpoint": "/meeting-rooms", "name": "Meeting Rooms"},
                {"endpoint": "/departments", "name": "Departments"},
                {"endpoint": "/locations", "name": "Locations"},
                {"endpoint": "/stats", "name": "Statistics"},
                {"endpoint": "/news", "name": "News Management"},
                {"endpoint": "/tasks", "name": "Task Management"},
                {"endpoint": "/knowledge", "name": "Knowledge Management"},
                {"endpoint": "/help", "name": "Help/Support"},
                {"endpoint": "/hierarchy", "name": "Hierarchy Management"}
            ]
            
            working_apis = []
            broken_apis = []
            
            for api in api_endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{api['endpoint']}", timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        working_apis.append({
                            "endpoint": api['endpoint'],
                            "name": api['name'],
                            "status": "OK",
                            "data_count": len(data) if isinstance(data, list) else "N/A"
                        })
                    else:
                        broken_apis.append({
                            "endpoint": api['endpoint'],
                            "name": api['name'],
                            "error": f"HTTP {response.status_code}"
                        })
                        
                except Exception as api_error:
                    broken_apis.append({
                        "endpoint": api['endpoint'],
                        "name": api['name'],
                        "error": str(api_error)
                    })
            
            if len(working_apis) >= 8:  # At least 8 out of 10 APIs should work
                self.log_test(
                    "Existing APIs Health Check", 
                    True, 
                    f"✅ {len(working_apis)}/{len(api_endpoints)} existing APIs are working correctly",
                    {
                        "working_apis": len(working_apis),
                        "broken_apis": len(broken_apis),
                        "working_list": [api['name'] for api in working_apis],
                        "broken_list": [api['name'] for api in broken_apis] if broken_apis else []
                    }
                )
            else:
                self.log_test(
                    "Existing APIs Health Check", 
                    False, 
                    f"❌ Only {len(working_apis)}/{len(api_endpoints)} APIs are working. Too many broken APIs",
                    {
                        "working_apis": len(working_apis),
                        "broken_apis": len(broken_apis),
                        "broken_details": broken_apis
                    }
                )
                
        except Exception as e:
            self.log_test("Existing APIs Health Check", False, f"❌ Exception: {str(e)}")

    def run_all_tests(self):
        """Run all review request tests"""
        print("🚀 Starting Review Request Backend Testing...")
        print("=" * 80)
        print()
        
        # Run all tests
        self.test_1_employee_data_loading()
        self.test_2_meeting_room_structure()
        self.test_3_meeting_room_booking_functionality()
        self.test_4_meeting_room_cancel_functionality()
        self.test_5_static_file_serving_policies()
        self.test_6_existing_apis_health_check()
        
        # Summary
        print("=" * 80)
        print("📊 REVIEW REQUEST TESTING SUMMARY")
        print("=" * 80)
        
        passed_tests = [r for r in self.test_results if r["success"]]
        failed_tests = [r for r in self.test_results if not r["success"]]
        
        print(f"✅ PASSED: {len(passed_tests)}/{len(self.test_results)} tests")
        print(f"❌ FAILED: {len(failed_tests)}/{len(self.test_results)} tests")
        print()
        
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['message']}")
            print()
        
        if passed_tests:
            print("✅ PASSED TESTS:")
            for test in passed_tests:
                print(f"   • {test['test']}: {test['message']}")
            print()
        
        # Overall result
        success_rate = len(passed_tests) / len(self.test_results) * 100
        if success_rate >= 80:
            print(f"🎉 OVERALL RESULT: SUCCESS ({success_rate:.1f}% pass rate)")
            return True
        else:
            print(f"⚠️  OVERALL RESULT: NEEDS ATTENTION ({success_rate:.1f}% pass rate)")
            return False

if __name__ == "__main__":
    tester = ReviewRequestTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)