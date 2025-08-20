#!/usr/bin/env python3
"""
Photo File Upload Test via External URL
Tests the file upload method for photos using the corrected external URL
"""

import requests
import io
import base64
import sys

# Use the corrected external URL
EXTERNAL_URL = "https://fast-modify.preview.emergentagent.com/api"

def test_photo_file_upload():
    """Test photo file upload functionality via external URL"""
    session = requests.Session()
    
    try:
        # Get an employee for photo upload
        response = session.get(f"{EXTERNAL_URL}/employees")
        
        if response.status_code != 200:
            print(f"❌ Failed to get employees: HTTP {response.status_code}")
            return False
        
        employees = response.json()
        if not employees:
            print("❌ No employees found for photo upload test")
            return False
        
        test_employee = employees[1]  # Use second employee to avoid conflicts
        employee_id = test_employee['id']
        employee_name = test_employee['name']
        
        print(f"🧪 Testing file upload for employee: {employee_name} (ID: {employee_id})")
        
        # Create a minimal PNG file (1x1 red pixel)
        png_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==")
        
        # Prepare file for upload
        files = {
            'file': ('test_image.png', io.BytesIO(png_data), 'image/png')
        }
        
        # Upload photo via external URL using file upload method
        upload_response = session.post(
            f"{EXTERNAL_URL}/employees/{employee_id}/upload-image",
            files=files,
            timeout=10
        )
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            profile_image_url = upload_result.get('profileImage', '')
            
            # Verify the image URL is properly formatted
            if profile_image_url and '/api/uploads/images/' in profile_image_url:
                print(f"✅ Successfully uploaded photo file for {employee_name} via external URL")
                print(f"   Profile Image URL: {profile_image_url}")
                
                # Test image accessibility
                if profile_image_url.startswith('/api/'):
                    full_image_url = f"https://fast-modify.preview.emergentagent.com{profile_image_url}"
                else:
                    full_image_url = profile_image_url
                
                image_response = session.get(full_image_url, timeout=10)
                
                if image_response.status_code == 200:
                    content_length = len(image_response.content)
                    print(f"✅ Uploaded image is accessible via external URL (size: {content_length} bytes)")
                    return True
                else:
                    print(f"❌ Uploaded image not accessible: HTTP {image_response.status_code}")
                    return False
            else:
                print(f"❌ Photo uploaded but invalid image URL returned: {profile_image_url}")
                return False
        else:
            print(f"❌ Failed to upload photo file via external URL: HTTP {upload_response.status_code}")
            print(f"   Response: {upload_response.text[:300]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during photo file upload: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during photo file upload: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Photo File Upload via External URL")
    print("=" * 60)
    
    success = test_photo_file_upload()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Photo file upload test PASSED!")
        print("✅ File upload method works correctly via external URL")
    else:
        print("❌ Photo file upload test FAILED!")
    
    sys.exit(0 if success else 1)