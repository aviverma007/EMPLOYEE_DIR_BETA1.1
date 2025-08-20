#!/usr/bin/env python3
"""
Multiple Bookings System Testing - Advanced Scenarios
Tests multiple non-overlapping bookings and time conflict detection
"""

import requests
import json
import sys
from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid

# Get backend URL from frontend .env
BACKEND_URL = "https://app-launcher-37.preview.emergentagent.com/api"

class MultipleBookingsTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.test_room_id = None
        self.created_bookings = []
        
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

    def test_1_setup_test_room(self):
        """Test 1: Setup - Find a vacant room for testing"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            
            if response.status_code == 200:
                rooms = response.json()
                
                # Find a vacant room with no bookings
                test_room = None
                for room in rooms:
                    if room.get('status') == 'vacant' and len(room.get('bookings', [])) == 0:
                        test_room = room
                        break
                
                if test_room:
                    self.test_room_id = test_room['id']
                    self.log_test(
                        "Setup Test Room",
                        True,
                        f"Found vacant room for testing: {test_room['name']}",
                        {
                            "room_id": self.test_room_id,
                            "room_name": test_room['name'],
                            "location": test_room.get('location'),
                            "floor": test_room.get('floor'),
                            "capacity": test_room.get('capacity')
                        }
                    )
                else:
                    self.log_test(
                        "Setup Test Room",
                        False,
                        "No vacant rooms with zero bookings available for testing"
                    )
            else:
                self.log_test(
                    "Setup Test Room",
                    False,
                    f"Failed to fetch meeting rooms. Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Setup Test Room",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_2_create_first_booking(self):
        """Test 2: Create first booking (9 AM - 10 AM tomorrow)"""
        if not self.test_room_id:
            self.log_test(
                "Create First Booking",
                False,
                "No test room available"
            )
            return
            
        try:
            # Create booking for tomorrow 9 AM - 10 AM
            tomorrow = datetime.utcnow() + timedelta(days=1)
            start_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": "80002",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "First booking - Morning meeting"
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
                        if 'Morning meeting' in booking.get('remarks', ''):
                            our_booking = booking
                            break
                    
                    if our_booking:
                        self.created_bookings.append(our_booking['id'])
                        self.log_test(
                            "Create First Booking",
                            True,
                            f"Successfully created first booking (9-10 AM). Room has {len(bookings)} booking(s)",
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
                            "Booking created but not found in response"
                        )
                else:
                    self.log_test(
                        "Create First Booking",
                        False,
                        "No bookings found after creation"
                    )
            else:
                self.log_test(
                    "Create First Booking",
                    False,
                    f"Failed to create first booking. Status: {response.status_code}",
                    {"response": response.text[:300]}
                )
                
        except Exception as e:
            self.log_test(
                "Create First Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_3_create_second_non_overlapping_booking(self):
        """Test 3: Create second non-overlapping booking (11 AM - 12 PM tomorrow)"""
        if not self.test_room_id:
            self.log_test(
                "Create Second Non-Overlapping Booking",
                False,
                "No test room available"
            )
            return
            
        try:
            # Create booking for tomorrow 11 AM - 12 PM (1 hour gap from first booking)
            tomorrow = datetime.utcnow() + timedelta(days=1)
            start_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": "80024",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Second booking - Lunch meeting"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                updated_room = response.json()
                bookings = updated_room.get('bookings', [])
                
                if len(bookings) >= 2:
                    # Find our booking
                    our_booking = None
                    for booking in bookings:
                        if 'Lunch meeting' in booking.get('remarks', ''):
                            our_booking = booking
                            break
                    
                    if our_booking:
                        self.created_bookings.append(our_booking['id'])
                        self.log_test(
                            "Create Second Non-Overlapping Booking",
                            True,
                            f"Successfully created second non-overlapping booking (11-12 PM). Room has {len(bookings)} booking(s)",
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
                            "Second booking created but not found in response"
                        )
                else:
                    self.log_test(
                        "Create Second Non-Overlapping Booking",
                        False,
                        f"Expected at least 2 bookings, found {len(bookings)}"
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

    def test_4_create_third_non_overlapping_booking(self):
        """Test 4: Create third non-overlapping booking (2 PM - 3 PM tomorrow)"""
        if not self.test_room_id:
            self.log_test(
                "Create Third Non-Overlapping Booking",
                False,
                "No test room available"
            )
            return
            
        try:
            # Create booking for tomorrow 2 PM - 3 PM (2 hour gap from second booking)
            tomorrow = datetime.utcnow() + timedelta(days=1)
            start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": "80056",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Third booking - Afternoon meeting"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            if response.status_code == 200:
                updated_room = response.json()
                bookings = updated_room.get('bookings', [])
                
                if len(bookings) >= 3:
                    # Find our booking
                    our_booking = None
                    for booking in bookings:
                        if 'Afternoon meeting' in booking.get('remarks', ''):
                            our_booking = booking
                            break
                    
                    if our_booking:
                        self.created_bookings.append(our_booking['id'])
                        self.log_test(
                            "Create Third Non-Overlapping Booking",
                            True,
                            f"Successfully created third non-overlapping booking (2-3 PM). Room has {len(bookings)} booking(s)",
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
                            "Create Third Non-Overlapping Booking",
                            False,
                            "Third booking created but not found in response"
                        )
                else:
                    self.log_test(
                        "Create Third Non-Overlapping Booking",
                        False,
                        f"Expected at least 3 bookings, found {len(bookings)}"
                    )
            else:
                self.log_test(
                    "Create Third Non-Overlapping Booking",
                    False,
                    f"Failed to create third booking. Status: {response.status_code}",
                    {"response": response.text[:300]}
                )
                
        except Exception as e:
            self.log_test(
                "Create Third Non-Overlapping Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_5_test_overlapping_conflict_scenario_1(self):
        """Test 5: Test time conflict - try to book 9:30-10:30 AM (overlaps with first booking)"""
        if not self.test_room_id:
            self.log_test(
                "Time Conflict Scenario 1",
                False,
                "No test room available"
            )
            return
            
        try:
            # Try to create overlapping booking (9:30 AM - 10:30 AM) - should conflict with first booking (9-10 AM)
            tomorrow = datetime.utcnow() + timedelta(days=1)
            start_time = tomorrow.replace(hour=9, minute=30, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=10, minute=30, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": "80059",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Conflicting booking 1 - Should fail"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            # Should be rejected with 400 status
            if response.status_code == 400:
                error_message = response.text
                if "conflict" in error_message.lower() or "overlap" in error_message.lower():
                    self.log_test(
                        "Time Conflict Scenario 1",
                        True,
                        "Time conflict correctly detected for overlapping booking (9:30-10:30 AM vs 9-10 AM)",
                        {"error_message": error_message[:200]}
                    )
                else:
                    self.log_test(
                        "Time Conflict Scenario 1",
                        True,
                        "Booking rejected (good), but not specifically for time conflict",
                        {"error_message": error_message[:200]}
                    )
            else:
                self.log_test(
                    "Time Conflict Scenario 1",
                    False,
                    f"Overlapping booking was incorrectly accepted. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Time Conflict Scenario 1",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_6_test_overlapping_conflict_scenario_2(self):
        """Test 6: Test time conflict - try to book 10:30-11:30 AM (overlaps with second booking)"""
        if not self.test_room_id:
            self.log_test(
                "Time Conflict Scenario 2",
                False,
                "No test room available"
            )
            return
            
        try:
            # Try to create overlapping booking (10:30 AM - 11:30 AM) - should conflict with second booking (11-12 PM)
            tomorrow = datetime.utcnow() + timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=30, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=11, minute=30, second=0, microsecond=0)
            
            booking_data = {
                "employee_id": "80006",
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "remarks": "Conflicting booking 2 - Should fail"
            }
            
            response = self.session.post(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/book",
                json=booking_data
            )
            
            # Should be rejected with 400 status
            if response.status_code == 400:
                error_message = response.text
                if "conflict" in error_message.lower() or "overlap" in error_message.lower():
                    self.log_test(
                        "Time Conflict Scenario 2",
                        True,
                        "Time conflict correctly detected for overlapping booking (10:30-11:30 AM vs 11-12 PM)",
                        {"error_message": error_message[:200]}
                    )
                else:
                    self.log_test(
                        "Time Conflict Scenario 2",
                        True,
                        "Booking rejected (good), but not specifically for time conflict",
                        {"error_message": error_message[:200]}
                    )
            else:
                self.log_test(
                    "Time Conflict Scenario 2",
                    False,
                    f"Overlapping booking was incorrectly accepted. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Time Conflict Scenario 2",
                False,
                f"Exception occurred: {str(e)}"
            )

    def test_7_cancel_middle_booking(self):
        """Test 7: Cancel the middle booking (second booking) and verify room still has other bookings"""
        if not self.test_room_id or len(self.created_bookings) < 2:
            self.log_test(
                "Cancel Middle Booking",
                False,
                "Not enough test bookings available"
            )
            return
            
        try:
            # Cancel the second booking (middle one)
            booking_id_to_cancel = self.created_bookings[1]  # Second booking
            
            response = self.session.delete(
                f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{booking_id_to_cancel}"
            )
            
            if response.status_code == 200:
                # Verify the specific booking was removed but others remain
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
                        
                        expected_bookings = len(self.created_bookings) - 1  # Should have 2 remaining
                        
                        self.log_test(
                            "Cancel Middle Booking",
                            not cancelled_booking_found and len(bookings) == expected_bookings,
                            f"Middle booking cancelled successfully. Room has {len(bookings)} remaining booking(s)",
                            {
                                "cancelled_booking_id": booking_id_to_cancel,
                                "booking_removed": not cancelled_booking_found,
                                "remaining_bookings": len(bookings),
                                "expected_bookings": expected_bookings
                            }
                        )
                    else:
                        self.log_test(
                            "Cancel Middle Booking",
                            False,
                            "Could not find test room to verify cancellation"
                        )
                else:
                    self.log_test(
                        "Cancel Middle Booking",
                        False,
                        "Could not fetch rooms to verify cancellation"
                    )
            else:
                self.log_test(
                    "Cancel Middle Booking",
                    False,
                    f"Failed to cancel middle booking. Status: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Cancel Middle Booking",
                False,
                f"Exception occurred: {str(e)}"
            )

    def cleanup_test_bookings(self):
        """Cleanup: Remove all remaining test bookings"""
        if not self.test_room_id or not self.created_bookings:
            return
            
        try:
            # Get current bookings
            response = self.session.get(f"{self.base_url}/meeting-rooms")
            if response.status_code == 200:
                rooms = response.json()
                test_room = None
                
                for room in rooms:
                    if room['id'] == self.test_room_id:
                        test_room = room
                        break
                
                if test_room:
                    bookings = test_room.get('bookings', [])
                    
                    # Cancel all remaining bookings
                    for booking in bookings:
                        booking_id = booking.get('id')
                        if booking_id:
                            self.session.delete(
                                f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{booking_id}"
                            )
                    
                    print(f"🧹 Cleaned up {len(bookings)} remaining test booking(s)")
        except:
            pass  # Ignore cleanup errors

    def run_all_tests(self):
        """Run all multiple bookings tests"""
        print("🚀 Starting Multiple Bookings System Tests")
        print("Testing multiple non-overlapping bookings and time conflict detection")
        print("=" * 75)
        
        try:
            # Run tests in sequence
            self.test_1_setup_test_room()
            self.test_2_create_first_booking()
            self.test_3_create_second_non_overlapping_booking()
            self.test_4_create_third_non_overlapping_booking()
            self.test_5_test_overlapping_conflict_scenario_1()
            self.test_6_test_overlapping_conflict_scenario_2()
            self.test_7_cancel_middle_booking()
            
        finally:
            # Always cleanup
            self.cleanup_test_bookings()
        
        # Summary
        print("=" * 75)
        print("📊 TEST SUMMARY")
        print("=" * 75)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All multiple bookings tests passed!")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check details above.")
            return False

def main():
    """Main function to run the tests"""
    tester = MultipleBookingsTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()