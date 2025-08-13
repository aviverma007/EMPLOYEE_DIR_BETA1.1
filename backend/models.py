from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class Employee(BaseModel):
    id: str = Field(..., description="Employee ID from Excel (EMP ID)")
    name: str = Field(..., description="Employee name")
    department: str = Field(..., description="Department")
    grade: str = Field(..., description="Grade/Designation")
    reportingManager: Optional[str] = Field(None, description="Reporting manager name")
    reportingId: Optional[str] = Field(None, description="Reporting manager ID")
    location: str = Field(..., description="Work location")
    mobile: str = Field(..., description="Mobile number")
    extension: str = Field(default="0", description="Extension number")
    email: str = Field(..., description="Email address")
    dateOfJoining: Optional[str] = Field(None, description="Date of joining")
    profileImage: str = Field(default="/api/placeholder/150/150", description="Profile image URL")
    lastUpdated: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    name: str
    department: str
    grade: str
    location: str
    mobile: str
    email: str
    extension: Optional[str] = "0"
    dateOfJoining: Optional[str] = None

class EmployeeUpdate(BaseModel):
    profileImage: str

class HierarchyRelation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employeeId: str = Field(..., description="Employee ID")
    reportsTo: str = Field(..., description="Manager employee ID")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class HierarchyRelationCreate(BaseModel):
    employeeId: str
    reportsTo: str

class EmployeeSearchParams(BaseModel):
    search: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None

class RefreshResponse(BaseModel):
    message: str
    count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# News models
class News(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="News title")
    content: str = Field(..., description="News content")
    priority: str = Field(default="normal", description="Priority: normal, medium, high")
    author: str = Field(default="Administrator", description="Author name")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NewsCreate(BaseModel):
    title: str
    content: str
    priority: str = "normal"

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None

# Task models
class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    assigned_to: str = Field(..., description="Employee ID task is assigned to")
    priority: str = Field(default="medium", description="Priority: low, medium, high")
    status: str = Field(default="pending", description="Status: pending, in_progress, completed")
    due_date: Optional[datetime] = Field(None, description="Due date")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: str
    priority: str = "medium"
    status: str = "pending"
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None

# Knowledge models
class Knowledge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Article title")
    content: str = Field(..., description="Article content")
    category: str = Field(default="policy", description="Category: policy, process, training, announcement, guideline, other")
    tags: List[str] = Field(default_factory=list, description="Article tags")
    author: str = Field(default="Administrator", description="Author name")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class KnowledgeCreate(BaseModel):
    title: str
    content: str
    category: str = "policy"
    tags: List[str] = []

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# Help/Support models
class HelpReply(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str = Field(..., description="Reply message")
    author: str = Field(default="Administrator", description="Reply author")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Help(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Request title")
    message: str = Field(..., description="Request message")
    priority: str = Field(default="normal", description="Priority: normal, medium, high")
    status: str = Field(default="open", description="Status: open, in_progress, resolved")
    author: str = Field(default="User", description="Request author")
    replies: List[HelpReply] = Field(default_factory=list, description="Replies to the request")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class HelpCreate(BaseModel):
    title: str
    message: str
    priority: str = "normal"

class HelpUpdate(BaseModel):
    status: Optional[str] = None

class HelpReplyCreate(BaseModel):
    message: str

# Meeting Room models
class MeetingRoomBooking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str = Field(..., description="Employee ID who booked the room")
    employee_name: str = Field(..., description="Employee name who booked the room")
    start_time: datetime = Field(..., description="Booking start time")
    end_time: datetime = Field(..., description="Booking end time")
    remarks: str = Field(default="", description="Booking remarks")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MeetingRoom(BaseModel):
    id: str = Field(..., description="Unique room ID")
    name: str = Field(..., description="Room name")
    capacity: int = Field(..., description="Room capacity")
    location: str = Field(..., description="Room location")
    floor: str = Field(..., description="Room floor")
    status: str = Field(default="vacant", description="Room status: vacant, occupied")
    current_booking: Optional[MeetingRoomBooking] = Field(None, description="Current booking information")
    equipment: List[str] = Field(default_factory=list, description="Available equipment")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MeetingRoomCreate(BaseModel):
    id: str
    name: str
    capacity: int
    location: str
    floor: str
    equipment: List[str] = []

class MeetingRoomUpdate(BaseModel):
    status: Optional[str] = None
    current_booking: Optional[MeetingRoomBooking] = None

class MeetingRoomBookingCreate(BaseModel):
    employee_id: str
    start_time: str
    end_time: str
    remarks: str = ""

# Policy models
class Policy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Policy title")
    content: str = Field(..., description="Policy content")
    category: str = Field(default="general", description="Policy category")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    version: str = Field(default="1.0", description="Policy version")
    author: str = Field(default="Administrator", description="Policy author")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyCreate(BaseModel):
    title: str
    content: str
    category: str = "general"
    effective_date: Optional[str] = None
    version: str = "1.0"

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    effective_date: Optional[str] = None
    version: Optional[str] = None

# Workflow models
class WorkflowStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Step name")
    description: str = Field(..., description="Step description")
    order: int = Field(..., description="Step order")
    assigned_to: Optional[str] = Field(None, description="Employee ID assigned to this step")
    status: str = Field(default="pending", description="Step status: pending, in_progress, completed")
    completed_at: Optional[datetime] = Field(None, description="Step completion time")

class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    category: str = Field(default="general", description="Workflow category")
    steps: List[WorkflowStep] = Field(default_factory=list, description="Workflow steps")
    status: str = Field(default="active", description="Workflow status: active, inactive, completed")
    created_by: str = Field(default="Administrator", description="Workflow creator")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WorkflowCreate(BaseModel):
    name: str
    description: str
    category: str = "general"
    steps: List[dict] = []

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    steps: Optional[List[dict]] = None

# Attendance models
class AttendanceRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str = Field(..., description="Employee ID")
    employee_name: str = Field(..., description="Employee name")
    date: str = Field(..., description="Attendance date (YYYY-MM-DD)")
    punch_in: Optional[str] = Field(None, description="Punch in time")
    punch_out: Optional[str] = Field(None, description="Punch out time")
    punch_in_location: Optional[str] = Field(None, description="Punch in location")
    punch_out_location: Optional[str] = Field(None, description="Punch out location")
    total_hours: Optional[float] = Field(None, description="Total working hours")
    status: str = Field(default="present", description="Attendance status: present, absent, half_day, late")
    remarks: Optional[str] = Field(None, description="Attendance remarks")
    created_at: Optional[str] = Field(None, description="Created timestamp")
    updated_at: Optional[str] = Field(None, description="Updated timestamp")

class AttendanceCreate(BaseModel):
    employee_id: str
    date: str
    punch_in: Optional[str] = None
    punch_out: Optional[str] = None
    punch_in_location: Optional[str] = None
    punch_out_location: Optional[str] = None
    status: str = "present"
    remarks: str = ""

class AttendanceUpdate(BaseModel):
    punch_in: Optional[str] = None
    punch_out: Optional[str] = None
    punch_in_location: Optional[str] = None
    punch_out_location: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None