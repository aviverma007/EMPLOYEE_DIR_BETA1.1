// Frontend-only API using dataService
import dataService from './dataService';

// Employee API endpoints
export const employeeAPI = {
  // Get all employees with optional search and filters
  getAll: async (searchParams = {}) => {
    return await dataService.getEmployees(searchParams);
  },

  // Update employee profile image
  updateImage: async (employeeId, imageData) => {
    return await dataService.updateEmployeeImage(employeeId, imageData);
  },

  // Upload employee profile image file (original images)
  uploadImage: async (employeeId, imageFile) => {
    // Convert file to base64 for frontend storage
    const base64 = await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.readAsDataURL(imageFile);
    });
    
    return await dataService.updateEmployeeImage(employeeId, base64);
  }
};

// Hierarchy API endpoints
export const hierarchyAPI = {
  // Get all hierarchy relationships
  getAll: async () => {
    const response = await api.get('/api/hierarchy');
    return response.data;
  },

  // Add new hierarchy relationship
  create: async (relationshipData) => {
    const response = await api.post('/api/hierarchy', relationshipData);
    return response.data;
  },

  // Remove hierarchy relationship
  remove: async (employeeId) => {
    const response = await api.delete(`/api/hierarchy/${employeeId}`);
    return response.data;
  },

  // Clear all hierarchy relationships
  clearAll: async () => {
    const response = await api.delete('/api/hierarchy/clear');
    return response.data;
  }
};

// Utility API endpoints
export const utilityAPI = {
  // Refresh Excel data
  refreshExcel: async () => {
    const response = await api.post('/api/refresh-excel');
    return response.data;
  },

  // Get departments
  getDepartments: async () => {
    const response = await api.get('/api/departments');
    return response.data.departments;
  },

  // Get locations  
  getLocations: async () => {
    const response = await api.get('/api/locations');
    return response.data.locations;
  },

  // Get system statistics
  getStats: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  }
};

export default api;