#!/usr/bin/env python3
"""
External URL Routing Fix Verification Test
Tests meeting room booking and photo upload functionality using the corrected external URL
to verify the fix for user-reported issues: "rooms not booking properly" and "photos not being saved"
"""

import requests
import json
import sys
import base64
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time

# Use the corrected external URL from frontend/.env
EXTERNAL_URL = "https://admin-mirror-1.preview.emergentagent.com/api"

class ExternalURLFixTester:
    def __init__(self):
        self.base_url = EXTERNAL_URL
        self.session = requests.Session()
        self.test_results = []
        self.created_bookings = []  # Track created bookings for cleanup
        
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

    def test_1_external_url_connectivity(self):
        """Test basic connectivity to external URL"""
        try:
            response = self.session.get(f"{self.base_url}/employees", timeout=10)
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                self.log_test(
                    "External URL Connectivity",
                    True,
                    f"Successfully connected to external URL, retrieved {employee_count} employees",
                    {"status_code": response.status_code, "employee_count": employee_count}
                )
                return True
            else:
                self.log_test(
                    "External URL Connectivity",
                    False,
                    f"External URL returned HTTP {response.status_code}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                "External URL Connectivity",
                False,
                f"Failed to connect to external URL: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_2_meeting_room_booking_via_external_url(self):
        """Test meeting room booking functionality via external URL"""
        try:
            # First, get available meeting rooms
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code != 200:
                self.log_test(
                    "Meeting Room Booking - Get Rooms",
                    False,
                    f"Failed to get meeting rooms: HTTP {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            rooms = response.json()
            if not rooms:
                self.log_test(
                    "Meeting Room Booking - Get Rooms",
                    False,
                    "No meeting rooms available for booking",
                    {"room_count": 0}
                )
                return False
            
            # Find a vacant room for booking
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
            
            # Get an employee for booking
            employees_response = self.session.get(f"{self.base_url}/employees", params={"search": "Manager"})
            if employees_response.status_code != 200:
                self.log_test(
                    "Meeting Room Booking - Get Employee",
                    False,
                    "Failed to get employees for booking",
                    {"status_code": employees_response.status_code}
                )
                return False
            
            employees = employees_response.json()
            if not employees:
                self.log_test(
                    "Meeting Room Booking - Get Employee",
                    False,
                    "No employees found for booking",
                    {"employee_count": 0}
                )
                return False
            
            test_employee = employees[0]
            employee_id = test_employee['id']
            employee_name = test_employee['name']
            
            # Create booking data for future time
            now = datetime.utcnow()
            start_time = now + timedelta(hours=2)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "External URL Fix Verification Test"
            }
            
            # Attempt to book the room via external URL
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{room_id}/book",
                json=booking_data,
                timeout=10
            )
            
            if booking_response.status_code == 200:
                booking_result = booking_response.json()
                booking_id = None
                
                # Extract booking ID from the response
                if 'bookings' in booking_result and booking_result['bookings']:
                    for booking in booking_result['bookings']:
                        if booking.get('employee_id') == employee_id and booking.get('remarks') == "External URL Fix Verification Test":
                            booking_id = booking.get('id')
                            break
                
                self.created_bookings.append({'room_id': room_id, 'booking_id': booking_id})
                
                self.log_test(
                    "Meeting Room Booking via External URL",
                    True,
                    f"Successfully booked {room_name} for {employee_name} via external URL",
                    {
                        "room_id": room_id,
                        "room_name": room_name,
                        "employee_name": employee_name,
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "booking_id": booking_id
                    }
                )
                return True
            else:
                self.log_test(
                    "Meeting Room Booking via External URL",
                    False,
                    f"Failed to book meeting room via external URL: HTTP {booking_response.status_code}",
                    {
                        "status_code": booking_response.status_code,
                        "response": booking_response.text[:300],
                        "room_id": room_id,
                        "employee_id": employee_id
                    }
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                "Meeting Room Booking via External URL",
                False,
                f"Network error during booking: {str(e)}",
                {"error": str(e)}
            )
            return False
        except Exception as e:
            self.log_test(
                "Meeting Room Booking via External URL",
                False,
                f"Unexpected error during booking: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_3_photo_upload_base64_via_external_url(self):
        """Test photo upload (base64) functionality via external URL"""
        try:
            # Get an employee for photo upload
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code != 200:
                self.log_test(
                    "Photo Upload Base64 - Get Employee",
                    False,
                    f"Failed to get employees: HTTP {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            employees = response.json()
            if not employees:
                self.log_test(
                    "Photo Upload Base64 - Get Employee",
                    False,
                    "No employees found for photo upload test",
                    {"employee_count": 0}
                )
                return False
            
            test_employee = employees[0]
            employee_id = test_employee['id']
            employee_name = test_employee['name']
            
            # Create a small test image in base64 format (1x1 red pixel PNG)
            test_image_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            
            # Upload photo via external URL using base64 method
            upload_data = {
                "profileImage": test_image_base64
            }
            
            upload_response = self.session.put(
                f"{self.base_url}/employees/{employee_id}/image",
                json=upload_data,
                timeout=10
            )
            
            if upload_response.status_code == 200:
                upload_result = upload_response.json()
                profile_image_url = upload_result.get('profileImage', '')
                
                # Verify the image URL is properly formatted
                if profile_image_url and '/api/uploads/images/' in profile_image_url:
                    self.log_test(
                        "Photo Upload Base64 via External URL",
                        True,
                        f"Successfully uploaded photo for {employee_name} via external URL",
                        {
                            "employee_id": employee_id,
                            "employee_name": employee_name,
                            "profile_image_url": profile_image_url
                        }
                    )
                    return True
                else:
                    self.log_test(
                        "Photo Upload Base64 via External URL",
                        False,
                        f"Photo uploaded but invalid image URL returned: {profile_image_url}",
                        {
                            "employee_id": employee_id,
                            "profile_image_url": profile_image_url
                        }
                    )
                    return False
            else:
                self.log_test(
                    "Photo Upload Base64 via External URL",
                    False,
                    f"Failed to upload photo via external URL: HTTP {upload_response.status_code}",
                    {
                        "status_code": upload_response.status_code,
                        "response": upload_response.text[:300],
                        "employee_id": employee_id
                    }
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                "Photo Upload Base64 via External URL",
                False,
                f"Network error during photo upload: {str(e)}",
                {"error": str(e)}
            )
            return False
        except Exception as e:
            self.log_test(
                "Photo Upload Base64 via External URL",
                False,
                f"Unexpected error during photo upload: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_4_photo_accessibility_via_external_url(self):
        """Test that uploaded photos are accessible via external URL"""
        try:
            # Get an employee with a profile image
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code != 200:
                self.log_test(
                    "Photo Accessibility - Get Employees",
                    False,
                    f"Failed to get employees: HTTP {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            employees = response.json()
            employee_with_image = None
            
            for employee in employees:
                profile_image = employee.get('profileImage', '')
                if profile_image and '/api/uploads/images/' in profile_image and not profile_image.endswith('placeholder/150/150'):
                    employee_with_image = employee
                    break
            
            if not employee_with_image:
                self.log_test(
                    "Photo Accessibility via External URL",
                    False,
                    "No employees found with uploaded profile images to test accessibility",
                    {"total_employees": len(employees)}
                )
                return False
            
            profile_image_url = employee_with_image['profileImage']
            employee_name = employee_with_image['name']
            
            # Convert relative URL to full external URL
            if profile_image_url.startswith('/api/'):
                full_image_url = f"https://admin-mirror-1.preview.emergentagent.com{profile_image_url}"
            else:
                full_image_url = profile_image_url
            
            # Test image accessibility
            image_response = self.session.get(full_image_url, timeout=10)
            
            if image_response.status_code == 200:
                content_type = image_response.headers.get('content-type', '')
                content_length = len(image_response.content)
                
                self.log_test(
                    "Photo Accessibility via External URL",
                    True,
                    f"Successfully accessed profile image for {employee_name} via external URL",
                    {
                        "employee_name": employee_name,
                        "image_url": full_image_url,
                        "content_type": content_type,
                        "content_length": content_length
                    }
                )
                return True
            else:
                self.log_test(
                    "Photo Accessibility via External URL",
                    False,
                    f"Failed to access profile image via external URL: HTTP {image_response.status_code}",
                    {
                        "status_code": image_response.status_code,
                        "image_url": full_image_url,
                        "employee_name": employee_name
                    }
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                "Photo Accessibility via External URL",
                False,
                f"Network error accessing photo: {str(e)}",
                {"error": str(e)}
            )
            return False
        except Exception as e:
            self.log_test(
                "Photo Accessibility via External URL",
                False,
                f"Unexpected error accessing photo: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_5_booking_persistence_verification(self):
        """Verify that bookings are properly saved and persist in the database"""
        try:
            if not self.created_bookings:
                self.log_test(
                    "Booking Persistence Verification",
                    False,
                    "No bookings were created in previous tests to verify persistence",
                    {}
                )
                return False
            
            # Check if the booking we created still exists
            booking_info = self.created_bookings[0]
            room_id = booking_info['room_id']
            
            # Get the room details to check if booking persists
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code != 200:
                self.log_test(
                    "Booking Persistence Verification",
                    False,
                    f"Failed to get meeting rooms for persistence check: HTTP {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
            
            rooms = response.json()
            target_room = None
            
            for room in rooms:
                if room['id'] == room_id:
                    target_room = room
                    break
            
            if not target_room:
                self.log_test(
                    "Booking Persistence Verification",
                    False,
                    f"Room {room_id} not found in database",
                    {"room_id": room_id}
                )
                return False
            
            # Check if our booking exists in the room's bookings
            bookings = target_room.get('bookings', [])
            test_booking_found = False
            
            for booking in bookings:
                if booking.get('remarks') == "External URL Fix Verification Test":
                    test_booking_found = True
                    break
            
            if test_booking_found:
                self.log_test(
                    "Booking Persistence Verification",
                    True,
                    f"Booking successfully persisted in database for room {target_room['name']}",
                    {
                        "room_id": room_id,
                        "room_name": target_room['name'],
                        "total_bookings": len(bookings)
                    }
                )
                return True
            else:
                self.log_test(
                    "Booking Persistence Verification",
                    False,
                    f"Test booking not found in room {target_room['name']} - persistence failed",
                    {
                        "room_id": room_id,
                        "room_name": target_room['name'],
                        "total_bookings": len(bookings),
                        "booking_remarks": [b.get('remarks', '') for b in bookings]
                    }
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Booking Persistence Verification",
                False,
                f"Error verifying booking persistence: {str(e)}",
                {"error": str(e)}
            )
            return False

    def cleanup_test_bookings(self):
        """Clean up test bookings created during testing"""
        print("\n🧹 Cleaning up test bookings...")
        
        for booking_info in self.created_bookings:
            try:
                room_id = booking_info['room_id']
                booking_id = booking_info['booking_id']
                
                if booking_id:
                    # Try to cancel the specific booking
                    response = self.session.delete(f"{self.base_url}/meeting-rooms/{room_id}/booking/{booking_id}")
                    if response.status_code == 200:
                        print(f"✅ Cleaned up booking {booking_id} for room {room_id}")
                    else:
                        print(f"⚠️  Could not clean up booking {booking_id} for room {room_id}: HTTP {response.status_code}")
                else:
                    print(f"⚠️  No booking ID available for room {room_id} cleanup")
                    
            except Exception as e:
                print(f"❌ Error cleaning up booking for room {room_id}: {str(e)}")

    def run_all_tests(self):
        """Run all external URL fix verification tests"""
        print("🚀 Starting External URL Routing Fix Verification Tests")
        print(f"🌐 Testing External URL: {self.base_url}")
        print("=" * 80)
        
        # Test sequence
        tests = [
            self.test_1_external_url_connectivity,
            self.test_2_meeting_room_booking_via_external_url,
            self.test_3_photo_upload_base64_via_external_url,
            self.test_4_photo_accessibility_via_external_url,
            self.test_5_booking_persistence_verification
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_func.__name__}: {str(e)}")
        
        # Cleanup
        self.cleanup_test_bookings()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 EXTERNAL URL FIX VERIFICATION TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{status}: {result['test']}")
        
        print(f"\n🎯 OVERALL RESULT: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - External URL routing fix is working correctly!")
            print("✅ Meeting room booking functionality works via external URL")
            print("✅ Photo upload functionality works via external URL")
            print("✅ Both functionalities are now working as expected for the frontend")
        else:
            print("⚠️  SOME TESTS FAILED - External URL routing may still have issues")
            failed_tests = [r for r in self.test_results if not r["success"]]
            print("❌ Failed tests:")
            for failed in failed_tests:
                print(f"   - {failed['test']}: {failed['message']}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = ExternalURLFixTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)