import React, { useState, useMemo, useEffect } from "react";
import { Search, Grid3X3, List, User, X } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { useAuth } from "../context/AuthContext";
import { mockEmployees, departments, locations, loadAllEmployeesFromExcel } from "../mock";
import EmployeeCard from "./EmployeeCard";
import EmployeeList from "./EmployeeList";

const EmployeeDirectory = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All Departments");
  const [locationFilter, setLocationFilter] = useState("All Locations");
  const [viewMode, setViewMode] = useState("grid");
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  
  const { isAdmin } = useAuth();

  // Load employees based on user role
  useEffect(() => {
    const loadEmployees = async () => {
      try {
        if (isAdmin()) {
          // Admin can see all employees immediately
          setLoading(true);
          const allEmployees = await loadAllEmployeesFromExcel();
          setEmployees(allEmployees);
          setHasSearched(true);
        } else {
          // Regular users start with empty list
          setEmployees([]);
          setHasSearched(false);
        }
      } catch (error) {
        console.error("Error loading employees:", error);
        setEmployees(mockEmployees);
      } finally {
        setLoading(false);
      }
    };

    loadEmployees();
  }, [isAdmin]);

  // Handle search for regular users
  useEffect(() => {
    if (!isAdmin() && searchTerm.trim().length > 0) {
      const performSearch = async () => {
        setLoading(true);
        try {
          const allEmployees = await loadAllEmployeesFromExcel();
          setEmployees(allEmployees);
          setHasSearched(true);
        } catch (error) {
          console.error("Error loading employees:", error);
        } finally {
          setLoading(false);
        }
      };
      performSearch();
    } else if (!isAdmin() && searchTerm.trim().length === 0 && hasSearched) {
      // Clear results when search is cleared for regular users
      setEmployees([]);
      setHasSearched(false);
    }
  }, [searchTerm, isAdmin]);

  // Filter and search logic
  const filteredEmployees = useMemo(() => {
    if (!hasSearched && !isAdmin()) {
      return [];
    }

    return employees.filter(employee => {
      const matchesSearch = 
        employee.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        employee.id.includes(searchTerm) ||
        employee.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
        employee.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
        employee.grade.toLowerCase().includes(searchTerm.toLowerCase()) ||
        employee.mobile.includes(searchTerm);

      const matchesDepartment = departmentFilter === "All Departments" || 
        employee.department === departmentFilter;

      const matchesLocation = locationFilter === "All Locations" || 
        employee.location === locationFilter;

      return matchesSearch && matchesDepartment && matchesLocation;
    });
  }, [employees, searchTerm, departmentFilter, locationFilter, hasSearched, isAdmin]);

  const handleImageUpdate = (employeeId, newImage) => {
    if (!isAdmin()) {
      return; // Users cannot update images
    }
    setEmployees(prev => prev.map(emp => 
      emp.id === employeeId ? { ...emp, profileImage: newImage } : emp
    ));
  };

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee);
    setShowDetailModal(true);
  };

  const closeDetailModal = () => {
    setShowDetailModal(false);
    setSelectedEmployee(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-blue-600">Loading employee data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <Card className="border-blue-200 shadow-sm bg-white">
        <CardHeader className="pb-4 bg-blue-50">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-blue-400 h-4 w-4" />
              <Input
                placeholder={!isAdmin() ? "Search to view employees (name, employee code, department, location, designation, mobile)..." : "Search by name, employee code, department, location, designation, mobile..."}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 h-11 border-blue-200 focus:border-blue-400"
              />
            </div>

            {/* Filters - Only show if admin or user has searched */}
            {(isAdmin() || hasSearched) && (
              <>
                {/* Department Filter */}
                <div className="w-full lg:w-48">
                  <Select value={departmentFilter} onValueChange={setDepartmentFilter}>
                    <SelectTrigger className="h-11 border-blue-200">
                      <SelectValue placeholder="Department" />
                    </SelectTrigger>
                    <SelectContent>
                      {departments.map(dept => (
                        <SelectItem key={dept} value={dept}>{dept}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Location Filter */}
                <div className="w-full lg:w-48">
                  <Select value={locationFilter} onValueChange={setLocationFilter}>
                    <SelectTrigger className="h-11 border-blue-200">
                      <SelectValue placeholder="Location" />
                    </SelectTrigger>
                    <SelectContent>
                      {locations.map(location => (
                        <SelectItem key={location} value={location}>{location}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* View Toggle */}
                <div className="flex space-x-2">
                  <Button
                    variant={viewMode === "grid" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("grid")}
                    className={`h-11 px-3 ${viewMode === "grid" ? "bg-blue-600 hover:bg-blue-700" : "border-blue-200 text-blue-700 hover:bg-blue-50"}`}
                  >
                    <Grid3X3 className="h-4 w-4" />
                  </Button>
                  <Button
                    variant={viewMode === "list" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("list")}
                    className={`h-11 px-3 ${viewMode === "list" ? "bg-blue-600 hover:bg-blue-700" : "border-blue-200 text-blue-700 hover:bg-blue-50"}`}
                  >
                    <List className="h-4 w-4" />
                  </Button>
                </div>
              </>
            )}
          </div>
        </CardHeader>
      </Card>

      {/* User Instructions */}
      {!isAdmin() && !hasSearched && (
        <Card className="border-blue-200 shadow-sm bg-blue-50">
          <CardContent className="p-6 text-center">
            <User className="h-12 w-12 mx-auto mb-4 text-blue-400" />
            <h3 className="text-lg font-semibold text-blue-900 mb-2">Search to View Employees</h3>
            <p className="text-blue-600">
              As an employee, you need to search using keywords to view employee information. 
              Try searching by name, department, location, or other criteria.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Results Summary */}
      {(isAdmin() || hasSearched) && (
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Badge variant="secondary" className="px-3 py-1 bg-blue-100 text-blue-700">
              {filteredEmployees.length} of {employees.length} employees found
            </Badge>
            {(searchTerm || departmentFilter !== "All Departments" || locationFilter !== "All Locations") && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setSearchTerm("");
                  setDepartmentFilter("All Departments");
                  setLocationFilter("All Locations");
                }}
                className="text-blue-600 hover:bg-blue-50"
              >
                Clear filters
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Employee Display */}
      {(isAdmin() || hasSearched) && (
        viewMode === "grid" ? (
          <EmployeeCard 
            employees={filteredEmployees} 
            onImageUpdate={handleImageUpdate}
            onEmployeeClick={handleEmployeeClick}
          />
        ) : (
          <EmployeeList 
            employees={filteredEmployees} 
            onImageUpdate={handleImageUpdate}
            onEmployeeClick={handleEmployeeClick}
          />
        )
      )}

      {/* Employee Detail Modal */}
      <Dialog open={showDetailModal} onOpenChange={closeDetailModal}>
        <DialogContent className="sm:max-w-2xl border-blue-200">
          <DialogHeader>
            <div className="flex items-center justify-between">
              <DialogTitle className="text-xl text-blue-900">Employee Details</DialogTitle>
              <Button variant="ghost" size="sm" onClick={closeDetailModal}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </DialogHeader>
          
          {selectedEmployee && (
            <div className="space-y-6">
              {/* Profile Section */}
              <div className="flex items-center space-x-6">
                <div className="w-24 h-24 rounded-full overflow-hidden bg-gradient-to-br from-blue-200 to-blue-300 flex items-center justify-center">
                  {selectedEmployee.profileImage && selectedEmployee.profileImage !== "/api/placeholder/150/150" ? (
                    <img 
                      src={selectedEmployee.profileImage} 
                      alt={selectedEmployee.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <User className="h-12 w-12 text-blue-500" style={{display: selectedEmployee.profileImage && selectedEmployee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-blue-900">{selectedEmployee.name}</h2>
                  <Badge variant="secondary" className="mt-1 bg-blue-100 text-blue-700">{selectedEmployee.id}</Badge>
                  <p className="text-lg text-blue-600 mt-2">{selectedEmployee.grade}</p>
                </div>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">D</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Department</p>
                      <p className="font-medium text-blue-900">{selectedEmployee.department}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">L</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Location</p>
                      <p className="font-medium text-blue-900">{selectedEmployee.location}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">P</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Mobile</p>
                      <p className="font-medium text-blue-900">{selectedEmployee.mobile}</p>
                      {selectedEmployee.extension !== "0" && (
                        <p className="text-sm text-blue-600">Ext: {selectedEmployee.extension}</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">@</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Email</p>
                      <p className="font-medium text-blue-900 text-sm">{selectedEmployee.email}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">📅</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Date of Joining</p>
                      <p className="font-medium text-blue-900">
                        {selectedEmployee.dateOfJoining ? new Date(selectedEmployee.dateOfJoining).toLocaleDateString() : 'N/A'}
                      </p>
                    </div>
                  </div>
                  
                  {selectedEmployee.reportingManager && selectedEmployee.reportingManager !== "*" && (
                    <div className="flex items-center space-x-3">
                      <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                        <span className="text-xs text-blue-600">👤</span>
                      </div>
                      <div>
                        <p className="text-sm text-blue-500">Reports To</p>
                        <p className="font-medium text-blue-900">{selectedEmployee.reportingManager}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EmployeeDirectory;