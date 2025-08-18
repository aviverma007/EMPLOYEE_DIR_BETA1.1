#!/usr/bin/env python3
"""
User Issue Testing - Meeting Room Booking and Photo Upload
Testing the specific issues reported by the user:
1. Rooms are not booking properly and not saving to the backend server
2. Photos are not being saved
"""

import requests
import json
import sys
import base64
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time

# Use internal URL for testing
BACKEND_URL = "http://localhost:8001/api"

class UserIssueTester:
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

    def setup_test_data(self):
        """Get test employee and room for booking tests"""
        try:
            # Get employees
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code == 200:
                employees = emp_response.json()
                if employees:
                    # Use a real employee from the system
                    self.test_employee_id = employees[0]["id"]
                    print(f"Using test employee: {employees[0]['name']} (ID: {self.test_employee_id})")
                
            # Get meeting rooms
            room_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if room_response.status_code == 200:
                rooms = room_response.json()
                if rooms:
                    # Find a vacant room for testing
                    for room in rooms:
                        if room.get("status") == "vacant":
                            self.test_room_id = room["id"]
                            print(f"Using test room: {room['name']} (ID: {self.test_room_id})")
                            break
                    
                    if not self.test_room_id and rooms:
                        # If no vacant room, use the first one
                        self.test_room_id = rooms[0]["id"]
                        print(f"Using test room: {rooms[0]['name']} (ID: {self.test_room_id})")
                        
        except Exception as e:
            print(f"Error setting up test data: {str(e)}")

    def test_1_meeting_room_booking_basic(self):
        """Test basic meeting room booking - POST /api/meeting-rooms/{room_id}/book"""
        if not self.test_employee_id or not self.test_room_id:
            self.log_test("Meeting Room Booking Basic", False, "Test data not available")
            return
            
        try:
            # Create booking for 2 hours from now to avoid conflicts
            start_time = datetime.utcnow() + timedelta(hours=2)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "User issue test booking"
            }
            
            print(f"Attempting to book room {self.test_room_id} for employee {self.test_employee_id}")
            print(f"Time slot: {start_time.isoformat()} to {end_time.isoformat()}")
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            print(f"Booking response status: {response.status_code}")
            
            if response.status_code == 200:
                booking_result = response.json()
                bookings = booking_result.get("bookings", [])
                
                # Check if booking was added
                test_booking_found = False
                for booking in bookings:
                    if (booking.get("employee_id") == self.test_employee_id and 
                        booking.get("remarks") == "User issue test booking"):
                        test_booking_found = True
                        print(f"Found test booking: {booking}")
                        break
                
                if test_booking_found:
                    self.log_test(
                        "Meeting Room Booking Basic", 
                        True, 
                        "✅ BOOKING WORKS: Room booking successful and saved to backend",
                        {
                            "room_id": self.test_room_id,
                            "employee_id": self.test_employee_id,
                            "total_bookings": len(bookings),
                            "booking_saved": True
                        }
                    )
                else:
                    self.log_test(
                        "Meeting Room Booking Basic", 
                        False, 
                        "❌ BOOKING ISSUE: API returned success but booking not found in response",
                        {"response_bookings": len(bookings)}
                    )
            else:
                error_text = response.text
                self.log_test(
                    "Meeting Room Booking Basic", 
                    False, 
                    f"❌ BOOKING FAILED: HTTP {response.status_code} - {error_text}",
                    {"status_code": response.status_code, "error": error_text}
                )
                
        except Exception as e:
            self.log_test("Meeting Room Booking Basic", False, f"❌ BOOKING EXCEPTION: {str(e)}")

    def test_2_booking_persistence_check(self):
        """Test if bookings persist in the database"""
        if not self.test_room_id:
            self.log_test("Booking Persistence Check", False, "Test room not available")
            return
            
        try:
            # Get room details to check if booking persists
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                test_room = None
                
                for room in rooms:
                    if room["id"] == self.test_room_id:
                        test_room = room
                        break
                
                if test_room:
                    bookings = test_room.get("bookings", [])
                    
                    # Look for our test booking
                    test_booking_found = False
                    for booking in bookings:
                        if (booking.get("employee_id") == self.test_employee_id and 
                            booking.get("remarks") == "User issue test booking"):
                            test_booking_found = True
                            break
                    
                    if test_booking_found:
                        self.log_test(
                            "Booking Persistence Check", 
                            True, 
                            "✅ PERSISTENCE WORKS: Booking successfully saved and persisted in database",
                            {
                                "room_id": self.test_room_id,
                                "total_bookings": len(bookings),
                                "booking_persisted": True
                            }
                        )
                    else:
                        self.log_test(
                            "Booking Persistence Check", 
                            False, 
                            "❌ PERSISTENCE ISSUE: Test booking not found in database",
                            {"total_bookings": len(bookings)}
                        )
                else:
                    self.log_test("Booking Persistence Check", False, "Test room not found")
            else:
                self.log_test(
                    "Booking Persistence Check", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Booking Persistence Check", False, f"Exception: {str(e)}")

    def test_3_multiple_bookings_same_room(self):
        """Test multiple bookings to the same room"""
        if not self.test_employee_id or not self.test_room_id:
            self.log_test("Multiple Bookings Same Room", False, "Test data not available")
            return
            
        try:
            # Create second booking for different time slot (4 hours from now)
            start_time = datetime.utcnow() + timedelta(hours=4)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "User issue test booking #2"
            }
            
            print(f"Attempting second booking for room {self.test_room_id}")
            print(f"Time slot: {start_time.isoformat()} to {end_time.isoformat()}")
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            print(f"Second booking response status: {response.status_code}")
            
            if response.status_code == 200:
                booking_result = response.json()
                bookings = booking_result.get("bookings", [])
                
                # Check if we now have multiple bookings
                test_bookings_count = 0
                for booking in bookings:
                    if (booking.get("employee_id") == self.test_employee_id and 
                        "User issue test booking" in booking.get("remarks", "")):
                        test_bookings_count += 1
                
                if test_bookings_count >= 2:
                    self.log_test(
                        "Multiple Bookings Same Room", 
                        True, 
                        f"✅ MULTIPLE BOOKINGS WORK: Successfully created {test_bookings_count} bookings for same room",
                        {
                            "room_id": self.test_room_id,
                            "test_bookings_count": test_bookings_count,
                            "total_bookings": len(bookings)
                        }
                    )
                else:
                    self.log_test(
                        "Multiple Bookings Same Room", 
                        False, 
                        f"❌ MULTIPLE BOOKINGS ISSUE: Expected multiple bookings but found only {test_bookings_count}",
                        {"test_bookings_count": test_bookings_count, "total_bookings": len(bookings)}
                    )
            else:
                error_text = response.text
                self.log_test(
                    "Multiple Bookings Same Room", 
                    False, 
                    f"❌ MULTIPLE BOOKINGS FAILED: HTTP {response.status_code} - {error_text}",
                    {"status_code": response.status_code, "error": error_text}
                )
                
        except Exception as e:
            self.log_test("Multiple Bookings Same Room", False, f"❌ MULTIPLE BOOKINGS EXCEPTION: {str(e)}")

    def create_test_image_base64(self):
        """Create a simple test image in base64 format"""
        # Create a simple 10x10 red square PNG
        import struct
        
        # PNG header
        png_header = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk (image header)
        width = height = 10
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = 0x9D8A8C8F  # Pre-calculated CRC for this specific IHDR
        ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
        
        # IDAT chunk (image data) - simple red pixels
        import zlib
        # Create red pixels (RGB: 255, 0, 0)
        pixels = b''
        for y in range(height):
            pixels += b'\x00'  # Filter type (none)
            for x in range(width):
                pixels += b'\xff\x00\x00'  # Red pixel (RGB)
        
        compressed_pixels = zlib.compress(pixels)
        idat_chunk = struct.pack('>I', len(compressed_pixels)) + b'IDAT' + compressed_pixels
        idat_crc = zlib.crc32(b'IDAT' + compressed_pixels) & 0xffffffff
        idat_chunk += struct.pack('>I', idat_crc)
        
        # IEND chunk (end of image)
        iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', 0xAE426082)
        
        # Combine all chunks
        png_data = png_header + ihdr_chunk + idat_chunk + iend_chunk
        
        # Convert to base64
        base64_data = base64.b64encode(png_data).decode('utf-8')
        return f"data:image/png;base64,{base64_data}"

    def test_4_photo_upload_base64(self):
        """Test base64 photo upload - PUT /api/employees/{id}/image"""
        if not self.test_employee_id:
            self.log_test("Photo Upload Base64", False, "Test employee not available")
            return
            
        try:
            # Create test image
            test_image_base64 = self.create_test_image_base64()
            
            # Upload image using base64 method
            image_data = {
                "profileImage": test_image_base64
            }
            
            print(f"Attempting to upload base64 image for employee {self.test_employee_id}")
            
            response = self.session.put(
                f"{self.base_url}/employees/{self.test_employee_id}/image",
                json=image_data
            )
            
            print(f"Base64 upload response status: {response.status_code}")
            
            if response.status_code == 200:
                employee_result = response.json()
                profile_image_url = employee_result.get("profileImage")
                
                if profile_image_url and profile_image_url.startswith("/api/uploads/images/"):
                    # Test if image file exists on filesystem
                    import os
                    file_path = f"/app/backend/uploads/images/{self.test_employee_id}.png"
                    file_exists = os.path.exists(file_path)
                    
                    if file_exists:
                        file_size = os.path.getsize(file_path)
                        self.log_test(
                            "Photo Upload Base64", 
                            True, 
                            "✅ PHOTO UPLOAD WORKS: Base64 image successfully uploaded and saved to filesystem",
                            {
                                "employee_id": self.test_employee_id,
                                "image_url": profile_image_url,
                                "file_exists": True,
                                "file_size_bytes": file_size,
                                "file_path": file_path
                            }
                        )
                    else:
                        self.log_test(
                            "Photo Upload Base64", 
                            False, 
                            "❌ PHOTO SAVE ISSUE: Image uploaded but file not found on filesystem",
                            {"expected_file_path": file_path}
                        )
                else:
                    self.log_test(
                        "Photo Upload Base64", 
                        False, 
                        "❌ PHOTO UPLOAD ISSUE: Image uploaded but no valid URL returned",
                        {"returned_url": profile_image_url}
                    )
            else:
                error_text = response.text
                self.log_test(
                    "Photo Upload Base64", 
                    False, 
                    f"❌ PHOTO UPLOAD FAILED: HTTP {response.status_code} - {error_text}",
                    {"status_code": response.status_code, "error": error_text}
                )
                
        except Exception as e:
            self.log_test("Photo Upload Base64", False, f"❌ PHOTO UPLOAD EXCEPTION: {str(e)}")

    def test_5_photo_upload_file(self):
        """Test file photo upload - POST /api/employees/{id}/upload-image"""
        if not self.test_employee_id:
            self.log_test("Photo Upload File", False, "Test employee not available")
            return
            
        try:
            # Create a simple test image file
            test_image_base64 = self.create_test_image_base64()
            # Remove the data URL prefix to get just the base64 data
            base64_data = test_image_base64.split(',')[1]
            image_bytes = base64.b64decode(base64_data)
            
            # Create file-like object
            files = {
                'file': ('test_image.png', io.BytesIO(image_bytes), 'image/png')
            }
            
            print(f"Attempting to upload file image for employee {self.test_employee_id}")
            
            response = self.session.post(
                f"{self.base_url}/employees/{self.test_employee_id}/upload-image",
                files=files
            )
            
            print(f"File upload response status: {response.status_code}")
            
            if response.status_code == 200:
                employee_result = response.json()
                profile_image_url = employee_result.get("profileImage")
                
                if profile_image_url and profile_image_url.startswith("/api/uploads/images/"):
                    # Test if image file exists on filesystem
                    import os
                    file_path = f"/app/backend/uploads/images/{self.test_employee_id}.png"
                    file_exists = os.path.exists(file_path)
                    
                    if file_exists:
                        file_size = os.path.getsize(file_path)
                        self.log_test(
                            "Photo Upload File", 
                            True, 
                            "✅ PHOTO FILE UPLOAD WORKS: File image successfully uploaded and saved to filesystem",
                            {
                                "employee_id": self.test_employee_id,
                                "image_url": profile_image_url,
                                "file_exists": True,
                                "file_size_bytes": file_size,
                                "file_path": file_path
                            }
                        )
                    else:
                        self.log_test(
                            "Photo Upload File", 
                            False, 
                            "❌ PHOTO FILE SAVE ISSUE: Image uploaded but file not found on filesystem",
                            {"expected_file_path": file_path}
                        )
                else:
                    self.log_test(
                        "Photo Upload File", 
                        False, 
                        "❌ PHOTO FILE UPLOAD ISSUE: Image uploaded but no valid URL returned",
                        {"returned_url": profile_image_url}
                    )
            else:
                error_text = response.text
                self.log_test(
                    "Photo Upload File", 
                    False, 
                    f"❌ PHOTO FILE UPLOAD FAILED: HTTP {response.status_code} - {error_text}",
                    {"status_code": response.status_code, "error": error_text}
                )
                
        except Exception as e:
            self.log_test("Photo Upload File", False, f"❌ PHOTO FILE UPLOAD EXCEPTION: {str(e)}")

    def test_6_photo_accessibility(self):
        """Test if uploaded photos are accessible via API"""
        if not self.test_employee_id:
            self.log_test("Photo Accessibility", False, "Test employee not available")
            return
            
        try:
            # Get employee details to check image URL
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                test_employee = None
                
                for emp in employees:
                    if emp["id"] == self.test_employee_id:
                        test_employee = emp
                        break
                
                if test_employee:
                    profile_image_url = test_employee.get("profileImage")
                    
                    if profile_image_url and profile_image_url.startswith("/api/uploads/images/"):
                        # Test if image is accessible via API
                        image_response = self.session.get(f"http://localhost:8001{profile_image_url}")
                        
                        if image_response.status_code == 200:
                            self.log_test(
                                "Photo Accessibility", 
                                True, 
                                "✅ PHOTO ACCESS WORKS: Uploaded photo is accessible via API",
                                {
                                    "employee_id": self.test_employee_id,
                                    "image_url": profile_image_url,
                                    "image_size_bytes": len(image_response.content),
                                    "content_type": image_response.headers.get("content-type", "unknown")
                                }
                            )
                        else:
                            self.log_test(
                                "Photo Accessibility", 
                                False, 
                                f"❌ PHOTO ACCESS ISSUE: Image URL exists but not accessible: HTTP {image_response.status_code}",
                                {"image_url": profile_image_url}
                            )
                    else:
                        self.log_test(
                            "Photo Accessibility", 
                            False, 
                            "❌ PHOTO URL ISSUE: No valid image URL found for test employee",
                            {"returned_url": profile_image_url}
                        )
                else:
                    self.log_test("Photo Accessibility", False, "Test employee not found")
            else:
                self.log_test(
                    "Photo Accessibility", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Photo Accessibility", False, f"Exception: {str(e)}")

    def cleanup_test_data(self):
        """Clean up test bookings and images created during testing"""
        try:
            # Clean up test bookings
            if self.test_room_id:
                response = self.session.get(f"{self.base_url}/meeting-rooms")
                if response.status_code == 200:
                    rooms = response.json()
                    for room in rooms:
                        if room["id"] == self.test_room_id:
                            bookings = room.get("bookings", [])
                            for booking in bookings:
                                if (booking.get("employee_id") == self.test_employee_id and 
                                    "User issue test booking" in booking.get("remarks", "")):
                                    booking_id = booking.get("id")
                                    if booking_id:
                                        cancel_response = self.session.delete(
                                            f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{booking_id}"
                                        )
                                        if cancel_response.status_code == 200:
                                            print(f"Cleaned up test booking: {booking_id}")
                            break
            
            print("Test cleanup completed")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def run_all_tests(self):
        """Run all user issue tests"""
        print("=" * 80)
        print("USER ISSUE TESTING - MEETING ROOM BOOKING & PHOTO UPLOAD")
        print("Testing specific issues reported by user:")
        print("1. Rooms are not booking properly and not saving to the backend server")
        print("2. Photos are not being saved")
        print("=" * 80)
        print()
        
        # Setup test data
        self.setup_test_data()
        
        if not self.test_employee_id or not self.test_room_id:
            print("❌ CRITICAL: Cannot run tests - missing test data")
            print(f"Employee ID: {self.test_employee_id}")
            print(f"Room ID: {self.test_room_id}")
            return False
        
        # Run tests
        self.test_1_meeting_room_booking_basic()
        self.test_2_booking_persistence_check()
        self.test_3_multiple_bookings_same_room()
        self.test_4_photo_upload_base64()
        self.test_5_photo_upload_file()
        self.test_6_photo_accessibility()
        
        # Cleanup
        self.cleanup_test_data()
        
        # Summary
        print("=" * 80)
        print("USER ISSUE TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        # Analyze user issues
        print("USER ISSUE ANALYSIS:")
        print("-" * 40)
        
        booking_tests = [r for r in self.test_results if "Booking" in r["test"]]
        booking_passed = sum(1 for r in booking_tests if r["success"])
        
        photo_tests = [r for r in self.test_results if "Photo" in r["test"]]
        photo_passed = sum(1 for r in photo_tests if r["success"])
        
        print(f"📅 MEETING ROOM BOOKING: {booking_passed}/{len(booking_tests)} tests passed")
        if booking_passed == len(booking_tests):
            print("   ✅ BOOKING SYSTEM IS WORKING PROPERLY")
        else:
            print("   ❌ BOOKING SYSTEM HAS ISSUES")
            
        print(f"📸 PHOTO UPLOAD: {photo_passed}/{len(photo_tests)} tests passed")
        if photo_passed == len(photo_tests):
            print("   ✅ PHOTO SYSTEM IS WORKING PROPERLY")
        else:
            print("   ❌ PHOTO SYSTEM HAS ISSUES")
        
        print()
        
        # List failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("FAILED TESTS:")
            for test in failed_tests:
                print(f"❌ {test['test']}: {test['message']}")
        else:
            print("🎉 ALL TESTS PASSED - USER ISSUES RESOLVED!")
        
        print("=" * 80)
        
        return passed == total

if __name__ == "__main__":
    tester = UserIssueTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)