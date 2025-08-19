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
    console.log("Refresh button clicked. Admin status:", isAdmin());
    
    if (!isAdmin()) {
      console.log("Not an admin, showing error");
      toast.error("Only administrators can refresh data");
      return;
    }
    
    try {
      console.log("Starting Excel refresh...");
      setIsRefreshing(true);
      const result = await utilityAPI.refreshExcel();
      console.log("Refresh result:", result);
      
      toast.success(`Excel data refreshed successfully! Updated ${result.count} employees.`, {
        description: `Last updated: ${new Date().toLocaleString()}`
      });
      
      // Trigger a page reload to refresh all data
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (error) {
      console.error("Error refreshing data:", error);
      console.error("Error details:", error.response?.data, error.message);
      toast.error(`Failed to refresh Excel data: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
  };

  return (
    <header className="bg-white shadow-md border-b border-blue-200">
      <div className="w-full px-4 py-2">
        <div className="flex justify-between items-center">
          {/* Left side - Logo and System Name */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-3">
              <img 
                src="https://customer-assets.emergentagent.com/job_site-modifier-3/artifacts/j921etso_2%5B2%5D.png"
                alt="Company Logo"
                className="h-12 w-12 object-contain rounded-lg shadow-sm"
              />
              <div>
                <p className="text-lg font-semibold text-blue-600">
                  Employee Management System
                </p>
              </div>
            </div>
          </div>
          
          {/* Right side - Profile, Refresh, Logout */}
          <div className="flex items-center space-x-2">
            {/* User Info */}
            <div className="flex items-center space-x-2">
              <div className="text-right">
                <p className="text-sm font-medium text-blue-900">{user?.name}</p>
                <div className="flex items-center justify-end space-x-1">
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
            <div className="flex items-center space-x-1">
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