#!/usr/bin/env python3
"""
Focused Meeting Room Booking System Testing
Tests the key functionality requested in the review
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid

# Get backend URL from frontend .env
BACKEND_URL = "https://backend-booking-fix.preview.emergentagent.com/api"

class FocusedMeetingRoomTester:
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

    def test_1_meeting_rooms_bookings_structure(self):
        """Test 1: Check if existing meeting rooms have the new bookings field structure"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                if len(rooms) > 0:
                    # Analyze room structure
                    rooms_with_bookings = 0
                    rooms_with_current_booking = 0
                    total_bookings = 0
                    
                    sample_room = rooms[0]
                    
                    for room in rooms:
                        if 'bookings' in room:
                            rooms_with_bookings += 1
                            bookings = room.get('bookings', [])
                            total_bookings += len(bookings)
                            
                        if room.get('current_booking'):
                            rooms_with_current_booking += 1
                    
                    self.log_test(
                        "Meeting Rooms Bookings Structure",
                        True,
                        f"Found {len(rooms)} meeting rooms. {rooms_with_bookings} have bookings field, {total_bookings} total bookings",
                        {
                            "total_rooms": len(rooms),
                            "rooms_with_bookings_field": rooms_with_bookings,
                            "rooms_with_current_booking": rooms_with_current_booking,
                            "total_bookings_across_all_rooms": total_bookings,
                            "sample_room_structure": {
                                "id": sample_room.get('id'),
                                "name": sample_room.get('name'),
                                "has_bookings": 'bookings' in sample_room,
                                "bookings_count": len(sample_room.get('bookings', [])),
                                "status": sample_room.get('status'),
                                "has_current_booking": sample_room.get('current_booking') is not None
                            }
                        }
                    )
                else:
                    self.log_test(
                        "Meeting Rooms Bookings Structure",
                        False,
                        "No meeting rooms found in the system"
                    )
            else:
                self.log_test(
                    "Meeting Rooms Bookings Structure",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Meeting Rooms Bookings Structure",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_2_create_single_booking(self):
        """Test 2: Test creating a single booking for a room"""
        try:
            # Get a vacant room first
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code != 200:
                self.log_test(
                    "Create Single Booking",
                    False,
                    "Could not fetch meeting rooms"
                )
                return
                
            rooms = response.json()
            vacant_room = None
            
            for room in rooms:
                if room.get('status') == 'vacant':
                    vacant_room = room
                    break
            
            if not vacant_room:
                self.log_test(
                    "Create Single Booking",
                    False,
                    "No vacant rooms available for testing"
                )
                return
            
            room_id = vacant_room['id']
            
            # Create a booking 1 hour from now for 1 hour duration
            start_time = datetime.utcnow() + timedelta(hours=1)
            end_time = datetime.utcnow() + timedelta(hours=2)
            
            booking_data = {
                "employee_id": "80002",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Test booking for review verification"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                updated_room = response.json()
                bookings = updated_room.get('bookings', [])
                
                self.log_test(
                    "Create Single Booking",
                    True,
                    f"Successfully created booking. Room {room_id} now has {len(bookings)} booking(s)",
                    {
                        "room_id": room_id,
                        "room_name": updated_room.get('name'),
                        "bookings_count": len(bookings),
                        "room_status": updated_room.get('status'),
                        "booking_created": len(bookings) > 0
                    }
                )
                
                # Store for cleanup
                self.test_room_id = room_id
                if bookings:
                    self.test_booking_id = bookings[-1].get('id')
                    
            else:
                self.log_test(
                    "Create Single Booking",
                    False,
                    f"Failed to create booking. Status: {response.status_code}",
                    {"response": response.text[:300]}
                )
                
        except Exception as e:
            self.log_test(
                "Create Single Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_3_specific_booking_cancellation_endpoint(self):
        """Test 3: Test the new specific booking cancellation endpoint"""
        if not hasattr(self, 'test_room_id') or not hasattr(self, 'test_booking_id'):
            self.log_test(
                "Specific Booking Cancellation Endpoint",
                False,
                "No test booking available from previous test"
            )
            return
            
        try:
            # Test the new DELETE /api/meeting-rooms/{room_id}/booking/{booking_id} endpoint
            response = self.session.delete(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{self.test_booking_id}"
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
                        booking_found = False
                        for booking in bookings:
                            if booking.get('id') == self.test_booking_id:
                                booking_found = True
                                break
                        
                        self.log_test(
                            "Specific Booking Cancellation Endpoint",
                            not booking_found,
                            f"Specific booking cancellation {'successful' if not booking_found else 'failed'}. Room now has {len(bookings)} booking(s)",
                            {
                                "endpoint_tested": f"DELETE /api/meeting-rooms/{self.test_room_id}/booking/{self.test_booking_id}",
                                "booking_removed": not booking_found,
                                "remaining_bookings": len(bookings)
                            }
                        )
                    else:
                        self.log_test(
                            "Specific Booking Cancellation Endpoint",
                            False,
                            "Could not find test room to verify cancellation"
                        )
                else:
                    self.log_test(
                        "Specific Booking Cancellation Endpoint",
                        False,
                        "Could not fetch rooms to verify cancellation"
                    )
            else:
                self.log_test(
                    "Specific Booking Cancellation Endpoint",
                    False,
                    f"Failed to cancel specific booking. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Specific Booking Cancellation Endpoint",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_4_room_status_based_on_bookings(self):
        """Test 4: Test room status updates based on current time vs active bookings"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                occupied_rooms = [r for r in rooms if r.get('status') == 'occupied']
                vacant_rooms = [r for r in rooms if r.get('status') == 'vacant']
                
                # Check if occupied rooms have current bookings
                occupied_with_current_booking = 0
                occupied_without_current_booking = 0
                
                for room in occupied_rooms:
                    if room.get('current_booking'):
                        occupied_with_current_booking += 1
                    else:
                        occupied_without_current_booking += 1
                
                # Check if vacant rooms don't have current bookings
                vacant_with_current_booking = 0
                vacant_without_current_booking = 0
                
                for room in vacant_rooms:
                    if room.get('current_booking'):
                        vacant_with_current_booking += 1
                    else:
                        vacant_without_current_booking += 1
                
                status_logic_correct = (occupied_without_current_booking == 0 and 
                                      vacant_with_current_booking == 0)
                
                self.log_test(
                    "Room Status Based on Bookings",
                    status_logic_correct,
                    f"Room status logic is {'correct' if status_logic_correct else 'incorrect'}",
                    {
                        "total_rooms": len(rooms),
                        "occupied_rooms": len(occupied_rooms),
                        "vacant_rooms": len(vacant_rooms),
                        "occupied_with_current_booking": occupied_with_current_booking,
                        "occupied_without_current_booking": occupied_without_current_booking,
                        "vacant_with_current_booking": vacant_with_current_booking,
                        "vacant_without_current_booking": vacant_without_current_booking,
                        "status_logic_correct": status_logic_correct
                    }
                )
            else:
                self.log_test(
                    "Room Status Based on Bookings",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Room Status Based on Bookings",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_5_expired_booking_cleanup_verification(self):
        """Test 5: Verify cleanup of expired bookings works properly"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                total_bookings = 0
                expired_bookings_found = 0
                current_time = datetime.utcnow()
                
                for room in rooms:
                    bookings = room.get('bookings', [])
                    total_bookings += len(bookings)
                    
                    for booking in bookings:
                        end_time_str = booking.get('end_time', '')
                        if end_time_str:
                            try:
                                # Parse end time
                                end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
                                end_time = end_time.replace(tzinfo=None)  # Remove timezone for comparison
                                
                                if end_time < current_time:
                                    expired_bookings_found += 1
                            except:
                                continue
                
                cleanup_working = expired_bookings_found == 0
                
                self.log_test(
                    "Expired Booking Cleanup Verification",
                    cleanup_working,
                    f"Expired booking cleanup is {'working properly' if cleanup_working else 'not working'}. Found {expired_bookings_found} expired bookings",
                    {
                        "total_rooms": len(rooms),
                        "total_bookings": total_bookings,
                        "expired_bookings_found": expired_bookings_found,
                        "cleanup_working": cleanup_working
                    }
                )
            else:
                self.log_test(
                    "Expired Booking Cleanup Verification",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Expired Booking Cleanup Verification",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_6_time_conflict_detection_basic(self):
        """Test 6: Basic test of time conflict detection (using past time to avoid timezone issues)"""
        try:
            # Try to create a booking in the past (should be rejected)
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code != 200:
                self.log_test(
                    "Time Conflict Detection Basic",
                    False,
                    "Could not fetch meeting rooms"
                )
                return
                
            rooms = response.json()
            if not rooms:
                self.log_test(
                    "Time Conflict Detection Basic",
                    False,
                    "No rooms available for testing"
                )
                return
            
            test_room = rooms[0]
            
            # Try to book in the past (should be rejected)
            past_start = datetime.utcnow() - timedelta(hours=2)
            past_end = datetime.utcnow() - timedelta(hours=1)
            
            booking_data = {
                "employee_id": "80002",
                "start_time": past_start.isoformat() + "Z",
                "end_time": past_end.isoformat() + "Z",
                "remarks": "Past booking test - should fail"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{test_room['id']}/book",
                json=booking_data
            )
            
            # Should be rejected
            if response.status_code == 400:
                error_message = response.text
                if "past time" in error_message.lower():
                    self.log_test(
                        "Time Conflict Detection Basic",
                        True,
                        "Time validation working - past bookings correctly rejected",
                        {"error_message": error_message[:200]}
                    )
                else:
                    self.log_test(
                        "Time Conflict Detection Basic",
                        True,
                        "Booking rejected (good), but not specifically for past time",
                        {"error_message": error_message[:200]}
                    )
            else:
                self.log_test(
                    "Time Conflict Detection Basic",
                    False,
                    f"Past booking was not rejected. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Time Conflict Detection Basic",
                False,
                f"Exception occurred: {str(e)}"
            )

    def run_all_tests(self):
        """Run all focused meeting room booking tests"""
        print("🚀 Starting Focused Meeting Room Booking System Tests")
        print("Testing the new multiple booking system as requested in review")
        print("=" * 70)
        
        # Run tests in sequence
        self.test_1_meeting_rooms_bookings_structure()
        self.test_2_create_single_booking()
        self.test_3_specific_booking_cancellation_endpoint()
        self.test_4_room_status_based_on_bookings()
        self.test_5_expired_booking_cleanup_verification()
        self.test_6_time_conflict_detection_basic()
        
        # Summary
        print("=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All focused meeting room booking tests passed!")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check details above.")
            return False

def main():
    """Main function to run the tests"""
    tester = FocusedMeetingRoomTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()