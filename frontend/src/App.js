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
import { AuthProvider, useAuth } from "./context/AuthContext";
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

const AppContent = () => {
  const { isAuthenticated, initializeAuth, isAdmin } = useAuth();
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
                  {/* Navigation Tabs - Different for Admin vs User */}
                  <div className="flex justify-start mb-4 overflow-x-auto">
                  <TabsList className="flex w-auto h-10 bg-white shadow-md border border-blue-200 rounded-lg p-1 min-w-max">
                      <TabsTrigger 
                        value="home" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Home
                      </TabsTrigger>
                      
                      {/* Admin gets Employee Directory with Hierarchy dropdown, User gets just Employee Directory */}
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
                          onClick={() => {
                            setActiveTab("directory");
                            setActiveDirectorySection("directory");
                          }}
                        >
                          Employee Directory
                        </TabsTrigger>
                      )}
                      
                      {/* Both Admin and User get limited tabs as requested */}
                      <TabsTrigger 
                        value="policies" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Policies
                      </TabsTrigger>
                      <TabsTrigger 
                        value="meeting-rooms" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Meeting Rooms
                      </TabsTrigger>
                      <TabsTrigger 
                        value="holiday-calendar" 
                        className="text-xs sm:text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-2 sm:px-4 py-2 whitespace-nowrap"
                      >
                        Holiday Calendar
                      </TabsTrigger>
                    </TabsList>
                  </div>
                  
                  <div className="flex-1 overflow-auto">
                    <TabsContent value="home" className="mt-0 h-full">
                      <Home />
                    </TabsContent>
                    
                    <TabsContent value="directory" className="mt-0 h-full">
                      {activeDirectorySection === "directory" ? (
                        <EmployeeDirectory />
                      ) : isAdmin() ? (
                        <HierarchyBuilder />
                      ) : (
                        <EmployeeDirectory />
                      )}
                    </TabsContent>
                    
                    {/* Both Admin and User get limited content as requested */}
                    <TabsContent value="policies" className="mt-0 h-full">
                      <Policies />
                    </TabsContent>
                    
                    <TabsContent value="meeting-rooms" className="mt-0 h-full">
                      <MeetingRooms />
                    </TabsContent>
                    
                    <TabsContent value="holiday-calendar" className="mt-0 h-full">
                      <HolidayCalendar />
                    </TabsContent>
                  </div>
                </Tabs>
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