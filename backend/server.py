from fastapi import FastAPI, APIRouter, HTTPException, Query, UploadFile, File
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import base64
import uuid
import mimetypes

from models import (
    Employee, EmployeeCreate, EmployeeUpdate, 
    HierarchyRelation, HierarchyRelationCreate,
    RefreshResponse
)
from excel_parser import ExcelParser

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Employee Directory API", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = ROOT_DIR / "uploads" / "images"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Serve static files for images
app.mount("/uploads", StaticFiles(directory=str(ROOT_DIR / "uploads")), name="uploads")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize Excel parser
excel_parser = ExcelParser()

# Helper functions for image processing
def save_base64_image(base64_data: str, employee_id: str) -> str:
    """Convert base64 image data to file and return URL"""
    try:
        # Remove data:image/jpeg;base64, or similar prefix
        if ',' in base64_data:
            header, data = base64_data.split(',', 1)
            
            # Determine file extension from header
            if 'image/jpeg' in header or 'image/jpg' in header:
                ext = 'jpg'
            elif 'image/png' in header:
                ext = 'png'
            elif 'image/gif' in header:
                ext = 'gif'
            elif 'image/webp' in header:
                ext = 'webp'
            else:
                ext = 'jpg'  # default
        else:
            data = base64_data
            ext = 'jpg'  # default
        
        # Decode base64 data
        image_data = base64.b64decode(data)
        
        # Generate unique filename
        filename = f"{employee_id}_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = UPLOAD_DIR / filename
        
        # Save the image file
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # Return the URL path
        return f"/uploads/images/{filename}"
        
    except Exception as e:
        logging.error(f"Error saving base64 image: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image data")

