import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { PlusCircle, Calendar, User, Clock, CheckCircle, AlertCircle, Trash2, Edit3 } from 'lucide-react';
import { toast } from 'sonner';

const Work = () => {
  const [tasks, setTasks] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assigned_to: '',
    priority: 'medium',
    status: 'pending',
    due_date: ''
  });
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchTasks();
    fetchEmployees();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/tasks`);
      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      toast.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/employees`);
      if (response.ok) {
        const data = await response.json();
        setEmployees(data);
      }
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const method = editingTask ? 'PUT' : 'POST';
      const url = editingTask 
        ? `${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/tasks/${editingTask.id}`
        : `${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/tasks`;
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        toast.success(editingTask ? 'Task updated successfully' : 'Task created successfully');
        setFormData({
          title: '',
          description: '',
          assigned_to: '',
          priority: 'medium',
          status: 'pending',
          due_date: ''
        });
        setShowAddForm(false);
        setEditingTask(null);
        fetchTasks();
      } else {
        throw new Error('Failed to save task');
      }
    } catch (error) {
      console.error('Error saving task:', error);
      toast.error('Failed to save task');
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (response.ok) {
        toast.success('Task status updated');
        fetchTasks();
      } else {
        throw new Error('Failed to update task status');
      }
    } catch (error) {
      console.error('Error updating task status:', error);
      toast.error('Failed to update task status');
    }
  };

  const handleDelete = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'}/api/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        toast.success('Task deleted successfully');
        fetchTasks();
      } else {
        throw new Error('Failed to delete task');
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      toast.error('Failed to delete task');
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description,
      assigned_to: task.assigned_to,
      priority: task.priority,
      status: task.status,
      due_date: task.due_date ? task.due_date.split('T')[0] : ''
    });
    setShowAddForm(true);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'in_progress': return <Clock className="h-4 w-4 text-yellow-600" />;
      default: return <AlertCircle className="h-4 w-4 text-blue-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-green-100 text-green-800';
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  const getEmployeeName = (employeeId) => {
    const employee = employees.find(emp => emp.employee_id === employeeId);
    return employee ? employee.name : employeeId;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-blue-600">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-blue-900">Task Management</h2>
          <p className="text-blue-600 mt-1">Assign and track work tasks</p>
        </div>
        <Button
          onClick={() => {
            setShowAddForm(!showAddForm);
            setEditingTask(null);
            setFormData({
              title: '',
              description: '',
              assigned_to: '',
              priority: 'medium',
              status: 'pending',
              due_date: ''
            });
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          <PlusCircle className="h-4 w-4 mr-2" />
          Add Task
        </Button>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2 flex-wrap">
        {['all', 'pending', 'in_progress', 'completed'].map((status) => (
          <Button
            key={status}
            onClick={() => setFilter(status)}
            variant={filter === status ? "default" : "outline"}
            size="sm"
            className={filter === status ? "bg-blue-600 hover:bg-blue-700" : ""}
          >
            {status === 'all' ? 'All Tasks' : status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </Button>
        ))}
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <Card className="border-blue-200 shadow-sm">
          <CardHeader className="bg-blue-50">
            <CardTitle className="text-blue-900">
              {editingTask ? 'Edit Task' : 'Create New Task'}
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Title</label>
                  <Input
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Enter task title"
                    required
                    className="border-blue-200 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Assign to Employee</label>
                  <select
                    value={formData.assigned_to}
                    onChange={(e) => setFormData({ ...formData, assigned_to: e.target.value })}
                    required
                    className="w-full p-2 border border-blue-200 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Select Employee</option>
                    {employees.map((employee) => (
                      <option key={employee.employee_id} value={employee.employee_id}>
                        {employee.name} ({employee.employee_id})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-900 mb-2">Description</label>
                <Textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Enter task description"
                  required
                  rows={3}
                  className="border-blue-200 focus:border-blue-500"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full p-2 border border-blue-200 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full p-2 border border-blue-200 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-2">Due Date</label>
                  <Input
                    type="date"
                    value={formData.due_date}
                    onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                    className="border-blue-200 focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  {editingTask ? 'Update Task' : 'Create Task'}
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setShowAddForm(false);
                    setEditingTask(null);
                  }}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Tasks List */}
      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <Card className="border-blue-200">
            <CardContent className="p-8 text-center">
              <div className="text-blue-600 mb-2">No tasks found</div>
              <p className="text-sm text-gray-600">
                {filter === 'all' ? 'Click "Add Task" to create your first task.' : `No ${filter.replace('_', ' ')} tasks found.`}
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredTasks.map((task) => (
            <Card key={task.id} className="border-blue-200 shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-semibold text-blue-900">{task.title}</h3>
                      <div className="flex gap-2">
                        <Badge className={`text-xs ${getStatusColor(task.status)}`}>
                          {getStatusIcon(task.status)}
                          <span className="ml-1">{task.status.replace('_', ' ').toUpperCase()}</span>
                        </Badge>
                        <Badge className={`text-xs ${getPriorityColor(task.priority)}`}>
                          {task.priority.toUpperCase()}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-blue-600 mb-3">
                      <div className="flex items-center gap-1">
                        <User className="h-4 w-4" />
                        {getEmployeeName(task.assigned_to)}
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </div>
                      {task.due_date && (
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          Due: {new Date(task.due_date).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(task)}
                      className="text-blue-600 hover:bg-blue-50"
                    >
                      <Edit3 className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDelete(task.id)}
                      className="text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <p className="text-gray-700 leading-relaxed mb-4">{task.description}</p>
                
                {/* Status Change Buttons */}
                {task.status !== 'completed' && (
                  <div className="flex gap-2 pt-3 border-t border-gray-200">
                    {task.status === 'pending' && (
                      <Button
                        size="sm"
                        onClick={() => handleStatusChange(task.id, 'in_progress')}
                        className="bg-yellow-600 hover:bg-yellow-700 text-white"
                      >
                        Start Task
                      </Button>
                    )}
                    {task.status === 'in_progress' && (
                      <Button
                        size="sm"
                        onClick={() => handleStatusChange(task.id, 'completed')}
                        className="bg-green-600 hover:bg-green-700 text-white"
                      >
                        Mark Complete
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default Work;