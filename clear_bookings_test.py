#!/usr/bin/env python3
"""
Meeting Rooms Clear All Bookings Functionality Test
Tests the specific functionality requested in the review:
1. Check current meeting room status
2. Test clear all bookings endpoint
3. Verify results after clearing
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Get backend URL from frontend .env
BACKEND_URL = "https://user-profile-app.preview.emergentagent.com/api"

class ClearBookingsTester:
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

    def test_1_check_current_meeting_room_status(self):
        """Test GET /api/meeting-rooms - Check current status before clearing"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                total_rooms = len(rooms)
                
                # Count occupied vs vacant rooms
                occupied_rooms = [room for room in rooms if room.get('status') == 'occupied']
                vacant_rooms = [room for room in rooms if room.get('status') == 'vacant']
                
                occupied_count = len(occupied_rooms)
                vacant_count = len(vacant_rooms)
                
                # Count rooms with bookings
                rooms_with_bookings = [room for room in rooms if room.get('bookings') and len(room.get('bookings', [])) > 0]
                rooms_with_current_booking = [room for room in rooms if room.get('current_booking') is not None]
                
                details = {
                    "total_rooms": total_rooms,
                    "occupied_rooms": occupied_count,
                    "vacant_rooms": vacant_count,
                    "rooms_with_bookings": len(rooms_with_bookings),
                    "rooms_with_current_booking": len(rooms_with_current_booking)
                }
                
                # Show some sample room data
                if occupied_rooms:
                    sample_occupied = occupied_rooms[0]
                    details["sample_occupied_room"] = {
                        "id": sample_occupied.get('id'),
                        "name": sample_occupied.get('name'),
                        "status": sample_occupied.get('status'),
                        "bookings_count": len(sample_occupied.get('bookings', [])),
                        "has_current_booking": sample_occupied.get('current_booking') is not None
                    }
                
                self.log_test(
                    "Check Current Meeting Room Status",
                    True,
                    f"Found {total_rooms} total rooms: {occupied_count} occupied, {vacant_count} vacant",
                    details
                )
                
                return rooms
                
            else:
                self.log_test(
                    "Check Current Meeting Room Status",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}",
                    {"response": response.text}
                )
                return None
                
        except Exception as e:
            self.log_test(
                "Check Current Meeting Room Status",
                False,
                f"Exception occurred: {str(e)}"
            )
            return None

    def test_2_clear_all_bookings(self):
        """Test DELETE /api/meeting-rooms/clear-all-bookings - Clear all bookings"""
        try:
            response = self.session.delete(f"{self.base_url}/meeting-rooms/clear-all-bookings")
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify response structure
                if "message" in result and "rooms_updated" in result:
                    rooms_updated = result.get("rooms_updated", 0)
                    message = result.get("message", "")
                    
                    details = {
                        "rooms_updated": rooms_updated,
                        "response_message": message,
                        "full_response": result
                    }
                    
                    self.log_test(
                        "Clear All Bookings",
                        True,
                        f"Successfully cleared bookings from {rooms_updated} rooms",
                        details
                    )
                    
                    return result
                else:
                    self.log_test(
                        "Clear All Bookings",
                        False,
                        "Response missing expected fields (message, rooms_updated)",
                        {"response": result}
                    )
                    return None
                    
            else:
                self.log_test(
                    "Clear All Bookings",
                    False,
                    f"Failed to clear bookings. Status: {response.status_code}",
                    {"response": response.text}
                )
                return None
                
        except Exception as e:
            self.log_test(
                "Clear All Bookings",
                False,
                f"Exception occurred: {str(e)}"
            )
            return None

    def test_3_verify_results_after_clearing(self):
        """Test GET /api/meeting-rooms - Verify all rooms are cleared after clearing"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                total_rooms = len(rooms)
                
                # Verify all rooms are vacant
                vacant_rooms = [room for room in rooms if room.get('status') == 'vacant']
                occupied_rooms = [room for room in rooms if room.get('status') == 'occupied']
                
                # Verify all rooms have empty bookings array
                rooms_with_empty_bookings = [room for room in rooms if not room.get('bookings') or len(room.get('bookings', [])) == 0]
                
                # Verify all rooms have null current_booking
                rooms_with_null_current_booking = [room for room in rooms if room.get('current_booking') is None]
                
                # Check for any issues
                issues = []
                
                if len(occupied_rooms) > 0:
                    issues.append(f"{len(occupied_rooms)} rooms still showing as occupied")
                    
                if len(rooms_with_empty_bookings) != total_rooms:
                    issues.append(f"{total_rooms - len(rooms_with_empty_bookings)} rooms still have bookings")
                    
                if len(rooms_with_null_current_booking) != total_rooms:
                    issues.append(f"{total_rooms - len(rooms_with_null_current_booking)} rooms still have current_booking")
                
                details = {
                    "total_rooms": total_rooms,
                    "vacant_rooms": len(vacant_rooms),
                    "occupied_rooms": len(occupied_rooms),
                    "rooms_with_empty_bookings": len(rooms_with_empty_bookings),
                    "rooms_with_null_current_booking": len(rooms_with_null_current_booking),
                    "issues_found": issues
                }
                
                # Show sample room data after clearing
                if rooms:
                    sample_room = rooms[0]
                    details["sample_room_after_clearing"] = {
                        "id": sample_room.get('id'),
                        "name": sample_room.get('name'),
                        "status": sample_room.get('status'),
                        "bookings": sample_room.get('bookings'),
                        "current_booking": sample_room.get('current_booking')
                    }
                
                if not issues:
                    self.log_test(
                        "Verify Results After Clearing",
                        True,
                        f"All {total_rooms} rooms successfully cleared: status='vacant', bookings=[], current_booking=null",
                        details
                    )
                else:
                    self.log_test(
                        "Verify Results After Clearing",
                        False,
                        f"Issues found after clearing: {'; '.join(issues)}",
                        details
                    )
                
                return rooms
                
            else:
                self.log_test(
                    "Verify Results After Clearing",
                    False,
                    f"Failed to fetch meeting rooms after clearing. Status: {response.status_code}",
                    {"response": response.text}
                )
                return None
                
        except Exception as e:
            self.log_test(
                "Verify Results After Clearing",
                False,
                f"Exception occurred: {str(e)}"
            )
            return None

    def test_4_create_test_booking_and_verify_clear_again(self):
        """Create a test booking and verify clear functionality works again"""
        try:
            # First, get a room to book
            rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if rooms_response.status_code != 200:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    "Could not fetch rooms for test booking"
                )
                return
            
            rooms = rooms_response.json()
            if not rooms:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    "No rooms available for test booking"
                )
                return
            
            test_room = rooms[0]
            room_id = test_room.get('id')
            
            # Get an employee for booking
            employees_response = self.session.get(f"{self.base_url}/employees")
            if employees_response.status_code != 200:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    "Could not fetch employees for test booking"
                )
                return
            
            employees = employees_response.json()
            if not employees:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    "No employees available for test booking"
                )
                return
            
            test_employee = employees[0]
            employee_id = test_employee.get('id')
            
            # Create a test booking for tomorrow
            from datetime import datetime, timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking for clear functionality verification"
            }
            
            # Create the booking
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code != 200:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    f"Failed to create test booking. Status: {booking_response.status_code}",
                    {"response": booking_response.text}
                )
                return
            
            # Verify the booking was created
            room_check_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if room_check_response.status_code == 200:
                updated_rooms = room_check_response.json()
                booked_rooms = [room for room in updated_rooms if room.get('status') == 'occupied']
                
                if len(booked_rooms) > 0:
                    # Now clear all bookings again
                    clear_response = self.session.delete(f"{self.base_url}/meeting-rooms/clear-all-bookings")
                    
                    if clear_response.status_code == 200:
                        # Verify clearing worked
                        final_check_response = self.session.get(f"{self.base_url}/meeting-rooms")
                        if final_check_response.status_code == 200:
                            final_rooms = final_check_response.json()
                            final_occupied = [room for room in final_rooms if room.get('status') == 'occupied']
                            
                            if len(final_occupied) == 0:
                                self.log_test(
                                    "Create Test Booking and Verify Clear Again",
                                    True,
                                    "Successfully created test booking and cleared it again",
                                    {
                                        "test_room": room_id,
                                        "test_employee": employee_id,
                                        "booking_created": True,
                                        "clearing_successful": True
                                    }
                                )
                            else:
                                self.log_test(
                                    "Create Test Booking and Verify Clear Again",
                                    False,
                                    f"Clear function failed - {len(final_occupied)} rooms still occupied after second clear"
                                )
                        else:
                            self.log_test(
                                "Create Test Booking and Verify Clear Again",
                                False,
                                "Could not verify final room status after second clear"
                            )
                    else:
                        self.log_test(
                            "Create Test Booking and Verify Clear Again",
                            False,
                            f"Second clear operation failed. Status: {clear_response.status_code}"
                        )
                else:
                    self.log_test(
                        "Create Test Booking and Verify Clear Again",
                        False,
                        "Test booking was not created successfully - no occupied rooms found"
                    )
            else:
                self.log_test(
                    "Create Test Booking and Verify Clear Again",
                    False,
                    "Could not verify test booking creation"
                )
                
        except Exception as e:
            self.log_test(
                "Create Test Booking and Verify Clear Again",
                False,
                f"Exception occurred: {str(e)}"
            )

    def run_all_tests(self):
        """Run all clear bookings functionality tests"""
        print("=" * 80)
        print("MEETING ROOMS CLEAR ALL BOOKINGS FUNCTIONALITY TEST")
        print("=" * 80)
        print(f"Backend URL: {self.base_url}")
        print()
        
        # Test sequence as requested in review
        print("🔍 STEP 1: Check current meeting room status")
        initial_rooms = self.test_1_check_current_meeting_room_status()
        
        print("🧹 STEP 2: Test clear all bookings endpoint")
        clear_result = self.test_2_clear_all_bookings()
        
        print("✅ STEP 3: Verify results after clearing")
        cleared_rooms = self.test_3_verify_results_after_clearing()
        
        print("🔄 STEP 4: Create test booking and verify clear works again")
        self.test_4_create_test_booking_and_verify_clear_again()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = [test for test in self.test_results if test["success"]]
        failed_tests = [test for test in self.test_results if not test["success"]]
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(passed_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Success Rate: {len(passed_tests)/len(self.test_results)*100:.1f}%")
        
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        print("\n" + "=" * 80)
        
        # Return overall success
        return len(failed_tests) == 0

if __name__ == "__main__":
    tester = ClearBookingsTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED - Clear All Bookings functionality is working correctly!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Clear All Bookings functionality has issues!")
        sys.exit(1)