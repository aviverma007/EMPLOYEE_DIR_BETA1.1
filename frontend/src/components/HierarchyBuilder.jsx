import React, { useState, useMemo, useEffect } from "react";
import { Users, Plus, Trash2, RotateCcw, Network, Table as TableIcon, Save } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { mockEmployees, mockHierarchy, loadAllEmployeesFromExcel } from "../mock";
import HierarchyTree from "./HierarchyTree";
import HierarchyTable from "./HierarchyTable";
import { toast } from "sonner";

const HierarchyBuilder = () => {
  const [hierarchyData, setHierarchyData] = useState(mockHierarchy);
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

  // Get available employees for dropdown
  const availableEmployees = employees.map(emp => ({
    id: emp.id,
    name: emp.name,
    department: emp.department
  }));

  // Get available managers (all employees can be managers)
  const availableManagers = availableEmployees;

  // Build hierarchy structure for tree view
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

    // Find top-level employees (those without managers)
    const employeesWithManagers = new Set(hierarchyData.map(rel => rel.employeeId));
    const topLevel = employees.filter(emp => !employeesWithManagers.has(emp.id));

    return { empMap, childrenMap, topLevel };
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

  return (
    <div className="space-y-6">
      {/* Header with View Toggle */}
      <Card className="border-0 shadow-sm bg-white">
        <CardHeader className="pb-4">
          <div className="flex justify-between items-center">
            <CardTitle className="flex items-center space-x-2">
              <Network className="h-5 w-5" />
              <span>Hierarchy Builder</span>
            </CardTitle>
            
            <div className="flex space-x-2">
              <Button
                variant={viewMode === "tree" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("tree")}
                className="flex items-center space-x-2"
              >
                <Network className="h-4 w-4" />
                <span>Tree View</span>
              </Button>
              <Button
                variant={viewMode === "table" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("table")}
                className="flex items-center space-x-2"
              >
                <TableIcon className="h-4 w-4" />
                <span>Table View</span>
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Add Relationship Form */}
      <Card className="border-0 shadow-sm bg-white">
        <CardHeader>
          <CardTitle className="text-lg">Add Reporting Relationship</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Select Employee */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Select Employee</label>
              <Select value={selectedEmployee} onValueChange={setSelectedEmployee}>
                <SelectTrigger>
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
              <label className="text-sm font-medium">Reports To</label>
              <Select value={selectedManager} onValueChange={setSelectedManager}>
                <SelectTrigger>
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
              <Button onClick={handleAddRelationship} className="flex-1">
                <Plus className="h-4 w-4 mr-2" />
                Add
              </Button>
              <Button 
                variant="outline" 
                onClick={handleClearAll}
                className="flex items-center space-x-2"
              >
                <RotateCcw className="h-4 w-4" />
                <span>Clear All</span>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Current Relationships Summary */}
      <Card className="border-0 shadow-sm bg-white">
        <CardHeader>
          <CardTitle className="text-lg">Current Relationships ({hierarchyData.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {hierarchyData.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No reporting relationships defined yet.</p>
              <p className="text-sm">Add relationships above to build the organizational hierarchy.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {hierarchyData.map(rel => (
                <div key={rel.employeeId} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div className="space-y-1">
                    <p className="font-medium text-sm">{getEmployeeName(rel.employeeId)}</p>
                    <p className="text-xs text-gray-600">reports to {getEmployeeName(rel.reportsTo)}</p>
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
        <Card className="border-0 shadow-sm bg-white">
          <CardHeader>
            <CardTitle className="text-lg">Organizational Hierarchy</CardTitle>
          </CardHeader>
          <CardContent>
            {viewMode === "tree" ? (
              <HierarchyTree hierarchyStructure={hierarchyStructure} />
            ) : (
              <HierarchyTable hierarchyData={hierarchyData} employees={mockEmployees} />
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default HierarchyBuilder;