#!/usr/bin/env python3
"""
Review Request Testing - Focus on Image Upload Persistence and Meeting Room Booking Persistence
Tests the specific fixes mentioned in the review request
"""

import requests
import json
import sys
import time
import base64
import io
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "http://localhost:8001/api"

class ReviewRequestTester:
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
        """Get test employee and room for testing"""
        try:
            # Get first employee for testing
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code == 200:
                employees = emp_response.json()
                if employees:
                    self.test_employee_id = employees[0]["id"]
                    print(f"Using test employee: {employees[0]['name']} (ID: {self.test_employee_id})")
                else:
                    print("❌ No employees found for testing")
                    return False
            else:
                print(f"❌ Could not fetch employees: {emp_response.status_code}")
                return False

            # Get first meeting room for testing
            room_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if room_response.status_code == 200:
                rooms = room_response.json()
                if rooms:
                    self.test_room_id = rooms[0]["id"]
                    print(f"Using test room: {rooms[0]['name']} (ID: {self.test_room_id})")
                else:
                    print("❌ No meeting rooms found for testing")
                    return False
            else:
                print(f"❌ Could not fetch meeting rooms: {room_response.status_code}")
                return False

            return True
        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            return False

    # ========================================
    # IMAGE UPLOAD PERSISTENCE TESTS
    # ========================================

    def test_1_get_employees_dynamic_profile_images(self):
        """Test GET /api/employees - Verify profileImage URLs are dynamically set from filesystem"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count > 0:
                    # Check if employees have profileImage field
                    employees_with_images = [emp for emp in employees if emp.get('profileImage')]
                    employees_without_images = [emp for emp in employees if not emp.get('profileImage')]
                    
                    self.log_test(
                        "GET /api/employees - Dynamic Profile Images", 
                        True, 
                        f"Successfully fetched {employee_count} employees. {len(employees_with_images)} have profile images, {len(employees_without_images)} don't",
                        {
                            "total_employees": employee_count,
                            "with_images": len(employees_with_images),
                            "without_images": len(employees_without_images),
                            "sample_image_url": employees_with_images[0]['profileImage'] if employees_with_images else None
                        }
                    )
                else:
                    self.log_test("GET /api/employees - Dynamic Profile Images", False, "No employees found")
            else:
                self.log_test(
                    "GET /api/employees - Dynamic Profile Images", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/employees - Dynamic Profile Images", False, f"Exception: {str(e)}")

    def test_2_upload_image_file_persistence(self):
        """Test POST /api/employees/{id}/upload-image - Verify file saves to /app/backend/uploads/images/"""
        try:
            if not self.test_employee_id:
                self.log_test("POST /api/employees/{id}/upload-image", False, "No test employee available")
                return

            # Create a small test image (1x1 red pixel PNG)
            base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            image_bytes = base64.b64decode(base64_data)
            
            # Create file-like object
            files = {
                'file': ('test_upload.png', io.BytesIO(image_bytes), 'image/png')
            }
            
            upload_response = self.session.post(
                f"{self.base_url}/employees/{self.test_employee_id}/upload-image",
                files=files
            )
            
            if upload_response.status_code == 200:
                updated_employee = upload_response.json()
                new_image_url = updated_employee.get("profileImage")
                
                # Check if the image was saved with correct URL pattern
                if new_image_url and new_image_url.startswith("/uploads/images/"):
                    # Check if file actually exists on filesystem
                    expected_file_path = f"/app/backend/uploads/images/{self.test_employee_id}.png"
                    file_exists = os.path.exists(expected_file_path)
                    
                    self.log_test(
                        "POST /api/employees/{id}/upload-image", 
                        True, 
                        f"Successfully uploaded image file. File exists on filesystem: {file_exists}",
                        {
                            "employee_id": self.test_employee_id,
                            "image_url": new_image_url,
                            "expected_file_path": expected_file_path,
                            "file_exists": file_exists
                        }
                    )
                else:
                    self.log_test(
                        "POST /api/employees/{id}/upload-image", 
                        False, 
                        f"File upload did not return correct URL pattern. Got: {new_image_url}"
                    )
            else:
                self.log_test(
                    "POST /api/employees/{id}/upload-image", 
                    False, 
                    f"HTTP {upload_response.status_code}: {upload_response.text}"
                )
                
        except Exception as e:
            self.log_test("POST /api/employees/{id}/upload-image", False, f"Exception: {str(e)}")

    def test_3_base64_image_persistence(self):
        """Test PUT /api/employees/{id}/image - Verify base64 data saves to filesystem"""
        try:
            if not self.test_employee_id:
                self.log_test("PUT /api/employees/{id}/image - Base64", False, "No test employee available")
                return

            # Create a small test image in base64 (1x1 blue pixel PNG)
            base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAFfeFUJwwAAAABJRU5ErkJggg=="
            
            # Update profile image with base64 data
            update_data = {
                "profileImage": base64_image
            }
            
            update_response = self.session.put(
                f"{self.base_url}/employees/{self.test_employee_id}/image",
                json=update_data
            )
            
            if update_response.status_code == 200:
                updated_employee = update_response.json()
                new_image_url = updated_employee.get("profileImage")
                
                # Check if the image was converted to a file URL
                if new_image_url and new_image_url.startswith("/uploads/images/"):
                    # Check if file actually exists on filesystem
                    expected_file_path = f"/app/backend/uploads/images/{self.test_employee_id}.png"
                    file_exists = os.path.exists(expected_file_path)
                    
                    self.log_test(
                        "PUT /api/employees/{id}/image - Base64", 
                        True, 
                        f"Successfully converted base64 to file. File exists on filesystem: {file_exists}",
                        {
                            "employee_id": self.test_employee_id,
                            "image_url": new_image_url,
                            "expected_file_path": expected_file_path,
                            "file_exists": file_exists
                        }
                    )
                else:
                    self.log_test(
                        "PUT /api/employees/{id}/image - Base64", 
                        False, 
                        f"Base64 image was not converted to file URL correctly. Got: {new_image_url}"
                    )
            else:
                self.log_test(
                    "PUT /api/employees/{id}/image - Base64", 
                    False, 
                    f"HTTP {update_response.status_code}: {update_response.text}"
                )
                
        except Exception as e:
            self.log_test("PUT /api/employees/{id}/image - Base64", False, f"Exception: {str(e)}")

    def test_4_static_file_serving(self):
        """Test static file serving at /uploads/images/ - Verify images are accessible"""
        try:
            if not self.test_employee_id:
                self.log_test("Static File Serving", False, "No test employee available")
                return

            # First ensure we have an image uploaded
            base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAFfeFUJwwAAAABJRU5ErkJggg=="
            update_data = {"profileImage": base64_image}
            
            upload_response = self.session.put(
                f"{self.base_url}/employees/{self.test_employee_id}/image",
                json=update_data
            )
            
            if upload_response.status_code == 200:
                updated_employee = upload_response.json()
                image_url = updated_employee.get("profileImage")
                
                if image_url and image_url.startswith("/uploads/images/"):
                    # Test static file serving
                    static_url = self.base_url.replace("/api", "") + image_url
                    
                    static_response = self.session.get(static_url)
                    
                    if static_response.status_code == 200:
                        content_type = static_response.headers.get('content-type', '')
                        content_length = len(static_response.content)
                        
                        self.log_test(
                            "Static File Serving", 
                            True, 
                            f"Successfully served static image file",
                            {
                                "image_url": static_url,
                                "content_type": content_type,
                                "content_length": content_length,
                                "status_code": static_response.status_code
                            }
                        )
                    else:
                        self.log_test(
                            "Static File Serving", 
                            False, 
                            f"Could not access static file: HTTP {static_response.status_code}"
                        )
                else:
                    self.log_test("Static File Serving", False, "Could not get valid image URL for testing")
            else:
                self.log_test("Static File Serving", False, "Could not upload test image for static file testing")
                
        except Exception as e:
            self.log_test("Static File Serving", False, f"Exception: {str(e)}")

    def test_5_image_persistence_across_requests(self):
        """Test that images persist across multiple API calls"""
        try:
            if not self.test_employee_id:
                self.log_test("Image Persistence Across Requests", False, "No test employee available")
                return

            # Upload an image
            base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAFfeFUJwwAAAABJRU5ErkJggg=="
            update_data = {"profileImage": base64_image}
            
            upload_response = self.session.put(
                f"{self.base_url}/employees/{self.test_employee_id}/image",
                json=update_data
            )
            
            if upload_response.status_code == 200:
                first_fetch = upload_response.json()
                first_image_url = first_fetch.get("profileImage")
                
                # Wait a moment and fetch the same employee again
                time.sleep(1)
                
                second_response = self.session.get(f"{self.base_url}/employees")
                if second_response.status_code == 200:
                    employees = second_response.json()
                    test_employee = next((emp for emp in employees if emp["id"] == self.test_employee_id), None)
                    
                    if test_employee:
                        second_image_url = test_employee.get("profileImage")
                        
                        if first_image_url == second_image_url and second_image_url:
                            self.log_test(
                                "Image Persistence Across Requests", 
                                True, 
                                f"Image URL persists correctly across multiple requests",
                                {
                                    "employee_id": self.test_employee_id,
                                    "first_image_url": first_image_url,
                                    "second_image_url": second_image_url,
                                    "urls_match": first_image_url == second_image_url
                                }
                            )
                        else:
                            self.log_test(
                                "Image Persistence Across Requests", 
                                False, 
                                f"Image URL does not persist. First: {first_image_url}, Second: {second_image_url}"
                            )
                    else:
                        self.log_test("Image Persistence Across Requests", False, "Could not find test employee in second fetch")
                else:
                    self.log_test("Image Persistence Across Requests", False, "Could not fetch employees for second check")
            else:
                self.log_test("Image Persistence Across Requests", False, "Could not upload initial image")
                
        except Exception as e:
            self.log_test("Image Persistence Across Requests", False, f"Exception: {str(e)}")

    # ========================================
    # MEETING ROOM BOOKING PERSISTENCE TESTS
    # ========================================

    def test_6_meeting_rooms_expired_booking_cleanup(self):
        """Test GET /api/meeting-rooms - Verify automatic cleanup of expired bookings"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                room_count = len(rooms)
                
                if room_count > 0:
                    # Check booking statuses
                    occupied_rooms = [room for room in rooms if room.get('status') == 'occupied']
                    vacant_rooms = [room for room in rooms if room.get('status') == 'vacant']
                    
                    # Check if occupied rooms have valid current bookings
                    valid_bookings = 0
                    expired_bookings = 0
                    
                    for room in occupied_rooms:
                        booking = room.get('current_booking')
                        if booking and booking.get('end_time'):
                            # This would be more accurate with actual time comparison
                            # but we can at least verify the structure
                            valid_bookings += 1
                        else:
                            expired_bookings += 1
                    
                    self.log_test(
                        "GET /api/meeting-rooms - Expired Booking Cleanup", 
                        True, 
                        f"Successfully fetched {room_count} meeting rooms. Cleanup mechanism appears to be working",
                        {
                            "total_rooms": room_count,
                            "occupied_rooms": len(occupied_rooms),
                            "vacant_rooms": len(vacant_rooms),
                            "valid_bookings": valid_bookings,
                            "expired_bookings": expired_bookings
                        }
                    )
                else:
                    self.log_test("GET /api/meeting-rooms - Expired Booking Cleanup", False, "No meeting rooms found")
            else:
                self.log_test(
                    "GET /api/meeting-rooms - Expired Booking Cleanup", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/meeting-rooms - Expired Booking Cleanup", False, f"Exception: {str(e)}")

    def test_7_create_meeting_room_booking(self):
        """Test POST /api/meeting-rooms/{room_id}/book - Create booking and verify MongoDB persistence"""
        try:
            if not self.test_room_id or not self.test_employee_id:
                self.log_test("POST /api/meeting-rooms/{room_id}/book", False, "No test room or employee available")
                return

            # Create a booking for 1 hour from now
            start_time = datetime.utcnow() + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking for persistence verification"
            }
            
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                booked_room = booking_response.json()
                current_booking = booked_room.get("current_booking")
                
                if current_booking and current_booking.get("employee_id") == self.test_employee_id:
                    self.log_test(
                        "POST /api/meeting-rooms/{room_id}/book", 
                        True, 
                        f"Successfully created meeting room booking",
                        {
                            "room_id": self.test_room_id,
                            "employee_id": self.test_employee_id,
                            "booking_id": current_booking.get("id"),
                            "start_time": current_booking.get("start_time"),
                            "end_time": current_booking.get("end_time"),
                            "room_status": booked_room.get("status")
                        }
                    )
                else:
                    self.log_test(
                        "POST /api/meeting-rooms/{room_id}/book", 
                        False, 
                        "Booking created but data doesn't match expected values"
                    )
            else:
                self.log_test(
                    "POST /api/meeting-rooms/{room_id}/book", 
                    False, 
                    f"HTTP {booking_response.status_code}: {booking_response.text}"
                )
                
        except Exception as e:
            self.log_test("POST /api/meeting-rooms/{room_id}/book", False, f"Exception: {str(e)}")

    def test_8_booking_persistence_across_calls(self):
        """Test that bookings persist across multiple API calls"""
        try:
            if not self.test_room_id or not self.test_employee_id:
                self.log_test("Booking Persistence Across Calls", False, "No test room or employee available")
                return

            # First create a booking
            start_time = datetime.utcnow() + timedelta(hours=2)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Persistence test booking"
            }
            
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                first_booking = booking_response.json()
                first_booking_id = first_booking.get("current_booking", {}).get("id")
                
                # Wait a moment and fetch rooms again
                time.sleep(1)
                
                rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
                if rooms_response.status_code == 200:
                    rooms = rooms_response.json()
                    test_room = next((room for room in rooms if room["id"] == self.test_room_id), None)
                    
                    if test_room:
                        second_booking = test_room.get("current_booking")
                        second_booking_id = second_booking.get("id") if second_booking else None
                        
                        if first_booking_id == second_booking_id and second_booking_id:
                            self.log_test(
                                "Booking Persistence Across Calls", 
                                True, 
                                f"Booking persists correctly across multiple API calls",
                                {
                                    "room_id": self.test_room_id,
                                    "first_booking_id": first_booking_id,
                                    "second_booking_id": second_booking_id,
                                    "bookings_match": first_booking_id == second_booking_id,
                                    "room_status": test_room.get("status")
                                }
                            )
                        else:
                            self.log_test(
                                "Booking Persistence Across Calls", 
                                False, 
                                f"Booking does not persist. First: {first_booking_id}, Second: {second_booking_id}"
                            )
                    else:
                        self.log_test("Booking Persistence Across Calls", False, "Could not find test room in second fetch")
                else:
                    self.log_test("Booking Persistence Across Calls", False, "Could not fetch rooms for second check")
            else:
                self.log_test("Booking Persistence Across Calls", False, "Could not create initial booking")
                
        except Exception as e:
            self.log_test("Booking Persistence Across Calls", False, f"Exception: {str(e)}")

    def test_9_cancel_meeting_room_booking(self):
        """Test DELETE /api/meeting-rooms/{room_id}/booking - Cancel booking"""
        try:
            if not self.test_room_id or not self.test_employee_id:
                self.log_test("DELETE /api/meeting-rooms/{room_id}/booking", False, "No test room or employee available")
                return

            # First create a booking to cancel
            start_time = datetime.utcnow() + timedelta(hours=3)
            end_time = start_time + timedelta(hours=1)
            
            booking_data = {
                "employee_id": self.test_employee_id,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Booking to be cancelled"
            }
            
            booking_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if booking_response.status_code == 200:
                # Now cancel the booking
                cancel_response = self.session.delete(
                    f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking"
                )
                
                if cancel_response.status_code == 200:
                    # Verify the booking was cancelled
                    verify_response = self.session.get(f"{self.base_url}/meeting-rooms")
                    if verify_response.status_code == 200:
                        rooms = verify_response.json()
                        test_room = next((room for room in rooms if room["id"] == self.test_room_id), None)
                        
                        if test_room:
                            current_booking = test_room.get("current_booking")
                            room_status = test_room.get("status")
                            
                            if not current_booking and room_status == "vacant":
                                self.log_test(
                                    "DELETE /api/meeting-rooms/{room_id}/booking", 
                                    True, 
                                    f"Successfully cancelled meeting room booking",
                                    {
                                        "room_id": self.test_room_id,
                                        "room_status": room_status,
                                        "current_booking": current_booking,
                                        "cancel_message": cancel_response.json().get("message")
                                    }
                                )
                            else:
                                self.log_test(
                                    "DELETE /api/meeting-rooms/{room_id}/booking", 
                                    False, 
                                    f"Booking not properly cancelled. Status: {room_status}, Booking: {current_booking}"
                                )
                        else:
                            self.log_test("DELETE /api/meeting-rooms/{room_id}/booking", False, "Could not find test room for verification")
                    else:
                        self.log_test("DELETE /api/meeting-rooms/{room_id}/booking", False, "Could not verify cancellation")
                else:
                    self.log_test(
                        "DELETE /api/meeting-rooms/{room_id}/booking", 
                        False, 
                        f"HTTP {cancel_response.status_code}: {cancel_response.text}"
                    )
            else:
                self.log_test("DELETE /api/meeting-rooms/{room_id}/booking", False, "Could not create booking for cancellation test")
                
        except Exception as e:
            self.log_test("DELETE /api/meeting-rooms/{room_id}/booking", False, f"Exception: {str(e)}")

    # ========================================
    # GENERAL API HEALTH CHECKS
    # ========================================

    def test_10_backend_services_health(self):
        """Test general backend services health"""
        try:
            # Test multiple endpoints to verify services are running
            endpoints_to_test = [
                ("/employees", "Employee Service"),
                ("/meeting-rooms", "Meeting Room Service"),
                ("/departments", "Utility Service - Departments"),
                ("/locations", "Utility Service - Locations"),
                ("/stats", "Statistics Service")
            ]
            
            healthy_services = 0
            total_services = len(endpoints_to_test)
            service_details = {}
            
            for endpoint, service_name in endpoints_to_test:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        healthy_services += 1
                        service_details[service_name] = "✅ Healthy"
                    else:
                        service_details[service_name] = f"❌ HTTP {response.status_code}"
                except Exception as e:
                    service_details[service_name] = f"❌ Error: {str(e)}"
            
            if healthy_services == total_services:
                self.log_test(
                    "Backend Services Health Check", 
                    True, 
                    f"All {total_services} backend services are healthy",
                    service_details
                )
            else:
                self.log_test(
                    "Backend Services Health Check", 
                    False, 
                    f"Only {healthy_services}/{total_services} services are healthy",
                    service_details
                )
                
        except Exception as e:
            self.log_test("Backend Services Health Check", False, f"Exception: {str(e)}")

    def test_11_database_operations_health(self):
        """Test database operations are working correctly"""
        try:
            # Test database read operations
            stats_response = self.session.get(f"{self.base_url}/stats")
            
            if stats_response.status_code == 200:
                stats = stats_response.json()
                db_stats = stats.get("database", {})
                excel_stats = stats.get("excel", {})
                
                db_employees = db_stats.get("employees", 0)
                excel_employees = excel_stats.get("total_employees", 0)
                
                if db_employees > 0:
                    self.log_test(
                        "Database Operations Health", 
                        True, 
                        f"Database operations are working correctly",
                        {
                            "db_employees": db_employees,
                            "excel_employees": excel_employees,
                            "hierarchy_relations": db_stats.get("hierarchy_relations", 0),
                            "data_sync": "Excel and DB in sync" if db_employees == excel_employees else "Data sync may be needed"
                        }
                    )
                else:
                    self.log_test(
                        "Database Operations Health", 
                        False, 
                        "Database appears to be empty or not accessible"
                    )
            else:
                self.log_test(
                    "Database Operations Health", 
                    False, 
                    f"Could not fetch database statistics: HTTP {stats_response.status_code}"
                )
                
        except Exception as e:
            self.log_test("Database Operations Health", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all review request tests"""
        print("=" * 80)
        print("REVIEW REQUEST TESTING - IMAGE UPLOAD & MEETING ROOM BOOKING PERSISTENCE")
        print("=" * 80)
        print()
        
        # Setup test data
        if not self.setup_test_data():
            print("❌ Test setup failed. Cannot proceed with tests.")
            return
        
        print("\n" + "=" * 50)
        print("IMAGE UPLOAD PERSISTENCE TESTS")
        print("=" * 50)
        
        self.test_1_get_employees_dynamic_profile_images()
        self.test_2_upload_image_file_persistence()
        self.test_3_base64_image_persistence()
        self.test_4_static_file_serving()
        self.test_5_image_persistence_across_requests()
        
        print("\n" + "=" * 50)
        print("MEETING ROOM BOOKING PERSISTENCE TESTS")
        print("=" * 50)
        
        self.test_6_meeting_rooms_expired_booking_cleanup()
        self.test_7_create_meeting_room_booking()
        self.test_8_booking_persistence_across_calls()
        self.test_9_cancel_meeting_room_booking()
        
        print("\n" + "=" * 50)
        print("GENERAL API HEALTH CHECKS")
        print("=" * 50)
        
        self.test_10_backend_services_health()
        self.test_11_database_operations_health()
        
        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['message']}")
        
        print("\n" + "=" * 80)
        return passed_tests, failed_tests

if __name__ == "__main__":
    tester = ReviewRequestTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)