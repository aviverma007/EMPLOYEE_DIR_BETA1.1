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
    return await dataService.getHierarchy();
  },

  // Add new hierarchy relationship
  create: async (relationshipData) => {
    return await dataService.createHierarchy(relationshipData);
  },

  // Remove hierarchy relationship
  remove: async (employeeId) => {
    return await dataService.deleteHierarchy(employeeId);
  },

  // Clear all hierarchy relationships
  clearAll: async () => {
    return await dataService.clearAllHierarchy();
  }
};

// Utility API endpoints
export const utilityAPI = {
  // Refresh Excel data (now just reloads from frontend)
  refreshExcel: async () => {
    const stats = await dataService.loadAllData();
    return { 
      message: 'Excel data refreshed successfully',
      count: stats.employees
    };
  },

  // Get departments
  getDepartments: async () => {
    return await dataService.getDepartments();
  },

  // Get locations  
  getLocations: async () => {
    return await dataService.getLocations();
  },

  // Get system statistics
  getStats: async () => {
    return await dataService.getStats();
  }
};

export default api;