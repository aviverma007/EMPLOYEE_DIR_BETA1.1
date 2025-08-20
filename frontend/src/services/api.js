// Frontend-only API using dataService
import dataService from './dataService';
import imageStorage from './imageStorage';

// Employee API endpoints
export const employeeAPI = {
  // Get all employees with optional search and filters
  getAll: async (searchParams = {}) => {
    const employees = await dataService.getEmployees(searchParams);
    
    // Load stored images for all employees
    const allImages = await imageStorage.getAllImages();
    
    // Add stored images to employee data
    return employees.map(emp => ({
      ...emp,
      profileImage: allImages[emp.id] || emp.profileImage
    }));
  },

  // Update employee profile image
  updateImage: async (employeeId, imageData) => {
    // If it's base64 data, save to storage
    if (typeof imageData === 'string' && imageData.startsWith('data:image/')) {
      // Create a mock file object from base64 for storage
      const response = await fetch(imageData);
      const blob = await response.blob();
      const file = new File([blob], `profile_${employeeId}.jpg`, { type: blob.type });
      
      const savedUrl = await imageStorage.saveImage(employeeId, file);
      
      // Update in dataService as well
      const updatedEmployee = await dataService.updateEmployeeImage(employeeId, savedUrl);
      return { ...updatedEmployee, profileImage: savedUrl };
    }
    
    return await dataService.updateEmployeeImage(employeeId, imageData);
  },

  // Upload employee profile image file (original images)
  uploadImage: async (employeeId, imageFile) => {
    // Save the actual file to local storage
    const savedUrl = await imageStorage.saveImage(employeeId, imageFile);
    
    // Also update in dataService
    const updatedEmployee = await dataService.updateEmployeeImage(employeeId, savedUrl);
    
    return { ...updatedEmployee, profileImage: savedUrl };
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

// News API endpoints
export const newsAPI = {
  getAll: async () => {
    return await dataService.getNews();
  },

  create: async (newsData) => {
    return await dataService.createNews(newsData);
  },

  update: async (id, newsData) => {
    return await dataService.updateNews(id, newsData);
  },

  delete: async (id) => {
    return await dataService.deleteNews(id);
  }
};

// Task API endpoints
export const taskAPI = {
  getAll: async () => {
    return await dataService.getTasks();
  },

  create: async (taskData) => {
    return await dataService.createTask(taskData);
  },

  update: async (id, taskData) => {
    return await dataService.updateTask(id, taskData);
  },

  delete: async (id) => {
    return await dataService.deleteTask(id);
  }
};

// Knowledge API endpoints
export const knowledgeAPI = {
  getAll: async () => {
    return await dataService.getKnowledge();
  },

  create: async (knowledgeData) => {
    return await dataService.createKnowledge(knowledgeData);
  },

  update: async (id, knowledgeData) => {
    return await dataService.updateKnowledge(id, knowledgeData);
  },

  delete: async (id) => {
    return await dataService.deleteKnowledge(id);
  }
};

// Help API endpoints
export const helpAPI = {
  getAll: async () => {
    return await dataService.getHelp();
  },

  create: async (helpData) => {
    return await dataService.createHelp(helpData);
  },

  update: async (id, helpData) => {
    return await dataService.updateHelp(id, helpData);
  },

  addReply: async (id, replyData) => {
    return await dataService.addHelpReply(id, replyData);
  },

  delete: async (id) => {
    return await dataService.deleteHelp(id);
  }
};

// Meeting Rooms API endpoints
export const meetingRoomAPI = {
  getAll: async (filters = {}) => {
    return await dataService.getMeetingRooms(filters);
  },

  getLocations: async () => {
    return await dataService.getLocations();
  },

  getFloors: async () => {
    // Extract floors from meeting rooms data
    const rooms = await dataService.getMeetingRooms();
    const floors = [...new Set(rooms.map(room => room.floor))];
    return floors;
  },

  book: async (roomId, bookingData) => {
    return await dataService.bookMeetingRoom(roomId, bookingData);
  },

  cancelBooking: async (roomId, bookingId = null) => {
    return await dataService.cancelMeetingRoomBooking(roomId, bookingId);
  },

  clearAllBookings: async () => {
    return await dataService.clearAllMeetingRoomBookings();
  }
};

// Attendance API endpoints
export const attendanceAPI = {
  getAll: async (searchParams = {}) => {
    return await dataService.getAttendance(searchParams);
  },

  create: async (attendanceData) => {
    return await dataService.createAttendance(attendanceData);
  },

  update: async (id, attendanceData) => {
    // For frontend-only, we'll just update the existing record
    const attendance = dataService.attendance.find(a => a.id === id);
    if (attendance) {
      Object.assign(attendance, attendanceData, { updated_at: new Date().toISOString() });
      return attendance;
    }
    throw new Error('Attendance record not found');
  }
};

// Policies API endpoints
export const policyAPI = {
  getAll: async () => {
    return await dataService.getPolicies();
  },

  create: async (policyData) => {
    return await dataService.createPolicy(policyData);
  },

  update: async (id, policyData) => {
    const index = dataService.policies.findIndex(p => p.id === id);
    if (index > -1) {
      dataService.policies[index] = {
        ...dataService.policies[index],
        ...policyData,
        updated_at: new Date().toISOString()
      };
      return dataService.policies[index];
    }
    throw new Error('Policy not found');
  },

  delete: async (id) => {
    const index = dataService.policies.findIndex(p => p.id === id);
    if (index > -1) {
      dataService.policies.splice(index, 1);
      return { message: 'Policy deleted' };
    }
    throw new Error('Policy not found');
  }
};

// Workflows API endpoints
export const workflowAPI = {
  getAll: async () => {
    return await dataService.getWorkflows();
  },

  create: async (workflowData) => {
    return await dataService.createWorkflow(workflowData);
  },

  update: async (id, workflowData) => {
    const index = dataService.workflows.findIndex(w => w.id === id);
    if (index > -1) {
      dataService.workflows[index] = {
        ...dataService.workflows[index],
        ...workflowData,
        updated_at: new Date().toISOString()
      };
      return dataService.workflows[index];
    }
    throw new Error('Workflow not found');
  }
};

// Chat API endpoints (simplified for frontend-only)
export const chatAPI = {
  getHistory: async (sessionId) => {
    // Return empty history for frontend-only mode
    return [];
  },

  send: async (message, sessionId) => {
    // Return a mock response for frontend-only mode
    return {
      response: "I'm sorry, the AI chat feature is currently unavailable in offline mode. Please use other features of the application.",
      sessionId: sessionId
    };
  },

  clearHistory: async (sessionId) => {
    // No-op for frontend-only mode
    return { message: 'Chat history cleared' };
  }
};