def save_uploaded_file(file: UploadFile, employee_id: str) -> str:
    """Save uploaded file and return URL"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.")
        
        # Get file extension
        ext = mimetypes.guess_extension(file.content_type) or '.jpg'
        if ext.startswith('.'):
            ext = ext[1:]
        
        # Generate unique filename
        filename = f"{employee_id}_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = UPLOAD_DIR / filename
        
        # Save the file
        with open(file_path, 'wb') as buffer:
            content = file.file.read()
            buffer.write(content)
        
        # Return the URL path
        return f"/uploads/images/{filename}"
        
    except Exception as e:
        logging.error(f"Error saving uploaded file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save image file")

# Employee Management Endpoints

@api_router.get("/employees", response_model=List[Employee])
async def get_employees(
    search: Optional[str] = Query(None, description="Search term for name, id, department, location, designation, mobile"),
    department: Optional[str] = Query(None, description="Filter by department"),
    location: Optional[str] = Query(None, description="Filter by location")
):
    """Get all employees with optional search and filters"""
    try:
        # Build query
        query = {}
        
        if search:
            # Create search query for multiple fields
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"id": {"$regex": search, "$options": "i"}},
                {"department": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}},
                {"grade": {"$regex": search, "$options": "i"}},
                {"mobile": {"$regex": search, "$options": "i"}}
            ]
        
        if department and department != "All Departments":
            query["department"] = department
            
        if location and location != "All Locations":
            query["location"] = location
        
        # Get employees from database
        employees_cursor = db.employees.find(query)
        employees = await employees_cursor.to_list(1000)  # Limit to 1000 for performance
        
        # Convert MongoDB documents to Employee models
        result = []
        for emp in employees:
            emp.pop('_id', None)  # Remove MongoDB _id field
            result.append(Employee(**emp))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch employees")

@api_router.put("/employees/{employee_id}/image", response_model=Employee)
async def update_employee_image(employee_id: str, update_data: EmployeeUpdate):
    """Update employee profile image (supports URL or base64 data)"""
    try:
        image_url = update_data.profileImage
        
        # Check if it's base64 data
        if image_url.startswith('data:image/'):
            # Convert base64 to file and get URL
            image_url = save_base64_image(image_url, employee_id)
        
        # Update employee in database
        result = await db.employees.update_one(
            {"id": employee_id},
            {
                "$set": {
                    "profileImage": image_url,
                    "lastUpdated": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Get updated employee
        employee_doc = await db.employees.find_one({"id": employee_id})
        if not employee_doc:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        employee_doc.pop('_id', None)
        return Employee(**employee_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating employee image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update employee image")

@api_router.post("/employees/{employee_id}/upload-image", response_model=Employee)
async def upload_employee_image(employee_id: str, file: UploadFile = File(...)):
    """Upload employee profile image file"""
    try:
        # Save uploaded file
        image_url = save_uploaded_file(file, employee_id)
        
        # Update employee in database
        result = await db.employees.update_one(
            {"id": employee_id},
            {
                "$set": {
                    "profileImage": image_url,
                    "lastUpdated": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Get updated employee
        employee_doc = await db.employees.find_one({"id": employee_id})
        if not employee_doc:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        employee_doc.pop('_id', None)
        return Employee(**employee_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error uploading employee image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload employee image")

@api_router.post("/refresh-excel", response_model=RefreshResponse)
async def refresh_excel_data():
    """Sync with Excel file data"""
    try:
        # Parse Excel file
        employees_data = excel_parser.parse_excel_to_employees()
        
        # Clear existing employees
        await db.employees.delete_many({})
        
        # Insert new employees
        if employees_data:
            # Convert to proper format for MongoDB
            for emp in employees_data:
                emp['lastUpdated'] = datetime.utcnow()
            
            await db.employees.insert_many(employees_data)
        
        return RefreshResponse(
            message="Data refreshed successfully",
            count=len(employees_data)
        )
        
    except Exception as e:
        logging.error(f"Error refreshing Excel data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh data: {str(e)}")

# Hierarchy Management Endpoints

@api_router.get("/hierarchy", response_model=List[HierarchyRelation])
async def get_hierarchy():
    """Fetch all reporting relationships"""
    try:
        hierarchy_cursor = db.hierarchy.find()
        hierarchy_docs = await hierarchy_cursor.to_list(1000)
        
        result = []
        for doc in hierarchy_docs:
            doc.pop('_id', None)
            result.append(HierarchyRelation(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching hierarchy: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch hierarchy")

@api_router.post("/hierarchy", response_model=HierarchyRelation)
async def add_hierarchy_relation(relation: HierarchyRelationCreate):
    """Add new reporting relationship"""
    try:
        # Check if relationship already exists
        existing = await db.hierarchy.find_one({"employeeId": relation.employeeId})
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Employee already has a reporting relationship"
            )
        
        # Verify both employees exist
        employee = await db.employees.find_one({"id": relation.employeeId})
        manager = await db.employees.find_one({"id": relation.reportsTo})
        
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        
        # Create new relationship
        new_relation = HierarchyRelation(
            employeeId=relation.employeeId,
            reportsTo=relation.reportsTo
        )
        
        # Insert into database
        relation_dict = new_relation.dict()
        await db.hierarchy.insert_one(relation_dict)
        
        return new_relation
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error adding hierarchy relation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add hierarchy relation")

@api_router.delete("/hierarchy/clear")
async def clear_all_hierarchy():
    """Clear all reporting relationships"""
    try:
        result = await db.hierarchy.delete_many({})
        
        return {
            "message": "All hierarchy relations cleared",
            "count": result.deleted_count
        }
        
    except Exception as e:
        logging.error(f"Error clearing hierarchy: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear hierarchy")

@api_router.delete("/hierarchy/{employee_id}")
async def remove_hierarchy_relation(employee_id: str):
    """Remove reporting relationship"""
    try:
        result = await db.hierarchy.delete_one({"employeeId": employee_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Hierarchy relation not found")
        
        return {"message": "Hierarchy relation removed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error removing hierarchy relation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to remove hierarchy relation")

# Utility Endpoints

@api_router.get("/departments")
async def get_departments():
    """Get unique departments"""
    try:
        departments = excel_parser.get_unique_departments()
        return {"departments": departments}
    except Exception as e:
        logging.error(f"Error getting departments: {str(e)}")
        return {"departments": ["All Departments"]}

@api_router.get("/locations")
async def get_locations():
    """Get unique locations"""
    try:
        locations = excel_parser.get_unique_locations()
        return {"locations": locations}
    except Exception as e:
        logging.error(f"Error getting locations: {str(e)}")
        return {"locations": ["All Locations"]}

@api_router.get("/stats")
async def get_stats():
    """Get Excel file and database statistics"""
    try:
        excel_stats = excel_parser.get_file_stats()
        
        # Get database counts
        emp_count = await db.employees.count_documents({})
        hierarchy_count = await db.hierarchy.count_documents({})
        
        return {
            "excel": excel_stats,
            "database": {
                "employees": emp_count,
                "hierarchy_relations": hierarchy_count
            }
        }
    except Exception as e:
        logging.error(f"Error getting stats: {str(e)}")
        return {"error": str(e)}

# Legacy endpoint for backward compatibility
@api_router.get("/")
async def root():
    return {"message": "Employee Directory API is running"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database with Excel data on startup
@app.on_event("startup")
async def startup_db():
    """Initialize database with Excel data if empty"""
    try:
        # Check if employees collection is empty
        count = await db.employees.count_documents({})
        if count == 0:
            logger.info("Database empty, loading Excel data...")
            employees_data = excel_parser.parse_excel_to_employees()
            
            if employees_data:
                # Add timestamps
                for emp in employees_data:
                    emp['lastUpdated'] = datetime.utcnow()
                
                await db.employees.insert_many(employees_data)
                logger.info(f"Loaded {len(employees_data)} employees from Excel")
            else:
                logger.warning("No employee data found in Excel file")
        else:
            logger.info(f"Database already has {count} employees")
            
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()