from fastapi import FastAPI, APIRouter, HTTPException, Query, UploadFile, File
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone
import base64
import uuid
import mimetypes

from models import (
    Employee, EmployeeCreate, EmployeeUpdate, 
    HierarchyRelation, HierarchyRelationCreate,
    RefreshResponse,
    News, NewsCreate, NewsUpdate,
    Task, TaskCreate, TaskUpdate,
    Knowledge, KnowledgeCreate, KnowledgeUpdate,
    Help, HelpCreate, HelpUpdate, HelpReply, HelpReplyCreate,
    MeetingRoom, MeetingRoomCreate, MeetingRoomUpdate, MeetingRoomBooking, MeetingRoomBookingCreate, MeetingRoomBulkBookingCreate,
    Policy, PolicyCreate, PolicyUpdate,
    Workflow, WorkflowCreate, WorkflowUpdate, WorkflowStep,
    AttendanceRecord, AttendanceCreate, AttendanceUpdate
)
from excel_parser import ExcelParser
from attendance_parser import parse_attendance_excel

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Employee Directory API", version="1.0.0")

# Create uploads directory if it doesn't exist - make it persistent
UPLOAD_DIR = ROOT_DIR / "uploads" / "images"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Ensure proper permissions for upload directory
import stat
try:
    UPLOAD_DIR.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
except:
    pass  # Ignore permission errors on some systems

# Serve static files for images
app.mount("/api/uploads", StaticFiles(directory=str(ROOT_DIR / "uploads")), name="uploads")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize Excel parser
excel_parser = ExcelParser()

# Helper function for datetime normalization
def normalize_datetime(dt_input):
    """Convert various datetime inputs to naive UTC datetime for comparison"""
    if isinstance(dt_input, str):
        # Handle ISO format strings
        if 'T' in dt_input:
            # Remove 'Z' and replace with UTC offset if present
            dt_str = dt_input.replace('Z', '+00:00')
            dt_obj = datetime.fromisoformat(dt_str)
        else:
            # Handle simple datetime strings
            dt_obj = datetime.fromisoformat(dt_input)
        # Convert to naive UTC
        if dt_obj.tzinfo is not None:
            dt_obj = dt_obj.astimezone(timezone.utc).replace(tzinfo=None)
        return dt_obj
    elif isinstance(dt_input, datetime):
        # Handle datetime objects
        if dt_input.tzinfo is not None:
            return dt_input.astimezone(timezone.utc).replace(tzinfo=None)
        return dt_input
    else:
        raise ValueError(f"Unsupported datetime type: {type(dt_input)}")

# Helper functions for image processing
def save_base64_image(base64_data: str, employee_id: str) -> str:
    """Convert base64 image data to file and save with employee ID as filename"""
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
        
        # Use employee ID as filename (replace any existing image)
        filename = f"{employee_id}.{ext}"
        file_path = UPLOAD_DIR / filename
        
        # Remove any existing image files for this employee first
        for existing_file in UPLOAD_DIR.glob(f"{employee_id}*"):
            try:
                existing_file.unlink()
                logging.info(f"Removed existing image file: {existing_file}")
            except Exception as e:
                logging.warning(f"Could not remove existing file {existing_file}: {e}")
        
        # Save the new image file
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # Set proper file permissions
        try:
            file_path.chmod(0o644)
        except:
            pass
        
        logging.info(f"Successfully saved image for employee {employee_id} as {filename} ({len(image_data)} bytes)")
        return f"/api/uploads/images/{filename}"
        
    except Exception as e:
        logging.error(f"Error saving base64 image for employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to save image: {str(e)}")

