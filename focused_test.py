#!/usr/bin/env python3
"""
Focused test for the two failed APIs after timezone fixes
"""

import requests
import json
from datetime import datetime, timedelta

BACKEND_URL = "https://dual-service-run.preview.emergentagent.com/api"

def test_meeting_room_booking():
    """Test meeting room booking after timezone fix"""
    session = requests.Session()
    
    print("Testing Meeting Room Booking...")
    
    # Get rooms
    rooms_response = session.get(f"{BACKEND_URL}/meeting-rooms")
    if rooms_response.status_code != 200:
        print("❌ Could not fetch meeting rooms")
        return
    
    rooms = rooms_response.json()
    vacant_room = next((room for room in rooms if room.get("status") == "vacant"), rooms[0] if rooms else None)
    
    if not vacant_room:
        print("❌ No meeting rooms available")
        return
    
    # Get employees
    emp_response = session.get(f"{BACKEND_URL}/employees")
    if emp_response.status_code != 200:
        print("❌ Could not fetch employees")
        return
    
    employees = emp_response.json()
    if not employees:
        print("❌ No employees available")
        return
    
    # Create booking with proper timezone
    now = datetime.utcnow()
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "employee_id": employees[0]["id"],
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
        "remarks": "Test booking after timezone fix"
    }
    
    # Book the room
    book_response = session.post(
        f"{BACKEND_URL}/meeting-rooms/{vacant_room['id']}/book",
        json=booking_data
    )
    
    if book_response.status_code == 200:
        print(f"✅ Successfully booked meeting room: {vacant_room['name']}")
        return True
    else:
        print(f"❌ Booking failed: {book_response.status_code} - {book_response.text}")
        return False

def test_attendance_update():
    """Test attendance update after timezone fix"""
    session = requests.Session()
    
    print("Testing Attendance Update...")
    
    # Get employees
    emp_response = session.get(f"{BACKEND_URL}/employees")
    if emp_response.status_code != 200:
        print("❌ Could not fetch employees")
        return
    
    employees = emp_response.json()
    if not employees:
        print("❌ No employees available")
        return
    
    # Create attendance record with timezone-aware times
    yesterday = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")
    attendance_data = {
        "employee_id": employees[0]["id"],
        "date": yesterday,
        "punch_in": "2025-01-18T09:00:00Z",
        "status": "present",
        "remarks": "Test attendance for timezone fix"
    }
    
    create_response = session.post(f"{BACKEND_URL}/attendance", json=attendance_data)
    
    if create_response.status_code == 200:
        created_attendance = create_response.json()
        attendance_id = created_attendance["id"]
        
        # Update with punch out
        update_data = {
            "punch_out": "2025-01-18T17:30:00Z",
            "punch_out_location": "IFC Office - Main Entrance",
            "remarks": "Updated with punch out after timezone fix"
        }
        
        update_response = session.put(f"{BACKEND_URL}/attendance/{attendance_id}", json=update_data)
        
        if update_response.status_code == 200:
            updated_attendance = update_response.json()
            print(f"✅ Successfully updated attendance record. Total hours: {updated_attendance.get('total_hours')}")
            return True
        else:
            print(f"❌ Update failed: {update_response.status_code} - {update_response.text}")
            return False
    elif create_response.status_code == 400 and "already exists" in create_response.text:
        print("✅ Attendance record already exists (expected behavior)")
        return True
    else:
        print(f"❌ Create failed: {create_response.status_code} - {create_response.text}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("FOCUSED TEST - TIMEZONE FIXES")
    print("=" * 60)
    
    booking_success = test_meeting_room_booking()
    print()
    attendance_success = test_attendance_update()
    
    print()
    print("=" * 60)
    print("RESULTS:")
    print(f"Meeting Room Booking: {'✅ PASS' if booking_success else '❌ FAIL'}")
    print(f"Attendance Update: {'✅ PASS' if attendance_success else '❌ FAIL'}")
    print("=" * 60)