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
import HierarchyBuilder from "./components/HierarchyBuilder";
import HierarchyViewer from "./components/HierarchyViewer";
import Header from "./components/Header";
import { Toaster } from "./components/ui/sonner";
import { ChevronDown } from "lucide-react";
import { Button } from "./components/ui/button";

// Import new components
import Home from "./components/Home";
import Work from "./components/Work";
import Knowledge from "./components/Knowledge";
import Help from "./components/Help";
import PO from "./components/PO";
import PS from "./components/PS";

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
              <div className="container mx-auto px-4 py-8 max-w-7xl">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-5 max-w-4xl mx-auto mb-8 h-12 bg-white shadow-sm border border-blue-200">
                    <TabsTrigger 
                      value="home" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      Home
                    </TabsTrigger>
                    
                    {/* Employee Directory Dropdown */}
                    <div className="relative">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            variant="ghost"
                            className={`h-full w-full text-sm font-medium rounded-md ${
                              activeTab === "directory" 
                                ? "bg-blue-600 text-white" 
                                : "text-blue-700 hover:bg-blue-50"
                            } flex items-center justify-center gap-1`}
                            onClick={() => setActiveTab("directory")}
                          >
                            Employee Directory
                            <ChevronDown className="h-4 w-4" />
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
                              setActiveDirectorySection("po");
                            }}
                            className="cursor-pointer"
                          >
                            PO
                          </DropdownMenuItem>
                          <DropdownMenuItem 
                            onClick={() => {
                              setActiveTab("directory");
                              setActiveDirectorySection("ps");
                            }}
                            className="cursor-pointer"
                          >
                            PS
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                    
                    <TabsTrigger 
                      value="work" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      Work
                    </TabsTrigger>
                    <TabsTrigger 
                      value="knowledge" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      Knowledge
                    </TabsTrigger>
                    <TabsTrigger 
                      value="help" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      Help
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="home" className="mt-6">
                    <Home />
                  </TabsContent>
                  
                  <TabsContent value="directory" className="mt-6">
                    {activeDirectorySection === "directory" && (
                      <div className="space-y-6">
                        <EmployeeDirectory />
                        <div className="border-t border-blue-200 pt-6">
                          <HierarchyBuilder />
                        </div>
                      </div>
                    )}
                    {activeDirectorySection === "po" && <PO />}
                    {activeDirectorySection === "ps" && <PS />}
                  </TabsContent>
                  
                  <TabsContent value="work" className="mt-6">
                    <Work />
                  </TabsContent>
                  
                  <TabsContent value="knowledge" className="mt-6">
                    <Knowledge />
                  </TabsContent>
                  
                  <TabsContent value="help" className="mt-6">
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