#!/usr/bin/env python3
"""
Adjacent Time Slots Testing - Edge Case Verification
Tests booking exactly adjacent time slots (touching but not overlapping)
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Get backend URL from frontend .env
BACKEND_URL = "https://profile-gallery-4.preview.emergentagent.com/api"

class AdjacentSlotsTest:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_room_id = None
        self.test_bookings = []
        
    def log_test(self, test_name: str, success: bool, message: str, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        print()
        return success

    def setup_test_room(self):
        """Get a vacant room for testing"""
        try:
            response = self.session.get(f"{self.base_url}/meeting-rooms?status=vacant")
            if response.status_code == 200:
                rooms = response.json()
                if rooms:
                    self.test_room_id = rooms[0]['id']
                    return self.log_test("Setup Test Room", True, f"Selected room: {rooms[0]['name']}")
            return self.log_test("Setup Test Room", False, "No vacant rooms available")
        except Exception as e:
            return self.log_test("Setup Test Room", False, f"Exception: {str(e)}")

    def test_adjacent_bookings(self):
        """Test booking exactly adjacent time slots"""
        if not self.test_room_id:
            return self.log_test("Adjacent Bookings", False, "No test room available")
            
        try:
            # Create base time for tomorrow
            tomorrow = datetime.utcnow() + timedelta(days=1)
            base_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
            
            # First booking: 10:00-11:00
            booking1_data = {
                "employee_id": "EMP001",
                "start_time": base_time.isoformat() + "Z",
                "end_time": (base_time + timedelta(hours=1)).isoformat() + "Z",
                "remarks": "First adjacent booking"
            }
            
            response1 = self.session.post(f"{self.base_url}/meeting-rooms/{self.test_room_id}/book", json=booking1_data)
            if response1.status_code != 200:
                return self.log_test("Adjacent Bookings", False, f"First booking failed: {response1.text}")
            
            # Second booking: 11:00-12:00 (starts exactly when first ends)
            booking2_data = {
                "employee_id": "EMP002", 
                "start_time": (base_time + timedelta(hours=1)).isoformat() + "Z",
                "end_time": (base_time + timedelta(hours=2)).isoformat() + "Z",
                "remarks": "Second adjacent booking"
            }
            
            response2 = self.session.post(f"{self.base_url}/meeting-rooms/{self.test_room_id}/book", json=booking2_data)
            if response2.status_code != 200:
                return self.log_test("Adjacent Bookings", False, f"Second booking failed: {response2.text}")
            
            # Third booking: 12:00-13:00 (starts exactly when second ends)
            booking3_data = {
                "employee_id": "EMP003",
                "start_time": (base_time + timedelta(hours=2)).isoformat() + "Z", 
                "end_time": (base_time + timedelta(hours=3)).isoformat() + "Z",
                "remarks": "Third adjacent booking"
            }
            
            response3 = self.session.post(f"{self.base_url}/meeting-rooms/{self.test_room_id}/book", json=booking3_data)
            if response3.status_code != 200:
                return self.log_test("Adjacent Bookings", False, f"Third booking failed: {response3.text}")
            
            # Verify all bookings exist
            room_data = response3.json()
            bookings = room_data.get('bookings', [])
            
            if len(bookings) >= 3:
                self.test_bookings = bookings[-3:]  # Store last 3 bookings
                return self.log_test("Adjacent Bookings", True, f"Successfully created 3 adjacent bookings (10-11, 11-12, 12-13)", 
                                   {"total_bookings": len(bookings)})
            else:
                return self.log_test("Adjacent Bookings", False, f"Expected 3+ bookings, got {len(bookings)}")
                
        except Exception as e:
            return self.log_test("Adjacent Bookings", False, f"Exception: {str(e)}")

    def test_overlapping_with_adjacent(self):
        """Test that overlapping bookings are still rejected even with adjacent slots"""
        if not self.test_room_id:
            return self.log_test("Overlapping Test", False, "No test room available")
            
        try:
            # Try to book 10:30-11:30 (overlaps with both 10-11 and 11-12)
            tomorrow = datetime.utcnow() + timedelta(days=1)
            overlap_start = tomorrow.replace(hour=10, minute=30, second=0, microsecond=0)
            overlap_end = tomorrow.replace(hour=11, minute=30, second=0, microsecond=0)
            
            overlap_booking = {
                "employee_id": "EMP004",
                "start_time": overlap_start.isoformat() + "Z",
                "end_time": overlap_end.isoformat() + "Z", 
                "remarks": "Overlapping booking - should fail"
            }
            
            response = self.session.post(f"{self.base_url}/meeting-rooms/{self.test_room_id}/book", json=overlap_booking)
            
            if response.status_code == 400 and "conflict" in response.text.lower():
                return self.log_test("Overlapping Test", True, "Overlapping booking correctly rejected",
                                   {"error": response.text})
            else:
                return self.log_test("Overlapping Test", False, f"Expected 400 conflict error, got {response.status_code}: {response.text}")
                
        except Exception as e:
            return self.log_test("Overlapping Test", False, f"Exception: {str(e)}")

    def cleanup_bookings(self):
        """Clean up test bookings"""
        if not self.test_room_id or not self.test_bookings:
            return True
            
        try:
            cleaned = 0
            for booking in self.test_bookings:
                booking_id = booking.get('id')
                if booking_id:
                    response = self.session.delete(f"{self.base_url}/meeting-rooms/{self.test_room_id}/booking/{booking_id}")
                    if response.status_code == 200:
                        cleaned += 1
            
            return self.log_test("Cleanup", True, f"Cleaned up {cleaned} test bookings")
            
        except Exception as e:
            return self.log_test("Cleanup", False, f"Exception: {str(e)}")

    def run_tests(self):
        """Run all adjacent slots tests"""
        print("🚀 Starting Adjacent Time Slots Tests")
        print("=" * 60)
        
        tests = [
            self.setup_test_room,
            self.test_adjacent_bookings,
            self.test_overlapping_with_adjacent,
            self.cleanup_bookings
        ]
        
        passed = 0
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Results: {passed}/{len(tests)} tests passed")
        
        if passed == len(tests):
            print("🎉 All adjacent slots tests passed!")
            print("✅ Adjacent time slots work correctly")
            print("✅ Overlapping detection still works with adjacent slots")
        else:
            print("❌ Some tests failed")
        
        return passed == len(tests)

if __name__ == "__main__":
    tester = AdjacentSlotsTest()
    success = tester.run_tests()
    sys.exit(0 if success else 1)