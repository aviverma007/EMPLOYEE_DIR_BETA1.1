import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Badge } from "./ui/badge";
import { 
  AlertTriangle, 
  Bell, 
  CheckCircle, 
  Info, 
  X, 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  EyeOff,
  Calendar,
  Clock
} from "lucide-react";
import { toast } from "sonner";
import dataService from "../services/dataService";
import useSharedDataSync from '../hooks/useSharedDataSync';

const AlertManagement = () => {
  const { dataUpdates } = useSharedDataSync(['alerts']); // Listen for alert updates
  const [alerts, setAlerts] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingAlert, setEditingAlert] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    message: "",
    type: "info",
    priority: "normal",
    isActive: true,
    expiryDate: ""
  });

  // Load alerts on component mount
  useEffect(() => {
    loadAlerts();
  }, []);

  // Listen for real-time alert updates from other systems
  useEffect(() => {
    const handleSharedDataUpdate = (event) => {
      if (event.detail.dataType === 'alerts') {
        console.log('[AlertManagement] Received real-time update from another system');
        loadAlerts(); // Refresh alert data when changes detected
        toast.info('Alerts updated from another system', {
          duration: 3000,
        });
      }
    };

    window.addEventListener('sharedDataUpdate', handleSharedDataUpdate);
    return () => window.removeEventListener('sharedDataUpdate', handleSharedDataUpdate);
  }, []);

  const loadAlerts = () => {
    try {
      const alertsData = dataService.getAlerts();
      setAlerts(alertsData);
    } catch (error) {
      console.error('Error loading alerts:', error);
      toast.error('Failed to load alerts');
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim() || !formData.message.trim()) {
      toast.error('Title and message are required');
      return;
    }

    try {
      if (editingAlert) {
        // Update existing alert
        await dataService.updateAlert(editingAlert.id, formData);
        toast.success('Alert updated successfully');
      } else {
        // Create new alert
        await dataService.createAlert(formData);
        toast.success('Alert created successfully');
      }
      
      loadAlerts();
      resetForm();
    } catch (error) {
      console.error('Error saving alert:', error);
      toast.error('Failed to save alert');
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      message: "",
      type: "info",
      priority: "normal",
      isActive: true,
      expiryDate: ""
    });
    setShowForm(false);
    setEditingAlert(null);
  };

  const handleEdit = (alert) => {
    setFormData({
      title: alert.title,
      message: alert.message,
      type: alert.type,
      priority: alert.priority,
      isActive: alert.isActive,
      expiryDate: alert.expiryDate || ""
    });
    setEditingAlert(alert);
    setShowForm(true);
  };

  const handleDelete = async (alertId) => {
    if (window.confirm('Are you sure you want to delete this alert?')) {
      try {
        await dataService.deleteAlert(alertId);
        toast.success('Alert deleted successfully');
        loadAlerts();
      } catch (error) {
        console.error('Error deleting alert:', error);
        toast.error('Failed to delete alert');
      }
    }
  };

  const handleToggleStatus = async (alertId) => {
    try {
      await dataService.toggleAlertStatus(alertId);
      toast.success('Alert status updated');
      loadAlerts();
    } catch (error) {
      console.error('Error toggling alert status:', error);
      toast.error('Failed to update alert status');
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error': return <AlertTriangle className="h-4 w-4" />;
      case 'warning': return <AlertTriangle className="h-4 w-4" />;
      case 'success': return <CheckCircle className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  const getAlertColors = (type) => {
    switch (type) {
      case 'error': return 'bg-red-100 text-red-800 border-red-200';
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'success': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-blue-100 text-blue-800 border-blue-200';
    }
  };

  const getPriorityColors = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-700';
      case 'low': return 'bg-gray-100 text-gray-700';
      default: return 'bg-blue-100 text-blue-700';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Alert Management</h1>
          <p className="text-gray-600 mt-1">Create and manage alerts for users</p>
        </div>
        <Button 
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          New Alert
        </Button>
      </div>

      {/* Alert Form */}
      {showForm && (
        <Card className="border-blue-200">
          <CardHeader className="bg-blue-50">
            <CardTitle className="flex items-center text-blue-900">
              <Bell className="h-5 w-5 mr-2" />
              {editingAlert ? 'Edit Alert' : 'Create New Alert'}
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Alert Title *
                  </label>
                  <Input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    placeholder="Enter alert title"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Alert Type
                  </label>
                  <select
                    name="type"
                    value={formData.type}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="info">Info</option>
                    <option value="success">Success</option>
                    <option value="warning">Warning</option>
                    <option value="error">Error</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Message *
                </label>
                <Textarea
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  placeholder="Enter alert message"
                  rows={4}
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Priority
                  </label>
                  <select
                    name="priority"
                    value={formData.priority}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="low">Low</option>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Expiry Date (Optional)
                  </label>
                  <Input
                    type="datetime-local"
                    name="expiryDate"
                    value={formData.expiryDate}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="isActive"
                    name="isActive"
                    checked={formData.isActive}
                    onChange={handleInputChange}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label htmlFor="isActive" className="text-sm font-medium text-gray-700">
                    Active
                  </label>
                </div>
              </div>

              <div className="flex space-x-4 pt-4">
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  {editingAlert ? 'Update Alert' : 'Create Alert'}
                </Button>
                <Button type="button" variant="outline" onClick={resetForm}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Alerts List */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Bell className="h-5 w-5 mr-2" />
            All Alerts ({alerts.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {alerts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Bell className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No alerts created yet</p>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts.map((alert) => (
                <div key={alert.id} className={`border rounded-lg p-4 ${getAlertColors(alert.type)}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        {getAlertIcon(alert.type)}
                        <h3 className="font-semibold text-lg">{alert.title}</h3>
                        <Badge className={getPriorityColors(alert.priority)}>
                          {alert.priority.toUpperCase()}
                        </Badge>
                        {alert.isActive ? (
                          <Badge className="bg-green-100 text-green-700">
                            <Eye className="h-3 w-3 mr-1" />
                            Active
                          </Badge>
                        ) : (
                          <Badge className="bg-gray-100 text-gray-700">
                            <EyeOff className="h-3 w-3 mr-1" />
                            Inactive
                          </Badge>
                        )}
                      </div>
                      
                      <p className="text-sm mb-3">{alert.message}</p>
                      
                      <div className="flex items-center space-x-4 text-xs">
                        <span className="flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          Created: {new Date(alert.created_at).toLocaleDateString()}
                        </span>
                        {alert.expiryDate && (
                          <span className="flex items-center">
                            <Calendar className="h-3 w-3 mr-1" />
                            Expires: {new Date(alert.expiryDate).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleToggleStatus(alert.id)}
                        className="h-8"
                      >
                        {alert.isActive ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleEdit(alert)}
                        className="h-8"
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleDelete(alert.id)}
                        className="h-8 text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AlertManagement;