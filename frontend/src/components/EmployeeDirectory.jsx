import React, { useState, useMemo, useEffect, useCallback } from "react";
import { Search, Grid3X3, List, User, X } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { useAuth } from "../context/AuthContext";
import { employeeAPI, utilityAPI } from "../services/api";
import EmployeeCard from "./EmployeeCard";
import EmployeeList from "./EmployeeList";

const EmployeeDirectory = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All Departments");
  const [locationFilter, setLocationFilter] = useState("All Locations");
  const [viewMode, setViewMode] = useState("grid");
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState(["All Departments"]);
  const [locations, setLocations] = useState(["All Locations"]);
  const [loading, setLoading] = useState(true);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  
  const { isAdmin } = useAuth();

  // Load all data on mount - same for both admin and regular users
  useEffect(() => {
    const loadAllData = async () => {
      try {
        setLoading(true);
        const [employeeData, depts, locs] = await Promise.all([
          employeeAPI.getAll(), // Load all employees upfront
          utilityAPI.getDepartments(),
          utilityAPI.getLocations()
        ]);
        
        setEmployees(employeeData);
        setDepartments(depts);
        setLocations(locs);
      } catch (error) {
        console.error("Error loading data:", error);
        setEmployees([]);
      } finally {
        setLoading(false);
      }
    };

    loadAllData();
  }, []);

  // Debounce search term for better performance
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  // Client-side filtering - same logic for both admin and regular users
  const filteredEmployees = useMemo(() => {
    let filtered = employees;

    // Apply search filter
    if (debouncedSearchTerm.trim().length > 0) {
      const searchLower = debouncedSearchTerm.toLowerCase();
      filtered = filtered.filter(employee => {
        return (
          employee.name.toLowerCase().includes(searchLower) ||
          employee.id.includes(debouncedSearchTerm) ||
          employee.department.toLowerCase().includes(searchLower) ||
          employee.location.toLowerCase().includes(searchLower) ||
          employee.grade.toLowerCase().includes(searchLower) ||
          employee.mobile.includes(debouncedSearchTerm)
        );
      });
    }

    // Apply department filter
    if (departmentFilter !== "All Departments") {
      filtered = filtered.filter(employee => employee.department === departmentFilter);
    }

    // Apply location filter
    if (locationFilter !== "All Locations") {
      filtered = filtered.filter(employee => employee.location === locationFilter);
    }

    return filtered;
  }, [employees, debouncedSearchTerm, departmentFilter, locationFilter]);

  const handleImageUpdate = async (employeeId, newImageUrl) => {
    try {
      // Update on backend
      await employeeAPI.updateImage(employeeId, newImageUrl);
      
      // Update local state
      setEmployees(prev => prev.map(emp => 
        emp.id === employeeId ? { ...emp, profileImage: newImageUrl } : emp
      ));
      
      // Update selected employee if it's being viewed
      if (selectedEmployee && selectedEmployee.id === employeeId) {
        setSelectedEmployee({ ...selectedEmployee, profileImage: newImageUrl });
      }
      
    } catch (error) {
      console.error("Error updating image:", error);
      throw error; // Re-throw so EmployeeCard can show error
    }
  };

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee);
    setShowDetailModal(true);
  };

  const closeDetailModal = () => {
    setShowDetailModal(false);
    setSelectedEmployee(null);
  };

  // Show loading only on initial data load
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-blue-600">Loading employee directory...</p>
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
            {/* Search Bar - Same for both admin and regular users */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-blue-400 h-4 w-4" />
              <Input
                placeholder="Search by name, employee code, department, location, designation, mobile..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 h-11 border-blue-200 focus:border-blue-400"
              />
              {searchTerm && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSearchTerm("")}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 h-7 w-7 p-0 hover:bg-blue-100"
                >
                  <X className="h-4 w-4 text-blue-500" />
                </Button>
              )}
            </div>

            {/* Filters - Always show for both user types */}
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
          </div>
        </CardHeader>
      </Card>

      {/* Results Summary */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className="px-3 py-1 bg-blue-100 text-blue-700">
            {filteredEmployees.length} of {employees.length} employees
            {debouncedSearchTerm && ` matching "${debouncedSearchTerm}"`}
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

      {/* Employee Display */}
      {filteredEmployees.length > 0 ? (
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
      ) : (
        <Card className="p-8 text-center border-blue-200 bg-blue-50">
          <div className="text-blue-500">
            <User className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <h3 className="text-lg font-semibold text-blue-900 mb-2">No employees found</h3>
            <p>
              {debouncedSearchTerm || departmentFilter !== "All Departments" || locationFilter !== "All Locations"
                ? "Try adjusting your search criteria or filters."
                : "No employee data available."}
            </p>
          </div>
        </Card>
      )}

      {/* Employee Detail Modal */}
      <Dialog open={showDetailModal} onOpenChange={closeDetailModal}>
        <DialogContent className="sm:max-w-2xl border-blue-200">
          <DialogHeader>
            <DialogTitle className="text-xl text-blue-900">Employee Details</DialogTitle>
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
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 bg-blue-100 rounded flex items-center justify-center">
                      <span className="text-xs text-blue-600">E</span>
                    </div>
                    <div>
                      <p className="text-sm text-blue-500">Extension</p>
                      <p className="font-medium text-blue-900">{selectedEmployee.extension !== "0" ? selectedEmployee.extension : "Not Available"}</p>
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