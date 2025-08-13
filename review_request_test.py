#!/usr/bin/env python3
"""
Focused Meeting Rooms System Testing - Review Request Verification
Tests the updated meeting rooms system focusing on:
1. Excel Data Loading: Verify that 640 employees are loaded correctly from the Excel file
2. Meeting Rooms Update: Test that the 14th floor meeting rooms have the new names
3. API Functionality: Test the GET /api/meeting-rooms endpoint with filters for IFC location and floor 14
4. Booking System: Ensure the booking system still works correctly with the new room structure
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "https://change-maker.preview.emergentagent.com/api"

class MeetingRoomsSystemTester:
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

    def test_1_excel_data_loading(self):
        """Test Excel Data Loading: Verify that 640 employees are loaded correctly from the Excel file"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    self.log_test(
                        "Excel Data Loading",
                        True,
                        f"✅ Exactly 640 employees loaded correctly from Excel file",
                        {"employee_count": employee_count, "expected": 640}
                    )
                else:
                    self.log_test(
                        "Excel Data Loading",
                        False,
                        f"❌ Expected 640 employees, found {employee_count}",
                        {"employee_count": employee_count, "expected": 640}
                    )
            else:
                self.log_test(
                    "Excel Data Loading",
                    False,
                    f"❌ Failed to fetch employees: HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Excel Data Loading", False, f"❌ Exception: {str(e)}")

    def test_2_meeting_rooms_14th_floor_names(self):
        """Test Meeting Rooms Update: Test that the 14th floor meeting rooms have the new names"""
        try:
            # Get all meeting rooms for IFC location, floor 14
            response = self.session.get(f"{self.base_url}/meeting-rooms?location=IFC&floor=14")
            
            if response.status_code == 200:
                rooms = response.json()
                
                # Expected room names for 14th floor as specified in review request
                expected_rooms = {
                    'OVAL MEETING ROOM': {'capacity': 10},
                    'PETRONAS MEETING ROOM': {'capacity': 5},
                    'GLOBAL CENTER MEETING ROOM': {'capacity': 5},
                    'LOUVRE MEETING ROOM': {'capacity': 5},
                    'GOLDEN GATE MEETING ROOM': {'capacity': 10},
                    'EMPIRE STATE MEETING ROOM': {'capacity': 5},
                    'MARINA BAY MEETING ROOM': {'capacity': 5},
                    'BURJ MEETING ROOM': {'capacity': 5},
                    'BOARD ROOM': {'capacity': 20}
                }
                
                found_rooms = {}
                for room in rooms:
                    if room.get('floor') == '14' and room.get('location') == 'IFC':
                        found_rooms[room.get('name')] = {
                            'capacity': room.get('capacity'),
                            'id': room.get('id'),
                            'status': room.get('status')
                        }
                
                # Check if we have all expected rooms with correct capacities
                missing_rooms = []
                incorrect_capacities = []
                
                for room_name, expected_details in expected_rooms.items():
                    if room_name not in found_rooms:
                        missing_rooms.append(room_name)
                    else:
                        found_details = found_rooms[room_name]
                        if found_details['capacity'] != expected_details['capacity']:
                            incorrect_capacities.append(
                                f"{room_name}: capacity {found_details['capacity']} != {expected_details['capacity']}"
                            )
                
                if not missing_rooms and not incorrect_capacities and len(found_rooms) == 9:
                    self.log_test(
                        "14th Floor Meeting Rooms Names",
                        True,
                        f"✅ All 9 expected meeting rooms found with correct names and capacities",
                        {
                            "rooms_found": len(found_rooms),
                            "room_names": list(found_rooms.keys()),
                            "all_rooms_verified": True
                        }
                    )
                else:
                    error_details = []
                    if missing_rooms:
                        error_details.append(f"Missing rooms: {missing_rooms}")
                    if incorrect_capacities:
                        error_details.append(f"Incorrect capacities: {incorrect_capacities}")
                    if len(found_rooms) != 9:
                        error_details.append(f"Expected 9 rooms, found {len(found_rooms)}")
                    
                    self.log_test(
                        "14th Floor Meeting Rooms Names",
                        False,
                        f"❌ {'; '.join(error_details)}",
                        {
                            "found_rooms": list(found_rooms.keys()),
                            "expected_rooms": list(expected_rooms.keys()),
                            "rooms_count": len(found_rooms)
                        }
                    )
            else:
                self.log_test(
                    "14th Floor Meeting Rooms Names",
                    False,
                    f"❌ Failed to fetch 14th floor meeting rooms: HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("14th Floor Meeting Rooms Names", False, f"❌ Exception: {str(e)}")

    def test_3_api_functionality_filters(self):
        """Test API Functionality: Test the GET /api/meeting-rooms endpoint with filters for IFC location and floor 14"""
        try:
            # Test 1: Get all meeting rooms (baseline)
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            if response.status_code != 200:
                self.log_test(
                    "API Functionality Filters",
                    False,
                    f"❌ Failed to fetch all meeting rooms: HTTP {response.status_code}"
                )
                return
            
            all_rooms = response.json()
            total_rooms = len(all_rooms)
            
            # Test 2: Filter by IFC location only
            response = self.session.get(f"{self.base_url}/meeting-rooms?location=IFC")
            if response.status_code != 200:
                self.log_test(
                    "API Functionality Filters",
                    False,
                    f"❌ Failed to filter by IFC location: HTTP {response.status_code}"
                )
                return
            
            ifc_rooms = response.json()
            ifc_count = len(ifc_rooms)
            
            # Verify all returned rooms are from IFC
            ifc_filter_valid = all(room.get('location') == 'IFC' for room in ifc_rooms)
            
            # Test 3: Filter by IFC location and floor 14
            response = self.session.get(f"{self.base_url}/meeting-rooms?location=IFC&floor=14")
            if response.status_code != 200:
                self.log_test(
                    "API Functionality Filters",
                    False,
                    f"❌ Failed to filter by IFC location and floor 14: HTTP {response.status_code}"
                )
                return
            
            floor_14_rooms = response.json()
            floor_14_count = len(floor_14_rooms)
            
            # Verify all returned rooms are from IFC floor 14
            floor_14_filter_valid = all(
                room.get('location') == 'IFC' and room.get('floor') == '14' 
                for room in floor_14_rooms
            )
            
            # Expected: 9 rooms on floor 14 based on the review request
            expected_floor_14_count = 9
            
            if (ifc_filter_valid and floor_14_filter_valid and 
                floor_14_count == expected_floor_14_count):
                self.log_test(
                    "API Functionality Filters",
                    True,
                    f"✅ API filters working correctly for IFC location and floor 14",
                    {
                        "total_rooms": total_rooms,
                        "ifc_rooms": ifc_count,
                        "floor_14_rooms": floor_14_count,
                        "expected_floor_14": expected_floor_14_count,
                        "filters_valid": True
                    }
                )
            else:
                self.log_test(
                    "API Functionality Filters",
                    False,
                    f"❌ API filter validation failed",
                    {
                        "total_rooms": total_rooms,
                        "ifc_rooms": ifc_count,
                        "floor_14_rooms": floor_14_count,
                        "expected_floor_14": expected_floor_14_count,
                        "ifc_filter_valid": ifc_filter_valid,
                        "floor_14_filter_valid": floor_14_filter_valid
                    }
                )
                
        except Exception as e:
            self.log_test("API Functionality Filters", False, f"❌ Exception: {str(e)}")

    def test_4_booking_system_functionality(self):
        """Test Booking System: Ensure the booking system still works correctly with the new room structure"""
        try:
            # Get a room from the 14th floor to test booking
            response = self.session.get(f"{self.base_url}/meeting-rooms?location=IFC&floor=14")
            if response.status_code != 200:
                self.log_test(
                    "Booking System Functionality",
                    False,
                    f"❌ Failed to get 14th floor rooms for booking test: HTTP {response.status_code}"
                )
                return
            
            rooms = response.json()
            if not rooms:
                self.log_test(
                    "Booking System Functionality",
                    False,
                    "❌ No 14th floor rooms available for booking test"
                )
                return
            
            # Get a vacant room
            vacant_room = None
            for room in rooms:
                if room.get('status') == 'vacant':
                    vacant_room = room
                    break
            
            if not vacant_room:
                # If no vacant room, use the first room and test anyway
                vacant_room = rooms[0]
            
            # Get an employee ID for booking (from the 640 employees)
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test(
                    "Booking System Functionality",
                    False,
                    "❌ Failed to get employees for booking test"
                )
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test(
                    "Booking System Functionality",
                    False,
                    "❌ No employees found for booking test"
                )
                return
            
            # Use first employee for test
            test_employee = employees[0]
            
            # Create a booking for future time
            booking_data = {
                "employee_id": test_employee.get('id'),
                "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                "remarks": "Test booking for 14th floor meeting room system verification"
            }
            
            room_id = vacant_room.get('id')
            room_name = vacant_room.get('name')
            
            # Test booking creation
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{room_id}/book",
                json=booking_data
            )
            
            booking_created = booking_response.status_code == 200
            
            # Test booking cancellation if booking was created
            booking_cancelled = False
            if booking_created:
                cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{room_id}/booking")
                booking_cancelled = cancel_response.status_code == 200
            
            if booking_created and booking_cancelled:
                self.log_test(
                    "Booking System Functionality",
                    True,
                    f"✅ Booking system working correctly with new room structure",
                    {
                        "room_name": room_name,
                        "room_id": room_id,
                        "employee_name": test_employee.get('name'),
                        "employee_id": test_employee.get('id'),
                        "booking_created": True,
                        "booking_cancelled": True
                    }
                )
            else:
                error_msg = []
                if not booking_created:
                    error_msg.append(f"Booking creation failed (HTTP {booking_response.status_code})")
                if booking_created and not booking_cancelled:
                    error_msg.append("Booking cancellation failed")
                
                self.log_test(
                    "Booking System Functionality",
                    False,
                    f"❌ {'; '.join(error_msg)}",
                    {
                        "room_name": room_name,
                        "room_id": room_id,
                        "employee_id": test_employee.get('id'),
                        "booking_created": booking_created,
                        "booking_cancelled": booking_cancelled,
                        "booking_response_code": booking_response.status_code
                    }
                )
                
        except Exception as e:
            self.log_test("Booking System Functionality", False, f"❌ Exception: {str(e)}")

    def run_all_tests(self):
        """Run all meeting rooms system tests"""
        print("=" * 80)
        print("MEETING ROOMS SYSTEM TESTING - REVIEW REQUEST VERIFICATION")
        print("=" * 80)
        print("Testing the updated meeting rooms system focusing on:")
        print("1. Excel Data Loading: 640 employees loaded correctly")
        print("2. Meeting Rooms Update: 14th floor rooms have new names")
        print("3. API Functionality: GET /api/meeting-rooms with IFC/floor 14 filters")
        print("4. Booking System: Works correctly with new room structure")
        print("=" * 80)
        print()
        
        # Run tests in order
        self.test_1_excel_data_loading()
        self.test_2_meeting_rooms_14th_floor_names()
        self.test_3_api_functionality_filters()
        self.test_4_booking_system_functionality()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Meeting Rooms System updates verified successfully!")
            print("✅ Excel data loading: 640 employees confirmed")
            print("✅ 14th floor meeting rooms: All 9 rooms with correct names and capacities")
            print("✅ API functionality: Filters working correctly for IFC location and floor 14")
            print("✅ Booking system: Working correctly with new room structure")
        else:
            print("⚠️  Some tests failed - Review the issues above")
            failed_tests = [result["test"] for result in self.test_results if not result["success"]]
            print(f"Failed tests: {', '.join(failed_tests)}")
            
        return passed == total

if __name__ == "__main__":
    tester = MeetingRoomsSystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)