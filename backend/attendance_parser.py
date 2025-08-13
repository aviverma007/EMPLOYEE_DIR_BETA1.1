import pandas as pd
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

def parse_attendance_excel():
    """Parse attendance data from Excel file"""
    try:
        # Try to find the Excel file in multiple locations
        possible_paths = [
    '/app/backend/attendance_data.xlsx',
    '/app/attendance_data.xlsx',
    r'C:\EmployeeDirectoryServer\EMPLOYEE_DIR\backend\attendance_data.xlsx'
]
        
        excel_path = None
        for path in possible_paths:
            if os.path.exists(path):
                excel_path = path
                break
        
        if not excel_path:
            logger.warning("Attendance Excel file not found")
            return []
        
        logger.info(f"Loading attendance data from: {excel_path}")
        
        # Read Excel file
        df = pd.read_excel(excel_path, sheet_name='Attendance')
        
        attendance_records = []
        for _, row in df.iterrows():
            try:
                # Parse dates and times
                date_str = str(row['date'])
                if 'T' in date_str:
                    date_obj = datetime.fromisoformat(date_str.replace('T', ' '))
                    date_formatted = date_obj.strftime('%Y-%m-%d')
                else:
                    date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
                    date_formatted = date_obj.strftime('%Y-%m-%d')
                
                # Parse punch in time  
                punch_in_str = str(row['punch_in'])
                if punch_in_str and punch_in_str != 'nan':
                    punch_in = datetime.fromisoformat(punch_in_str.replace('T', ' '))
                else:
                    punch_in = None
                
                # Parse punch out time
                punch_out_str = str(row['punch_out'])
                if punch_out_str and punch_out_str != 'nan':
                    punch_out = datetime.fromisoformat(punch_out_str.replace('T', ' '))
                else:
                    punch_out = None
                
                record = {
                    'id': f"att_{len(attendance_records) + 1:04d}",
                    'employee_id': str(row['employee_id']),
                    'employee_name': str(row['employee_name']),
                    'date': date_formatted,
                    'punch_in': punch_in.isoformat() if punch_in else None,
                    'punch_out': punch_out.isoformat() if punch_out else None,
                    'punch_in_location': str(row['punch_in_location']) if pd.notna(row['punch_in_location']) else None,
                    'punch_out_location': str(row['punch_out_location']) if pd.notna(row['punch_out_location']) else None,
                    'status': str(row['status']).lower(),
                    'total_hours': float(row['total_hours']) if pd.notna(row['total_hours']) else 0.0,
                    'remarks': str(row['remarks']) if pd.notna(row['remarks']) and str(row['remarks']) != 'nan' else None,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                attendance_records.append(record)
                
            except Exception as e:
                logger.error(f"Error parsing attendance row: {e}")
                continue
        
        logger.info(f"Successfully parsed {len(attendance_records)} attendance records")
        return attendance_records
        
    except Exception as e:
        logger.error(f"Error loading attendance Excel file: {e}")
        return []

def get_sample_attendance_data():
    """Get sample attendance data if Excel file is not available"""
    from datetime import datetime, timedelta
    import random
    
    # Sample data for testing
    sample_employees = [
        ("80001", "Aarav Sharma"),
        ("80002", "Aditi Patel"), 
        ("80003", "Akash Kumar"),
        ("80004", "Ananya Singh"),
        ("80005", "Arjun Verma")
    ]
    
    locations = ["IFC Office", "Remote", "Client Site", "Branch Office"]
    statuses = ["present", "late", "half_day"]
    
    attendance_records = []
    
    # Generate last 7 days of data
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        if date.weekday() < 5:  # Only weekdays
            for j, (emp_id, emp_name) in enumerate(sample_employees[:3]):  # First 3 employees
                punch_in = date.replace(hour=9, minute=random.randint(0, 30))
                punch_out = date.replace(hour=17, minute=random.randint(30, 59))
                
                record = {
                    'id': f"att_{len(attendance_records) + 1:04d}",
                    'employee_id': emp_id,
                    'employee_name': emp_name,
                    'date': date.strftime('%Y-%m-%d'),
                    'punch_in': punch_in.isoformat(),
                    'punch_out': punch_out.isoformat(),
                    'punch_in_location': random.choice(locations),
                    'punch_out_location': random.choice(locations),
                    'status': random.choice(statuses),
                    'total_hours': round((punch_out - punch_in).total_seconds() / 3600, 2),
                    'remarks': None,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                attendance_records.append(record)
    
    return attendance_records