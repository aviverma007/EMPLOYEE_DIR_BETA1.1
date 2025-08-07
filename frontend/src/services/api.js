import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://2918f274-e9ec-4e1a-b511-774b77bd5ec3.preview.emergentagent.com';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API endpoints
export const employeeAPI = {
  // Get all employees with optional search and filters
  getAll: async (searchParams = {}) => {
    const params = new URLSearchParams();
    if (searchParams.search) params.append('search', searchParams.search);
    if (searchParams.department && searchParams.department !== 'All Departments') {
      params.append('department', searchParams.department);
    }
    if (searchParams.location && searchParams.location !== 'All Locations') {
      params.append('location', searchParams.location);
    }
    
    const response = await api.get(`/api/employees?${params}`);
    return response.data;
  },

  // Update employee profile image
  updateImage: async (employeeId, imageUrl) => {
    const response = await api.put(`/api/employees/${employeeId}/image`, {
      profileImage: imageUrl
    });
    return response.data;
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