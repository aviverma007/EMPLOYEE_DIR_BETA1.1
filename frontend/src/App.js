import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginForm from "./components/LoginForm";
import EmployeeDirectory from "./components/EmployeeDirectory";
import HierarchyBuilder from "./components/HierarchyBuilder";
import HierarchyViewer from "./components/HierarchyViewer";
import Header from "./components/Header";
import { Toaster } from "./components/ui/sonner";

// Import new components
import Home from "./components/Home";
import Work from "./components/Work";
import Knowledge from "./components/Knowledge";
import Help from "./components/Help";

const AppContent = () => {
  const { isAuthenticated, initializeAuth, isAdmin } = useAuth();
  const [activeTab, setActiveTab] = useState("directory");

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
                  <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto mb-8 h-12 bg-white shadow-sm border border-blue-200">
                    <TabsTrigger 
                      value="directory" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      Employee Directory
                    </TabsTrigger>
                    <TabsTrigger 
                      value="hierarchy" 
                      className="text-sm font-medium data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=inactive]:text-blue-700"
                    >
                      {isAdmin() ? "Hierarchy Builder" : "Hierarchy View"}
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="directory" className="mt-6">
                    <EmployeeDirectory />
                  </TabsContent>
                  
                  <TabsContent value="hierarchy" className="mt-6">
                    {isAdmin() ? <HierarchyBuilder /> : <HierarchyViewer />}
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