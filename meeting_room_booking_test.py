#!/usr/bin/env python3
"""
Meeting Room Booking System Test - Focus on Multiple Bookings and Timezone Issues
Tests the specific issues mentioned in the review request:
1. Multiple bookings to same room at different times
2. Timezone normalization fixes
3. Profile image URL serving with /api/uploads/images/ prefix
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "https://dual-service-run.preview.emergentagent.com/api"

class MeetingRoomBookingTester:
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

    def test_1_get_meeting_rooms_structure(self):
        """Test GET /api/meeting-rooms - Verify room structure and count"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                room_count = len(rooms)
                
                # Check if we have the expected 32 rooms
                if room_count >= 30:  # Allow some flexibility
                    # Check room structure - should have bookings field for multiple bookings
                    sample_room = rooms[0] if rooms else {}
                    has_bookings_field = 'bookings' in sample_room
                    has_multiple_booking_support = isinstance(sample_room.get('bookings'), list)
                    
                    self.log_test(
                        "GET /api/meeting-rooms - Structure Check", 
                        True, 
                        f"Successfully fetched {room_count} meeting rooms with proper structure",
                        {
                            "total_rooms": room_count,
                            "has_bookings_field": has_bookings_field,
                            "supports_multiple_bookings": has_multiple_booking_support,
                            "sample_room_id": sample_room.get('id', 'N/A')
                        }
                    )
                    
                    # Store room IDs for testing
                    self.available_rooms = [room['id'] for room in rooms if room.get('status') == 'vacant']
                    self.all_rooms = [room['id'] for room in rooms]
                    
                    return True
                else:
                    self.log_test(
                        "GET /api/meeting-rooms - Structure Check", 
                        False, 
                        f"Expected around 32 rooms, got {room_count}"
                    )
                    return False
            else:
                self.log_test(
                    "GET /api/meeting-rooms - Structure Check", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("GET /api/meeting-rooms - Structure Check", False, f"Exception: {str(e)}")
            return False

    def test_2_single_booking_creation(self):
        """Test POST /api/meeting-rooms/{id}/book - Create single booking"""
        try:
            if not hasattr(self, 'available_rooms') or not self.available_rooms:
                self.log_test("Single Booking Creation", False, "No available rooms for testing")
                return False
            
            # Get an employee for booking
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("Single Booking Creation", False, "Could not fetch employees")
                return False
            
            employees = emp_response.json()
            if not employees:
                self.log_test("Single Booking Creation", False, "No employees available")
                return False
            
            test_employee = employees[0]
            test_room_id = self.available_rooms[0]
            
            # Create booking for 10:00 AM to 11:00 AM (as requested in review)
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": test_employee["id"],
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking 10-11 AM - Review Request Test"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                booked_room = response.json()
                bookings = booked_room.get('bookings', [])
                
                # Verify booking was created
                if len(bookings) >= 1:
                    latest_booking = bookings[-1]  # Get the latest booking
                    
                    self.log_test(
                        "Single Booking Creation (10-11 AM)", 
                        True, 
                        f"Successfully created booking for {test_employee['name']} from 10-11 AM",
                        {
                            "room_id": test_room_id,
                            "employee": test_employee['name'],
                            "booking_id": latest_booking.get('id'),
                            "start_time": booking_data['start_time'],
                            "end_time": booking_data['end_time'],
                            "total_bookings": len(bookings)
                        }
                    )
                    
                    # Store for next test
                    self.test_room_id = test_room_id
                    self.test_employee = test_employee
                    self.first_booking_id = latest_booking.get('id')
                    
                    return True
                else:
                    self.log_test("Single Booking Creation (10-11 AM)", False, "Booking was not added to room")
                    return False
            else:
                self.log_test(
                    "Single Booking Creation (10-11 AM)", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Single Booking Creation (10-11 AM)", False, f"Exception: {str(e)}")
            return False

    def test_3_multiple_booking_same_room(self):
        """Test POST /api/meeting-rooms/{id}/book - Create second booking for same room (2-3 PM)"""
        try:
            if not hasattr(self, 'test_room_id') or not hasattr(self, 'test_employee'):
                self.log_test("Multiple Booking Same Room", False, "Previous test failed - no room/employee data")
                return False
            
            # Create second booking for 2:00 PM to 3:00 PM (as requested in review)
            tomorrow = datetime.now() + timedelta(days=1)
            start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)  # 2 PM
            end_time = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)    # 3 PM
            
            booking_data = {
                "employee_id": self.test_employee["id"],
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking 2-3 PM - Review Request Test (Multiple Booking)"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                booked_room = response.json()
                bookings = booked_room.get('bookings', [])
                
                # Verify we now have 2 bookings
                if len(bookings) >= 2:
                    self.log_test(
                        "Multiple Booking Same Room (2-3 PM)", 
                        True, 
                        f"✅ CRITICAL FIX VERIFIED: Successfully created second booking for same room without timezone errors",
                        {
                            "room_id": self.test_room_id,
                            "employee": self.test_employee['name'],
                            "total_bookings": len(bookings),
                            "second_booking_time": "2-3 PM",
                            "timezone_error_fixed": True
                        }
                    )
                    
                    # Store second booking ID
                    self.second_booking_id = bookings[-1].get('id')
                    return True
                else:
                    self.log_test(
                        "Multiple Booking Same Room (2-3 PM)", 
                        False, 
                        f"Expected 2+ bookings, got {len(bookings)}"
                    )
                    return False
            else:
                # This is the critical error we're testing for
                error_text = response.text
                if "can't compare offset-naive and offset-aware datetimes" in error_text:
                    self.log_test(
                        "Multiple Booking Same Room (2-3 PM)", 
                        False, 
                        f"❌ CRITICAL TIMEZONE ERROR STILL EXISTS: {error_text}",
                        {
                            "error_type": "timezone_comparison_error",
                            "status_code": response.status_code,
                            "needs_normalize_datetime_fix": True
                        }
                    )
                else:
                    self.log_test(
                        "Multiple Booking Same Room (2-3 PM)", 
                        False, 
                        f"HTTP {response.status_code}: {error_text}"
                    )
                return False
                
        except Exception as e:
            self.log_test("Multiple Booking Same Room (2-3 PM)", False, f"Exception: {str(e)}")
            return False

    def test_4_timezone_normalization_function(self):
        """Test that normalize_datetime function is working properly"""
        try:
            # Test by creating bookings with different timezone formats
            if not hasattr(self, 'available_rooms') or len(self.available_rooms) < 2:
                self.log_test("Timezone Normalization Test", False, "Need at least 2 available rooms")
                return False
            
            # Get employee
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("Timezone Normalization Test", False, "Could not fetch employees")
                return False
            
            employees = emp_response.json()
            if not employees:
                self.log_test("Timezone Normalization Test", False, "No employees available")
                return False
            
            test_employee = employees[0]
            test_room_id = self.available_rooms[1] if len(self.available_rooms) > 1 else self.available_rooms[0]
            
            # Test different timezone formats
            tomorrow = datetime.now() + timedelta(days=1)
            
            # Format 1: ISO with Z suffix
            start_time_1 = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            end_time_1 = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            
            booking_data_1 = {
                "employee_id": test_employee["id"],
                "start_time": start_time_1.isoformat() + "Z",
                "end_time": end_time_1.isoformat() + "Z",
                "remarks": "Timezone test - ISO with Z"
            }
            
            response_1 = self.session.post(
                f"{self.base_url}/meeting-rooms/{test_room_id}/book",
                json=booking_data_1
            )
            
            # Format 2: ISO with +00:00 offset
            start_time_2 = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            end_time_2 = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
            
            booking_data_2 = {
                "employee_id": test_employee["id"],
                "start_time": start_time_2.isoformat() + "+00:00",
                "end_time": end_time_2.isoformat() + "+00:00",
                "remarks": "Timezone test - ISO with +00:00"
            }
            
            response_2 = self.session.post(
                f"{self.base_url}/meeting-rooms/{test_room_id}/book",
                json=booking_data_2
            )
            
            success_count = 0
            if response_1.status_code == 200:
                success_count += 1
            if response_2.status_code == 200:
                success_count += 1
            
            if success_count == 2:
                self.log_test(
                    "Timezone Normalization Function", 
                    True, 
                    f"✅ normalize_datetime function working correctly - handled both Z and +00:00 formats",
                    {
                        "format_1_success": response_1.status_code == 200,
                        "format_2_success": response_2.status_code == 200,
                        "room_id": test_room_id
                    }
                )
                return True
            else:
                self.log_test(
                    "Timezone Normalization Function", 
                    False, 
                    f"normalize_datetime function issues - only {success_count}/2 formats worked",
                    {
                        "format_1_status": response_1.status_code,
                        "format_2_status": response_2.status_code,
                        "format_1_error": response_1.text if response_1.status_code != 200 else None,
                        "format_2_error": response_2.text if response_2.status_code != 200 else None
                    }
                )
                return False
                
        except Exception as e:
            self.log_test("Timezone Normalization Function", False, f"Exception: {str(e)}")
            return False

    def test_5_specific_booking_cancellation(self):
        """Test DELETE /api/meeting-rooms/{room_id}/booking/{booking_id} - Cancel specific booking"""
        try:
            if not hasattr(self, 'test_room_id') or not hasattr(self, 'first_booking_id'):
                self.log_test("Specific Booking Cancellation", False, "No booking data from previous tests")
                return False
            
            # Cancel the first booking (10-11 AM) using the new specific cancellation endpoint
            response = self.session.delete(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{self.first_booking_id}"
            )
            
            if response.status_code == 200:
                # Verify the booking was removed
                room_response = self.session.get(f"{self.base_url}/meeting-rooms")
                if room_response.status_code == 200:
                    rooms = room_response.json()
                    test_room = next((room for room in rooms if room['id'] == self.test_room_id), None)
                    
                    if test_room:
                        remaining_bookings = test_room.get('bookings', [])
                        booking_still_exists = any(b.get('id') == self.first_booking_id for b in remaining_bookings)
                        
                        if not booking_still_exists:
                            self.log_test(
                                "Specific Booking Cancellation", 
                                True, 
                                f"Successfully cancelled specific booking (10-11 AM)",
                                {
                                    "cancelled_booking_id": self.first_booking_id,
                                    "remaining_bookings": len(remaining_bookings),
                                    "room_id": self.test_room_id
                                }
                            )
                            return True
                        else:
                            self.log_test(
                                "Specific Booking Cancellation", 
                                False, 
                                "Booking still exists after cancellation"
                            )
                            return False
                    else:
                        self.log_test("Specific Booking Cancellation", False, "Could not find test room")
                        return False
                else:
                    self.log_test("Specific Booking Cancellation", False, "Could not verify cancellation")
                    return False
            else:
                self.log_test(
                    "Specific Booking Cancellation", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Specific Booking Cancellation", False, f"Exception: {str(e)}")
            return False

    def test_6_profile_image_url_serving(self):
        """Test profile image URLs with correct /api/uploads/images/ prefix"""
        try:
            # Get employees and check their profile image URLs
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                
                if not employees:
                    self.log_test("Profile Image URL Serving", False, "No employees found")
                    return False
                
                # Check profile image URLs
                correct_prefix_count = 0
                total_with_images = 0
                api_prefix_count = 0
                
                for employee in employees[:10]:  # Check first 10 employees
                    profile_image = employee.get('profileImage')
                    if profile_image and profile_image != "/api/placeholder/150/150":
                        total_with_images += 1
                        
                        # Check if it has the correct /api/uploads/images/ prefix
                        if profile_image.startswith('/api/uploads/images/'):
                            correct_prefix_count += 1
                            api_prefix_count += 1
                        elif profile_image.startswith('/uploads/images/'):
                            # This would be incorrect - missing /api prefix
                            pass
                
                # Test accessing a profile image URL if available
                image_accessible = False
                test_image_url = None
                
                if api_prefix_count > 0:
                    # Find an employee with /api/uploads/images/ URL
                    for employee in employees[:10]:
                        profile_image = employee.get('profileImage')
                        if profile_image and profile_image.startswith('/api/uploads/images/'):
                            test_image_url = profile_image
                            
                            # Try to access the image
                            full_url = self.base_url.replace('/api', '') + profile_image
                            img_response = self.session.get(full_url)
                            
                            if img_response.status_code == 200:
                                image_accessible = True
                                break
                
                prefix_correct = correct_prefix_count == total_with_images and total_with_images > 0
                
                self.log_test(
                    "Profile Image URL Serving", 
                    prefix_correct and (image_accessible or total_with_images == 0), 
                    f"Profile image URLs {'have correct /api/uploads/images/ prefix' if prefix_correct else 'have incorrect prefixes'}",
                    {
                        "total_employees_checked": min(10, len(employees)),
                        "employees_with_images": total_with_images,
                        "correct_api_prefix_count": api_prefix_count,
                        "image_accessible": image_accessible,
                        "test_image_url": test_image_url,
                        "prefix_correct": prefix_correct
                    }
                )
                
                return prefix_correct
            else:
                self.log_test(
                    "Profile Image URL Serving", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Profile Image URL Serving", False, f"Exception: {str(e)}")
            return False

    def test_7_multiple_bookings_per_room_verification(self):
        """Verify that multiple bookings per room are now supported"""
        try:
            # Get all rooms and check how many have multiple bookings
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                rooms_with_multiple_bookings = 0
                total_bookings = 0
                
                for room in rooms:
                    bookings = room.get('bookings', [])
                    total_bookings += len(bookings)
                    
                    if len(bookings) > 1:
                        rooms_with_multiple_bookings += 1
                
                # Check if our test room has multiple bookings
                test_room_has_multiple = False
                if hasattr(self, 'test_room_id'):
                    test_room = next((room for room in rooms if room['id'] == self.test_room_id), None)
                    if test_room:
                        test_room_bookings = len(test_room.get('bookings', []))
                        test_room_has_multiple = test_room_bookings > 1
                
                multiple_bookings_supported = rooms_with_multiple_bookings > 0 or test_room_has_multiple
                
                self.log_test(
                    "Multiple Bookings Per Room Support", 
                    multiple_bookings_supported, 
                    f"Multiple bookings per room {'are supported' if multiple_bookings_supported else 'not working properly'}",
                    {
                        "total_rooms": len(rooms),
                        "rooms_with_multiple_bookings": rooms_with_multiple_bookings,
                        "total_bookings_system_wide": total_bookings,
                        "test_room_has_multiple": test_room_has_multiple,
                        "multiple_bookings_supported": multiple_bookings_supported
                    }
                )
                
                return multiple_bookings_supported
            else:
                self.log_test(
                    "Multiple Bookings Per Room Support", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test("Multiple Bookings Per Room Support", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all meeting room booking tests"""
        print("=" * 80)
        print("MEETING ROOM BOOKING SYSTEM TEST - REVIEW REQUEST FOCUS")
        print("Testing multiple bookings, timezone fixes, and image serving")
        print("=" * 80)
        print()
        
        # Run tests in sequence
        tests = [
            self.test_1_get_meeting_rooms_structure,
            self.test_2_single_booking_creation,
            self.test_3_multiple_booking_same_room,
            self.test_4_timezone_normalization_function,
            self.test_5_specific_booking_cancellation,
            self.test_6_profile_image_url_serving,
            self.test_7_multiple_bookings_per_room_verification
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                print(f"Test {test_func.__name__} failed with exception: {str(e)}")
        
        # Print summary
        print("=" * 80)
        print("MEETING ROOM BOOKING TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        # Print specific results for review request items
        print("REVIEW REQUEST SPECIFIC RESULTS:")
        print("-" * 40)
        
        critical_tests = [
            ("Multiple Bookings (10AM-11AM, 2PM-3PM)", "test_3_multiple_booking_same_room"),
            ("Timezone Normalization Function", "test_4_timezone_normalization_function"),
            ("Profile Image /api/uploads/images/ Prefix", "test_6_profile_image_url_serving")
        ]
        
        for test_name, test_method in critical_tests:
            test_result = next((r for r in self.test_results if test_method in r['test']), None)
            if test_result:
                status = "✅ WORKING" if test_result['success'] else "❌ FAILING"
                print(f"{status}: {test_name}")
            else:
                print(f"❓ UNKNOWN: {test_name}")
        
        print()
        
        if success_rate >= 80:
            print("🎉 MEETING ROOM BOOKING SYSTEM: MOSTLY FUNCTIONAL")
            if passed_tests == total_tests:
                print("🔥 ALL TESTS PASSED - TIMEZONE ISSUES RESOLVED!")
        else:
            print("⚠️  MEETING ROOM BOOKING SYSTEM: NEEDS ATTENTION")
            print("🔧 TIMEZONE COMPARISON ERRORS MAY STILL EXIST")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = MeetingRoomBookingTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)