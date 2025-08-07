import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import EmployeeDirectory from "./components/EmployeeDirectory";
import HierarchyBuilder from "./components/HierarchyBuilder";
import Header from "./components/Header";
import { Toaster } from "./components/ui/sonner";

function App() {
  const [activeTab, setActiveTab] = useState("directory");

  return (
    <div className="App min-h-screen bg-gradient-to-br from-slate-50 to-gray-100">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            <div className="w-full">
              <Header />
              <div className="container mx-auto px-4 py-8 max-w-7xl">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto mb-8 h-12 bg-white shadow-sm">
                    <TabsTrigger 
                      value="directory" 
                      className="text-sm font-medium data-[state=active]:bg-slate-900 data-[state=active]:text-white"
                    >
                      Employee Directory
                    </TabsTrigger>
                    <TabsTrigger 
                      value="hierarchy" 
                      className="text-sm font-medium data-[state=active]:bg-slate-900 data-[state=active]:text-white"
                    >
                      Hierarchy Builder
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="directory" className="mt-6">
                    <EmployeeDirectory />
                  </TabsContent>
                  
                  <TabsContent value="hierarchy" className="mt-6">
                    <HierarchyBuilder />
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
}

export default App;