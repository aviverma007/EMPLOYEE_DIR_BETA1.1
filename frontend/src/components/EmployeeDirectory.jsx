import React, { useState, useMemo, useEffect } from "react";
import { Search, Filter, Grid3X3, List, User, Phone, Mail, MapPin, Calendar, Briefcase, Eye, X } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { mockEmployees, departments, locations, loadAllEmployeesFromExcel } from "../mock";
import EmployeeCard from "./EmployeeCard";
import EmployeeList from "./EmployeeList";

const EmployeeDirectory = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All Departments");
  const [locationFilter, setLocationFilter] = useState("All Locations");
  const [viewMode, setViewMode] = useState("grid"); // grid or list
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);

  // Load all employees on component mount
  useEffect(() => {
    const loadEmployees = async () => {
      try {
        setLoading(true);
        const allEmployees = await loadAllEmployeesFromExcel();
        setEmployees(allEmployees);
      } catch (error) {
        console.error("Error loading employees:", error);
        setEmployees(mockEmployees);
      } finally {
        setLoading(false);
      }
    };

    loadEmployees();
  }, []);

  // Filter and search logic
  const filteredEmployees = useMemo(() => {
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
  }, [employees, searchTerm, departmentFilter, locationFilter]);

  const handleImageUpdate = (employeeId, newImage) => {
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
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading employee data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <Card className="border-0 shadow-sm bg-white">
        <CardHeader className="pb-4">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search by name, employee code, department, location, designation, mobile..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 h-11 border-gray-300 focus:border-slate-400"
              />
            </div>

            {/* Department Filter */}
            <div className="w-full lg:w-48">
              <Select value={departmentFilter} onValueChange={setDepartmentFilter}>
                <SelectTrigger className="h-11">
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
                <SelectTrigger className="h-11">
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
                className="h-11 px-3"
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "list" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("list")}
                className="h-11 px-3"
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
          <Badge variant="secondary" className="px-3 py-1">
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
            >
              Clear filters
            </Button>
          )}
        </div>
      </div>

      {/* Employee Display */}
      {viewMode === "grid" ? (
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
      )}

      {/* Employee Detail Modal */}
      <Dialog open={showDetailModal} onOpenChange={closeDetailModal}>
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <div className="flex items-center justify-between">
              <DialogTitle className="text-xl">Employee Details</DialogTitle>
              <Button variant="ghost" size="sm" onClick={closeDetailModal}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </DialogHeader>
          
          {selectedEmployee && (
            <div className="space-y-6">
              {/* Profile Section */}
              <div className="flex items-center space-x-6">
                <div className="w-24 h-24 rounded-full overflow-hidden bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
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
                  <User className="h-12 w-12 text-gray-500" style={{display: selectedEmployee.profileImage && selectedEmployee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">{selectedEmployee.name}</h2>
                  <Badge variant="secondary" className="mt-1">{selectedEmployee.id}</Badge>
                  <p className="text-lg text-slate-600 mt-2">{selectedEmployee.grade}</p>
                </div>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Briefcase className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-500">Department</p>
                      <p className="font-medium text-slate-900">{selectedEmployee.department}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <MapPin className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-500">Location</p>
                      <p className="font-medium text-slate-900">{selectedEmployee.location}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Phone className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-500">Mobile</p>
                      <p className="font-medium text-slate-900">{selectedEmployee.mobile}</p>
                      {selectedEmployee.extension !== "0" && (
                        <p className="text-sm text-gray-600">Ext: {selectedEmployee.extension}</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Mail className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-500">Email</p>
                      <p className="font-medium text-slate-900 text-sm">{selectedEmployee.email}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Calendar className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-500">Date of Joining</p>
                      <p className="font-medium text-slate-900">
                        {selectedEmployee.dateOfJoining ? new Date(selectedEmployee.dateOfJoining).toLocaleDateString() : 'N/A'}
                      </p>
                    </div>
                  </div>
                  
                  {selectedEmployee.reportingManager && selectedEmployee.reportingManager !== "*" && (
                    <div className="flex items-center space-x-3">
                      <User className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm text-gray-500">Reports To</p>
                        <p className="font-medium text-slate-900">{selectedEmployee.reportingManager}</p>
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