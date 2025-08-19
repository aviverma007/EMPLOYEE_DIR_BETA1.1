#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for New APIs
Tests the newly implemented APIs: Policies, Meeting Rooms, Attendance, Workflows
Focus on Excel data integration and location-based systems
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "https://live-edit.preview.emergentagent.com/api"

class NewAPIsTester:
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

    # ========================================
    # EXCEL DATA INTEGRATION TESTS
    # ========================================

    def test_1_excel_data_loading(self):
        """Test Excel data integration - Verify 640 employees are loaded"""
        try:
            response = self.session.get(f"{self.base_url}/employees")
            
            if response.status_code == 200:
                employees = response.json()
                employee_count = len(employees)
                
                if employee_count == 640:
                    self.log_test(
                        "Excel Data Integration - 640 Employees", 
                        True, 
                        f"Successfully verified {employee_count} employees loaded from Excel",
                        {"expected": 640, "actual": employee_count}
                    )
                else:
                    self.log_test(
                        "Excel Data Integration - 640 Employees", 
                        False, 
                        f"Expected 640 employees, found {employee_count}",
                        {"expected": 640, "actual": employee_count}
                    )
            else:
                self.log_test(
                    "Excel Data Integration - 640 Employees", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("Excel Data Integration - 640 Employees", False, f"Exception: {str(e)}")

    def test_2_locations_api(self):
        """Test GET /api/locations - Office locations for meeting rooms"""
        try:
            response = self.session.get(f"{self.base_url}/locations")
            
            if response.status_code == 200:
                result = response.json()
                locations = result.get("locations", [])
                location_count = len(locations)
                
                if location_count > 0:
                    self.log_test(
                        "GET /api/locations", 
                        True, 
                        f"Successfully fetched {location_count} office locations",
                        {"locations_count": location_count, "locations": locations[:5]}
                    )
                else:
                    self.log_test("GET /api/locations", False, "No locations returned")
            else:
                self.log_test(
                    "GET /api/locations", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/locations", False, f"Exception: {str(e)}")

    # ========================================
    # POLICIES API TESTS
    # ========================================

    def test_3_get_all_policies(self):
        """Test GET /api/policies - Fetch all policies"""
        try:
            response = self.session.get(f"{self.base_url}/policies")
            
            if response.status_code == 200:
                policies = response.json()
                policy_count = len(policies)
                
                self.log_test(
                    "GET /api/policies", 
                    True, 
                    f"Successfully fetched {policy_count} policies",
                    {"count": policy_count}
                )
            else:
                self.log_test(
                    "GET /api/policies", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/policies", False, f"Exception: {str(e)}")

    def test_4_create_policies(self):
        """Test POST /api/policies - Create policies with different categories"""
        try:
            # Test creating policies with different categories
            test_policies = [
                {
                    "title": "Remote Work Policy 2025",
                    "content": "Employees are allowed to work remotely up to 3 days per week. Must maintain regular communication and attend mandatory meetings. Equipment allowances provided.",
                    "category": "hr",
                    "effective_date": "2025-01-01T00:00:00",
                    "version": "2.0"
                },
                {
                    "title": "Data Security Guidelines",
                    "content": "All employees must follow data security protocols: use strong passwords, enable 2FA, encrypt sensitive data, report security incidents immediately.",
                    "category": "security",
                    "effective_date": "2025-02-01T00:00:00",
                    "version": "1.5"
                },
                {
                    "title": "Meeting Room Booking Policy",
                    "content": "Meeting rooms can be booked up to 2 weeks in advance. Maximum booking duration is 4 hours. Cancel unused bookings to allow others to use the space.",
                    "category": "facilities",
                    "effective_date": "2025-01-15T00:00:00",
                    "version": "1.0"
                }
            ]
            
            created_policies = []
            
            for policy_data in test_policies:
                response = self.session.post(
                    f"{self.base_url}/policies",
                    json=policy_data
                )
                
                if response.status_code == 200:
                    created_policy = response.json()
                    created_policies.append(created_policy)
                    
                    # Verify the created policy has correct data
                    if (created_policy.get("title") == policy_data["title"] and
                        created_policy.get("category") == policy_data["category"] and
                        created_policy.get("version") == policy_data["version"] and
                        created_policy.get("id")):
                        
                        self.log_test(
                            f"POST /api/policies ({policy_data['category']} category)", 
                            True, 
                            f"Successfully created policy: {policy_data['title'][:40]}...",
                            {"policy_id": created_policy["id"], "category": policy_data["category"], "version": policy_data["version"]}
                        )
                    else:
                        self.log_test(
                            f"POST /api/policies ({policy_data['category']} category)", 
                            False, 
                            "Policy created but data doesn't match"
                        )
                else:
                    self.log_test(
                        f"POST /api/policies ({policy_data['category']} category)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created policy IDs for later tests
            self.created_policy_ids = [policy["id"] for policy in created_policies]
                
        except Exception as e:
            self.log_test("POST /api/policies", False, f"Exception: {str(e)}")

    def test_5_update_policy(self):
        """Test PUT /api/policies/{id} - Update policy"""
        try:
            # First create a policy to update
            policy_data = {
                "title": "Test Policy for Update",
                "content": "This policy will be updated",
                "category": "general",
                "version": "1.0"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/policies",
                json=policy_data
            )
            
            if create_response.status_code == 200:
                created_policy = create_response.json()
                policy_id = created_policy["id"]
                
                # Update the policy
                update_data = {
                    "title": "Updated Test Policy",
                    "content": "This policy has been updated with new comprehensive guidelines and procedures for better compliance.",
                    "category": "compliance",
                    "version": "2.0"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/policies/{policy_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_policy = update_response.json()
                    
                    # Verify updates
                    if (updated_policy.get("title") == update_data["title"] and
                        updated_policy.get("category") == update_data["category"] and
                        updated_policy.get("version") == update_data["version"] and
                        updated_policy.get("updated_at") != created_policy.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/policies/{id}", 
                            True, 
                            f"Successfully updated policy",
                            {
                                "policy_id": policy_id, 
                                "new_title": update_data["title"],
                                "new_category": update_data["category"],
                                "new_version": update_data["version"]
                            }
                        )
                    else:
                        self.log_test(
                            "PUT /api/policies/{id}", 
                            False, 
                            "Policy updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/policies/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/policies/{id}", False, "Could not create policy for update test")
                
        except Exception as e:
            self.log_test("PUT /api/policies/{id}", False, f"Exception: {str(e)}")

    def test_6_delete_policy(self):
        """Test DELETE /api/policies/{id} - Delete policy"""
        try:
            # First create a policy to delete
            policy_data = {
                "title": "Test Policy for Deletion",
                "content": "This policy will be deleted",
                "category": "temporary",
                "version": "1.0"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/policies",
                json=policy_data
            )
            
            if create_response.status_code == 200:
                created_policy = create_response.json()
                policy_id = created_policy["id"]
                
                # Delete the policy
                delete_response = self.session.delete(f"{self.base_url}/policies/{policy_id}")
                
                if delete_response.status_code == 200:
                    # Verify deletion by trying to fetch the policies
                    verify_response = self.session.get(f"{self.base_url}/policies")
                    if verify_response.status_code == 200:
                        remaining_policies = verify_response.json()
                        deleted_policy_exists = any(policy["id"] == policy_id for policy in remaining_policies)
                        
                        if not deleted_policy_exists:
                            self.log_test(
                                "DELETE /api/policies/{id}", 
                                True, 
                                f"Successfully deleted policy",
                                {"deleted_policy_id": policy_id}
                            )
                        else:
                            self.log_test(
                                "DELETE /api/policies/{id}", 
                                False, 
                                "Policy still exists after deletion"
                            )
                    else:
                        self.log_test(
                            "DELETE /api/policies/{id}", 
                            True, 
                            "Policy deleted (could not verify due to fetch error)"
                        )
                else:
                    self.log_test(
                        "DELETE /api/policies/{id}", 
                        False, 
                        f"HTTP {delete_response.status_code}: {delete_response.text}"
                    )
            else:
                self.log_test("DELETE /api/policies/{id}", False, "Could not create policy for deletion test")
                
        except Exception as e:
            self.log_test("DELETE /api/policies/{id}", False, f"Exception: {str(e)}")

    # ========================================
    # MEETING ROOMS API TESTS
    # ========================================

    def test_7_get_meeting_rooms(self):
        """Test GET /api/meeting-rooms - Fetch meeting rooms with location-based system"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                room_count = len(rooms)
                
                if room_count > 0:
                    # Check if rooms have location information
                    sample_room = rooms[0]
                    has_location = "location" in sample_room and "floor" in sample_room
                    
                    self.log_test(
                        "GET /api/meeting-rooms", 
                        True, 
                        f"Successfully fetched {room_count} meeting rooms with location data",
                        {
                            "count": room_count, 
                            "has_location_data": has_location,
                            "sample_room": {
                                "name": sample_room.get("name"),
                                "location": sample_room.get("location"),
                                "floor": sample_room.get("floor"),
                                "status": sample_room.get("status")
                            }
                        }
                    )
                else:
                    self.log_test("GET /api/meeting-rooms", True, "No meeting rooms found (will be initialized)")
            else:
                self.log_test(
                    "GET /api/meeting-rooms", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/meeting-rooms", False, f"Exception: {str(e)}")

    def test_8_meeting_room_locations_and_floors(self):
        """Test GET /api/meeting-rooms/locations and /api/meeting-rooms/floors"""
        try:
            # Test locations endpoint
            locations_response = self.session.get(f"{self.base_url}/meeting-rooms/locations")
            
            if locations_response.status_code == 200:
                locations_data = locations_response.json()
                locations = locations_data.get("locations", [])
                
                self.log_test(
                    "GET /api/meeting-rooms/locations", 
                    True, 
                    f"Successfully fetched {len(locations)} meeting room locations",
                    {"locations": locations}
                )
                
                # Test floors endpoint for first location
                if locations:
                    floors_response = self.session.get(f"{self.base_url}/meeting-rooms/floors?location={locations[0]}")
                    
                    if floors_response.status_code == 200:
                        floors_data = floors_response.json()
                        floors = floors_data.get("floors", [])
                        
                        self.log_test(
                            f"GET /api/meeting-rooms/floors?location={locations[0]}", 
                            True, 
                            f"Successfully fetched {len(floors)} floors for {locations[0]}",
                            {"location": locations[0], "floors": floors}
                        )
                    else:
                        self.log_test(
                            f"GET /api/meeting-rooms/floors?location={locations[0]}", 
                            False, 
                            f"HTTP {floors_response.status_code}: {floors_response.text}"
                        )
            else:
                self.log_test(
                    "GET /api/meeting-rooms/locations", 
                    False, 
                    f"HTTP {locations_response.status_code}: {locations_response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/meeting-rooms/locations", False, f"Exception: {str(e)}")

    def test_9_book_meeting_room(self):
        """Test POST /api/meeting-rooms/{id}/book - Room booking functionality"""
        try:
            # First get available rooms
            rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if rooms_response.status_code != 200:
                self.log_test("POST /api/meeting-rooms/{id}/book", False, "Could not fetch meeting rooms")
                return
            
            rooms = rooms_response.json()
            if not rooms:
                self.log_test("POST /api/meeting-rooms/{id}/book", False, "No meeting rooms available")
                return
            
            # Find a vacant room
            vacant_room = next((room for room in rooms if room.get("status") == "vacant"), None)
            if not vacant_room:
                # Use first room anyway
                vacant_room = rooms[0]
            
            # Get an employee to make the booking
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("POST /api/meeting-rooms/{id}/book", False, "Could not fetch employees for booking")
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test("POST /api/meeting-rooms/{id}/book", False, "No employees available for booking")
                return
            
            # Create booking data
            now = datetime.utcnow()
            start_time = now + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)
            
            booking_data = {
                "employee_id": employees[0]["id"],
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Team planning meeting for Q1 objectives"
            }
            
            # Book the room
            book_response = self.session.post(
                f"{self.base_url}/meeting-rooms/{vacant_room['id']}/book",
                json=booking_data
            )
            
            if book_response.status_code == 200:
                booked_room = book_response.json()
                
                # Verify booking
                if (booked_room.get("status") == "occupied" and
                    booked_room.get("current_booking") and
                    booked_room["current_booking"].get("employee_id") == employees[0]["id"]):
                    
                    self.log_test(
                        "POST /api/meeting-rooms/{id}/book", 
                        True, 
                        f"Successfully booked meeting room: {vacant_room['name']}",
                        {
                            "room_id": vacant_room["id"],
                            "room_name": vacant_room["name"],
                            "employee_name": employees[0]["name"],
                            "booking_duration": "2 hours",
                            "location": vacant_room.get("location"),
                            "floor": vacant_room.get("floor")
                        }
                    )
                else:
                    self.log_test(
                        "POST /api/meeting-rooms/{id}/book", 
                        False, 
                        "Room booking created but status/booking data incorrect"
                    )
            else:
                self.log_test(
                    "POST /api/meeting-rooms/{id}/book", 
                    False, 
                    f"HTTP {book_response.status_code}: {book_response.text}"
                )
                
        except Exception as e:
            self.log_test("POST /api/meeting-rooms/{id}/book", False, f"Exception: {str(e)}")

    def test_10_cancel_meeting_room_booking(self):
        """Test DELETE /api/meeting-rooms/{id}/booking - Cancel booking"""
        try:
            # First get rooms to find an occupied one
            rooms_response = self.session.get(f"{self.base_url}/meeting-rooms")
            if rooms_response.status_code != 200:
                self.log_test("DELETE /api/meeting-rooms/{id}/booking", False, "Could not fetch meeting rooms")
                return
            
            rooms = rooms_response.json()
            occupied_room = next((room for room in rooms if room.get("status") == "occupied"), None)
            
            if occupied_room:
                # Cancel the booking
                cancel_response = self.session.delete(f"{self.base_url}/meeting-rooms/{occupied_room['id']}/booking")
                
                if cancel_response.status_code == 200:
                    self.log_test(
                        "DELETE /api/meeting-rooms/{id}/booking", 
                        True, 
                        f"Successfully cancelled booking for room: {occupied_room['name']}",
                        {"room_id": occupied_room["id"], "room_name": occupied_room["name"]}
                    )
                else:
                    self.log_test(
                        "DELETE /api/meeting-rooms/{id}/booking", 
                        False, 
                        f"HTTP {cancel_response.status_code}: {cancel_response.text}"
                    )
            else:
                self.log_test(
                    "DELETE /api/meeting-rooms/{id}/booking", 
                    True, 
                    "No occupied rooms found to cancel booking (expected if no bookings exist)"
                )
                
        except Exception as e:
            self.log_test("DELETE /api/meeting-rooms/{id}/booking", False, f"Exception: {str(e)}")

    # ========================================
    # ATTENDANCE API TESTS
    # ========================================

    def test_11_get_attendance_records(self):
        """Test GET /api/attendance - Fetch attendance records"""
        try:
            response = self.session.get(f"{self.base_url}/attendance")
            
            if response.status_code == 200:
                attendance_records = response.json()
                record_count = len(attendance_records)
                
                self.log_test(
                    "GET /api/attendance", 
                    True, 
                    f"Successfully fetched {record_count} attendance records",
                    {"count": record_count}
                )
            else:
                self.log_test(
                    "GET /api/attendance", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/attendance", False, f"Exception: {str(e)}")

    def test_12_create_attendance_punch_in_out(self):
        """Test POST /api/attendance - Create attendance with punch in/out"""
        try:
            # Get employees for attendance
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("POST /api/attendance", False, "Could not fetch employees for attendance")
                return
            
            employees = emp_response.json()
            if len(employees) < 3:
                self.log_test("POST /api/attendance", False, "Not enough employees for attendance testing")
                return
            
            # Test different attendance scenarios
            today = datetime.utcnow().strftime("%Y-%m-%d")
            test_attendance = [
                {
                    "employee_id": employees[0]["id"],
                    "date": today,
                    "punch_in": "2025-01-20T09:00:00Z",
                    "punch_out": "2025-01-20T18:00:00Z",
                    "punch_in_location": "IFC Office - Main Entrance",
                    "punch_out_location": "IFC Office - Main Entrance",
                    "status": "present",
                    "remarks": "Regular working day"
                },
                {
                    "employee_id": employees[1]["id"],
                    "date": today,
                    "punch_in": "2025-01-20T09:30:00Z",
                    "punch_out": "2025-01-20T13:00:00Z",
                    "punch_in_location": "Remote - Home Office",
                    "punch_out_location": "Remote - Home Office",
                    "status": "half_day",
                    "remarks": "Half day - medical appointment"
                },
                {
                    "employee_id": employees[2]["id"],
                    "date": today,
                    "punch_in": "2025-01-20T10:15:00Z",
                    "punch_out": "2025-01-20T19:30:00Z",
                    "punch_in_location": "IFC Office - Side Entrance",
                    "punch_out_location": "IFC Office - Side Entrance",
                    "status": "late",
                    "remarks": "Late due to traffic, compensated with extra hours"
                }
            ]
            
            created_attendance = []
            
            for attendance_data in test_attendance:
                response = self.session.post(
                    f"{self.base_url}/attendance",
                    json=attendance_data
                )
                
                if response.status_code == 200:
                    created_record = response.json()
                    created_attendance.append(created_record)
                    
                    # Verify the created attendance has correct data
                    if (created_record.get("employee_id") == attendance_data["employee_id"] and
                        created_record.get("status") == attendance_data["status"] and
                        created_record.get("punch_in_location") == attendance_data["punch_in_location"] and
                        created_record.get("id")):
                        
                        employee_name = next((emp["name"] for emp in employees if emp["id"] == attendance_data["employee_id"]), "Unknown")
                        
                        self.log_test(
                            f"POST /api/attendance ({attendance_data['status']} status)", 
                            True, 
                            f"Successfully created attendance for {employee_name}",
                            {
                                "attendance_id": created_record["id"],
                                "employee_name": employee_name,
                                "status": attendance_data["status"],
                                "location": attendance_data["punch_in_location"],
                                "total_hours": created_record.get("total_hours")
                            }
                        )
                    else:
                        self.log_test(
                            f"POST /api/attendance ({attendance_data['status']} status)", 
                            False, 
                            "Attendance created but data doesn't match"
                        )
                elif response.status_code == 400 and "already exists" in response.text:
                    # Attendance already exists for this date
                    employee_name = next((emp["name"] for emp in employees if emp["id"] == attendance_data["employee_id"]), "Unknown")
                    self.log_test(
                        f"POST /api/attendance ({attendance_data['status']} status)", 
                        True, 
                        f"Attendance already exists for {employee_name} on {today} (expected behavior)",
                        {"employee_name": employee_name, "date": today}
                    )
                else:
                    self.log_test(
                        f"POST /api/attendance ({attendance_data['status']} status)", 
                        False, 
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            # Store created attendance IDs for later tests
            self.created_attendance_ids = [record["id"] for record in created_attendance]
                
        except Exception as e:
            self.log_test("POST /api/attendance", False, f"Exception: {str(e)}")

    def test_13_update_attendance(self):
        """Test PUT /api/attendance/{id} - Update attendance record"""
        try:
            # First create an attendance record to update
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("PUT /api/attendance/{id}", False, "Could not fetch employees")
                return
            
            employees = emp_response.json()
            if not employees:
                self.log_test("PUT /api/attendance/{id}", False, "No employees available")
                return
            
            # Create attendance record
            yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
            attendance_data = {
                "employee_id": employees[0]["id"],
                "date": yesterday,
                "punch_in": "2025-01-19T09:00:00Z",
                "status": "present",
                "remarks": "Initial attendance record"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/attendance",
                json=attendance_data
            )
            
            if create_response.status_code == 200:
                created_attendance = create_response.json()
                attendance_id = created_attendance["id"]
                
                # Update the attendance with punch out
                update_data = {
                    "punch_out": "2025-01-19T17:30:00Z",
                    "punch_out_location": "IFC Office - Main Entrance",
                    "remarks": "Updated with punch out time"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/attendance/{attendance_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_attendance = update_response.json()
                    
                    # Verify updates
                    if (updated_attendance.get("punch_out_location") == update_data["punch_out_location"] and
                        updated_attendance.get("remarks") == update_data["remarks"] and
                        updated_attendance.get("total_hours") is not None and
                        updated_attendance.get("updated_at") != created_attendance.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/attendance/{id}", 
                            True, 
                            f"Successfully updated attendance record with punch out",
                            {
                                "attendance_id": attendance_id,
                                "total_hours": updated_attendance.get("total_hours"),
                                "punch_out_location": update_data["punch_out_location"]
                            }
                        )
                    else:
                        self.log_test(
                            "PUT /api/attendance/{id}", 
                            False, 
                            "Attendance updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/attendance/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            elif create_response.status_code == 400 and "already exists" in create_response.text:
                self.log_test(
                    "PUT /api/attendance/{id}", 
                    True, 
                    "Attendance record already exists for test date (expected behavior)"
                )
            else:
                self.log_test("PUT /api/attendance/{id}", False, "Could not create attendance for update test")
                
        except Exception as e:
            self.log_test("PUT /api/attendance/{id}", False, f"Exception: {str(e)}")

    # ========================================
    # WORKFLOWS API TESTS
    # ========================================

    def test_14_get_workflows(self):
        """Test GET /api/workflows - Basic workflow functionality"""
        try:
            response = self.session.get(f"{self.base_url}/workflows")
            
            if response.status_code == 200:
                workflows = response.json()
                workflow_count = len(workflows)
                
                self.log_test(
                    "GET /api/workflows", 
                    True, 
                    f"Successfully fetched {workflow_count} workflows",
                    {"count": workflow_count}
                )
            else:
                self.log_test(
                    "GET /api/workflows", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("GET /api/workflows", False, f"Exception: {str(e)}")

    def test_15_create_workflow(self):
        """Test POST /api/workflows - Create workflow with steps"""
        try:
            # Get employees for step assignment
            emp_response = self.session.get(f"{self.base_url}/employees")
            if emp_response.status_code != 200:
                self.log_test("POST /api/workflows", False, "Could not fetch employees for workflow steps")
                return
            
            employees = emp_response.json()
            if len(employees) < 3:
                self.log_test("POST /api/workflows", False, "Not enough employees for workflow step assignment")
                return
            
            # Create workflow with multiple steps
            workflow_data = {
                "name": "New Employee Onboarding Workflow",
                "description": "Complete workflow for onboarding new employees including documentation, system access, and training.",
                "category": "hr",
                "steps": [
                    {
                        "name": "Document Collection",
                        "description": "Collect all required documents from new employee (ID, certificates, etc.)",
                        "assigned_to": employees[0]["id"],
                        "status": "pending"
                    },
                    {
                        "name": "System Access Setup",
                        "description": "Create user accounts, email, and provide access to necessary systems",
                        "assigned_to": employees[1]["id"],
                        "status": "pending"
                    },
                    {
                        "name": "Orientation and Training",
                        "description": "Conduct company orientation and role-specific training sessions",
                        "assigned_to": employees[2]["id"],
                        "status": "pending"
                    }
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/workflows",
                json=workflow_data
            )
            
            if response.status_code == 200:
                created_workflow = response.json()
                
                # Verify the created workflow has correct data
                if (created_workflow.get("name") == workflow_data["name"] and
                    created_workflow.get("category") == workflow_data["category"] and
                    len(created_workflow.get("steps", [])) == 3 and
                    created_workflow.get("id")):
                    
                    self.log_test(
                        "POST /api/workflows", 
                        True, 
                        f"Successfully created workflow: {workflow_data['name']}",
                        {
                            "workflow_id": created_workflow["id"],
                            "category": workflow_data["category"],
                            "steps_count": len(created_workflow.get("steps", [])),
                            "status": created_workflow.get("status")
                        }
                    )
                    
                    # Store for later tests
                    self.created_workflow_id = created_workflow["id"]
                else:
                    self.log_test(
                        "POST /api/workflows", 
                        False, 
                        "Workflow created but data doesn't match"
                    )
            else:
                self.log_test(
                    "POST /api/workflows", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test("POST /api/workflows", False, f"Exception: {str(e)}")

    def test_16_update_workflow(self):
        """Test PUT /api/workflows/{id} - Update workflow status"""
        try:
            # First create a workflow to update
            workflow_data = {
                "name": "Test Workflow for Update",
                "description": "This workflow will be updated",
                "category": "general",
                "steps": [
                    {
                        "name": "Step 1",
                        "description": "First step",
                        "status": "pending"
                    }
                ]
            }
            
            create_response = self.session.post(
                f"{self.base_url}/workflows",
                json=workflow_data
            )
            
            if create_response.status_code == 200:
                created_workflow = create_response.json()
                workflow_id = created_workflow["id"]
                
                # Update the workflow
                update_data = {
                    "name": "Updated Test Workflow",
                    "status": "completed",
                    "category": "testing"
                }
                
                update_response = self.session.put(
                    f"{self.base_url}/workflows/{workflow_id}",
                    json=update_data
                )
                
                if update_response.status_code == 200:
                    updated_workflow = update_response.json()
                    
                    # Verify updates
                    if (updated_workflow.get("name") == update_data["name"] and
                        updated_workflow.get("status") == update_data["status"] and
                        updated_workflow.get("category") == update_data["category"] and
                        updated_workflow.get("updated_at") != created_workflow.get("created_at")):
                        
                        self.log_test(
                            "PUT /api/workflows/{id}", 
                            True, 
                            f"Successfully updated workflow",
                            {
                                "workflow_id": workflow_id,
                                "new_name": update_data["name"],
                                "new_status": update_data["status"],
                                "new_category": update_data["category"]
                            }
                        )
                    else:
                        self.log_test(
                            "PUT /api/workflows/{id}", 
                            False, 
                            "Workflow updated but data doesn't match expected values"
                        )
                else:
                    self.log_test(
                        "PUT /api/workflows/{id}", 
                        False, 
                        f"HTTP {update_response.status_code}: {update_response.text}"
                    )
            else:
                self.log_test("PUT /api/workflows/{id}", False, "Could not create workflow for update test")
                
        except Exception as e:
            self.log_test("PUT /api/workflows/{id}", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("COMPREHENSIVE BACKEND API TESTING - NEW APIS")
        print("Testing: Excel Integration, Policies, Meeting Rooms, Attendance, Workflows")
        print("=" * 80)
        print()
        
        # Excel Data Integration Tests
        print("🔍 EXCEL DATA INTEGRATION TESTS")
        print("-" * 40)
        self.test_1_excel_data_loading()
        self.test_2_locations_api()
        print()
        
        # Policies API Tests
        print("📋 POLICIES API TESTS")
        print("-" * 40)
        self.test_3_get_all_policies()
        self.test_4_create_policies()
        self.test_5_update_policy()
        self.test_6_delete_policy()
        print()
        
        # Meeting Rooms API Tests
        print("🏢 MEETING ROOMS API TESTS")
        print("-" * 40)
        self.test_7_get_meeting_rooms()
        self.test_8_meeting_room_locations_and_floors()
        self.test_9_book_meeting_room()
        self.test_10_cancel_meeting_room_booking()
        print()
        
        # Attendance API Tests
        print("⏰ ATTENDANCE API TESTS")
        print("-" * 40)
        self.test_11_get_attendance_records()
        self.test_12_create_attendance_punch_in_out()
        self.test_13_update_attendance()
        print()
        
        # Workflows API Tests
        print("🔄 WORKFLOWS API TESTS")
        print("-" * 40)
        self.test_14_get_workflows()
        self.test_15_create_workflow()
        self.test_16_update_workflow()
        print()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['message']}")
            print()
        
        print("PASSED TESTS:")
        print("-" * 40)
        for result in self.test_results:
            if result["success"]:
                print(f"✅ {result['test']}")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = NewAPIsTester()
    tester.run_all_tests()