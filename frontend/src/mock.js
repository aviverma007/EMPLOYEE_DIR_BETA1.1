// Mock data for employee directory - All 640 employees from Excel
export const mockEmployees = [
  {
    "id": "80002",
    "name": "Vikas Malhotra",
    "department": "Human Resources",
    "grade": "President - Human Resource",
    "reportingManager": "*",
    "reportingId": null,
    "location": "IFC",
    "mobile": "9910698391",
    "extension": "6606",
    "email": "vikas.malhotra@smartworlddevelopers.com",
    "dateOfJoining": "2021-02-01",
    "profileImage": "/api/placeholder/150/150"
  },
  {
    "id": "80024",
    "name": "Jyotsna Chauhan",
    "department": "Marketing",
    "grade": "President - Marketing",
    "reportingManager": "Ashish Jerath(80006)",
    "reportingId": "80006",
    "location": "62 Sales Gallery",
    "mobile": "9910430289",
    "extension": "0",
    "email": "jyotsna.chauhan@smartworlddevelopers.com",
    "dateOfJoining": "2021-03-01",
    "profileImage": "/api/placeholder/150/150"
  },
  {
    "id": "80056",
    "name": "Pallav Saxena",
    "department": "Project Management",
    "grade": "President - Management Office",
    "reportingManager": "*",
    "reportingId": null,
    "location": "PMO 75",
    "mobile": "9818328571",
    "extension": "0",
    "email": "pallav.saxena@smartworlddevelopers.com",
    "dateOfJoining": "2021-05-04",
    "profileImage": "/api/placeholder/150/150"
  },
  {
    "id": "80059",
    "name": "Hari Easwaran",
    "department": "Contracts & Procurement",
    "grade": "President – Contracts & Procurement",
    "reportingManager": "*",
    "reportingId": null,
    "location": "IFC",
    "mobile": "9920321456",
    "extension": "6639",
    "email": "hari.easwaran@smartworlddevelopers.com",
    "dateOfJoining": "2021-05-19",
    "profileImage": "/api/placeholder/150/150"
  },
  {
    "id": "80006",
    "name": "Ashish Jerath",
    "department": "Sales",
    "grade": "President - Sales & Marketing",
    "reportingManager": "*",
    "reportingId": null,
    "location": "62 Sales Gallery",
    "mobile": "9818588123",
    "extension": "0",
    "email": "ashish.jerath@smartworlddevelopers.com",
    "dateOfJoining": "2021-02-03",
    "profileImage": "/api/placeholder/150/150"
  }
];

// This will be loaded from the backend with all 640 employees
// For now showing first 5 as sample, backend will provide full data

// Mock hierarchy relationships
export const mockHierarchy = [
  { employeeId: "80024", reportsTo: "80006" },
  { employeeId: "80101", reportsTo: "80002" },
  { employeeId: "80102", reportsTo: "80006" },
  { employeeId: "80103", reportsTo: "80056" }
];

// Departments for filter - Complete list from Excel
export const departments = [
  "All Departments",
  "Accounts", 
  "Admin",
  "Architecture",
  "Branding",
  "Contracts & Procurement",
  "Corporate Communications",
  "Customer Relationship Management",
  "Design & PMC",
  "Digital Marketing",
  "Director",
  "Facilities",
  "Finance",
  "Human Resources",
  "Interior",
  "IT",
  "Landscape",
  "Legal",
  "Leasing",
  "Marketing",
  "Project Management",
  "Sales",
  "Structure",
  "Technical"
];

// Locations for filter - Complete list from Excel  
export const locations = [
  "All Locations",
  "62 Sales Gallery",
  "Admin",
  "Branding",
  "CRM 69",
  "Design",
  "Digital Marketing",
  "Facilities",
  "Finance 68",
  "Head Office",
  "IFC",
  "Interior",
  "IT 66",
  "Landscape",
  "Legal 67",
  "Marketing",
  "PMO 65",
  "PMO 75",
  "Sales 62",
  "Sales 69",
  "Sales Gallery 62",
  "Site Office",
  "Structure"
];

// Function to simulate loading all employees from backend
export const loadAllEmployeesFromExcel = async () => {
  // This will be replaced with actual API call
  // For now return extended mock data
  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate loading 640 employees
      const allEmployees = [];
      for (let i = 0; i < 640; i++) {
        const baseEmployee = mockEmployees[i % mockEmployees.length];
        allEmployees.push({
          ...baseEmployee,
          id: `${80000 + i}`,
          name: `${baseEmployee.name} ${i > 4 ? i : ''}`.trim(),
        });
      }
      resolve(allEmployees);
    }, 1000);
  });
};

// Save state for hierarchy changes
export const hierarchySaveState = {
  hasUnsavedChanges: false,
  pendingChanges: []
};