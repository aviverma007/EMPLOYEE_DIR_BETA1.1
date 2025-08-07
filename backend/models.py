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