#!/usr/bin/env python3
"""
Comprehensive User Issue Testing
Tests both internal and external API access to identify the root cause of user issues
"""

import requests
import json
import sys
import base64
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time

# URLs to test
INTERNAL_URL = "http://localhost:8001/api"
EXTERNAL_URL = "https://backend-booking-fix.preview.emergentagent.com/api"

class ComprehensiveUserIssueTester:
    def __init__(self):
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

    def test_api_connectivity(self, url_name: str, base_url: str):
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{base_url}/employees", timeout=10)
            
            if response.status_code == 200:
                employees = response.json()
                self.log_test(
                    f"API Connectivity ({url_name})", 
                    True, 
                    f"✅ API accessible - {len(employees)} employees found",
                    {"url": base_url, "employee_count": len(employees)}
                )
                return True
            else:
                self.log_test(
                    f"API Connectivity ({url_name})", 
                    False, 
                    f"❌ API not accessible - HTTP {response.status_code}: {response.text[:100]}",
                    {"url": base_url, "status_code": response.status_code}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                f"API Connectivity ({url_name})", 
                False, 
                f"❌ Connection failed - {str(e)}",
                {"url": base_url, "error": str(e)}
            )
            return False

    def test_meeting_room_booking(self, url_name: str, base_url: str):
        """Test meeting room booking functionality"""
        try:
            # Get employees
            emp_response = self.session.get(f"{base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test(f"Meeting Room Booking ({url_name})", False, "Cannot get employees")
                return False
                
            employees = emp_response.json()
            if not employees:
                self.log_test(f"Meeting Room Booking ({url_name})", False, "No employees available")
                return False
                
            test_employee_id = employees[0]["id"]
            
            # Get meeting rooms
            room_response = self.session.get(f"{base_url}/meeting-rooms")
            if room_response.status_code != 200:
                self.log_test(f"Meeting Room Booking ({url_name})", False, "Cannot get meeting rooms")
                return False
                
            rooms = room_response.json()
            if not rooms:
                self.log_test(f"Meeting Room Booking ({url_name})", False, "No meeting rooms available")
                return False
                
            test_room_id = rooms[0]["id"]
            
            # Create booking
            start_time = datetime.utcnow() + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": f"Test booking via {url_name}"
            }
            
            booking_response = self.session.post(
                f"{base_url}/meeting-rooms/{test_room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                booking_result = booking_response.json()
                bookings = booking_result.get("bookings", [])
                
                # Check if booking was created
                test_booking_found = any(
                    b.get("employee_id") == test_employee_id and 
                    f"Test booking via {url_name}" in b.get("remarks", "")
                    for b in bookings
                )
                
                if test_booking_found:
                    self.log_test(
                        f"Meeting Room Booking ({url_name})", 
                        True, 
                        f"✅ Booking successful via {url_name}",
                        {
                            "url": base_url,
                            "room_id": test_room_id,
                            "employee_id": test_employee_id,
                            "total_bookings": len(bookings)
                        }
                    )
                    
                    # Cleanup - cancel the test booking
                    for booking in bookings:
                        if (booking.get("employee_id") == test_employee_id and 
                            f"Test booking via {url_name}" in booking.get("remarks", "")):
                            booking_id = booking.get("id")
                            if booking_id:
                                self.session.delete(f"{base_url}/meeting-rooms/{test_room_id}/booking/{booking_id}")
                            break
                    
                    return True
                else:
                    self.log_test(
                        f"Meeting Room Booking ({url_name})", 
                        False, 
                        f"❌ Booking API returned success but booking not found"
                    )
                    return False
            else:
                self.log_test(
                    f"Meeting Room Booking ({url_name})", 
                    False, 
                    f"❌ Booking failed - HTTP {booking_response.status_code}: {booking_response.text[:100]}",
                    {"status_code": booking_response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test(f"Meeting Room Booking ({url_name})", False, f"❌ Exception: {str(e)}")
            return False

    def test_photo_upload(self, url_name: str, base_url: str):
        """Test photo upload functionality"""
        try:
            # Get employees
            emp_response = self.session.get(f"{base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test(f"Photo Upload ({url_name})", False, "Cannot get employees")
                return False
                
            employees = emp_response.json()
            if not employees:
                self.log_test(f"Photo Upload ({url_name})", False, "No employees available")
                return False
                
            test_employee_id = employees[0]["id"]
            
            # Create simple test image
            test_image_base64 = self.create_test_image_base64()
            
            # Upload image using base64 method
            image_data = {
                "profileImage": test_image_base64
            }
            
            upload_response = self.session.put(
                f"{base_url}/employees/{test_employee_id}/image",
                json=image_data
            )
            
            if upload_response.status_code == 200:
                employee_result = upload_response.json()
                profile_image_url = employee_result.get("profileImage")
                
                if profile_image_url and profile_image_url.startswith("/api/uploads/images/"):
                    self.log_test(
                        f"Photo Upload ({url_name})", 
                        True, 
                        f"✅ Photo upload successful via {url_name}",
                        {
                            "url": base_url,
                            "employee_id": test_employee_id,
                            "image_url": profile_image_url
                        }
                    )
                    return True
                else:
                    self.log_test(
                        f"Photo Upload ({url_name})", 
                        False, 
                        f"❌ Photo uploaded but invalid URL returned: {profile_image_url}"
                    )
                    return False
            else:
                self.log_test(
                    f"Photo Upload ({url_name})", 
                    False, 
                    f"❌ Photo upload failed - HTTP {upload_response.status_code}: {upload_response.text[:100]}",
                    {"status_code": upload_response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test(f"Photo Upload ({url_name})", False, f"❌ Exception: {str(e)}")
            return False

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

    def run_all_tests(self):
        """Run comprehensive tests on both internal and external URLs"""
        print("=" * 80)
        print("COMPREHENSIVE USER ISSUE TESTING")
        print("Testing both internal and external API access")
        print("=" * 80)
        print()
        
        # Test internal API (what backend actually serves)
        print("🔧 TESTING INTERNAL API (localhost:8001)")
        print("-" * 50)
        internal_connectivity = self.test_api_connectivity("Internal", INTERNAL_URL)
        internal_booking = False
        internal_photo = False
        
        if internal_connectivity:
            internal_booking = self.test_meeting_room_booking("Internal", INTERNAL_URL)
            internal_photo = self.test_photo_upload("Internal", INTERNAL_URL)
        
        print()
        
        # Test external API (what frontend tries to use)
        print("🌐 TESTING EXTERNAL API (backend-booking-fix.preview.emergentagent.com)")
        print("-" * 50)
        external_connectivity = self.test_api_connectivity("External", EXTERNAL_URL)
        external_booking = False
        external_photo = False
        
        if external_connectivity:
            external_booking = self.test_meeting_room_booking("External", EXTERNAL_URL)
            external_photo = self.test_photo_upload("External", EXTERNAL_URL)
        
        print()
        
        # Summary and analysis
        print("=" * 80)
        print("COMPREHENSIVE TEST ANALYSIS")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        # Root cause analysis
        print("ROOT CAUSE ANALYSIS:")
        print("-" * 40)
        
        if internal_connectivity and not external_connectivity:
            print("🔍 IDENTIFIED ISSUE: External URL routing problem")
            print("   ✅ Backend server is working correctly (internal API functional)")
            print("   ❌ External URL is not properly routed to backend server")
            print("   📋 RECOMMENDATION: Fix external URL routing/proxy configuration")
            print()
            print("   USER IMPACT:")
            print("   - Frontend cannot connect to backend via external URL")
            print("   - Meeting room bookings fail due to connectivity issues")
            print("   - Photo uploads fail due to connectivity issues")
            print("   - This explains why user reports 'not saving to backend server'")
            
        elif not internal_connectivity and not external_connectivity:
            print("🔍 IDENTIFIED ISSUE: Backend server problem")
            print("   ❌ Backend server is not responding on any URL")
            print("   📋 RECOMMENDATION: Check backend server status and logs")
            
        elif internal_connectivity and external_connectivity:
            if internal_booking and internal_photo and external_booking and external_photo:
                print("🎉 NO ISSUES FOUND: All systems working correctly")
                print("   ✅ Both internal and external APIs functional")
                print("   ✅ Meeting room booking working on both URLs")
                print("   ✅ Photo upload working on both URLs")
                print("   📋 User issues may be intermittent or resolved")
            else:
                print("🔍 IDENTIFIED ISSUE: Functional problems in backend")
                print("   ✅ APIs are accessible")
                print("   ❌ Some functionality not working correctly")
                
        else:
            print("🔍 MIXED RESULTS: Partial connectivity issues")
        
        print()
        
        # List failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("FAILED TESTS:")
            for test in failed_tests:
                print(f"❌ {test['test']}: {test['message']}")
        
        print("=" * 80)
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveUserIssueTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)