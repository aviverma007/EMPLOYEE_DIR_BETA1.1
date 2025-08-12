import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { 
  Workflow,
  Plus,
  Search,
  Filter,
  Calendar,
  User,
  Edit,
  Trash2,
  Eye,
  CheckCircle,
  Clock,
  Play,
  Pause
} from "lucide-react";

const Workflows = () => {
  const [workflows, setWorkflows] = useState([]);
  const [filteredWorkflows, setFilteredWorkflows] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  
  // Form state
  const [workflowForm, setWorkflowForm] = useState({
    name: "",
    description: "",
    category: "general",
    steps: []
  });
  const [stepForm, setStepForm] = useState({
    name: "",
    description: "",
    assigned_to: ""
  });
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showViewDialog, setShowViewDialog] = useState(false);
  const [showStepDialog, setShowStepDialog] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  const categories = [
    "general", "hr", "finance", "operations", "it", "procurement", "project", "quality"
  ];

  const statuses = ["active", "inactive", "completed"];

  // Fetch workflows and employees
  useEffect(() => {
    fetchWorkflows();
    fetchEmployees();
  }, []);

  // Apply filters
  useEffect(() => {
    let filtered = workflows;

    if (searchTerm) {
      filtered = filtered.filter(workflow =>
        workflow.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        workflow.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedCategory && selectedCategory !== "all") {
      filtered = filtered.filter(workflow => workflow.category === selectedCategory);
    }

    if (selectedStatus && selectedStatus !== "all") {
      filtered = filtered.filter(workflow => workflow.status === selectedStatus);
    }

    setFilteredWorkflows(filtered);
  }, [workflows, searchTerm, selectedCategory, selectedStatus]);

  const fetchWorkflows = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/workflows`);
      if (response.ok) {
        const data = await response.json();
        setWorkflows(data);
      }
    } catch (error) {
      console.error('Error fetching workflows:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/employees`);
      if (response.ok) {
        const data = await response.json();
        setEmployees(data);
      }
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleCreateWorkflow = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/workflows`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(workflowForm),
      });

      if (response.ok) {
        setShowCreateDialog(false);
        resetForms();
        fetchWorkflows();
        alert('Workflow created successfully!');
      } else {
        const error = await response.json();
        alert(`Error creating workflow: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error creating workflow:', error);
      alert('Failed to create workflow');
    }
  };

  const handleUpdateWorkflow = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/workflows/${selectedWorkflow.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(workflowForm),
      });

      if (response.ok) {
        setShowEditDialog(false);
        resetForms();
        setSelectedWorkflow(null);
        fetchWorkflows();
        alert('Workflow updated successfully!');
      } else {
        const error = await response.json();
        alert(`Error updating workflow: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error updating workflow:', error);
      alert('Failed to update workflow');
    }
  };

  const handleDeleteWorkflow = async (workflowId) => {
    if (window.confirm('Are you sure you want to delete this workflow?')) {
      try {
        const response = await fetch(`${backendUrl}/api/workflows/${workflowId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchWorkflows();
          alert('Workflow deleted successfully!');
        } else {
          alert('Failed to delete workflow');
        }
      } catch (error) {
        console.error('Error deleting workflow:', error);
        alert('Failed to delete workflow');
      }
    }
  };

  const resetForms = () => {
    setWorkflowForm({
      name: "",
      description: "",
      category: "general",
      steps: []
    });
    setStepForm({
      name: "",
      description: "",
      assigned_to: ""
    });
  };

  const addStep = () => {
    if (stepForm.name && stepForm.description) {
      setWorkflowForm(prev => ({
        ...prev,
        steps: [...prev.steps, { ...stepForm, status: "pending" }]
      }));
      setStepForm({
        name: "",
        description: "",
        assigned_to: ""
      });
      setShowStepDialog(false);
    }
  };

  const removeStep = (index) => {
    setWorkflowForm(prev => ({
      ...prev,
      steps: prev.steps.filter((_, i) => i !== index)
    }));
  };

  const getCategoryColor = (category) => {
    const colors = {
      general: 'bg-blue-100 text-blue-800',
      hr: 'bg-green-100 text-green-800',
      finance: 'bg-yellow-100 text-yellow-800',
      operations: 'bg-purple-100 text-purple-800',
      it: 'bg-indigo-100 text-indigo-800',
      procurement: 'bg-pink-100 text-pink-800',
      project: 'bg-orange-100 text-orange-800',
      quality: 'bg-red-100 text-red-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      completed: 'bg-blue-100 text-blue-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStepStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'in_progress':
        return <Play className="h-4 w-4 text-blue-600" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const startEdit = (workflow) => {
    setSelectedWorkflow(workflow);
    setWorkflowForm({
      name: workflow.name,
      description: workflow.description,
      category: workflow.category,
      steps: workflow.steps || []
    });
    setShowEditDialog(true);
  };

  const viewWorkflow = (workflow) => {
    setSelectedWorkflow(workflow);
    setShowViewDialog(true);
  };

  const getEmployeeName = (employeeId) => {
    const employee = employees.find(emp => emp.id === employeeId);
    return employee ? employee.name : 'Unassigned';
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Workflows</h1>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="h-4 w-4 mr-2" />
              Create Workflow
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl">
            <DialogHeader>
              <DialogTitle>Create New Workflow</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Name</Label>
                  <Input
                    value={workflowForm.name}
                    onChange={(e) => setWorkflowForm(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Workflow name..."
                  />
                </div>
                <div>
                  <Label>Category</Label>
                  <Select value={workflowForm.category} onValueChange={(value) => setWorkflowForm(prev => ({ ...prev, category: value }))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((cat) => (
                        <SelectItem key={cat} value={cat}>
                          {cat.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div>
                <Label>Description</Label>
                <Textarea
                  value={workflowForm.description}
                  onChange={(e) => setWorkflowForm(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Workflow description..."
                  rows={3}
                />
              </div>

              {/* Steps Section */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <Label>Steps ({workflowForm.steps.length})</Label>
                  <Dialog open={showStepDialog} onOpenChange={setShowStepDialog}>
                    <DialogTrigger asChild>
                      <Button size="sm" variant="outline">
                        <Plus className="h-4 w-4 mr-1" />
                        Add Step
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Add Workflow Step</DialogTitle>
                      </DialogHeader>
                      <div className="space-y-4">
                        <div>
                          <Label>Step Name</Label>
                          <Input
                            value={stepForm.name}
                            onChange={(e) => setStepForm(prev => ({ ...prev, name: e.target.value }))}
                            placeholder="Step name..."
                          />
                        </div>
                        <div>
                          <Label>Description</Label>
                          <Textarea
                            value={stepForm.description}
                            onChange={(e) => setStepForm(prev => ({ ...prev, description: e.target.value }))}
                            placeholder="Step description..."
                            rows={3}
                          />
                        </div>
                        <div>
                          <Label>Assign To</Label>
                          <Select value={stepForm.assigned_to} onValueChange={(value) => setStepForm(prev => ({ ...prev, assigned_to: value }))}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select employee" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="none">Unassigned</SelectItem>
                              {employees.map((emp) => (
                                <SelectItem key={emp.id} value={emp.id}>
                                  {emp.name} ({emp.id})
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="flex gap-2">
                          <Button onClick={addStep} disabled={!stepForm.name || !stepForm.description}>
                            Add Step
                          </Button>
                          <Button variant="outline" onClick={() => setShowStepDialog(false)}>
                            Cancel
                          </Button>
                        </div>
                      </div>
                    </DialogContent>
                  </Dialog>
                </div>

                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {workflowForm.steps.map((step, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                      <div className="flex-1">
                        <div className="font-medium text-sm">{step.name}</div>
                        <div className="text-xs text-gray-500">{step.description}</div>
                        <div className="text-xs text-gray-400">
                          Assigned to: {getEmployeeName(step.assigned_to)}
                        </div>
                      </div>
                      <Button size="sm" variant="outline" onClick={() => removeStep(index)}>
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex gap-2">
                <Button onClick={handleCreateWorkflow} disabled={!workflowForm.name || !workflowForm.description}>
                  Create Workflow
                </Button>
                <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative md:col-span-2">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search workflows..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat.toUpperCase()}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger>
                <SelectValue placeholder="Select Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                {statuses.map((status) => (
                  <SelectItem key={status} value={status}>
                    {status.toUpperCase()}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Workflows List */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-gray-500">Loading workflows...</div>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredWorkflows.map((workflow) => (
              <Card key={workflow.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{workflow.name}</CardTitle>
                      <p className="text-gray-600 mt-1">{workflow.description}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500 mt-2">
                        <Badge className={`${getCategoryColor(workflow.category)} border-0`}>
                          {workflow.category.toUpperCase()}
                        </Badge>
                        <Badge className={`${getStatusColor(workflow.status)} border-0`}>
                          {workflow.status.toUpperCase()}
                        </Badge>
                        <div className="flex items-center gap-1">
                          <Workflow className="h-4 w-4" />
                          {workflow.steps?.length || 0} steps
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" onClick={() => viewWorkflow(workflow)}>
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => startEdit(workflow)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => handleDeleteWorkflow(workflow.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                
                {workflow.steps && workflow.steps.length > 0 && (
                  <CardContent>
                    <div className="text-sm font-medium mb-2">Steps Progress:</div>
                    <div className="space-y-1">
                      {workflow.steps.slice(0, 3).map((step, index) => (
                        <div key={index} className="flex items-center gap-2 text-sm">
                          {getStepStatusIcon(step.status)}
                          <span className="flex-1">{step.name}</span>
                          <span className="text-gray-400">{getEmployeeName(step.assigned_to)}</span>
                        </div>
                      ))}
                      {workflow.steps.length > 3 && (
                        <div className="text-xs text-gray-500">
                          +{workflow.steps.length - 3} more steps
                        </div>
                      )}
                    </div>
                  </CardContent>
                )}
              </Card>
            ))}
          </div>
        )}

        {!loading && filteredWorkflows.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No workflows found</div>
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filters or create a new workflow</div>
          </div>
        )}
      </div>

      {/* Edit Dialog - Similar to Create but with pre-filled data */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Edit Workflow</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Name</Label>
                <Input
                  value={workflowForm.name}
                  onChange={(e) => setWorkflowForm(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Workflow name..."
                />
              </div>
              <div>
                <Label>Category</Label>
                <Select value={workflowForm.category} onValueChange={(value) => setWorkflowForm(prev => ({ ...prev, category: value }))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat.toUpperCase()}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <div>
              <Label>Description</Label>
              <Textarea
                value={workflowForm.description}
                onChange={(e) => setWorkflowForm(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Workflow description..."
                rows={3}
              />
            </div>

            <div className="flex gap-2">
              <Button onClick={handleUpdateWorkflow} disabled={!workflowForm.name || !workflowForm.description}>
                Update Workflow
              </Button>
              <Button variant="outline" onClick={() => setShowEditDialog(false)}>
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* View Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>{selectedWorkflow?.name}</DialogTitle>
          </DialogHeader>
          {selectedWorkflow && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <Badge className={`${getCategoryColor(selectedWorkflow.category)} border-0`}>
                  {selectedWorkflow.category.toUpperCase()}
                </Badge>
                <Badge className={`${getStatusColor(selectedWorkflow.status)} border-0`}>
                  {selectedWorkflow.status.toUpperCase()}
                </Badge>
                <div className="flex items-center gap-1">
                  <User className="h-4 w-4" />
                  {selectedWorkflow.created_by}
                </div>
              </div>
              
              <div>
                <h3 className="font-medium mb-2">Description:</h3>
                <p className="text-gray-700">{selectedWorkflow.description}</p>
              </div>

              {selectedWorkflow.steps && selectedWorkflow.steps.length > 0 && (
                <div>
                  <h3 className="font-medium mb-2">Steps ({selectedWorkflow.steps.length}):</h3>
                  <div className="space-y-3">
                    {selectedWorkflow.steps.map((step, index) => (
                      <div key={index} className="border rounded-lg p-3">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              {getStepStatusIcon(step.status)}
                              <span className="font-medium">Step {index + 1}: {step.name}</span>
                            </div>
                            <p className="text-gray-600 text-sm mb-2">{step.description}</p>
                            <div className="text-xs text-gray-500">
                              Assigned to: {getEmployeeName(step.assigned_to)}
                            </div>
                          </div>
                          <Badge variant="outline" className="ml-2">
                            {step.status}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Workflows;