def save_uploaded_file(file: UploadFile, employee_id: str) -> str:
    """Save uploaded file with employee ID as filename"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.")
        
        # Get file extension
        ext = mimetypes.guess_extension(file.content_type) or '.jpg'
        if ext.startswith('.'):
            ext = ext[1:]
        
        # Use employee ID as filename (replace any existing image)
        filename = f"{employee_id}.{ext}"
        file_path = UPLOAD_DIR / filename
        
        # Remove any existing image files for this employee first
        for existing_file in UPLOAD_DIR.glob(f"{employee_id}*"):
            try:
                existing_file.unlink()
                logging.info(f"Removed existing image file: {existing_file}")
            except Exception as e:
                logging.warning(f"Could not remove existing file {existing_file}: {e}")
        
        # Save the new file
        with open(file_path, 'wb') as buffer:
            # Reset file pointer to beginning and read all content
            file.file.seek(0)
            content = file.file.read()
            buffer.write(content)
        
        # Set proper file permissions
        try:
            file_path.chmod(0o644)
        except:
            pass
        
        logging.info(f"Successfully saved uploaded file for employee {employee_id} as {filename} ({len(content)} bytes)")
        return f"/api/uploads/images/{filename}"
        
    except Exception as e:
        logging.error(f"Error saving uploaded file for employee {employee_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save image file: {str(e)}")

def get_employee_image_url(employee_id: str) -> Optional[str]:
    """Get employee profile image URL if file exists on filesystem"""
    try:
        # Check for any image file with the employee ID as filename
        for ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            file_path = UPLOAD_DIR / f"{employee_id}.{ext}"
            if file_path.exists():
                # Return the full URL that includes the API prefix for proper routing
                image_url = f"/api/uploads/images/{employee_id}.{ext}"
                logging.debug(f"Found image for employee {employee_id}: {image_url}")
                return image_url
        
        # Check for legacy files with random suffixes (for cleanup)
        legacy_files = list(UPLOAD_DIR.glob(f"{employee_id}_*"))
        if legacy_files:
            logging.warning(f"Found {len(legacy_files)} legacy image files for employee {employee_id}, consider cleanup")
        
        # No image file found
        logging.debug(f"No image file found for employee {employee_id}")
        return None
        
    except Exception as e:
        logging.error(f"Error getting employee image URL for {employee_id}: {str(e)}")
        return None

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
            # Create search query for multiple fields using "starts with" pattern
            query["$or"] = [
                {"name": {"$regex": f"^{search}", "$options": "i"}},
                {"id": {"$regex": f"^{search}", "$options": "i"}},
                {"department": {"$regex": f"^{search}", "$options": "i"}},
                {"location": {"$regex": f"^{search}", "$options": "i"}},
                {"grade": {"$regex": f"^{search}", "$options": "i"}},
                {"mobile": {"$regex": f"^{search}", "$options": "i"}}
            ]
        
        if department and department != "All Departments":
            query["department"] = department
            
        if location and location != "All Locations":
            query["location"] = location
        
        # Get employees from database
        employees_cursor = db.employees.find(query)
        employees = await employees_cursor.to_list(1000)  # Limit to 1000 for performance
        
        # Convert MongoDB documents to Employee models and set dynamic profile images
        result = []
        for emp in employees:
            emp.pop('_id', None)  # Remove MongoDB _id field
            # Set dynamic profile image URL based on filesystem
            emp['profileImage'] = get_employee_image_url(emp['id']) or "/api/placeholder/150/150"
            result.append(Employee(**emp))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch employees")

@api_router.put("/employees/{employee_id}/image", response_model=Employee)
async def update_employee_image(employee_id: str, update_data: EmployeeUpdate):
    """Update employee profile image (saves to filesystem, not database)"""
    try:
        image_data = update_data.profileImage
        
        # Check if it's base64 data and save to filesystem
        if image_data.startswith('data:image/'):
            # Save base64 image to filesystem with employee ID as filename
            save_base64_image(image_data, employee_id)
        else:
            # If it's a URL, we don't save it - just indicate success
            pass
        
        # Update employee record with timestamp (no URL stored)
        result = await db.employees.update_one(
            {"id": employee_id},
            {
                "$set": {
                    "lastUpdated": datetime.utcnow(),
                    "hasProfileImage": True
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
        
        # Set dynamic profile image URL based on filesystem
        employee_doc['profileImage'] = get_employee_image_url(employee_id) or "/api/placeholder/150/150"
        
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
        save_uploaded_file(file, employee_id)
        
        # Update employee in database with timestamp (no URL stored)
        result = await db.employees.update_one(
            {"id": employee_id},
            {
                "$set": {
                    "lastUpdated": datetime.utcnow(),
                    "hasProfileImage": True
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
        
        # Set dynamic profile image URL based on filesystem
        employee_doc['profileImage'] = get_employee_image_url(employee_id) or "/api/placeholder/150/150"
        
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

# News Management Endpoints

@api_router.get("/news", response_model=List[News])
async def get_news():
    """Get all news items"""
    try:
        news_cursor = db.news.find().sort("created_at", -1)
        news_docs = await news_cursor.to_list(100)
        
        result = []
        for doc in news_docs:
            doc.pop('_id', None)
            result.append(News(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")

@api_router.post("/news", response_model=News)
async def create_news(news: NewsCreate):
    """Create new news item"""
    try:
        new_news = News(
            title=news.title,
            content=news.content,
            priority=news.priority
        )
        
        news_dict = new_news.dict()
        await db.news.insert_one(news_dict)
        
        return new_news
        
    except Exception as e:
        logging.error(f"Error creating news: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create news")

@api_router.put("/news/{news_id}", response_model=News)
async def update_news(news_id: str, news: NewsUpdate):
    """Update news item"""
    try:
        update_data = {k: v for k, v in news.dict().items() if v is not None}
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.news.update_one(
                {"id": news_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="News item not found")
        
        # Get updated news
        news_doc = await db.news.find_one({"id": news_id})
        if not news_doc:
            raise HTTPException(status_code=404, detail="News item not found")
        
        news_doc.pop('_id', None)
        return News(**news_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating news: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update news")

@api_router.delete("/news/{news_id}")
async def delete_news(news_id: str):
    """Delete news item"""
    try:
        result = await db.news.delete_one({"id": news_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="News item not found")
        
        return {"message": "News item deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting news: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete news")

# Task Management Endpoints

@api_router.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    try:
        tasks_cursor = db.tasks.find().sort("created_at", -1)
        tasks_docs = await tasks_cursor.to_list(200)
        
        result = []
        for doc in tasks_docs:
            doc.pop('_id', None)
            result.append(Task(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")

@api_router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    """Create new task"""
    try:
        # Parse due_date if provided
        due_date = None
        if task.due_date:
            try:
                due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
            except:
                due_date = datetime.fromisoformat(task.due_date)
        
        new_task = Task(
            title=task.title,
            description=task.description,
            assigned_to=task.assigned_to,
            priority=task.priority,
            status=task.status,
            due_date=due_date
        )
        
        task_dict = new_task.dict()
        await db.tasks.insert_one(task_dict)
        
        return new_task
        
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create task")

@api_router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate):
    """Update task"""
    try:
        update_data = {k: v for k, v in task.dict().items() if v is not None}
        
        # Handle due_date parsing
        if 'due_date' in update_data and update_data['due_date']:
            try:
                update_data['due_date'] = datetime.fromisoformat(update_data['due_date'].replace('Z', '+00:00'))
            except:
                update_data['due_date'] = datetime.fromisoformat(update_data['due_date'])
        
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.tasks.update_one(
                {"id": task_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Task not found")
        
        # Get updated task
        task_doc = await db.tasks.find_one({"id": task_id})
        if not task_doc:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task_doc.pop('_id', None)
        return Task(**task_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task")

@api_router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete task"""
    try:
        result = await db.tasks.delete_one({"id": task_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": "Task deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete task")

# Knowledge Management Endpoints

@api_router.get("/knowledge", response_model=List[Knowledge])
async def get_knowledge():
    """Get all knowledge articles"""
    try:
        knowledge_cursor = db.knowledge.find().sort("created_at", -1)
        knowledge_docs = await knowledge_cursor.to_list(100)
        
        result = []
        for doc in knowledge_docs:
            doc.pop('_id', None)
            result.append(Knowledge(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch knowledge articles")

@api_router.post("/knowledge", response_model=Knowledge)
async def create_knowledge(knowledge: KnowledgeCreate):
    """Create new knowledge article"""
    try:
        new_knowledge = Knowledge(
            title=knowledge.title,
            content=knowledge.content,
            category=knowledge.category,
            tags=knowledge.tags
        )
        
        knowledge_dict = new_knowledge.dict()
        await db.knowledge.insert_one(knowledge_dict)
        
        return new_knowledge
        
    except Exception as e:
        logging.error(f"Error creating knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create knowledge article")

@api_router.put("/knowledge/{knowledge_id}", response_model=Knowledge)
async def update_knowledge(knowledge_id: str, knowledge: KnowledgeUpdate):
    """Update knowledge article"""
    try:
        update_data = {k: v for k, v in knowledge.dict().items() if v is not None}
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.knowledge.update_one(
                {"id": knowledge_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Knowledge article not found")
        
        # Get updated knowledge
        knowledge_doc = await db.knowledge.find_one({"id": knowledge_id})
        if not knowledge_doc:
            raise HTTPException(status_code=404, detail="Knowledge article not found")
        
        knowledge_doc.pop('_id', None)
        return Knowledge(**knowledge_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update knowledge article")

@api_router.delete("/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: str):
    """Delete knowledge article"""
    try:
        result = await db.knowledge.delete_one({"id": knowledge_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Knowledge article not found")
        
        return {"message": "Knowledge article deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete knowledge article")

# Help/Support Management Endpoints

@api_router.get("/help", response_model=List[Help])
async def get_help_requests():
    """Get all help requests"""
    try:
        help_cursor = db.help.find().sort("created_at", -1)
        help_docs = await help_cursor.to_list(100)
        
        result = []
        for doc in help_docs:
            doc.pop('_id', None)
            result.append(Help(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching help requests: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch help requests")

@api_router.post("/help", response_model=Help)
async def create_help_request(help: HelpCreate):
    """Create new help request"""
    try:
        new_help = Help(
            title=help.title,
            message=help.message,
            priority=help.priority
        )
        
        help_dict = new_help.dict()
        await db.help.insert_one(help_dict)
        
        return new_help
        
    except Exception as e:
        logging.error(f"Error creating help request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create help request")

@api_router.put("/help/{help_id}", response_model=Help)
async def update_help_request(help_id: str, help: HelpUpdate):
    """Update help request status"""
    try:
        update_data = {k: v for k, v in help.dict().items() if v is not None}
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.help.update_one(
                {"id": help_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Help request not found")
        
        # Get updated help request
        help_doc = await db.help.find_one({"id": help_id})
        if not help_doc:
            raise HTTPException(status_code=404, detail="Help request not found")
        
        help_doc.pop('_id', None)
        return Help(**help_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating help request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update help request")

@api_router.post("/help/{help_id}/reply", response_model=Help)
async def add_help_reply(help_id: str, reply: HelpReplyCreate):
    """Add reply to help request"""
    try:
        new_reply = HelpReply(message=reply.message)
        
        result = await db.help.update_one(
            {"id": help_id},
            {
                "$push": {"replies": new_reply.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Help request not found")
        
        # Get updated help request
        help_doc = await db.help.find_one({"id": help_id})
        if not help_doc:
            raise HTTPException(status_code=404, detail="Help request not found")
        
        help_doc.pop('_id', None)
        return Help(**help_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error adding help reply: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add reply")

@api_router.delete("/help/{help_id}")
async def delete_help_request(help_id: str):
    """Delete help request"""
    try:
        result = await db.help.delete_one({"id": help_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Help request not found")
        
        return {"message": "Help request deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting help request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete help request")

# Helper function for meeting room cleanup
async def cleanup_expired_bookings():
    """Clean up expired meeting room bookings and update room statuses"""
    try:
        current_time = datetime.utcnow()
        
        # Find all rooms with bookings
        rooms_with_bookings = await db.meeting_rooms.find({}).to_list(None)
        
        for room in rooms_with_bookings:
            bookings = room.get('bookings', [])
            if not bookings:
                continue
                
            # Remove expired bookings and find current active booking
            active_bookings = []
            current_booking = None
            room_status = "vacant"
            
            for booking in bookings:
                end_time = booking.get('end_time')
                start_time = booking.get('start_time')
                
                if not end_time or not start_time:
                    continue
                    
                # Convert to naive datetime for consistent comparison
                end_time = normalize_datetime(end_time)
                start_time = normalize_datetime(start_time)
                
                # Keep non-expired bookings (use naive UTC current_time)
                if end_time >= current_time:
                    active_bookings.append(booking)
                    
                    # Check if this booking is currently active
                    if start_time <= current_time <= end_time:
                        current_booking = booking
                        room_status = "occupied"
            
            # Update room if there were changes
            if len(active_bookings) != len(bookings) or room.get('status') != room_status:
                await db.meeting_rooms.update_one(
                    {"id": room['id']},
                    {
                        "$set": {
                            "status": room_status,
                            "current_booking": current_booking,
                            "bookings": active_bookings,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
                expired_count = len(bookings) - len(active_bookings)
                if expired_count > 0:
                    logging.info(f"Cleaned up {expired_count} expired booking(s) for room {room['id']}")
                    
    except Exception as e:
        logging.error(f"Error cleaning up expired bookings: {str(e)}")

# Meeting Room Management Endpoints

@api_router.get("/meeting-rooms", response_model=List[MeetingRoom])
async def get_meeting_rooms(
    location: Optional[str] = Query(None, description="Filter by location"),
    floor: Optional[str] = Query(None, description="Filter by floor"),
    status: Optional[str] = Query(None, description="Filter by status: vacant, occupied")
):
    """Fetch all meeting rooms with filters"""
    try:
        # Check if we need to initialize with default rooms
        count = await db.meeting_rooms.count_documents({})
        if count == 0:
            # Get available locations from Excel file
            try:
                excel_locations = excel_parser.get_unique_locations()
                # Remove 'All Locations' and get actual locations
                actual_locations = [loc for loc in excel_locations if loc != 'All Locations']
            except:
                # Fallback locations if Excel parsing fails
                actual_locations = ['IFC', 'Central Office 75', 'Office 75', 'Noida', 'Project Office']
            
            # Initialize with meeting rooms using Excel locations
            default_rooms = []
            
            # IFC Location - Multi-floor with special 14th floor rooms
            if 'IFC' in actual_locations:
                # IFC - 11th Floor (1 room)
                default_rooms.append({
                    'id': 'ifc-11-001',
                    'name': 'IFC Conference Room 11A',
                    'capacity': 8,
                    'location': 'IFC',
                    'floor': '11',
                    'status': 'vacant',
                    'current_booking': None,
                    'amenities': ['TV Screen', 'Whiteboard', 'Video Conference'],
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                
                # IFC - 12th Floor (1 room)
                default_rooms.append({
                    'id': 'ifc-12-001',
                    'name': 'IFC Meeting Room 12A',
                    'capacity': 6,
                    'location': 'IFC',
                    'floor': '12',
                    'status': 'occupied',
                    'current_booking': {
                        'id': str(uuid.uuid4()),
                        'employee_id': 'EMP001',
                        'employee_name': 'John Doe',
                        'start_time': datetime.utcnow().replace(hour=14, minute=0, second=0, microsecond=0),
                        'end_time': datetime.utcnow().replace(hour=15, minute=30, second=0, microsecond=0),
                        'remarks': 'Team sync meeting',
                        'created_at': datetime.utcnow()
                    },
                    'amenities': ['TV Screen', 'Whiteboard'],
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                
                # IFC - 14th Floor (9 special rooms as requested)
                ifc_14_rooms = [
                    {'id': 'ifc-14-001', 'name': 'OVAL MEETING ROOM', 'capacity': 10, 'amenities': ['TV Screen', 'Marker with Glass Board']},
                    {'id': 'ifc-14-002', 'name': 'PETRONAS MEETING ROOM', 'capacity': 5, 'amenities': ['Marker with Glass Board']},
                    {'id': 'ifc-14-003', 'name': 'GLOBAL CENTER MEETING ROOM', 'capacity': 5, 'amenities': ['Marker with Glass Board']},
                    {'id': 'ifc-14-004', 'name': 'LOUVRE MEETING ROOM', 'capacity': 5, 'amenities': ['TV Screen', 'Marker with Glass Board']},
                    {'id': 'ifc-14-005', 'name': 'GOLDEN GATE MEETING ROOM', 'capacity': 10, 'amenities': ['TV Screen', 'Marker with Glass Board']},
                    {'id': 'ifc-14-006', 'name': 'EMPIRE STATE MEETING ROOM', 'capacity': 5, 'amenities': ['TV Screen', 'Marker with Glass Board']},
                    {'id': 'ifc-14-007', 'name': 'MARINA BAY MEETING ROOM', 'capacity': 5, 'amenities': ['Marker with Glass Board']},
                    {'id': 'ifc-14-008', 'name': 'BURJ MEETING ROOM', 'capacity': 5, 'amenities': ['Marker with Glass Board']},
                    {'id': 'ifc-14-009', 'name': 'BOARD ROOM', 'capacity': 20, 'amenities': ['TV Screen', 'Marker with Glass Board']}
                ]
                
                for room_data in ifc_14_rooms:
                    default_rooms.append({
                        'id': room_data['id'],
                        'name': room_data['name'],
                        'capacity': room_data['capacity'],
                        'location': 'IFC',
                        'floor': '14',
                        'status': 'vacant',
                        'current_booking': None,
                        'amenities': room_data['amenities'],
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    })
            
            # Add meeting rooms for other Excel locations (1 room each)
            location_counter = 1
            for location in actual_locations:
                if location != 'IFC':  # Skip IFC as it's already handled
                    # Clean location name for ID
                    clean_location = location.lower().replace(' ', '-').replace('/', '-')
                    default_rooms.append({
                        'id': f'{clean_location}-001',
                        'name': f'{location} Meeting Room',
                        'capacity': 6,
                        'location': location,
                        'floor': '1',
                        'status': 'vacant' if location_counter % 3 != 0 else 'occupied',  # Mix of vacant/occupied
                        'current_booking': {
                            'id': str(uuid.uuid4()),
                            'employee_id': 'EMP002',
                            'employee_name': 'Jane Smith',
                            'start_time': datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0),
                            'end_time': datetime.utcnow().replace(hour=11, minute=0, second=0, microsecond=0),
                            'remarks': 'Project discussion',
                            'created_at': datetime.utcnow()
                        } if location_counter % 3 == 0 else None,
                        'amenities': ['TV Screen', 'Whiteboard'],
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    })
                    location_counter += 1
            
            await db.meeting_rooms.insert_many(default_rooms)
            logging.info(f"Initialized {len(default_rooms)} meeting rooms")
        
        # Build query filters
        query_filter = {}
        if location:
            query_filter['location'] = location
        if floor:
            query_filter['floor'] = floor
        if status:
            query_filter['status'] = status
        
        # Get filtered rooms from database
        rooms_cursor = db.meeting_rooms.find(query_filter)
        rooms_docs = await rooms_cursor.to_list(100)
        
        # Before returning rooms, clean up expired bookings
        await cleanup_expired_bookings()
        
        result = []
        for doc in rooms_docs:
            doc.pop('_id', None)
            result.append(MeetingRoom(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching meeting rooms: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch meeting rooms")

@api_router.post("/meeting-rooms/{room_id}/book", response_model=MeetingRoom)
async def book_meeting_room(room_id: str, booking: MeetingRoomBookingCreate):
    """Book a meeting room (single booking only - no multiple bookings allowed)"""
    try:
        # Validate employee exists
        employee = await db.employees.find_one({"id": booking.employee_id})
        if not employee:
            raise HTTPException(status_code=400, detail="Employee not found")
        
        # Get room
        room = await db.meeting_rooms.find_one({"id": room_id})
        if not room:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        # Check if room already has any bookings (prevent multiple bookings)
        existing_bookings = room.get('bookings', [])
        if existing_bookings:
            raise HTTPException(
                status_code=400, 
                detail="Room is already booked. Multiple bookings are not allowed. Please cancel existing booking first."
            )
        
        start_time = normalize_datetime(booking.start_time)
        end_time = normalize_datetime(booking.end_time)
        
        # Validate booking time
        if start_time >= end_time:
            raise HTTPException(status_code=400, detail="End time must be after start time")
        
        # Use UTC for current time comparison
        current_time = datetime.utcnow()
        if start_time < current_time:
            raise HTTPException(status_code=400, detail="Cannot book room for past time")
        
        # Create booking object
        new_booking = {
            'id': str(uuid.uuid4()),
            'employee_id': booking.employee_id,
            'employee_name': employee['name'],
            'start_time': start_time,
            'end_time': end_time,
            'remarks': booking.remarks,
            'created_at': datetime.utcnow()
        }
        
        # Since we only allow one booking, the room should be occupied when booked
        # Find the current active booking and set proper status
        current_booking = None
        room_status = "occupied"  # Always occupied when there's a booking
        
        # Check if the new booking is currently active (happening now)
        if start_time <= current_time <= end_time:
            current_booking = new_booking
        
        # Update room with the single booking
        update_data = {
            'status': room_status,
            'current_booking': current_booking,
            'bookings': [new_booking],  # Only one booking allowed
            'updated_at': datetime.utcnow()
        }
        
        result = await db.meeting_rooms.update_one(
            {"id": room_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        # Return updated room
        updated_room = await db.meeting_rooms.find_one({"id": room_id})
        updated_room.pop('_id', None)
        return MeetingRoom(**updated_room)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error booking meeting room: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to book meeting room")

# Bulk booking endpoint removed - single booking system only

@api_router.delete("/meeting-rooms/{room_id}/booking")
async def cancel_booking(room_id: str):
    """Cancel all meeting room bookings (single booking system)"""
    try:
        update_data = {
            'status': 'vacant',
            'current_booking': None,
            'bookings': [],  # Clear all bookings for single booking system
            'updated_at': datetime.utcnow()
        }
        
        result = await db.meeting_rooms.update_one(
            {"id": room_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        return {"message": "Room booking cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error cancelling booking: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel booking")

@api_router.delete("/meeting-rooms/{room_id}/booking/{booking_id}")
async def cancel_specific_booking(room_id: str, booking_id: str):
    """Cancel a specific booking by booking ID"""
    try:
        # Get room
        room = await db.meeting_rooms.find_one({"id": room_id})
        if not room:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        # Get current bookings
        existing_bookings = room.get('bookings', [])
        
        # Find and remove the specific booking
        updated_bookings = [b for b in existing_bookings if b.get('id') != booking_id]
        
        if len(updated_bookings) == len(existing_bookings):
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # With single booking system, determine status based on remaining bookings
        current_time = datetime.utcnow()
        current_booking = None
        room_status = "vacant"
        
        # If there are any bookings remaining, room is occupied
        if updated_bookings:
            room_status = "occupied"
            # Check if any remaining booking is currently active
            for booking_info in updated_bookings:
                booking_start = normalize_datetime(booking_info['start_time'])
                booking_end = normalize_datetime(booking_info['end_time'])
                
                if booking_start <= current_time <= booking_end:
                    current_booking = booking_info
                    break
        
        # Update room
        update_data = {
            'status': room_status,
            'current_booking': current_booking,
            'bookings': updated_bookings,
            'updated_at': datetime.utcnow()
        }
        
        result = await db.meeting_rooms.update_one(
            {"id": room_id},
            {"$set": update_data}
        )
        
        return {"message": "Booking cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error cancelling specific booking: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel specific booking")

@api_router.get("/meeting-rooms/locations")
async def get_meeting_room_locations():
    """Get all available meeting room locations"""
    try:
        pipeline = [
            {"$group": {"_id": "$location"}},
            {"$sort": {"_id": 1}}
        ]
        
        locations_cursor = db.meeting_rooms.aggregate(pipeline)
        locations_docs = await locations_cursor.to_list(50)
        
        locations = [doc['_id'] for doc in locations_docs if doc['_id']]
        return {"locations": locations}
        
    except Exception as e:
        logging.error(f"Error getting locations: {str(e)}")
        return {"locations": ["IFC"]}

@api_router.get("/meeting-rooms/floors")
async def get_meeting_room_floors(location: Optional[str] = Query(None)):
    """Get all available floors for a location"""
    try:
        query_filter = {}
        if location:
            query_filter['location'] = location
            
        pipeline = [
            {"$match": query_filter},
            {"$group": {"_id": "$floor"}},
            {"$sort": {"_id": 1}}
        ]
        
        floors_cursor = db.meeting_rooms.aggregate(pipeline)
        floors_docs = await floors_cursor.to_list(50)
        
        floors = [doc['_id'] for doc in floors_docs if doc['_id']]
        return {"floors": floors}
        
    except Exception as e:
        logging.error(f"Error getting floors: {str(e)}")
        return {"floors": ["11th Floor", "12th Floor", "14th Floor"]}

@api_router.put("/meeting-rooms/{room_id}", response_model=MeetingRoom)
async def update_meeting_room(room_id: str, room: MeetingRoomUpdate):
    """Update meeting room status"""
    try:
        update_data = {k: v for k, v in room.dict().items() if v is not None}
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.meeting_rooms.update_one(
                {"id": room_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Meeting room not found")
        
        # Get updated room
        room_doc = await db.meeting_rooms.find_one({"id": room_id})
        if not room_doc:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        room_doc.pop('_id', None)
        return MeetingRoom(**room_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating meeting room: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update meeting room")

@api_router.delete("/meeting-rooms/clear-all")
async def clear_all_meeting_rooms():
    """Clear all meeting rooms - for reinitialization"""
    try:
        result = await db.meeting_rooms.delete_many({})
        
        return {
            "message": "All meeting rooms cleared successfully",
            "count": result.deleted_count
        }
        
    except Exception as e:
        logging.error(f"Error clearing meeting rooms: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear meeting rooms")

@api_router.delete("/meeting-rooms/{room_id}")
async def delete_meeting_room(room_id: str):
    """Delete meeting room"""
    try:
        result = await db.meeting_rooms.delete_one({"id": room_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Meeting room not found")
        
        return {"message": "Meeting room deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting meeting room: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete meeting room")

# Policy Management Endpoints

@api_router.get("/policies", response_model=List[Policy])
async def get_policies(category: Optional[str] = Query(None, description="Filter by category")):
    """Fetch all policies"""
    try:
        query_filter = {}
        if category:
            query_filter['category'] = category
            
        policies_cursor = db.policies.find(query_filter)
        policies_docs = await policies_cursor.to_list(100)
        
        result = []
        for doc in policies_docs:
            doc.pop('_id', None)
            result.append(Policy(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching policies: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch policies")

@api_router.post("/policies", response_model=Policy)
async def create_policy(policy: PolicyCreate):
    """Create new policy"""
    try:
        effective_date = None
        if policy.effective_date:
            effective_date = datetime.fromisoformat(policy.effective_date.replace('Z', '+00:00'))
            
        new_policy = Policy(
            title=policy.title,
            content=policy.content,
            category=policy.category,
            effective_date=effective_date,
            version=policy.version
        )
        
        policy_dict = new_policy.dict()
        await db.policies.insert_one(policy_dict)
        
        return new_policy
        
    except Exception as e:
        logging.error(f"Error creating policy: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create policy")

@api_router.put("/policies/{policy_id}", response_model=Policy)
async def update_policy(policy_id: str, policy: PolicyUpdate):
    """Update policy"""
    try:
        update_data = {k: v for k, v in policy.dict().items() if v is not None}
        if 'effective_date' in update_data and update_data['effective_date']:
            update_data['effective_date'] = datetime.fromisoformat(update_data['effective_date'].replace('Z', '+00:00'))
        
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.policies.update_one(
                {"id": policy_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Policy not found")
        
        # Get updated policy
        policy_doc = await db.policies.find_one({"id": policy_id})
        if not policy_doc:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        policy_doc.pop('_id', None)
        return Policy(**policy_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating policy: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update policy")

@api_router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: str):
    """Delete policy"""
    try:
        result = await db.policies.delete_one({"id": policy_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        return {"message": "Policy deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting policy: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete policy")

# Workflow Management Endpoints

@api_router.get("/workflows", response_model=List[Workflow])
async def get_workflows(
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Fetch all workflows"""
    try:
        query_filter = {}
        if category:
            query_filter['category'] = category
        if status:
            query_filter['status'] = status
            
        workflows_cursor = db.workflows.find(query_filter)
        workflows_docs = await workflows_cursor.to_list(100)
        
        result = []
        for doc in workflows_docs:
            doc.pop('_id', None)
            result.append(Workflow(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching workflows: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch workflows")

@api_router.post("/workflows", response_model=Workflow)
async def create_workflow(workflow: WorkflowCreate):
    """Create new workflow"""
    try:
        # Convert steps to WorkflowStep objects
        workflow_steps = []
        for i, step_data in enumerate(workflow.steps):
            step = WorkflowStep(
                name=step_data.get('name', ''),
                description=step_data.get('description', ''),
                order=i + 1,
                assigned_to=step_data.get('assigned_to'),
                status=step_data.get('status', 'pending')
            )
            workflow_steps.append(step)
        
        new_workflow = Workflow(
            name=workflow.name,
            description=workflow.description,
            category=workflow.category,
            steps=workflow_steps
        )
        
        workflow_dict = new_workflow.dict()
        await db.workflows.insert_one(workflow_dict)
        
        return new_workflow
        
    except Exception as e:
        logging.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create workflow")

@api_router.put("/workflows/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, workflow: WorkflowUpdate):
    """Update workflow"""
    try:
        update_data = {k: v for k, v in workflow.dict().items() if v is not None}
        
        # Handle steps update
        if 'steps' in update_data and update_data['steps']:
            workflow_steps = []
            for i, step_data in enumerate(update_data['steps']):
                step = WorkflowStep(
                    name=step_data.get('name', ''),
                    description=step_data.get('description', ''),
                    order=i + 1,
                    assigned_to=step_data.get('assigned_to'),
                    status=step_data.get('status', 'pending')
                )
                workflow_steps.append(step)
            update_data['steps'] = [step.dict() for step in workflow_steps]
        
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.workflows.update_one(
                {"id": workflow_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Get updated workflow
        workflow_doc = await db.workflows.find_one({"id": workflow_id})
        if not workflow_doc:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        workflow_doc.pop('_id', None)
        return Workflow(**workflow_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update workflow")

@api_router.delete("/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete workflow"""
    try:
        result = await db.workflows.delete_one({"id": workflow_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {"message": "Workflow deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting workflow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete workflow")

# Attendance Management Endpoints

@api_router.get("/attendance", response_model=List[AttendanceRecord])
async def get_attendance(
    search: Optional[str] = Query(None, description="Search term for employee name, id (starts with pattern)"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Fetch attendance records"""
    try:
        query_filter = {}
        
        if search:
            # Create search query for employee name and id using "starts with" pattern
            query_filter["$or"] = [
                {"employee_name": {"$regex": f"^{search}", "$options": "i"}},
                {"employee_id": {"$regex": f"^{search}", "$options": "i"}}
            ]
        
        if employee_id:
            query_filter['employee_id'] = employee_id
        if date:
            query_filter['date'] = date
        if status:
            query_filter['status'] = status
            
        attendance_cursor = db.attendance.find(query_filter).sort("date", -1)
        attendance_docs = await attendance_cursor.to_list(100)
        
        result = []
        for doc in attendance_docs:
            doc.pop('_id', None)
            result.append(AttendanceRecord(**doc))
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch attendance")

@api_router.post("/attendance", response_model=AttendanceRecord)
async def create_attendance(attendance: AttendanceCreate):
    """Create attendance record"""
    try:
        # Validate employee exists
        employee = await db.employees.find_one({"id": attendance.employee_id})
        if not employee:
            raise HTTPException(status_code=400, detail="Employee not found")
        
        # Check if attendance already exists for this date
        existing = await db.attendance.find_one({
            "employee_id": attendance.employee_id,
            "date": attendance.date
        })
        if existing:
            raise HTTPException(status_code=400, detail="Attendance record already exists for this date")
        
        # Parse datetime strings
        punch_in = None
        punch_out = None
        if attendance.punch_in:
            punch_in = datetime.fromisoformat(attendance.punch_in.replace('Z', '+00:00'))
        if attendance.punch_out:
            punch_out = datetime.fromisoformat(attendance.punch_out.replace('Z', '+00:00'))
        
        # Calculate total hours
        total_hours = None
        if punch_in and punch_out:
            # Ensure both datetimes have the same timezone info for calculation
            if punch_in.tzinfo and not punch_out.tzinfo:
                punch_out = punch_out.replace(tzinfo=punch_in.tzinfo)
            elif punch_out.tzinfo and not punch_in.tzinfo:
                punch_in = punch_in.replace(tzinfo=punch_out.tzinfo)
            total_hours = (punch_out - punch_in).total_seconds() / 3600
        
        new_attendance = AttendanceRecord(
            employee_id=attendance.employee_id,
            employee_name=employee['name'],
            date=attendance.date,
            punch_in=punch_in,
            punch_out=punch_out,
            punch_in_location=attendance.punch_in_location,
            punch_out_location=attendance.punch_out_location,
            total_hours=total_hours,
            status=attendance.status,
            remarks=attendance.remarks
        )
        
        attendance_dict = new_attendance.dict()
        await db.attendance.insert_one(attendance_dict)
        
        return new_attendance
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create attendance")

@api_router.put("/attendance/{attendance_id}", response_model=AttendanceRecord)
async def update_attendance(attendance_id: str, attendance: AttendanceUpdate):
    """Update attendance record"""
    try:
        update_data = {k: v for k, v in attendance.dict().items() if v is not None}
        
        # Parse datetime strings
        if 'punch_in' in update_data and update_data['punch_in']:
            update_data['punch_in'] = datetime.fromisoformat(update_data['punch_in'].replace('Z', '+00:00'))
        if 'punch_out' in update_data and update_data['punch_out']:
            update_data['punch_out'] = datetime.fromisoformat(update_data['punch_out'].replace('Z', '+00:00'))
        
        if update_data:
            # Recalculate total hours if both times are updated
            attendance_doc = await db.attendance.find_one({"id": attendance_id})
            if attendance_doc:
                punch_in = update_data.get('punch_in', attendance_doc.get('punch_in'))
                punch_out = update_data.get('punch_out', attendance_doc.get('punch_out'))
                
                if punch_in and punch_out:
                    # Ensure both datetimes have the same timezone info for calculation
                    if punch_in.tzinfo and not punch_out.tzinfo:
                        punch_out = punch_out.replace(tzinfo=punch_in.tzinfo)
                    elif punch_out.tzinfo and not punch_in.tzinfo:
                        punch_in = punch_in.replace(tzinfo=punch_out.tzinfo)
                    total_hours = (punch_out - punch_in).total_seconds() / 3600
                    update_data['total_hours'] = total_hours
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.attendance.update_one(
                {"id": attendance_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Attendance record not found")
        
        # Get updated attendance
        attendance_doc = await db.attendance.find_one({"id": attendance_id})
        if not attendance_doc:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        attendance_doc.pop('_id', None)
        return AttendanceRecord(**attendance_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update attendance")

@api_router.delete("/attendance/{attendance_id}")
async def delete_attendance(attendance_id: str):
    """Delete attendance record"""
    try:
        result = await db.attendance.delete_one({"id": attendance_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        return {"message": "Attendance record deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete attendance")

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

@api_router.post("/cleanup-images")
async def cleanup_image_files():
    """Clean up legacy image files and orphaned images"""
    try:
        cleanup_count = 0
        
        # Get all employees from database
        employees_cursor = db.employees.find({}, {"id": 1})
        valid_employee_ids = {emp["id"] async for emp in employees_cursor}
        
        # Scan upload directory
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                filename = file_path.name
                
                # Check if it's a legacy file with random suffix
                if '_' in filename:
                    base_name = filename.split('_')[0]
                    # If this is a legacy file for a valid employee, remove it
                    # The new system will create proper files without suffixes
                    if base_name in valid_employee_ids:
                        try:
                            file_path.unlink()
                            cleanup_count += 1
                            logging.info(f"Cleaned up legacy image file: {filename}")
                        except Exception as e:
                            logging.warning(f"Could not remove legacy file {filename}: {e}")
                
                # Check if it's an orphaned file (no corresponding employee)
                else:
                    base_name = filename.split('.')[0]  # Remove extension
                    if base_name not in valid_employee_ids:
                        try:
                            file_path.unlink()
                            cleanup_count += 1
                            logging.info(f"Cleaned up orphaned image file: {filename}")
                        except Exception as e:
                            logging.warning(f"Could not remove orphaned file {filename}: {e}")
        
        return {
            "message": "Image cleanup completed",
            "files_cleaned": cleanup_count
        }
        
    except Exception as e:
        logging.error(f"Error during image cleanup: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cleanup images")

# Temporary endpoint to force Excel reload
@api_router.post("/force-reload-excel")
async def force_reload_excel():
    """Force reload Excel data by clearing database first"""
    try:
        # Clear existing employees
        await db.employees.delete_many({})
        
        # Parse Excel file
        employees_data = excel_parser.parse_excel_to_employees()
        
        # Insert new employees
        if employees_data:
            # Convert to proper format for MongoDB
            for emp in employees_data:
                emp['lastUpdated'] = datetime.utcnow()
            
            await db.employees.insert_many(employees_data)
        
        return RefreshResponse(
            message="Excel data force reloaded successfully",
            count=len(employees_data)
        )
        
    except Exception as e:
        logging.error(f"Error force reloading Excel data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to force reload data: {str(e)}")

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
        # Force reload Excel data for testing
        logger.info("Starting database initialization...")
        
        # Check if employees collection is empty
        count = await db.employees.count_documents({})
        logger.info(f"Current employee count in database: {count}")
        
        if count == 0:
            logger.info("Database empty, loading Excel data...")
            
            # Try to load Excel data with better error handling
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
                # Try to check if file exists
                excel_file_path = os.path.join(os.path.dirname(__file__), "employee_directory.xlsx")
                if os.path.exists(excel_file_path):
                    logger.info(f"Excel file exists at: {excel_file_path}")
                else:
                    logger.error(f"Excel file not found at: {excel_file_path}")
                    
        else:
            logger.info(f"Database already has {count} employees, skipping Excel load")
        
        # Load attendance data from Excel
        try:
            logger.info("Loading attendance data from Excel...")
            attendance_count = await db.attendance.count_documents({})
            logger.info(f"Current attendance records in database: {attendance_count}")
            
            if attendance_count == 0:
                attendance_data = parse_attendance_excel()
                if attendance_data and len(attendance_data) > 0:
                    await db.attendance.insert_many(attendance_data)
                    logger.info(f"Successfully loaded {len(attendance_data)} attendance records from Excel")
                else:
                    logger.warning("No attendance data found in Excel file")
            else:
                logger.info(f"Database already has {attendance_count} attendance records, skipping load")
                
        except Exception as attendance_error:
            logger.error(f"Error loading attendance data: {str(attendance_error)}")
            
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()