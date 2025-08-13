#!/usr/bin/env python3
"""
Meeting Rooms API Testing - Focused Testing for Room Distribution and Structure
Tests the specific requirements mentioned in the review request
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Get backend URL from frontend .env
BACKEND_URL = "https://booking-persist.preview.emergentagent.com/api"

class MeetingRoomsTester:
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
        """Test Excel Data Loading: Confirm 640 employees are loaded correctly"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    self.log_test(
                        "Excel Data Loading",
                        True,
                        f"Successfully loaded exactly 640 employees from Excel",
                        {"employee_count": employee_count}
                    )
                else:
                    self.log_test(
                        "Excel Data Loading",
                        False,
                        f"Expected 640 employees, but found {employee_count}",
                        {"employee_count": employee_count}
                    )
            else:
                self.log_test(
                    "Excel Data Loading",
                    False,
                    f"Failed to fetch employees. Status: {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Excel Data Loading",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )

    def test_2_meeting_rooms_structure(self):
        """Test Meeting Room Structure: Verify room distribution across locations and floors"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                total_rooms = len(rooms)
                
                # Group rooms by location and floor
                location_floor_count = {}
                for room in rooms:
                    location = room.get('location', 'Unknown')
                    floor = room.get('floor', 'Unknown')
                    
                    if location not in location_floor_count:
                        location_floor_count[location] = {}
                    if floor not in location_floor_count[location]:
                        location_floor_count[location][floor] = 0
                    location_floor_count[location][floor] += 1
                
                # Verify IFC location structure
                ifc_structure_correct = True
                ifc_details = {}
                
                if 'IFC' in location_floor_count:
                    ifc_floors = location_floor_count['IFC']
                    ifc_details = ifc_floors
                    
                    # Check if IFC has rooms on floors 11, 12, and 14
                    expected_floors = ['11', '12', '14']
                    actual_floors = list(ifc_floors.keys())
                    
                    if not all(floor in actual_floors for floor in expected_floors):
                        ifc_structure_correct = False
                    
                    # Check if floor 14 has exactly 8 rooms
                    if ifc_floors.get('14', 0) != 8:
                        ifc_structure_correct = False
                        
                    # Check if floors 11 and 12 have 1 room each
                    if ifc_floors.get('11', 0) != 1 or ifc_floors.get('12', 0) != 1:
                        ifc_structure_correct = False
                else:
                    ifc_structure_correct = False
                
                # Verify other locations have 1 room each on floor 1
                other_locations_correct = True
                other_locations = ['Central Office 75', 'Office 75', 'Noida', 'Project Office']
                other_details = {}
                
                for location in other_locations:
                    if location in location_floor_count:
                        floors = location_floor_count[location]
                        other_details[location] = floors
                        
                        # Should have exactly 1 room on floor 1
                        if floors.get('1', 0) != 1 or len(floors) != 1:
                            other_locations_correct = False
                    else:
                        other_locations_correct = False
                        other_details[location] = "Missing"
                
                overall_success = ifc_structure_correct and other_locations_correct
                
                self.log_test(
                    "Meeting Room Structure",
                    overall_success,
                    f"Room distribution verification: IFC={'✓' if ifc_structure_correct else '✗'}, Others={'✓' if other_locations_correct else '✗'}",
                    {
                        "total_rooms": total_rooms,
                        "IFC_structure": ifc_details,
                        "other_locations": other_details,
                        "full_distribution": location_floor_count
                    }
                )
                
            else:
                self.log_test(
                    "Meeting Room Structure",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Meeting Room Structure",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )

    def test_3_meeting_room_details(self):
        """Test Meeting Room Details: Verify each room has correct properties"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                required_fields = ['id', 'name', 'capacity', 'location', 'floor', 'status', 'equipment']
                rooms_with_issues = []
                rooms_verified = 0
                
                for room in rooms:
                    room_issues = []
                    
                    # Check required fields
                    for field in required_fields:
                        if field not in room or room[field] is None:
                            room_issues.append(f"Missing {field}")
                    
                    # Verify equipment field (the actual field name in the model)
                    if 'equipment' in room and isinstance(room['equipment'], list):
                        # Good - equipment is a list
                        pass
                    else:
                        room_issues.append("Equipment field should be a list")
                    
                    # Verify capacity is a number
                    if 'capacity' in room:
                        try:
                            int(room['capacity'])
                        except (ValueError, TypeError):
                            room_issues.append("Capacity should be a number")
                    
                    if room_issues:
                        rooms_with_issues.append({
                            "room_id": room.get('id', 'Unknown'),
                            "room_name": room.get('name', 'Unknown'),
                            "issues": room_issues
                        })
                    else:
                        rooms_verified += 1
                
                success = len(rooms_with_issues) == 0
                
                self.log_test(
                    "Meeting Room Details",
                    success,
                    f"Verified {rooms_verified}/{len(rooms)} rooms have correct structure",
                    {
                        "total_rooms": len(rooms),
                        "rooms_verified": rooms_verified,
                        "rooms_with_issues": rooms_with_issues
                    }
                )
                
            else:
                self.log_test(
                    "Meeting Room Details",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Meeting Room Details",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )

    def test_4_room_distribution_filtering(self):
        """Test Room Distribution with Filters: Verify specific endpoint filtering"""
        try:
            test_cases = [
                {
                    "name": "IFC Floor 14 Rooms",
                    "url": f"{self.base_url}/meeting-rooms?location=IFC&floor=14",
                    "expected_count": 8,
                    "description": "Should return exactly 8 rooms on IFC floor 14"
                },
                {
                    "name": "Central Office 75 Rooms",
                    "url": f"{self.base_url}/meeting-rooms?location=Central Office 75",
                    "expected_count": 1,
                    "description": "Should return exactly 1 room at Central Office 75"
                },
                {
                    "name": "IFC All Rooms",
                    "url": f"{self.base_url}/meeting-rooms?location=IFC",
                    "expected_count": 10,
                    "description": "Should return exactly 10 rooms total at IFC (1+1+8)"
                }
            ]
            
            all_tests_passed = True
            test_details = []
            
            for test_case in test_cases:
                try:
                    response = self.session.get(test_case["url"])
                    
                    if response.status_code == 200:
                        rooms = response.json()
                        actual_count = len(rooms)
                        expected_count = test_case["expected_count"]
                        
                        test_passed = actual_count == expected_count
                        if not test_passed:
                            all_tests_passed = False
                        
                        test_details.append({
                            "test": test_case["name"],
                            "expected": expected_count,
                            "actual": actual_count,
                            "passed": test_passed,
                            "url": test_case["url"]
                        })
                        
                    else:
                        all_tests_passed = False
                        test_details.append({
                            "test": test_case["name"],
                            "error": f"HTTP {response.status_code}",
                            "passed": False,
                            "url": test_case["url"]
                        })
                        
                except Exception as e:
                    all_tests_passed = False
                    test_details.append({
                        "test": test_case["name"],
                        "error": str(e),
                        "passed": False,
                        "url": test_case["url"]
                    })
            
            self.log_test(
                "Room Distribution Filtering",
                all_tests_passed,
                f"Filter testing: {sum(1 for t in test_details if t.get('passed', False))}/{len(test_details)} tests passed",
                {"test_results": test_details}
            )
            
        except Exception as e:
            self.log_test(
                "Room Distribution Filtering",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )

    def test_5_booking_functionality(self):
        """Test Booking Functionality: Verify room booking works"""
        try:
            # First get a vacant room to test booking
            response = self.session.get(f"{self.base_url}/meeting-rooms?status=vacant")
            
            if response.status_code == 200:
                vacant_rooms = response.json()
                
                if len(vacant_rooms) > 0:
                    test_room = vacant_rooms[0]
                    room_id = test_room['id']
                    
                    # Get an employee to assign the booking to
                    emp_response = self.session.get(f"{self.base_url}/employees")
                    if emp_response.status_code == 200:
                        employees = emp_response.json()
                        if len(employees) > 0:
                            test_employee = employees[0]
                            
                            # Create a booking with future date
                            from datetime import datetime, timedelta
                            future_time = datetime.utcnow() + timedelta(hours=2)
                            end_time = future_time + timedelta(hours=1)
                            
                            booking_data = {
                                "employee_id": test_employee['id'],
                                "start_time": future_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "remarks": "Test booking for API verification"
                            }
                            
                            booking_response = self.session.post(
                                f"{self.base_url}/meeting-rooms/{room_id}/book",
                                json=booking_data
                            )
                            
                            if booking_response.status_code == 200:
                                booked_room = booking_response.json()
                                
                                # Verify booking was created
                                if (booked_room.get('status') == 'occupied' and 
                                    booked_room.get('current_booking') is not None):
                                    
                                    # Clean up - cancel the booking
                                    cancel_response = self.session.delete(
                                        f"{self.base_url}/meeting-rooms/{room_id}/booking"
                                    )
                                    
                                    self.log_test(
                                        "Booking Functionality",
                                        True,
                                        "Successfully created and cancelled test booking",
                                        {
                                            "room_id": room_id,
                                            "employee_id": test_employee['id'],
                                            "booking_created": True,
                                            "booking_cancelled": cancel_response.status_code == 200
                                        }
                                    )
                                else:
                                    self.log_test(
                                        "Booking Functionality",
                                        False,
                                        "Booking was created but room status/booking not updated correctly",
                                        {"room_status": booked_room.get('status'), "has_booking": booked_room.get('current_booking') is not None}
                                    )
                            else:
                                self.log_test(
                                    "Booking Functionality",
                                    False,
                                    f"Failed to create booking. Status: {booking_response.status_code}",
                                    {"status_code": booking_response.status_code, "response": booking_response.text}
                                )
                        else:
                            self.log_test(
                                "Booking Functionality",
                                False,
                                "No employees found to test booking with",
                                {"employee_count": 0}
                            )
                    else:
                        self.log_test(
                            "Booking Functionality",
                            False,
                            f"Failed to fetch employees for booking test. Status: {emp_response.status_code}",
                            {"status_code": emp_response.status_code}
                        )
                else:
                    self.log_test(
                        "Booking Functionality",
                        False,
                        "No vacant rooms available for booking test",
                        {"vacant_rooms_count": 0}
                    )
            else:
                self.log_test(
                    "Booking Functionality",
                    False,
                    f"Failed to fetch vacant rooms. Status: {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Booking Functionality",
                False,
                f"Exception occurred: {str(e)}",
                {"error": str(e)}
            )

    def run_all_tests(self):
        """Run all meeting room tests"""
        print("=" * 80)
        print("MEETING ROOMS API TESTING - FOCUSED VERIFICATION")
        print("=" * 80)
        print()
        
        # Run all tests
        self.test_1_excel_data_loading()
        self.test_2_meeting_rooms_structure()
        self.test_3_meeting_room_details()
        self.test_4_room_distribution_filtering()
        self.test_5_booking_functionality()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Meeting Rooms API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the details above.")
            
        return passed == total

if __name__ == "__main__":
    tester = MeetingRoomsTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)