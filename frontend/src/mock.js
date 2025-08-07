// Mock data for employee directory
export const mockEmployees = [
  {
    id: "80002",
    name: "Vikas Malhotra",
    department: "Human Resources",
    grade: "President - Human Resource",
    reportingManager: "*",
    reportingId: null,
    location: "IFC",
    mobile: "9910698391",
    extension: "6606",
    email: "vikas.malhotra@smartworlddevelopers.com",
    dateOfJoining: "2021-02-01",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80024",
    name: "Jyotsna Chauhan",
    department: "Marketing",
    grade: "President - Marketing",
    reportingManager: "Ashish Jerath(80006)",
    reportingId: "80006",
    location: "62 Sales Gallery",
    mobile: "9910430289",
    extension: "0",
    email: "jyotsna.chauhan@smartworlddevelopers.com",
    dateOfJoining: "2021-03-01",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80056",
    name: "Pallav Saxena",
    department: "Project Management",
    grade: "President - Management Office",
    reportingManager: "*",
    reportingId: null,
    location: "PMO 75",
    mobile: "9818328571",
    extension: "0",
    email: "pallav.saxena@smartworlddevelopers.com",
    dateOfJoining: "2021-05-04",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80059",
    name: "Hari Easwaran",
    department: "Contracts & Procurement",
    grade: "President – Contracts & Procurement",
    reportingManager: "*",
    reportingId: null,
    location: "IFC",
    mobile: "9920321456",
    extension: "6639",
    email: "hari.easwaran@smartworlddevelopers.com",
    dateOfJoining: "2021-05-19",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80006",
    name: "Ashish Jerath",
    department: "Sales",
    grade: "President - Sales & Marketing",
    reportingManager: "*",
    reportingId: null,
    location: "62 Sales Gallery",
    mobile: "9818588123",
    extension: "0",
    email: "ashish.jerath@smartworlddevelopers.com",
    dateOfJoining: "2021-02-03",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80101",
    name: "Rajesh Kumar",
    department: "IT",
    grade: "Senior Manager",
    reportingManager: "Vikas Malhotra(80002)",
    reportingId: "80002",
    location: "IFC",
    mobile: "9876543210",
    extension: "6610",
    email: "rajesh.kumar@smartworlddevelopers.com",
    dateOfJoining: "2021-06-15",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80102",
    name: "Priya Singh",
    department: "Sales",
    grade: "Manager",
    reportingManager: "Ashish Jerath(80006)",
    reportingId: "80006",
    location: "62 Sales Gallery",
    mobile: "9887654321",
    extension: "6611",
    email: "priya.singh@smartworlddevelopers.com",
    dateOfJoining: "2021-07-01",
    profileImage: "/api/placeholder/150/150"
  },
  {
    id: "80103",
    name: "Amit Sharma",
    department: "Project Management",
    grade: "Assistant Manager",
    reportingManager: "Pallav Saxena(80056)",
    reportingId: "80056",
    location: "PMO 75",
    mobile: "9798765432",
    extension: "6612",
    email: "amit.sharma@smartworlddevelopers.com",
    dateOfJoining: "2021-08-15",
    profileImage: "/api/placeholder/150/150"
  }
];

// Mock hierarchy relationships
export const mockHierarchy = [
  { employeeId: "80024", reportsTo: "80006" },
  { employeeId: "80101", reportsTo: "80002" },
  { employeeId: "80102", reportsTo: "80006" },
  { employeeId: "80103", reportsTo: "80056" }
];

// Departments for filter
export const departments = [
  "All Departments",
  "Human Resources",
  "Marketing", 
  "Project Management",
  "Contracts & Procurement",
  "Sales",
  "IT"
];

// Locations for filter
export const locations = [
  "All Locations",
  "IFC",
  "62 Sales Gallery", 
  "PMO 75"
];