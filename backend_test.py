#!/usr/bin/env python3
"""
Backend Testing Script for Minimal Frontend-Only Employee Directory API
Tests the minimal backend server to ensure it's working as a placeholder.
"""

import requests
import json
import sys
import os
from datetime import datetime

# Get the backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

class MinimalBackendTester:
    def __init__(self):
        self.backend_url = get_backend_url()
        if not self.backend_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        print(f"🔗 Testing Backend URL: {self.backend_url}")
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 10

    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def test_server_connectivity(self):
        """Test 1: Backend server connectivity (localhost)"""
        try:
            # Test backend server directly on localhost:8001
            response = self.session.get("http://localhost:8001/")
            if response.status_code == 200:
                data = response.json()
                if "Frontend-Only Employee Directory API" in data.get("message", ""):
                    self.log_test("Backend Server Connectivity", True, 
                                f"Backend server responding correctly on port 8001", 
                                f"Response: {data}")
                else:
                    self.log_test("Backend Server Connectivity", False, 
                                f"Unexpected response content", 
                                f"Response: {data}")
            else:
                self.log_test("Backend Server Connectivity", False, 
                            f"Backend server returned status {response.status_code}")
        except Exception as e:
            self.log_test("Backend Server Connectivity", False, f"Backend server connection failed: {str(e)}")

    def test_health_endpoint(self):
        """Test 2: Health check endpoint (localhost)"""
        try:
            # Test health endpoint directly on localhost:8001
            response = self.session.get("http://localhost:8001/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy" and data.get("mode") == "frontend-only":
                    self.log_test("Health Check", True, 
                                "Health endpoint working correctly on backend server", 
                                f"Response: {data}")
                else:
                    self.log_test("Health Check", False, 
                                "Health endpoint returned unexpected data", 
                                f"Response: {data}")
            else:
                self.log_test("Health Check", False, 
                            f"Health endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Health Check", False, f"Health check failed: {str(e)}")

    def test_cors_configuration(self):
        """Test 3: CORS configuration via external URL"""
        try:
            # Test preflight request via external URL for API endpoints
            headers = {
                'Origin': 'https://example.com',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            response = self.session.options(f"{self.backend_url}/api/employees", headers=headers)
            
            cors_headers = {
                'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
                'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
                'access-control-allow-headers': response.headers.get('access-control-allow-headers')
            }
            
            # Check if CORS allows the origin (should be * for allow all origins)
            allow_origin = cors_headers['access-control-allow-origin']
            if allow_origin == '*' or allow_origin == 'https://example.com':
                self.log_test("CORS Configuration", True, 
                            "CORS properly configured for API endpoints", 
                            f"CORS headers: {cors_headers}")
            else:
                self.log_test("CORS Configuration", False, 
                            "CORS not properly configured", 
                            f"CORS headers: {cors_headers}")
        except Exception as e:
            self.log_test("CORS Configuration", False, f"CORS test failed: {str(e)}")

    def test_employees_endpoint(self):
        """Test 4: /api/employees endpoint"""
        try:
            response = self.session.get(f"{self.backend_url}/api/employees")
            if response.status_code == 200:
                data = response.json()
                expected_message = "Data is now managed by frontend"
                if expected_message in data.get("message", ""):
                    self.log_test("Employees Endpoint", True, 
                                "Employees endpoint returns frontend-only message", 
                                f"Response: {data}")
                else:
                    self.log_test("Employees Endpoint", False, 
                                "Employees endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Employees Endpoint", False, 
                            f"Employees endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Employees Endpoint", False, f"Employees endpoint test failed: {str(e)}")

    def test_departments_endpoint(self):
        """Test 5: /api/departments endpoint"""
        try:
            response = self.session.get(f"{self.backend_url}/api/departments")
            if response.status_code == 200:
                data = response.json()
                expected_message = "Data is now managed by frontend"
                if expected_message in data.get("message", ""):
                    self.log_test("Departments Endpoint", True, 
                                "Departments endpoint returns frontend-only message", 
                                f"Response: {data}")
                else:
                    self.log_test("Departments Endpoint", False, 
                                "Departments endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Departments Endpoint", False, 
                            f"Departments endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Departments Endpoint", False, f"Departments endpoint test failed: {str(e)}")

    def test_stats_endpoint(self):
        """Test 6: /api/stats endpoint"""
        try:
            response = self.session.get(f"{self.backend_url}/api/stats")
            if response.status_code == 200:
                data = response.json()
                expected_message = "Data is now managed by frontend"
                if expected_message in data.get("message", ""):
                    self.log_test("Stats Endpoint", True, 
                                "Stats endpoint returns frontend-only message", 
                                f"Response: {data}")
                else:
                    self.log_test("Stats Endpoint", False, 
                                "Stats endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Stats Endpoint", False, 
                            f"Stats endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Stats Endpoint", False, f"Stats endpoint test failed: {str(e)}")

    def test_catch_all_endpoint(self):
        """Test 7: Catch-all API endpoint"""
        try:
            # Test a random API endpoint that should be caught by catch-all
            response = self.session.get(f"{self.backend_url}/api/random-endpoint")
            if response.status_code == 200:
                data = response.json()
                expected_message = "is now handled by frontend dataService"
                if expected_message in data.get("message", ""):
                    self.log_test("Catch-All Endpoint", True, 
                                "Catch-all endpoint working correctly", 
                                f"Response: {data}")
                else:
                    self.log_test("Catch-All Endpoint", False, 
                                "Catch-all endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Catch-All Endpoint", False, 
                            f"Catch-all endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Catch-All Endpoint", False, f"Catch-all endpoint test failed: {str(e)}")

    def test_post_request_handling(self):
        """Test 8: POST request handling via catch-all"""
        try:
            test_data = {"test": "data"}
            response = self.session.post(f"{self.backend_url}/api/test-post", json=test_data)
            if response.status_code == 200:
                data = response.json()
                expected_message = "is now handled by frontend dataService"
                if expected_message in data.get("message", ""):
                    self.log_test("POST Request Handling", True, 
                                "POST requests handled correctly by catch-all", 
                                f"Response: {data}")
                else:
                    self.log_test("POST Request Handling", False, 
                                "POST request returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("POST Request Handling", False, 
                            f"POST request returned status {response.status_code}")
        except Exception as e:
            self.log_test("POST Request Handling", False, f"POST request test failed: {str(e)}")

    def test_meeting_rooms_endpoints(self):
        """Test 9: Meeting rooms API endpoints redirect to frontend"""
        try:
            # Test meeting rooms endpoint
            response = self.session.get(f"{self.backend_url}/api/meeting-rooms")
            if response.status_code == 200:
                data = response.json()
                expected_message = "is now handled by frontend dataService"
                if expected_message in data.get("message", ""):
                    self.log_test("Meeting Rooms Endpoint", True, 
                                "Meeting rooms endpoint redirects to frontend correctly", 
                                f"Response: {data}")
                else:
                    self.log_test("Meeting Rooms Endpoint", False, 
                                "Meeting rooms endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Meeting Rooms Endpoint", False, 
                            f"Meeting rooms endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Meeting Rooms Endpoint", False, f"Meeting rooms endpoint test failed: {str(e)}")

    def test_meeting_rooms_booking_endpoints(self):
        """Test 10: Meeting rooms booking endpoints redirect to frontend"""
        try:
            # Test booking endpoint
            booking_data = {
                "employee_id": "12345",
                "start_time": "2024-12-20T10:00:00",
                "end_time": "2024-12-20T11:00:00",
                "purpose": "Test meeting"
            }
            response = self.session.post(f"{self.backend_url}/api/meeting-rooms/test-room/book", json=booking_data)
            if response.status_code == 200:
                data = response.json()
                expected_message = "is now handled by frontend dataService"
                if expected_message in data.get("message", ""):
                    self.log_test("Meeting Rooms Booking Endpoint", True, 
                                "Meeting rooms booking endpoint redirects to frontend correctly", 
                                f"Response: {data}")
                else:
                    self.log_test("Meeting Rooms Booking Endpoint", False, 
                                "Meeting rooms booking endpoint returned unexpected message", 
                                f"Response: {data}")
            else:
                self.log_test("Meeting Rooms Booking Endpoint", False, 
                            f"Meeting rooms booking endpoint returned status {response.status_code}")
        except Exception as e:
            self.log_test("Meeting Rooms Booking Endpoint", False, f"Meeting rooms booking endpoint test failed: {str(e)}")

    def test_excel_file_accessibility(self):
        """Test 11: Excel file accessibility at /employee_directory.xlsx"""
        try:
            # Test Excel file accessibility via frontend URL
            excel_url = f"{self.backend_url}/employee_directory.xlsx"
            response = self.session.get(excel_url)
            if response.status_code == 200:
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'spreadsheet' in content_type or 'excel' in content_type:
                    # Try to verify it's a valid Excel file by checking content length
                    content_length = len(response.content)
                    if content_length > 10000:  # Should be substantial for 625 employees
                        self.log_test("Excel File Accessibility", True, 
                                    f"Excel file accessible at /employee_directory.xlsx with {content_length} bytes", 
                                    f"Content-Type: {content_type}")
                    else:
                        self.log_test("Excel File Accessibility", False, 
                                    f"Excel file too small ({content_length} bytes), may be corrupted")
                else:
                    self.log_test("Excel File Accessibility", False, 
                                f"Excel file has incorrect content-type: {content_type}")
            else:
                self.log_test("Excel File Accessibility", False, 
                            f"Excel file returned status {response.status_code}")
        except Exception as e:
            self.log_test("Excel File Accessibility", False, f"Excel file accessibility test failed: {str(e)}")

    def test_excel_employee_count(self):
        """Test 12: Verify Excel file contains 625 employees"""
        try:
            import pandas as pd
            import tempfile
            
            # Download Excel file and verify employee count
            excel_url = f"{self.backend_url}/employee_directory.xlsx"
            response = self.session.get(excel_url)
            if response.status_code == 200:
                # Save to temporary file and read with pandas
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file.flush()
                    
                    try:
                        df = pd.read_excel(tmp_file.name)
                        employee_count = len(df)
                        
                        if employee_count == 625:
                            self.log_test("Excel Employee Count", True, 
                                        f"Excel file contains exactly 625 employees as expected", 
                                        f"Employee count: {employee_count}")
                        else:
                            self.log_test("Excel Employee Count", False, 
                                        f"Excel file contains {employee_count} employees, expected 625")
                    except Exception as e:
                        self.log_test("Excel Employee Count", False, 
                                    f"Failed to read Excel file: {str(e)}")
                    finally:
                        os.unlink(tmp_file.name)
            else:
                self.log_test("Excel Employee Count", False, 
                            f"Could not download Excel file (status {response.status_code})")
        except ImportError:
            self.log_test("Excel Employee Count", False, 
                        "pandas not available for Excel verification")
        except Exception as e:
            self.log_test("Excel Employee Count", False, f"Excel employee count test failed: {str(e)}")

    def test_frontend_accessibility(self):
        """Test 13: Frontend accessibility"""
        try:
            response = self.session.get(self.backend_url)
            if response.status_code == 200:
                content = response.text
                # Check for React app indicators
                if 'id="root"' in content and ('bundle.js' in content or 'static' in content):
                    self.log_test("Frontend Accessibility", True, 
                                "Frontend is accessible and serving React application", 
                                f"Content length: {len(content)} characters")
                else:
                    self.log_test("Frontend Accessibility", False, 
                                "Frontend accessible but not serving expected React content", 
                                f"Content preview: {content[:200]}...")
            else:
                self.log_test("Frontend Accessibility", False, 
                            f"Frontend returned status {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Accessibility", False, f"Frontend accessibility test failed: {str(e)}")

    def test_data_loading_errors(self):
        """Test 14: Check for any errors preventing proper data loading"""
        try:
            # Test multiple endpoints to ensure no 500 errors or exceptions
            endpoints_to_test = [
                "/api/employees",
                "/api/departments", 
                "/api/locations",
                "/api/stats",
                "/api/meeting-rooms"
            ]
            
            all_working = True
            error_details = []
            
            for endpoint in endpoints_to_test:
                try:
                    response = self.session.get(f"{self.backend_url}{endpoint}")
                    if response.status_code != 200:
                        all_working = False
                        error_details.append(f"{endpoint}: HTTP {response.status_code}")
                    else:
                        # Check if response is valid JSON
                        data = response.json()
                        if 'message' not in data:
                            all_working = False
                            error_details.append(f"{endpoint}: Invalid JSON structure")
                except Exception as e:
                    all_working = False
                    error_details.append(f"{endpoint}: {str(e)}")
            
            if all_working:
                self.log_test("Data Loading Error Check", True, 
                            "All API endpoints responding without errors", 
                            f"Tested {len(endpoints_to_test)} endpoints successfully")
            else:
                self.log_test("Data Loading Error Check", False, 
                            "Some endpoints have errors preventing proper data loading", 
                            f"Errors: {'; '.join(error_details)}")
        except Exception as e:
            self.log_test("Data Loading Error Check", False, f"Error check test failed: {str(e)}")

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Frontend-Only Backend API Tests")
        print("=" * 60)
        
        # Original tests
        self.test_server_connectivity()
        self.test_health_endpoint()
        self.test_cors_configuration()
        self.test_employees_endpoint()
        self.test_departments_endpoint()
        self.test_stats_endpoint()
        self.test_catch_all_endpoint()
        self.test_post_request_handling()
        self.test_meeting_rooms_endpoints()
        self.test_meeting_rooms_booking_endpoints()
        
        # New tests for review request
        self.test_excel_file_accessibility()
        self.test_excel_employee_count()
        self.test_frontend_accessibility()
        self.test_data_loading_errors()
        
        print("\n" + "=" * 60)
        print("📊 BACKEND API TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL BACKEND API TESTS PASSED! Backend correctly redirects to frontend dataService.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the details above.")
            
        return passed == total

if __name__ == "__main__":
    tester = MinimalBackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)