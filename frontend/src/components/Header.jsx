import React, { useState } from "react";
import { RefreshCw, LogOut, Shield, User } from "lucide-react";
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
      <div className="container mx-auto px-6 py-4 max-w-7xl">
        <div className="flex justify-between items-center">
          {/* Left side - Logo and Company Name */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_site-modifier-3/artifacts/j921etso_2%5B2%5D.png"
                alt="SmartWorld Logo"
                className="h-16 w-16 object-contain rounded-lg"
              />
              <div>
                <h1 className="text-2xl font-bold text-blue-900">
                  SMARTWORLD DEVELOPERS Pvt. Ltd.
                </h1>
                <p className="text-base text-blue-600">
                  Employee Management System
                </p>
              </div>
            </div>
          </div>
          
          {/* Right side - Profile, Refresh, Logout */}
          <div className="flex items-center space-x-3">
            {/* User Info */}
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-medium text-blue-900">{user?.name}</p>
                <div className="flex items-center justify-end space-x-2">
                  <p className="text-xs text-blue-600">ID: {user?.employeeId}</p>
                  <Badge 
                    variant={isAdmin() ? "default" : "secondary"} 
                    className={`text-xs ${isAdmin() ? "bg-blue-600" : "bg-blue-100 text-blue-700"}`}
                  >
                    {isAdmin() ? <Shield className="h-3 w-3 mr-1" /> : <User className="h-3 w-3 mr-1" />}
                    {isAdmin() ? "Admin" : "Employee"}
                  </Badge>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              {isAdmin() && (
                <Button 
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  size="sm"
                  variant="outline"
                  className="flex items-center space-x-1 hover:bg-blue-50 border-blue-200"
                >
                  <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                </Button>
              )}
              
              <Button 
                onClick={handleLogout}
                size="sm"
                variant="outline"
                className="flex items-center space-x-1 hover:bg-red-50 border-red-200 text-red-600"
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