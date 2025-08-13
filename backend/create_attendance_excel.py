#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Sample locations for punch in/out
locations = ["IFC Office", "Remote", "Client Site", "Branch Office", "Central Office 75", "Office 75", "Noida", "Project Office"]

# Sample employee IDs (using some from the existing 640 employees)
employee_ids = [
    "80001", "80002", "80003", "80004", "80005", "80006", "80007", "80008", "80009", "80010",
    "80011", "80012", "80013", "80014", "80015", "80016", "80017", "80018", "80019", "80020",
    "80021", "80022", "80023", "80024", "80025", "80026", "80027", "80028", "80029", "80030"
]

# Sample employee names
employee_names = [
    "Aarav Sharma", "Aditi Patel", "Akash Kumar", "Ananya Singh", "Arjun Verma", "Deepika Jain", 
    "Gaurav Gupta", "Isha Agarwal", "Karan Mehta", "Meera Reddy", "Nikhil Shah", "Pooja Thakur",
    "Rahul Joshi", "Riya Kapoor", "Siddharth Rao", "Sneha Nair", "Tanvi Mishra", "Uday Pandey",
    "Varun Sinha", "Yash Aggarwal", "Anjali Desai", "Harsh Bansal", "Ishita Malhotra", "Kunal Roy",
    "Nisha Sharma", "Rajesh Kumar", "Saniya Khan", "Tarun Singh", "Vanya Jain", "Zara Patel"
]

# Generate attendance data for the last 30 days
attendance_data = []
start_date = datetime.now() - timedelta(days=30)

for day_offset in range(30):
    current_date = start_date + timedelta(days=day_offset)
    
    # Skip weekends for most employees (Saturday = 5, Sunday = 6)
    if current_date.weekday() >= 5:
        continue
    
    # Generate attendance for random employees each day (70-90% attendance rate)
    daily_employees = random.sample(list(zip(employee_ids, employee_names)), random.randint(21, 27))
    
    for emp_id, emp_name in daily_employees:
        # Random punch in time (8:30 AM to 10:30 AM)
        punch_in_hour = random.randint(8, 10)
        punch_in_minute = random.choice([0, 15, 30, 45])
        
        # Adjust for late arrivals
        if punch_in_hour >= 10:
            punch_in_minute = random.choice([0, 15, 30])
        
        punch_in_time = current_date.replace(hour=punch_in_hour, minute=punch_in_minute, second=0)
        
        # Random punch out time (5:00 PM to 8:00 PM)
        punch_out_hour = random.randint(17, 20)
        punch_out_minute = random.choice([0, 15, 30, 45])
        punch_out_time = current_date.replace(hour=punch_out_hour, minute=punch_out_minute, second=0)
        
        # Determine status based on punch in time
        if punch_in_hour <= 9:
            status = "present"
        elif punch_in_hour == 10 and punch_in_minute <= 30:
            status = random.choice(["present", "late"])
        else:
            status = "late"
        
        # Sometimes mark as half day
        if random.random() < 0.05:  # 5% chance
            status = "half_day"
            punch_out_hour = random.randint(13, 15)
            punch_out_time = current_date.replace(hour=punch_out_hour, minute=punch_out_minute, second=0)
        
        # Random locations
        punch_in_location = random.choice(locations)
        punch_out_location = punch_in_location if random.random() < 0.8 else random.choice(locations)
        
        # Calculate total hours
        total_hours = (punch_out_time - punch_in_time).total_seconds() / 3600
        
        # Generate remarks occasionally
        remarks_options = [
            "", "", "", "",  # Empty remarks for most entries
            "Client meeting", "Training session", "Project work", "Team meeting",
            "Late due to traffic", "Medical appointment", "Working from home",
            "Conference call", "Site visit", "Documentation work"
        ]
        remarks = random.choice(remarks_options)
        
        attendance_data.append({
            "employee_id": emp_id,
            "employee_name": emp_name,
            "date": current_date.strftime("%Y-%m-%d"),
            "punch_in": punch_in_time.strftime("%Y-%m-%d %H:%M:%S"),
            "punch_out": punch_out_time.strftime("%Y-%m-%d %H:%M:%S"),
            "punch_in_location": punch_in_location,
            "punch_out_location": punch_out_location,
            "status": status,
            "total_hours": round(total_hours, 2),
            "remarks": remarks
        })

# Create DataFrame
df = pd.DataFrame(attendance_data)

# Sort by date and employee_id
df = df.sort_values(['date', 'employee_id'])

# Save to Excel
output_path = '/app/backend/attendance_data.xlsx'
df.to_excel(output_path, index=False, sheet_name='Attendance')

print(f"✅ Attendance Excel file created successfully!")
print(f"📊 Generated {len(df)} attendance records")
print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"👥 Employees: {df['employee_id'].nunique()} unique employees")
print(f"📍 File saved at: {output_path}")

# Display sample data
print("\n📋 Sample data:")
print(df.head(10).to_string(index=False))