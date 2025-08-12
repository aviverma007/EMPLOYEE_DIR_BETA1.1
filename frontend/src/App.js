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

// Import components
import Home from "./components/Home";
import Policies from "./components/Policies";
import Workflows from "./components/Workflows";
import ComingSoon from "./components/ComingSoon";
import Help from "./components/Help";
import MeetingRooms from "./components/MeetingRooms";

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
    <div className="App min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            <div className="w-full">
              <Header />
              <div className="container mx-auto px-4 py-4 max-w-7xl">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  {/* Navigation moved to top-left and made more compact */}
                  <div className="flex justify-start mb-4">
                    <TabsList className="flex w-auto h-10 bg-white shadow-md border border-blue-200 rounded-lg p-1">
                      <TabsTrigger 
                        value="home" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Home
                      </TabsTrigger>
                      
                      {/* Employee Directory Dropdown */}
                      <div className="relative">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              variant="ghost"
                              className={`h-8 text-sm font-medium rounded-md px-4 py-2 ${
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
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                      
                      <TabsTrigger 
                        value="policies" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Policies
                      </TabsTrigger>
                      <TabsTrigger 
                        value="workflows" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Workflows
                      </TabsTrigger>
                      <TabsTrigger 
                        value="meeting-rooms" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Meeting Rooms
                      </TabsTrigger>
                      <TabsTrigger 
                        value="coming-soon-2" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Coming Soon
                      </TabsTrigger>
                      <TabsTrigger 
                        value="help" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Help
                      </TabsTrigger>
                    </TabsList>
                  </div>
                  
                  <TabsContent value="home" className="mt-2">
                    <Home />
                  </TabsContent>
                  
                  <TabsContent value="directory" className="mt-2">
                    <EmployeeDirectory />
                  </TabsContent>
                  
                  <TabsContent value="policies" className="mt-2">
                    <Policies />
                  </TabsContent>
                  
                  <TabsContent value="workflows" className="mt-2">
                    <Workflows />
                  </TabsContent>
                  
                  <TabsContent value="meeting-rooms" className="mt-2">
                    <MeetingRooms />
                  </TabsContent>
                  
                  <TabsContent value="coming-soon-2" className="mt-2">
                    <ComingSoon title="Feature 2" />
                  </TabsContent>
                  
                  <TabsContent value="help" className="mt-2">
                    <Help />
                  </TabsContent>
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