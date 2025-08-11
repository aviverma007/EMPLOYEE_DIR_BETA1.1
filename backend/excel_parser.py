import os
from typing import List, Dict, Any
from pathlib import Path

# Try to import pandas with proper error handling
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pandas not available: {e}")
    PANDAS_AVAILABLE = False

# Ensure openpyxl is available for Excel operations
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    try:
        import pandas as pd
        # Try to trigger the openpyxl import through pandas
        pd.read_excel("dummy_test.xlsx")  # This will fail but will show the right error
    except Exception:
        pass
    OPENPYXL_AVAILABLE = False

class ExcelParser:
    def __init__(self, file_path: str = None):
        if file_path:
            self.file_path = file_path
        else:
            # Default to the Excel file in the backend directory
            current_dir = Path(__file__).parent
            self.file_path = str(current_dir / "employee_directory.xlsx")
            
            # Fallback to app directory if not found in backend
            if not os.path.exists(self.file_path):
                app_dir = current_dir.parent
                fallback_path = str(app_dir / "employee_directory.xlsx")
                if os.path.exists(fallback_path):
                    self.file_path = fallback_path
    
    def parse_excel_to_employees(self) -> List[Dict[str, Any]]:
        """Parse Excel file and return list of employee dictionaries"""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is not installed. Please install pandas to parse Excel files.")
        
        try:
            # Check if file exists
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Excel file not found at {self.file_path}")
            
            # Read Excel file with explicit engine specification
            try:
                df = pd.read_excel(self.file_path, engine='openpyxl')
            except ImportError as ie:
                raise ImportError(f"openpyxl is required for Excel file reading. Please install: pip install openpyxl. Error: {ie}")
            
            # Fill NaN values with empty strings or appropriate defaults
            df = df.fillna('')
            
            employees = []
            
            for _, row in df.iterrows():
                # Convert mobile number safely
                mobile = str(int(row['MOBILE'])) if pd.notna(row['MOBILE']) and row['MOBILE'] != '' else ''
                
                # Convert extension safely
                extension = str(int(row['EXTENSION NUMBER'])) if pd.notna(row['EXTENSION NUMBER']) else '0'
                
                # Handle reporting ID
                reporting_id = None
                if pd.notna(row['REPORTING ID']) and str(row['REPORTING ID']).strip() != '':
                    try:
                        reporting_id = str(int(row['REPORTING ID']))
                    except (ValueError, TypeError):
                        reporting_id = None
                
                # Handle date of joining
                date_joining = ''
                if pd.notna(row['DATE OF JOINING']):
                    try:
                        date_joining = str(row['DATE OF JOINING']).split(' ')[0]
                    except:
                        date_joining = str(row['DATE OF JOINING'])
                
                employee = {
                    'id': str(row['EMP ID']),
                    'name': str(row['EMP NAME']).strip(),
                    'department': str(row['DEPARTMENT']).strip(),
                    'grade': str(row['GRADE']).strip(),
                    'reportingManager': str(row['REPORTING MANAGER']).strip() if pd.notna(row['REPORTING MANAGER']) else '*',
                    'reportingId': reporting_id,
                    'location': str(row['LOCATION']).strip(),
                    'mobile': mobile,
                    'extension': extension,
                    'email': str(row['EMAIL ID']).strip(),
                    'dateOfJoining': date_joining,
                    'profileImage': '/api/placeholder/150/150'
                }
                
                employees.append(employee)
            
            return employees
            
        except ImportError as ie:
            # Re-raise import errors with clearer message
            raise ie
        except FileNotFoundError as fe:
            # Re-raise file errors
            raise fe
        except Exception as e:
            # Log other errors but provide more context
            error_msg = f"Unexpected error parsing Excel file: {str(e)}"
            print(error_msg)
            raise RuntimeError(error_msg) from e
    
    def get_unique_departments(self) -> List[str]:
        """Get unique departments from Excel file"""
        try:
            df = pd.read_excel(self.file_path)
            departments = ['All Departments'] + sorted(list(set(df['DEPARTMENT'].dropna().astype(str).tolist())))
            return [dept.strip() for dept in departments if dept.strip()]
        except Exception as e:
            print(f"Error getting departments: {str(e)}")
            return ['All Departments']
    
    def get_unique_locations(self) -> List[str]:
        """Get unique locations from Excel file"""
        try:
            df = pd.read_excel(self.file_path)
            locations = ['All Locations'] + sorted(list(set(df['LOCATION'].dropna().astype(str).tolist())))
            return [loc.strip() for loc in locations if loc.strip()]
        except Exception as e:
            print(f"Error getting locations: {str(e)}")
            return ['All Locations']
    
    def get_file_stats(self) -> Dict[str, Any]:
        """Get statistics about the Excel file"""
        try:
            df = pd.read_excel(self.file_path)
            return {
                'total_employees': len(df),
                'departments_count': len(df['DEPARTMENT'].dropna().unique()),
                'locations_count': len(df['LOCATION'].dropna().unique()),
                'file_path': self.file_path,
                'columns': df.columns.tolist()
            }
        except Exception as e:
            return {
                'error': str(e),
                'total_employees': 0,
                'departments_count': 0,
                'locations_count': 0
            }