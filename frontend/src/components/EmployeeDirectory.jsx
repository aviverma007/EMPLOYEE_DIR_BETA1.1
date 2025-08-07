import React, { useState, useMemo } from "react";
import { Search, Filter, Grid3X3, List, User, Phone, Mail, MapPin, Calendar, Briefcase } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { mockEmployees, departments, locations } from "../mock";
import EmployeeCard from "./EmployeeCard";
import EmployeeList from "./EmployeeList";

const EmployeeDirectory = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All Departments");
  const [locationFilter, setLocationFilter] = useState("All Locations");
  const [viewMode, setViewMode] = useState("grid"); // grid or list
  const [employees, setEmployees] = useState(mockEmployees);

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
            {filteredEmployees.length} employees found
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
        />
      ) : (
        <EmployeeList 
          employees={filteredEmployees} 
          onImageUpdate={handleImageUpdate}
        />
      )}
    </div>
  );
};

export default EmployeeDirectory;