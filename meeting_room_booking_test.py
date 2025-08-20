#!/usr/bin/env python3
"""
Meeting Room Booking System Test - Focus on Critical Fixes
Tests the specific fixes implemented for the meeting room booking system:
1. Room status update issue - rooms show 'occupied' immediately when booked
2. Single booking enforcement - no multiple bookings allowed
3. Bulk booking endpoint removal
4. Cancellation logic - proper reset to 'vacant' status
5. Excel loading verification - 640 employees
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "https://user-profile-app.preview.emergentagent.com/api"

class MeetingRoomBookingTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.test_employee_id = None
        self.test_room_id = None
        
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

    def test_1_excel_loading_verification(self):
        """Test 1: Verify 640 employees are still loading correctly"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    # Store a test employee for booking tests
                    self.test_employee_id = employees[0]["id"]
                    self.log_test(
                        "Excel Data Loading", 
                        True, 
                        f"✅ VERIFIED: Exactly 640 employees loaded correctly",
                        {"count": employee_count, "test_employee": employees[0]["name"]}
                    )
                else:
                    self.log_test(
                        "Excel Data Loading", 
                        False, 
                        f"❌ CRITICAL: Expected 640 employees, got {employee_count}",
                        {"expected": 640, "actual": employee_count}
                    )
            else:
                self.log_test(
                    "Excel Data Loading", 
                    False, 
                    f"❌ CRITICAL: Could not fetch employees - HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Excel Data Loading", False, f"❌ EXCEPTION: {str(e)}")

    def test_2_meeting_rooms_structure(self):
        """Test 2: Verify meeting rooms are available and get test room"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                room_count = len(rooms)
                
                if room_count > 0:
                    # Find a vacant room for testing
                    vacant_rooms = [room for room in rooms if room.get("status") == "vacant"]
                    if vacant_rooms:
                        self.test_room_id = vacant_rooms[0]["id"]
                        self.log_test(
                            "Meeting Rooms Structure", 
                            True, 
                            f"✅ VERIFIED: {room_count} meeting rooms available, found vacant room for testing",
                            {
                                "total_rooms": room_count, 
                                "vacant_rooms": len(vacant_rooms),
                                "test_room": vacant_rooms[0]["name"]
                            }
                        )
                    else:
                        # Use any room for testing
                        self.test_room_id = rooms[0]["id"]
                        self.log_test(
                            "Meeting Rooms Structure", 
                            True, 
                            f"✅ VERIFIED: {room_count} meeting rooms available, using first room for testing",
                            {"total_rooms": room_count, "test_room": rooms[0]["name"]}
                        )
                else:
                    self.log_test(
                        "Meeting Rooms Structure", 
                        False, 
                        "❌ CRITICAL: No meeting rooms found"
                    )
            else:
                self.log_test(
                    "Meeting Rooms Structure", 
                    False, 
                    f"❌ CRITICAL: Could not fetch meeting rooms - HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Meeting Rooms Structure", False, f"❌ EXCEPTION: {str(e)}")

    def test_3_room_booking_status_update(self):
        """Test 3: CRITICAL - Verify room shows 'occupied' immediately when booked"""
        try:
            if not self.test_employee_id or not self.test_room_id:
                self.log_test(
                    "Room Status Update Logic", 
                    False, 
                    "❌ SETUP FAILED: Missing test employee or room ID"
                )
                return

            # First, ensure room is vacant by canceling any existing bookings
            cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking")
            
            # Get current room status before booking
            pre_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if pre_response.status_code != 200:
                self.log_test("Room Status Update Logic", False, "❌ Could not fetch rooms before booking")
                return
            
            pre_rooms = pre_response.json()
            pre_room = next((r for r in pre_rooms if r["id"] == self.test_room_id), None)
            if not pre_room:
                self.log_test("Room Status Update Logic", False, "❌ Test room not found")
                return

            # Create a future booking (tomorrow at 10 AM)
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking for status verification"
            }
            
            # Make the booking
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                booked_room = booking_response.json()
                
                # CRITICAL CHECK: Room should show 'occupied' immediately, even for future bookings
                if booked_room.get("status") == "occupied":
                    self.log_test(
                        "Room Status Update Logic", 
                        True, 
                        f"✅ CRITICAL FIX VERIFIED: Room shows 'occupied' immediately when booked (even for future booking)",
                        {
                            "room_status": booked_room.get("status"),
                            "booking_time": f"{start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}",
                            "bookings_count": len(booked_room.get("bookings", []))
                        }
                    )
                else:
                    self.log_test(
                        "Room Status Update Logic", 
                        False, 
                        f"❌ CRITICAL ISSUE: Room status is '{booked_room.get('status')}' instead of 'occupied'",
                        {"expected": "occupied", "actual": booked_room.get("status")}
                    )
            else:
                self.log_test(
                    "Room Status Update Logic", 
                    False, 
                    f"❌ BOOKING FAILED: HTTP {booking_response.status_code} - {booking_response.text}"
                )
                
        except Exception as e:
            self.log_test("Room Status Update Logic", False, f"❌ EXCEPTION: {str(e)}")

    def test_4_single_booking_enforcement(self):
        """Test 4: CRITICAL - Verify single booking enforcement (no multiple bookings)"""
        try:
            if not self.test_employee_id or not self.test_room_id:
                self.log_test(
                    "Single Booking Enforcement", 
                    False, 
                    "❌ SETUP FAILED: Missing test employee or room ID"
                )
                return

            # First booking should already exist from previous test
            # Try to make a second booking to the same room
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(hours=1)
            
            second_booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Second booking attempt - should fail"
            }
            
            # Attempt second booking
            second_booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=second_booking_data
            )
            
            # This should FAIL with a clear error message
            if second_booking_response.status_code == 400:
                error_message = second_booking_response.text
                if "already booked" in error_message.lower() or "multiple bookings" in error_message.lower():
                    self.log_test(
                        "Single Booking Enforcement", 
                        True, 
                        f"✅ CRITICAL FIX VERIFIED: Second booking properly rejected with clear error",
                        {
                            "status_code": second_booking_response.status_code,
                            "error_message": error_message[:100] + "..." if len(error_message) > 100 else error_message
                        }
                    )
                else:
                    self.log_test(
                        "Single Booking Enforcement", 
                        False, 
                        f"❌ WRONG ERROR: Second booking rejected but with unclear error message",
                        {"error_message": error_message}
                    )
            elif second_booking_response.status_code == 200:
                self.log_test(
                    "Single Booking Enforcement", 
                    False, 
                    f"❌ CRITICAL ISSUE: Second booking was allowed - multiple bookings not properly prevented"
                )
            else:
                self.log_test(
                    "Single Booking Enforcement", 
                    False, 
                    f"❌ UNEXPECTED ERROR: HTTP {second_booking_response.status_code} - {second_booking_response.text}"
                )
                
        except Exception as e:
            self.log_test("Single Booking Enforcement", False, f"❌ EXCEPTION: {str(e)}")

    def test_5_bulk_booking_endpoint_removal(self):
        """Test 5: CRITICAL - Verify bulk booking endpoint is removed/non-functional"""
        try:
            if not self.test_employee_id or not self.test_room_id:
                self.log_test(
                    "Bulk Booking Endpoint Removal", 
                    False, 
                    "❌ SETUP FAILED: Missing test employee or room ID"
                )
                return

            # Try to access the bulk booking endpoint that should be removed
            bulk_booking_data = {
                "bookings": [
                    {
                        "employee_id": self.test_employee_id,
                        "start_time": "2025-01-20T10:00:00Z",
                        "end_time": "2025-01-20T11:00:00Z",
                        "remarks": "Bulk booking test 1"
                    },
                    {
                        "employee_id": self.test_employee_id,
                        "start_time": "2025-01-20T14:00:00Z",
                        "end_time": "2025-01-20T15:00:00Z",
                        "remarks": "Bulk booking test 2"
                    }
                ]
            }
            
            # Try the bulk booking endpoint
            bulk_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book-multiple",
                json=bulk_booking_data
            )
            
            # This should return 404 (not found) or 405 (method not allowed)
            if bulk_response.status_code in [404, 405]:
                self.log_test(
                    "Bulk Booking Endpoint Removal", 
                    True, 
                    f"✅ CRITICAL FIX VERIFIED: Bulk booking endpoint properly removed/disabled",
                    {
                        "status_code": bulk_response.status_code,
                        "endpoint": f"/meeting-rooms/{self.test_room_id}/book-multiple"
                    }
                )
            elif bulk_response.status_code == 200:
                self.log_test(
                    "Bulk Booking Endpoint Removal", 
                    False, 
                    f"❌ CRITICAL ISSUE: Bulk booking endpoint still functional - should be removed"
                )
            else:
                self.log_test(
                    "Bulk Booking Endpoint Removal", 
                    True, 
                    f"✅ LIKELY REMOVED: Bulk booking endpoint returns HTTP {bulk_response.status_code} (not functional)",
                    {"status_code": bulk_response.status_code}
                )
                
        except Exception as e:
            self.log_test("Bulk Booking Endpoint Removal", False, f"❌ EXCEPTION: {str(e)}")

    def test_6_booking_persistence(self):
        """Test 6: Verify bookings are properly saved to database"""
        try:
            if not self.test_room_id:
                self.log_test(
                    "Booking Persistence", 
                    False, 
                    "❌ SETUP FAILED: Missing test room ID"
                )
                return

            # Get room details to check booking persistence
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                test_room = next((r for r in rooms if r["id"] == self.test_room_id), None)
                
                if test_room:
                    bookings = test_room.get("bookings", [])
                    if bookings:
                        booking = bookings[0]
                        if (booking.get("employee_id") == self.test_employee_id and
                            booking.get("remarks") == "Test booking for status verification"):
                            self.log_test(
                                "Booking Persistence", 
                                True, 
                                f"✅ VERIFIED: Booking properly saved to database with correct details",
                                {
                                    "booking_id": booking.get("id"),
                                    "employee_id": booking.get("employee_id"),
                                    "employee_name": booking.get("employee_name"),
                                    "start_time": booking.get("start_time"),
                                    "end_time": booking.get("end_time")
                                }
                            )
                        else:
                            self.log_test(
                                "Booking Persistence", 
                                False, 
                                f"❌ ISSUE: Booking saved but details don't match expected values"
                            )
                    else:
                        self.log_test(
                            "Booking Persistence", 
                            False, 
                            f"❌ CRITICAL: No bookings found in database for test room"
                        )
                else:
                    self.log_test(
                        "Booking Persistence", 
                        False, 
                        f"❌ ERROR: Test room not found in database"
                    )
            else:
                self.log_test(
                    "Booking Persistence", 
                    False, 
                    f"❌ ERROR: Could not fetch rooms - HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Booking Persistence", False, f"❌ EXCEPTION: {str(e)}")

    def test_7_cancellation_logic(self):
        """Test 7: CRITICAL - Verify cancellation properly resets room to 'vacant' and clears bookings"""
        try:
            if not self.test_room_id:
                self.log_test(
                    "Cancellation Logic", 
                    False, 
                    "❌ SETUP FAILED: Missing test room ID"
                )
                return

            # Cancel the booking
            cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking")
            
            if cancel_response.status_code == 200:
                # Verify room status is reset to vacant
                verify_response = self.session.get(f"{self.base_url}/meeting-rooms")
                
                if verify_response.status_code == 200:
                    rooms = verify_response.json()
                    test_room = next((r for r in rooms if r["id"] == self.test_room_id), None)
                    
                    if test_room:
                        room_status = test_room.get("status")
                        bookings = test_room.get("bookings", [])
                        current_booking = test_room.get("current_booking")
                        
                        if (room_status == "vacant" and 
                            len(bookings) == 0 and 
                            current_booking is None):
                            self.log_test(
                                "Cancellation Logic", 
                                True, 
                                f"✅ CRITICAL FIX VERIFIED: Cancellation properly resets room to 'vacant' and clears all bookings",
                                {
                                    "room_status": room_status,
                                    "bookings_count": len(bookings),
                                    "current_booking": current_booking
                                }
                            )
                        else:
                            self.log_test(
                                "Cancellation Logic", 
                                False, 
                                f"❌ CRITICAL ISSUE: Cancellation did not properly reset room state",
                                {
                                    "expected_status": "vacant",
                                    "actual_status": room_status,
                                    "expected_bookings": 0,
                                    "actual_bookings": len(bookings),
                                    "current_booking": current_booking
                                }
                            )
                    else:
                        self.log_test(
                            "Cancellation Logic", 
                            False, 
                            f"❌ ERROR: Test room not found after cancellation"
                        )
                else:
                    self.log_test(
                        "Cancellation Logic", 
                        False, 
                        f"❌ ERROR: Could not verify room status after cancellation - HTTP {verify_response.status_code}"
                    )
            else:
                self.log_test(
                    "Cancellation Logic", 
                    False, 
                    f"❌ CANCELLATION FAILED: HTTP {cancel_response.status_code} - {cancel_response.text}"
                )
                
        except Exception as e:
            self.log_test("Cancellation Logic", False, f"❌ EXCEPTION: {str(e)}")

    def test_8_external_url_connectivity(self):
        """Test 8: Verify external URL access works (frontend connectivity)"""
        try:
            # Test basic connectivity to external URL
            response = self.session.get(f"{self.base_url}/employees", timeout=10)
            
            if response.status_code == 200:
                employees = response.json()
                if len(employees) == 640:
                    self.log_test(
                        "External URL Connectivity", 
                        True, 
                        f"✅ VERIFIED: External URL connectivity working perfectly - frontend can reach backend",
                        {
                            "url": self.base_url,
                            "employees_fetched": len(employees),
                            "response_time": f"{response.elapsed.total_seconds():.2f}s"
                        }
                    )
                else:
                    self.log_test(
                        "External URL Connectivity", 
                        False, 
                        f"❌ PARTIAL: External URL accessible but data incomplete ({len(employees)} employees)"
                    )
            else:
                self.log_test(
                    "External URL Connectivity", 
                    False, 
                    f"❌ CRITICAL: External URL not accessible - HTTP {response.status_code}"
                )
                
        except requests.exceptions.Timeout:
            self.log_test("External URL Connectivity", False, "❌ TIMEOUT: External URL request timed out")
        except requests.exceptions.ConnectionError:
            self.log_test("External URL Connectivity", False, "❌ CONNECTION ERROR: Cannot connect to external URL")
        except Exception as e:
            self.log_test("External URL Connectivity", False, f"❌ EXCEPTION: {str(e)}")

    def run_all_tests(self):
        """Run all meeting room booking tests in sequence"""
        print("=" * 80)
        print("🏢 MEETING ROOM BOOKING SYSTEM - CRITICAL FIXES TESTING")
        print("=" * 80)
        print("Testing specific fixes implemented for user-reported issues:")
        print("1. Room status update issue - rooms show 'occupied' immediately when booked")
        print("2. Single booking enforcement - no multiple bookings allowed")
        print("3. Bulk booking endpoint removal")
        print("4. Cancellation logic - proper reset to 'vacant' status")
        print("5. Excel loading verification - 640 employees")
        print("6. External URL connectivity for frontend")
        print("=" * 80)
        print()

        # Run tests in sequence
        self.test_1_excel_loading_verification()
        self.test_2_meeting_rooms_structure()
        self.test_3_room_booking_status_update()
        self.test_4_single_booking_enforcement()
        self.test_5_bulk_booking_endpoint_removal()
        self.test_6_booking_persistence()
        self.test_7_cancellation_logic()
        self.test_8_external_url_connectivity()

        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = [r for r in self.test_results if r["success"]]
        failed_tests = [r for r in self.test_results if not r["success"]]
        
        print(f"✅ PASSED: {len(passed_tests)}/{len(self.test_results)} tests")
        print(f"❌ FAILED: {len(failed_tests)}/{len(self.test_results)} tests")
        print()
        
        if failed_tests:
            print("🚨 FAILED TESTS:")
            for test in failed_tests:
                print(f"   ❌ {test['test']}: {test['message']}")
            print()
        
        critical_fixes_status = {
            "Room Status Update": any("Room Status Update Logic" in r["test"] and r["success"] for r in self.test_results),
            "Single Booking Enforcement": any("Single Booking Enforcement" in r["test"] and r["success"] for r in self.test_results),
            "Bulk Booking Removal": any("Bulk Booking Endpoint Removal" in r["test"] and r["success"] for r in self.test_results),
            "Cancellation Logic": any("Cancellation Logic" in r["test"] and r["success"] for r in self.test_results),
            "Excel Loading": any("Excel Data Loading" in r["test"] and r["success"] for r in self.test_results),
            "External URL": any("External URL Connectivity" in r["test"] and r["success"] for r in self.test_results)
        }
        
        print("🎯 CRITICAL FIXES STATUS:")
        for fix, status in critical_fixes_status.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {fix}")
        
        print("=" * 80)
        
        return len(failed_tests) == 0

if __name__ == "__main__":
    tester = MeetingRoomBookingTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)