import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { 
  DropdownMenu, 
  DropdownMenuTrigger, 
  DropdownMenuContent, 
  DropdownMenuItem 
} from "./components/ui/dropdown-menu";
import { AuthProvider, useAuth } from "./context/AuthContext.jsx";
import LoginForm from "./components/LoginForm";
import EmployeeDirectory from "./components/EmployeeDirectory";
import Header from "./components/Header";
import { Toaster } from "./components/ui/sonner";
import { ChevronDown } from "lucide-react";
import { Button } from "./components/ui/button";
import HierarchyBuilder from "./components/HierarchyBuilder";

// Import required components for complete feature set
import Home from "./components/Home";
import Help from "./components/Help";
import Work from "./components/Work";
import Knowledge from "./components/Knowledge";
import Policies from "./components/Policies";
import Workflows from "./components/Workflows";
import Attendance from "./components/Attendance";
import MeetingRooms from "./components/MeetingRooms";
import HolidayCalendar from "./components/HolidayCalendar";
import AlertManagement from "./components/AlertManagement";
import UserAlerts from "./components/UserAlerts";
import SyncStatus from "./components/SyncStatus";

const AppContent = () => {
  const { isAuthenticated, initializeAuth, isAdmin, isUser } = useAuth();
  const [activeTab, setActiveTab] = useState("home");
  const [activeDirectorySection, setActiveDirectorySection] = useState("directory");

  useEffect(() => {
    initializeAuth();
  }, []);

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <div className="App min-h-screen bg-blue-50">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            <div className="w-full min-h-screen flex flex-col">
              <Header />
              <div className="flex-1 w-full px-2 sm:px-4 lg:px-6 py-4">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full h-full flex flex-col">
                  {/* Navigation Tabs - Role-based access */}
                  <div className="flex justify-start mb-4 overflow-x-auto">
                  <TabsList className="flex w-auto h-10 bg-white shadow-md border border-blue-200 rounded-lg p-1 min-w-max">
                      <TabsTrigger 
                        value="home" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Home
                      </TabsTrigger>
                      
                      {/* Employee Directory - Admin gets dropdown, User gets direct access */}
                      {isAdmin() ? (
                        <div className="relative">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                className={`h-8 text-xs sm:text-sm font-medium rounded-md px-2 sm:px-4 py-2 whitespace-nowrap ${
                                  activeTab === "directory" 
                                    ? "bg-blue-600 text-white" 
                                    : "text-blue-700 hover:bg-blue-50"
                                } flex items-center justify-center gap-1`}
                                onClick={() => setActiveTab("directory")}
                              >
                                Employee Directory
                                <ChevronDown className="h-3 w-3" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="center" className="w-48">
                              <DropdownMenuItem 
                                onClick={() => {
                                  setActiveTab("directory");
                                  setActiveDirectorySection("directory");
                                }}
                                className="cursor-pointer"
                              >
                                Employee Directory
                              </DropdownMenuItem>
                              <DropdownMenuItem 
                                onClick={() => {
                                  setActiveTab("directory");
                                  setActiveDirectorySection("hierarchy");
                                }}
                                className="cursor-pointer"
                              >
                                Hierarchy Builder
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>
                      ) : (
                        <TabsTrigger 
                          value="directory" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Employee Directory
                        </TabsTrigger>
                      )}
                      
                      {/* Admin-only tabs */}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="work" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Work
                        </TabsTrigger>
                      )}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="knowledge" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Knowledge
                        </TabsTrigger>
                      )}
                      
                      {/* Both Admin and User get Policies */}
                      <TabsTrigger 
                        value="policies" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Policies
                      </TabsTrigger>
                      
                      {/* Admin-only tab */}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="workflows" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Workflows
                        </TabsTrigger>
                      )}
                      
                      {/* Both Admin and User get Meeting Rooms */}
                      <TabsTrigger 
                        value="meeting-rooms" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Meeting Rooms
                      </TabsTrigger>
                      
                      {/* Both Admin and User get Holiday Calendar */}
                      <TabsTrigger 
                        value="holiday-calendar" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Holiday Calendar
                      </TabsTrigger>
                      
                      {/* Admin-only tab */}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="attendance" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Attendance
                        </TabsTrigger>
                      )}
                      
                      {/* Admin-only Help tab */}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="help" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Help
                        </TabsTrigger>
                      )}
                      
                      {/* Admin-only Alerts tab */}
                      {isAdmin() && (
                        <TabsTrigger 
                          value="alerts" 
                          className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                        >
                          Alerts
                        </TabsTrigger>
                      )}
                    </TabsList>
                  </div>
                  
                  <div className="flex-1 overflow-auto">
                    <TabsContent value="home" className="mt-0 h-full">
                      <Home />
                    </TabsContent>
                    
                    <TabsContent value="directory" className="mt-0 h-full">
                      {isAdmin() && activeDirectorySection === "hierarchy" ? (
                        <HierarchyBuilder />
                      ) : (
                        <EmployeeDirectory />
                      )}
                    </TabsContent>
                    
                    {/* Admin-only content */}
                    {isAdmin() && (
                      <TabsContent value="work" className="mt-0 h-full">
                        <Work />
                      </TabsContent>
                    )}
                    
                    {isAdmin() && (
                      <TabsContent value="knowledge" className="mt-0 h-full">
                        <Knowledge />
                      </TabsContent>
                    )}
                    
                    {/* Both Admin and User can access Policies */}
                    <TabsContent value="policies" className="mt-0 h-full">
                      <Policies />
                    </TabsContent>
                    
                    {/* Admin-only content */}
                    {isAdmin() && (
                      <TabsContent value="workflows" className="mt-0 h-full">
                        <Workflows />
                      </TabsContent>
                    )}
                    
                    {/* Both Admin and User can access Meeting Rooms */}
                    <TabsContent value="meeting-rooms" className="mt-0 h-full">
                      <MeetingRooms />
                    </TabsContent>
                    
                    {/* Both Admin and User can access Holiday Calendar */}
                    <TabsContent value="holiday-calendar" className="mt-0 h-full">
                      <HolidayCalendar />
                    </TabsContent>
                    
                    {/* Admin-only content */}
                    {isAdmin() && (
                      <TabsContent value="attendance" className="mt-0 h-full">
                        <Attendance />
                      </TabsContent>
                    )}
                    
                    {/* Both Admin and User can access Help */}
                    <TabsContent value="help" className="mt-0 h-full">
                      <Help />
                    </TabsContent>
                    
                    {/* Admin-only Alerts Management */}
                    {isAdmin() && (
                      <TabsContent value="alerts" className="mt-0 h-full">
                        <AlertManagement />
                      </TabsContent>
                    )}
                  </div>
                </Tabs>
                
                {/* User Alerts - Show only for User role */}
                {isUser() && <UserAlerts />}
                
                {/* Sync Status - Show for all authenticated users */}
                <SyncStatus isAdmin={isAdmin()} />
              </div>
              <Toaster />
            </div>
          } />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;