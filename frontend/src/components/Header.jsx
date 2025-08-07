import React from "react";
import { Building2, RefreshCw } from "lucide-react";
import { Button } from "./ui/button";
import { toast } from "sonner";

const Header = () => {
  const handleRefresh = () => {
    // Mock refresh functionality - will be replaced with actual API call
    toast.success("Employee data refreshed successfully!");
  };

  return (
    <header className="bg-white shadow-lg border-b border-gray-200">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-slate-900 rounded-lg">
                <Building2 className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">
                  SMARTWORLD DEVELOPERS Pvt. Ltd.
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Employee Management System
                </p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Button 
              onClick={handleRefresh}
              variant="outline"
              className="flex items-center space-x-2 hover:bg-slate-50"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Refresh Data</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;