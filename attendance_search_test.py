#!/usr/bin/env python3
"""
Focused Attendance Search Testing
Tests the new search parameter in attendance API
"""

import requests
import json

BACKEND_URL = "https://app-launcher-37.preview.emergentagent.com/api"

def test_attendance_search():
    session = requests.Session()
    
    print("🔍 Testing Attendance Search with new search parameter...")
    
    # First get some attendance records to see what employee names we have
    response = session.get(f"{BACKEND_URL}/attendance")
    if response.status_code == 200:
        attendance_records = response.json()
        print(f"Found {len(attendance_records)} attendance records")
        
        if attendance_records:
            # Get unique employee names from attendance records
            employee_names = list(set([record.get("employee_name", "") for record in attendance_records]))
            print(f"Unique employee names in attendance: {len(employee_names)}")
            print(f"Sample names: {employee_names[:5]}")
            
            # Test search with first few characters of actual employee names
            test_searches = []
            for name in employee_names[:5]:
                if name and len(name) >= 2:
                    test_searches.append(name[:2])
            
            # Remove duplicates
            test_searches = list(set(test_searches))
            
            for search_term in test_searches:
                print(f"\n🔍 Testing attendance search for '{search_term}'")
                
                search_response = session.get(f"{BACKEND_URL}/attendance?search={search_term}")
                
                if search_response.status_code == 200:
                    search_results = search_response.json()
                    print(f"✅ Search for '{search_term}' returned {len(search_results)} results")
                    
                    if search_results:
                        # Verify results follow "starts with" pattern
                        starts_with_count = 0
                        contains_but_not_starts_count = 0
                        
                        for record in search_results:
                            employee_name = record.get("employee_name", "").lower()
                            employee_id = record.get("employee_id", "").lower()
                            search_lower = search_term.lower()
                            
                            if employee_name.startswith(search_lower) or employee_id.startswith(search_lower):
                                starts_with_count += 1
                            elif search_lower in employee_name or search_lower in employee_id:
                                contains_but_not_starts_count += 1
                        
                        if contains_but_not_starts_count == 0:
                            print(f"✅ CORRECT: All results START with '{search_term}'")
                        else:
                            print(f"❌ INCORRECT: Found {contains_but_not_starts_count} results that contain but don't start with '{search_term}'")
                        
                        # Show sample results
                        for i, record in enumerate(search_results[:3]):
                            print(f"   Sample {i+1}: {record.get('employee_name')} (ID: {record.get('employee_id')})")
                else:
                    print(f"❌ Search failed: HTTP {search_response.status_code}")
        else:
            print("No attendance records found to test with")
    else:
        print(f"❌ Could not fetch attendance records: HTTP {response.status_code}")

if __name__ == "__main__":
    test_attendance_search()