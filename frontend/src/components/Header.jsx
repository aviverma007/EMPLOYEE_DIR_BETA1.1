import React, { useState } from "react";
import { Building2, RefreshCw, LogOut, Shield, User } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { useAuth } from "../context/AuthContext";
import { utilityAPI } from "../services/api";
import { toast } from "sonner";

const Header = () => {
  const { user, logout, isAdmin } = useAuth();
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    if (!isAdmin()) {
      toast.error("Only administrators can refresh data");
      return;
    }
    
    try {
      setIsRefreshing(true);
      const result = await utilityAPI.refreshExcel();
      
      toast.success(`Excel data refreshed successfully! Updated ${result.count} employees.`, {
        description: `Last updated: ${new Date().toLocaleString()}`
      });
      
      // Trigger a page reload to refresh all data
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (error) {
      console.error("Error refreshing data:", error);
      toast.error("Failed to refresh Excel data. Please try again.");
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
  };

  return (
    <header className="bg-white shadow-lg border-b-2 border-blue-200">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Building2 className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-blue-900">
                  SMARTWORLD DEVELOPERS Pvt. Ltd.
                </h1>
                <p className="text-sm text-blue-600 mt-1">
                  Employee Management System
                </p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* User Info */}
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-medium text-blue-900">{user?.name}</p>
                <p className="text-xs text-blue-600">ID: {user?.employeeId}</p>
              </div>
              <Badge 
                variant={isAdmin() ? "default" : "secondary"} 
                className={isAdmin() ? "bg-blue-600" : "bg-blue-100 text-blue-700"}
              >
                {isAdmin() ? <Shield className="h-3 w-3 mr-1" /> : <User className="h-3 w-3 mr-1" />}
                {isAdmin() ? "Administrator" : "Employee"}
              </Badge>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              {isAdmin() && (
                <Button 
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  variant="outline"
                  className="flex items-center space-x-2 hover:bg-blue-50 border-blue-200"
                >
                  <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  <span>{isRefreshing ? 'Refreshing...' : 'Sync Excel'}</span>
                </Button>
              )}
              
              <Button 
                onClick={handleLogout}
                variant="outline"
                className="flex items-center space-x-2 hover:bg-red-50 border-red-200 text-red-600"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;