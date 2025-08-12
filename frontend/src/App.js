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

// Import the 5 main components as per the required structure
import Home from "./components/Home";
import Work from "./components/Work";
import Knowledge from "./components/Knowledge";
import Help from "./components/Help";

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
            <div className="w-full h-screen flex flex-col">
              <Header />
              <div className="flex-1 w-full px-6 py-4">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full h-full flex flex-col">
                  {/* Navigation - 5 Tab Structure as per requirements */}
                  <div className="flex justify-start mb-4">
                    <TabsList className="flex w-auto h-10 bg-white shadow-md border border-blue-200 rounded-lg p-1">
                      <TabsTrigger 
                        value="home" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Home
                      </TabsTrigger>
                      
                      {/* Employee Directory Dropdown with Hierarchy */}
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
                      
                      <TabsTrigger 
                        value="work" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Work
                      </TabsTrigger>
                      <TabsTrigger 
                        value="knowledge" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Knowledge
                      </TabsTrigger>
                      <TabsTrigger 
                        value="help" 
                        className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700 rounded-md px-4 py-2"
                      >
                        Help
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
                      ) : (
                        <HierarchyBuilder />
                      )}
                    </TabsContent>
                    
                    <TabsContent value="work" className="mt-0 h-full">
                      <Work />
                    </TabsContent>
                    
                    <TabsContent value="knowledge" className="mt-0 h-full">
                      <Knowledge />
                    </TabsContent>
                    
                    <TabsContent value="help" className="mt-0 h-full">
                      <Help />
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