import React, { useState, useMemo, useEffect } from "react";
import { Users, Plus, Trash2, RotateCcw, Network, Table as TableIcon, Save, Shield } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { mockEmployees, mockHierarchy, loadAllEmployeesFromExcel } from "../mock";
import HierarchyTree from "./HierarchyTree";
import HierarchyTable from "./HierarchyTable";
import SearchableSelect from "./ui/searchable-select";
import { toast } from "sonner";

const HierarchyBuilder = () => {
  const [hierarchyData, setHierarchyData] = useState([]); // Start with empty array
  const [selectedEmployee, setSelectedEmployee] = useState("");
  const [selectedManager, setSelectedManager] = useState("");
  const [viewMode, setViewMode] = useState("tree"); // tree or table
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

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

  // Get available employees for dropdown with search-friendly format
  const availableEmployees = useMemo(() => {
    return employees.map(emp => ({
      value: emp.id,
      label: `${emp.name} (${emp.id}) - ${emp.department}`,
      searchValue: `${emp.name} ${emp.id} ${emp.department}`.toLowerCase()
    }));
  }, [employees]);

  // Get available managers (all employees can be managers)
  const availableManagers = availableEmployees;

  // Build hierarchy structure for specific employee relationships only
  const hierarchyStructure = useMemo(() => {
    const empMap = new Map(employees.map(emp => [emp.id, emp]));
    const childrenMap = new Map();
    
    // Initialize children map
    employees.forEach(emp => {
      childrenMap.set(emp.id, []);
    });

    // Build children relationships from hierarchy data
    hierarchyData.forEach(rel => {
      const managerId = rel.reportsTo;
      if (childrenMap.has(managerId)) {
        const employee = empMap.get(rel.employeeId);
        if (employee) {
          childrenMap.get(managerId).push(employee);
        }
      }
    });

    // Return only employees involved in relationships (not all top-level employees)
    const employeesInRelationships = new Set();
    hierarchyData.forEach(rel => {
      employeesInRelationships.add(rel.employeeId);
      employeesInRelationships.add(rel.reportsTo);
    });
    
    const managersWithDirectReports = [...childrenMap.entries()]
      .filter(([managerId, children]) => children.length > 0)
      .map(([managerId]) => empMap.get(managerId))
      .filter(Boolean);

    return { empMap, childrenMap, topLevel: managersWithDirectReports };
  }, [hierarchyData, employees]);

  const handleAddRelationship = () => {
    if (!selectedEmployee || !selectedManager) {
      toast.error("Please select both employee and manager");
      return;
    }

    if (selectedEmployee === selectedManager) {
      toast.error("Employee cannot report to themselves");
      return;
    }

    // Check if relationship already exists
    const existingRelation = hierarchyData.find(rel => rel.employeeId === selectedEmployee);
    if (existingRelation) {
      toast.error("This employee already has a reporting manager");
      return;
    }

    // Add new relationship
    const newRelation = {
      employeeId: selectedEmployee,
      reportsTo: selectedManager
    };

    setHierarchyData(prev => [...prev, newRelation]);
    setSelectedEmployee("");
    setSelectedManager("");
    setHasUnsavedChanges(true);
    toast.success("Reporting relationship added! Click Save to persist changes.");
  };

  const handleRemoveRelationship = (employeeId) => {
    setHierarchyData(prev => prev.filter(rel => rel.employeeId !== employeeId));
    setHasUnsavedChanges(true);
    toast.success("Reporting relationship removed! Click Save to persist changes.");
  };

  const handleClearAll = () => {
    setHierarchyData([]);
    setHasUnsavedChanges(true);
    toast.success("All reporting relationships cleared! Click Save to persist changes.");
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      
      // Simulate API call to save hierarchy data
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setHasUnsavedChanges(false);
      toast.success("Hierarchy changes saved successfully!");
    } catch (error) {
      toast.error("Failed to save hierarchy changes");
    } finally {
      setIsSaving(false);
    }
  };

  const getEmployeeName = (employeeId) => {
    const employee = availableEmployees.find(emp => emp.id === employeeId);
    return employee ? employee.name : employeeId;
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
      {/* Header with View Toggle and Save Button */}
      <Card className="border-blue-200 shadow-sm bg-white">
        <CardHeader className="pb-4 bg-blue-50">
          <div className="flex justify-between items-center">
            <CardTitle className="flex items-center space-x-2 text-blue-900">
              <Shield className="h-5 w-5" />
              <span>Hierarchy Builder</span>
              {hasUnsavedChanges && (
                <Badge variant="secondary" className="ml-2 bg-orange-100 text-orange-700">
                  Unsaved Changes
                </Badge>
              )}
            </CardTitle>
            
            <div className="flex space-x-2">
              <Button
                variant={viewMode === "tree" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("tree")}
                className={`flex items-center space-x-2 ${
                  viewMode === "tree" 
                    ? "bg-blue-600 hover:bg-blue-700" 
                    : "border-blue-200 text-blue-700 hover:bg-blue-50"
                }`}
              >
                <Network className="h-4 w-4" />
                <span>Tree View</span>
              </Button>
              <Button
                variant={viewMode === "table" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("table")}
                className={`flex items-center space-x-2 ${
                  viewMode === "table" 
                    ? "bg-blue-600 hover:bg-blue-700" 
                    : "border-blue-200 text-blue-700 hover:bg-blue-50"
                }`}
              >
                <TableIcon className="h-4 w-4" />
                <span>Table View</span>
              </Button>
              
              {hasUnsavedChanges && (
                <Button
                  onClick={handleSave}
                  disabled={isSaving}
                  className="flex items-center space-x-2 bg-green-600 hover:bg-green-700"
                >
                  <Save className="h-4 w-4" />
                  <span>{isSaving ? "Saving..." : "Save Changes"}</span>
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Add Relationship Form */}
      <Card className="border-blue-200 shadow-sm bg-white">
        <CardHeader className="bg-blue-50">
          <CardTitle className="text-lg text-blue-900">Add Reporting Relationship</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Select Employee */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-blue-900">Select Employee</label>
              <Select value={selectedEmployee} onValueChange={setSelectedEmployee}>
                <SelectTrigger className="border-blue-200 focus:border-blue-400">
                  <SelectValue placeholder="Choose employee..." />
                </SelectTrigger>
                <SelectContent>
                  {availableEmployees.map(emp => (
                    <SelectItem key={emp.id} value={emp.id}>
                      {emp.name} ({emp.id}) - {emp.department}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Select Manager */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-blue-900">Reports To</label>
              <Select value={selectedManager} onValueChange={setSelectedManager}>
                <SelectTrigger className="border-blue-200 focus:border-blue-400">
                  <SelectValue placeholder="Choose manager..." />
                </SelectTrigger>
                <SelectContent>
                  {availableManagers.map(emp => (
                    <SelectItem key={emp.id} value={emp.id}>
                      {emp.name} ({emp.id}) - {emp.department}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2 items-end">
              <Button 
                onClick={handleAddRelationship} 
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add
              </Button>
              <Button 
                variant="outline" 
                onClick={handleClearAll}
                className="flex items-center space-x-2 border-blue-200 text-blue-700 hover:bg-blue-50"
              >
                <RotateCcw className="h-4 w-4" />
                <span>Clear All</span>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Current Relationships Summary */}
      <Card className="border-blue-200 shadow-sm bg-white">
        <CardHeader className="bg-blue-50">
          <CardTitle className="text-lg text-blue-900">Current Relationships ({hierarchyData.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          {hierarchyData.length === 0 ? (
            <div className="text-center py-8 text-blue-500">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No reporting relationships defined yet.</p>
              <p className="text-sm">Add relationships above to build the organizational hierarchy.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {hierarchyData.map(rel => (
                <div key={rel.employeeId} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="space-y-1">
                    <p className="font-medium text-sm text-blue-900">{getEmployeeName(rel.employeeId)}</p>
                    <p className="text-xs text-blue-600">reports to {getEmployeeName(rel.reportsTo)}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleRemoveRelationship(rel.employeeId)}
                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Hierarchy Display */}
      {hierarchyData.length > 0 && (
        <Card className="border-blue-200 shadow-sm bg-white">
          <CardHeader className="bg-blue-50">
            <CardTitle className="text-lg text-blue-900">Organizational Hierarchy Preview</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            {viewMode === "tree" ? (
              <HierarchyTree hierarchyStructure={hierarchyStructure} />
            ) : (
              <HierarchyTable hierarchyData={hierarchyData} employees={employees} />
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default HierarchyBuilder;