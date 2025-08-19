#!/usr/bin/env python3
"""
Script to force reload Excel data - clears database and reloads from Excel
Usage: python force_excel_load.py
"""
import asyncio
import os
import logging
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from excel_parser import ExcelParser
from attendance_parser import parse_attendance_excel
from datetime import datetime

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def force_reload_data():
    """Clear database and reload from Excel files"""
    try:
        # MongoDB connection
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        db_name = os.environ.get('DB_NAME', 'test_database')
        
        logger.info(f"Connecting to MongoDB: {mongo_url}")
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Test connection
        await client.admin.command('ismaster')
        logger.info("Successfully connected to MongoDB")
        
        # Clear existing data
        logger.info("Clearing existing employee data...")
        await db.employees.delete_many({})
        logger.info("Cleared employee data")
        
        logger.info("Clearing existing attendance data...")
        await db.attendance.delete_many({})
        logger.info("Cleared attendance data")
        
        # Clear other collections if needed
        collections_to_clear = ['news', 'tasks', 'knowledge', 'help', 'policies', 'meeting_rooms', 'hierarchy']
        for collection_name in collections_to_clear:
            await db[collection_name].delete_many({})
            logger.info(f"Cleared {collection_name} data")
        
        # Load Excel data
        logger.info("Loading Excel data...")
        excel_parser = ExcelParser()
        
        # Load employee data
        try:
            employees_data = excel_parser.parse_excel_to_employees()
            
            if employees_data and len(employees_data) > 0:
                # Add timestamps
                for emp in employees_data:
                    emp['lastUpdated'] = datetime.utcnow()
                
                await db.employees.insert_many(employees_data)
                logger.info(f"Successfully loaded {len(employees_data)} employees from Excel")
            else:
                logger.warning("No employee data found in Excel file")
                
        except Exception as excel_error:
            logger.error(f"Excel parsing error: {str(excel_error)}")
            # Check file existence
            excel_file_path = ROOT_DIR / "employee_directory.xlsx"
            if excel_file_path.exists():
                logger.info(f"Excel file exists at: {excel_file_path}")
            else:
                fallback_path = ROOT_DIR.parent / "employee_directory.xlsx"
                if fallback_path.exists():
                    logger.info(f"Excel file found at fallback location: {fallback_path}")
                else:
                    logger.error(f"Excel file not found at: {excel_file_path} or {fallback_path}")
        
        # Load attendance data
        try:
            logger.info("Loading attendance data from Excel...")
            attendance_data = parse_attendance_excel()
            if attendance_data and len(attendance_data) > 0:
                await db.attendance.insert_many(attendance_data)
                logger.info(f"Successfully loaded {len(attendance_data)} attendance records from Excel")
            else:
                logger.warning("No attendance data found in Excel file")
        except Exception as attendance_error:
            logger.error(f"Attendance parsing error: {str(attendance_error)}")
        
        # Initialize meeting rooms data
        try:
            logger.info("Initializing meeting rooms...")
            meeting_rooms_data = [
                # IFC Location - Floor 11
                {"id": "ifc_conf_11a", "name": "IFC Conference Room 11A", "location": "IFC", "floor": 11, "capacity": 8, "equipment": "Projector, Whiteboard", "status": "vacant", "bookings": []},
                
                # IFC Location - Floor 12  
                {"id": "ifc_conf_12a", "name": "IFC Conference Room 12A", "location": "IFC", "floor": 12, "capacity": 12, "equipment": "Video Conference, Projector", "status": "vacant", "bookings": []},
                
                # IFC Location - Floor 14 (9 rooms with updated names)
                {"id": "ifc_oval_14", "name": "OVAL MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 10, "equipment": "Smart Board, Video Conference", "status": "vacant", "bookings": []},
                {"id": "ifc_petronas_14", "name": "PETRONAS MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Projector, Whiteboard", "status": "vacant", "bookings": []},
                {"id": "ifc_global_14", "name": "GLOBAL CENTER MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Video Conference", "status": "vacant", "bookings": []},
                {"id": "ifc_louvre_14", "name": "LOUVRE MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Projector", "status": "vacant", "bookings": []},
                {"id": "ifc_golden_14", "name": "GOLDEN GATE MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 10, "equipment": "Smart Board", "status": "vacant", "bookings": []},
                {"id": "ifc_empire_14", "name": "EMPIRE STATE MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Whiteboard", "status": "vacant", "bookings": []},
                {"id": "ifc_marina_14", "name": "MARINA BAY MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Projector, Whiteboard", "status": "vacant", "bookings": []},
                {"id": "ifc_burj_14", "name": "BURJ MEETING ROOM", "location": "IFC", "floor": 14, "capacity": 5, "equipment": "Video Conference", "status": "vacant", "bookings": []},
                {"id": "ifc_board_14", "name": "BOARD ROOM", "location": "IFC", "floor": 14, "capacity": 20, "equipment": "Large Screen, Video Conference, Smart Board", "status": "vacant", "bookings": []},
                
                # Other locations with 1 room each
                {"id": "central_conf_1", "name": "Central Office Conference Room", "location": "Central Office 75", "floor": 1, "capacity": 6, "equipment": "Projector", "status": "vacant", "bookings": []},
                {"id": "office75_conf_1", "name": "Office 75 Meeting Room", "location": "Office 75", "floor": 1, "capacity": 4, "equipment": "Whiteboard", "status": "vacant", "bookings": []},
                {"id": "noida_conf_1", "name": "Noida Conference Room", "location": "Noida", "floor": 1, "capacity": 10, "equipment": "Video Conference, Projector", "status": "vacant", "bookings": []},
                {"id": "project_conf_1", "name": "Project Office Meeting Room", "location": "Project Office", "floor": 1, "capacity": 8, "equipment": "Projector, Whiteboard", "status": "vacant", "bookings": []}
            ]
            
            await db.meeting_rooms.insert_many(meeting_rooms_data)
            logger.info(f"Initialized {len(meeting_rooms_data)} meeting rooms")
            
        except Exception as room_error:
            logger.error(f"Meeting room initialization error: {str(room_error)}")
        
        logger.info("Database force reload completed successfully!")
        
        # Final count verification
        emp_count = await db.employees.count_documents({})
        att_count = await db.attendance.count_documents({})
        room_count = await db.meeting_rooms.count_documents({})
        
        logger.info(f"Final counts - Employees: {emp_count}, Attendance: {att_count}, Meeting Rooms: {room_count}")
        
    except Exception as e:
        logger.error(f"Error during force reload: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(force_reload_data())