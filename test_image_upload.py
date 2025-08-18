#!/usr/bin/env python3
"""
Test script to verify image upload functionality is working correctly
"""
import requests
import base64
import json

# Backend URL
BASE_URL = "http://localhost:8001/api"

def create_test_image_base64():
    """Create a small test PNG image in base64 format"""
    # A minimal 1x1 PNG image in base64
    png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAFKSFDIGAAAAABJRU5ErkJggg=="
    return f"data:image/png;base64,{png_base64}"

def test_image_upload():
    """Test the image upload functionality"""
    print("🧪 Testing Image Upload Functionality...")
    
    # Test employee ID (using first employee)
    test_employee_id = "80002"
    
    # Step 1: Test base64 image update
    print(f"\n1. Testing base64 image update for employee {test_employee_id}...")
    test_image_data = create_test_image_base64()
    
    response = requests.put(f"{BASE_URL}/employees/{test_employee_id}/image", 
                          json={"profileImage": test_image_data})
    
    if response.status_code == 200:
        employee_data = response.json()
        print(f"✅ Base64 image update successful!")
        print(f"   Employee: {employee_data['name']}")
        print(f"   Profile Image URL: {employee_data.get('profileImage', 'No URL')}")
        
        # Step 2: Verify image file exists
        image_url = employee_data.get('profileImage')
        if image_url:
            image_response = requests.get(f"http://localhost:8001{image_url}")
            if image_response.status_code == 200:
                print(f"✅ Image file accessible at {image_url}")
                print(f"   File size: {len(image_response.content)} bytes")
            else:
                print(f"❌ Image file not accessible: HTTP {image_response.status_code}")
        
    else:
        print(f"❌ Base64 image update failed: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Step 3: Test cleanup function
    print(f"\n3. Testing image cleanup...")
    cleanup_response = requests.post(f"{BASE_URL}/cleanup-images")
    if cleanup_response.status_code == 200:
        cleanup_data = cleanup_response.json()
        print(f"✅ Cleanup successful: {cleanup_data['message']}")
        print(f"   Files cleaned: {cleanup_data['files_cleaned']}")
    else:
        print(f"❌ Cleanup failed: HTTP {cleanup_response.status_code}")
    
    # Step 4: Verify employees API returns correct image URLs
    print(f"\n4. Testing employees API with image URLs...")
    employees_response = requests.get(f"{BASE_URL}/employees")
    if employees_response.status_code == 200:
        employees = employees_response.json()
        print(f"✅ Employees API successful: {len(employees)} employees")
        
        # Check how many employees have profile images
        employees_with_images = [emp for emp in employees if emp.get('profileImage') and not emp['profileImage'].endswith('/150/150')]
        print(f"   Employees with profile images: {len(employees_with_images)}")
        
        if employees_with_images:
            sample_employee = employees_with_images[0]
            print(f"   Sample employee with image: {sample_employee['name']} ({sample_employee['id']})")
            print(f"   Image URL: {sample_employee['profileImage']}")
    
    print(f"\n🎉 Image upload functionality test completed!")

if __name__ == "__main__":
    test_image_upload()