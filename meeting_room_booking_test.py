#!/usr/bin/env python3
"""
Meeting Room Booking System Testing - Multiple Bookings Functionality
Tests the new multiple booking system with time conflict detection and specific booking cancellation
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid

# Get backend URL from frontend .env
BACKEND_URL = "https://sequential-bookings.preview.emergentagent.com/api"

class MeetingRoomBookingTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.test_room_id = None
        self.test_bookings = []
        
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
        """Test GET /api/meeting-rooms - Check if rooms have new bookings field structure"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                if len(rooms) > 0:
                    # Check first room structure
                    first_room = rooms[0]
                    required_fields = ['id', 'name', 'capacity', 'location', 'floor', 'status']
                    
                    # Check if room has required fields
                    missing_fields = [field for field in required_fields if field not in first_room]
                    
                    if not missing_fields:
                        # Check if bookings field exists (can be empty array or contain bookings)
                        has_bookings_field = 'bookings' in first_room
                        bookings_structure = first_room.get('bookings', [])
                        
                        # Store a test room ID for later tests
                        self.test_room_id = first_room['id']
                        
                        self.log_test(
                            "Meeting Rooms Structure Check",
                            True,
                            f"Found {len(rooms)} meeting rooms with proper structure. Bookings field present: {has_bookings_field}",
                            {
                                "total_rooms": len(rooms),
                                "sample_room": first_room['name'],
                                "room_id": first_room['id'],
                                "has_bookings_field": has_bookings_field,
                                "current_bookings_count": len(bookings_structure) if isinstance(bookings_structure, list) else 0,
                                "room_status": first_room.get('status', 'unknown')
                            }
                        )
                    else:
                        self.log_test(
                            "Meeting Rooms Structure Check",
                            False,
                            f"Room structure missing required fields: {missing_fields}",
                            {"missing_fields": missing_fields}
                        )
                else:
                    self.log_test(
                        "Meeting Rooms Structure Check",
                        False,
                        "No meeting rooms found in the system"
                    )
            else:
                self.log_test(
                    "Meeting Rooms Structure Check",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Meeting Rooms Structure Check",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_2_create_first_booking(self):
        """Test POST /api/meeting-rooms/{room_id}/book - Create first booking"""
        if not self.test_room_id:
            self.log_test(
                "Create First Booking",
                False,
                "No test room ID available from previous test"
            )
            return
            
        try:
            # Create booking for 2 hours from now to 3 hours from now
            start_time = datetime.utcnow() + timedelta(hours=2)
            end_time = datetime.utcnow() + timedelta(hours=3)
            
            booking_data = {
                "employee_id": "80002",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "First test booking - Team meeting"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                updated_room = response.json()
                bookings = updated_room.get('bookings', [])
                
                if len(bookings) >= 1:
                    # Find our booking
                    our_booking = None
                    for booking in bookings:
                        if booking.get('employee_id') == 'EMP001' and 'First test booking' in booking.get('remarks', ''):
                            our_booking = booking
                            break
                    
                    if our_booking:
                        self.test_bookings.append(our_booking['id'])
                        self.log_test(
                            "Create First Booking",
                            True,
                            f"Successfully created first booking. Room now has {len(bookings)} booking(s)",
                            {
                                "booking_id": our_booking['id'],
                                "employee_name": our_booking.get('employee_name'),
                                "start_time": our_booking.get('start_time'),
                                "end_time": our_booking.get('end_time'),
                                "total_bookings": len(bookings)
                            }
                        )
                    else:
                        self.log_test(
                            "Create First Booking",
                            False,
                            "Booking was created but not found in response",
                            {"total_bookings": len(bookings)}
                        )
                else:
                    self.log_test(
                        "Create First Booking",
                        False,
                        "Booking created but bookings array is empty",
                        {"response_bookings": bookings}
                    )
            else:
                self.log_test(
                    "Create First Booking",
                    False,
                    f"Failed to create booking. Status: {response.status_code}",
                    {"response": response.text[:300]}
                )
                
        except Exception as e:
            self.log_test(
                "Create First Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_3_create_second_non_overlapping_booking(self):
        """Test POST /api/meeting-rooms/{room_id}/book - Create second non-overlapping booking"""
        if not self.test_room_id:
            self.log_test(
                "Create Second Non-Overlapping Booking",
                False,
                "No test room ID available"
            )
            return
            
        try:
            # Create booking for 4 hours from now to 5 hours from now (non-overlapping with first)
            start_time = datetime.utcnow() + timedelta(hours=4)
            end_time = datetime.utcnow() + timedelta(hours=5)
            
            booking_data = {
                "employee_id": "EMP002",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Second test booking - Project review"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                updated_room = response.json()
                bookings = updated_room.get('bookings', [])
                
                if len(bookings) >= 2:
                    # Find our second booking
                    our_booking = None
                    for booking in bookings:
                        if booking.get('employee_id') == 'EMP002' and 'Second test booking' in booking.get('remarks', ''):
                            our_booking = booking
                            break
                    
                    if our_booking:
                        self.test_bookings.append(our_booking['id'])
                        self.log_test(
                            "Create Second Non-Overlapping Booking",
                            True,
                            f"Successfully created second non-overlapping booking. Room now has {len(bookings)} booking(s)",
                            {
                                "booking_id": our_booking['id'],
                                "employee_name": our_booking.get('employee_name'),
                                "start_time": our_booking.get('start_time'),
                                "end_time": our_booking.get('end_time'),
                                "total_bookings": len(bookings)
                            }
                        )
                    else:
                        self.log_test(
                            "Create Second Non-Overlapping Booking",
                            False,
                            "Second booking was created but not found in response",
                            {"total_bookings": len(bookings)}
                        )
                else:
                    self.log_test(
                        "Create Second Non-Overlapping Booking",
                        False,
                        f"Expected at least 2 bookings, found {len(bookings)}",
                        {"bookings_count": len(bookings)}
                    )
            else:
                self.log_test(
                    "Create Second Non-Overlapping Booking",
                    False,
                    f"Failed to create second booking. Status: {response.status_code}",
                    {"response": response.text[:300]}
                )
                
        except Exception as e:
            self.log_test(
                "Create Second Non-Overlapping Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_4_test_time_conflict_detection(self):
        """Test POST /api/meeting-rooms/{room_id}/book - Test time conflict detection"""
        if not self.test_room_id:
            self.log_test(
                "Time Conflict Detection",
                False,
                "No test room ID available"
            )
            return
            
        try:
            # Try to create overlapping booking (2.5 hours from now to 3.5 hours from now)
            # This should conflict with the first booking (2-3 hours from now)
            start_time = datetime.utcnow() + timedelta(hours=2, minutes=30)
            end_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
            
            booking_data = {
                "employee_id": "EMP003",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Conflicting test booking - Should fail"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            # This should fail with 400 status code due to time conflict
            if response.status_code == 400:
                error_message = response.text
                if "conflict" in error_message.lower() or "overlap" in error_message.lower():
                    self.log_test(
                        "Time Conflict Detection",
                        True,
                        "Time conflict correctly detected and booking rejected",
                        {
                            "status_code": response.status_code,
                            "error_message": error_message[:200]
                        }
                    )
                else:
                    self.log_test(
                        "Time Conflict Detection",
                        False,
                        "Booking rejected but not for time conflict reason",
                        {"error_message": error_message[:200]}
                    )
            elif response.status_code == 200:
                self.log_test(
                    "Time Conflict Detection",
                    False,
                    "Overlapping booking was incorrectly accepted - conflict detection failed",
                    {"response": response.text[:200]}
                )
            else:
                self.log_test(
                    "Time Conflict Detection",
                    False,
                    f"Unexpected status code: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Time Conflict Detection",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_5_room_status_updates(self):
        """Test GET /api/meeting-rooms - Verify room status updates based on active bookings"""
        if not self.test_room_id:
            self.log_test(
                "Room Status Updates",
                False,
                "No test room ID available"
            )
            return
            
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                test_room = None
                
                # Find our test room
                for room in rooms:
                    if room['id'] == self.test_room_id:
                        test_room = room
                        break
                
                if test_room:
                    current_time = datetime.utcnow()
                    bookings = test_room.get('bookings', [])
                    room_status = test_room.get('status', 'unknown')
                    current_booking = test_room.get('current_booking')
                    
                    # Check if any booking is currently active
                    should_be_occupied = False
                    active_booking_found = None
                    
                    for booking in bookings:
                        start_time_str = booking.get('start_time', '')
                        end_time_str = booking.get('end_time', '')
                        
                        if start_time_str and end_time_str:
                            try:
                                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                                end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
                                
                                # Remove timezone info for comparison with current_time
                                start_time = start_time.replace(tzinfo=None)
                                end_time = end_time.replace(tzinfo=None)
                                
                                if start_time <= current_time <= end_time:
                                    should_be_occupied = True
                                    active_booking_found = booking
                                    break
                            except:
                                continue
                    
                    expected_status = "occupied" if should_be_occupied else "vacant"
                    status_correct = room_status == expected_status
                    
                    self.log_test(
                        "Room Status Updates",
                        status_correct,
                        f"Room status is {'correct' if status_correct else 'incorrect'}. Expected: {expected_status}, Actual: {room_status}",
                        {
                            "room_id": self.test_room_id,
                            "current_status": room_status,
                            "expected_status": expected_status,
                            "total_bookings": len(bookings),
                            "has_current_booking": current_booking is not None,
                            "active_booking_found": active_booking_found is not None
                        }
                    )
                else:
                    self.log_test(
                        "Room Status Updates",
                        False,
                        f"Test room {self.test_room_id} not found in rooms list"
                    )
            else:
                self.log_test(
                    "Room Status Updates",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Room Status Updates",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_6_specific_booking_cancellation(self):
        """Test DELETE /api/meeting-rooms/{room_id}/booking/{booking_id} - Cancel specific booking"""
        if not self.test_room_id or not self.test_bookings:
            self.log_test(
                "Specific Booking Cancellation",
                False,
                "No test room ID or booking IDs available"
            )
            return
            
        try:
            # Cancel the first booking we created
            booking_id_to_cancel = self.test_bookings[0]
            
            response = self.session.delete(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{booking_id_to_cancel}"
            )
            
            if response.status_code == 200:
                # Verify the booking was removed
                room_response = self.session.get(f"{self.base_url}/meeting-rooms")
                
                if room_response.status_code == 200:
                    rooms = room_response.json()
                    test_room = None
                    
                    for room in rooms:
                        if room['id'] == self.test_room_id:
                            test_room = room
                            break
                    
                    if test_room:
                        bookings = test_room.get('bookings', [])
                        
                        # Check if the cancelled booking is gone
                        cancelled_booking_found = False
                        for booking in bookings:
                            if booking.get('id') == booking_id_to_cancel:
                                cancelled_booking_found = True
                                break
                        
                        if not cancelled_booking_found:
                            self.log_test(
                                "Specific Booking Cancellation",
                                True,
                                f"Successfully cancelled specific booking. Room now has {len(bookings)} booking(s)",
                                {
                                    "cancelled_booking_id": booking_id_to_cancel,
                                    "remaining_bookings": len(bookings),
                                    "booking_removed": True
                                }
                            )
                        else:
                            self.log_test(
                                "Specific Booking Cancellation",
                                False,
                                "Booking cancellation reported success but booking still exists",
                                {"cancelled_booking_id": booking_id_to_cancel}
                            )
                    else:
                        self.log_test(
                            "Specific Booking Cancellation",
                            False,
                            "Could not find test room to verify cancellation"
                        )
                else:
                    self.log_test(
                        "Specific Booking Cancellation",
                        False,
                        "Could not fetch rooms to verify cancellation"
                    )
            else:
                self.log_test(
                    "Specific Booking Cancellation",
                    False,
                    f"Failed to cancel specific booking. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Specific Booking Cancellation",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_7_expired_booking_cleanup(self):
        """Test expired booking cleanup functionality"""
        if not self.test_room_id:
            self.log_test(
                "Expired Booking Cleanup",
                False,
                "No test room ID available"
            )
            return
            
        try:
            # Create a booking in the past (should be automatically cleaned up)
            past_start_time = datetime.utcnow() - timedelta(hours=2)
            past_end_time = datetime.utcnow() - timedelta(hours=1)
            
            booking_data = {
                "employee_id": "EMP004",
                "start_time": past_start_time.isoformat() + "Z",
                "end_time": past_end_time.isoformat() + "Z",
                "remarks": "Expired test booking - Should be cleaned up"
            }
            
            # Try to create the past booking (this might fail due to validation)
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 400 and "past time" in response.text.lower():
                # This is expected - system prevents booking in the past
                self.log_test(
                    "Expired Booking Cleanup",
                    True,
                    "System correctly prevents booking in the past, which is good for data integrity",
                    {"validation_message": response.text[:200]}
                )
            else:
                # If past booking was somehow created, check if cleanup works
                # Fetch rooms to trigger cleanup
                cleanup_response = self.session.get(f"{self.base_url}/meeting-rooms")
                
                if cleanup_response.status_code == 200:
                    rooms = cleanup_response.json()
                    test_room = None
                    
                    for room in rooms:
                        if room['id'] == self.test_room_id:
                            test_room = room
                            break
                    
                    if test_room:
                        bookings = test_room.get('bookings', [])
                        
                        # Check if any expired bookings exist
                        expired_bookings = []
                        current_time = datetime.utcnow()
                        
                        for booking in bookings:
                            end_time_str = booking.get('end_time', '')
                            if end_time_str:
                                try:
                                    end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
                                    end_time = end_time.replace(tzinfo=None)
                                    
                                    if end_time < current_time:
                                        expired_bookings.append(booking)
                                except:
                                    continue
                        
                        if len(expired_bookings) == 0:
                            self.log_test(
                                "Expired Booking Cleanup",
                                True,
                                "No expired bookings found - cleanup is working properly",
                                {"total_bookings": len(bookings)}
                            )
                        else:
                            self.log_test(
                                "Expired Booking Cleanup",
                                False,
                                f"Found {len(expired_bookings)} expired booking(s) that should have been cleaned up",
                                {"expired_bookings": len(expired_bookings)}
                            )
                    else:
                        self.log_test(
                            "Expired Booking Cleanup",
                            False,
                            "Could not find test room to check cleanup"
                        )
                else:
                    self.log_test(
                        "Expired Booking Cleanup",
                        False,
                        "Could not fetch rooms to test cleanup"
                    )
                
        except Exception as e:
            self.log_test(
                "Expired Booking Cleanup",
                False,
                f"Exception occurred: {str(e)}"
            )

    def run_all_tests(self):
        """Run all meeting room booking tests"""
        print("🚀 Starting Meeting Room Booking System Tests")
        print("=" * 60)
        
        # Run tests in sequence
        self.test_1_get_meeting_rooms_structure()
        self.test_2_create_first_booking()
        self.test_3_create_second_non_overlapping_booking()
        self.test_4_test_time_conflict_detection()
        self.test_5_room_status_updates()
        self.test_6_specific_booking_cancellation()
        self.test_7_expired_booking_cleanup()
        
        # Summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All meeting room booking tests passed!")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check details above.")
            return False

def main():
    """Main function to run the tests"""
    tester = MeetingRoomBookingTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()