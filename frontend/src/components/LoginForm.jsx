import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Building2, User, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';

const LoginForm = () => {
  const { login } = useAuth();

  const handleAdminLogin = () => {
    const userData = {
      name: 'Administrator',
      role: 'admin',
      employeeId: 'ADMIN001',
      loginTime: new Date().toISOString()
    };
    login(userData);
    toast.success('Welcome Administrator!');
  };

  const handleUserLogin = () => {
    const userData = {
      name: 'User',
      role: 'user',
      employeeId: 'USER001',
      loginTime: new Date().toISOString()
    };
    login(userData);
    toast.success('Welcome User!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-3">
            <div className="p-6 bg-blue-600 rounded-2xl shadow-lg">
              <Building2 className="h-16 w-16 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-blue-900">
                SMARTWORLD DEVELOPERS PVT. LTD.
              </h1>
              <p className="text-sm text-blue-600">
                Employee Management System
              </p>
            </div>
          </div>
        </div>

        {/* Login Buttons */}
        <div className="space-y-4">
          {/* Admin Access Card */}
          <Card className="border-blue-200 shadow-lg">
            <CardHeader className="bg-blue-50">
              <CardTitle className="text-blue-900 text-center">Administrator Access</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <button
                type="button"
                onClick={handleAdminLogin}
                className="w-full h-16 bg-blue-600 hover:bg-blue-700 text-white font-medium text-lg"
              >
                <Shield className="h-6 w-6 mr-3" />
                <div className="text-left">
                  <div className="font-semibold">Enter Admin Dashboard</div>
                  <div className="text-sm opacity-90">Full access to all features</div>
                </div>
              </button>
            </CardContent>
          </Card>

          {/* User Access Card */}
          <Card className="border-green-200 shadow-lg">
            <CardHeader className="bg-green-50">
              <CardTitle className="text-green-900 text-center">User Access</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <button
                type="button"
                onClick={handleUserLogin}
                className="w-full h-16 bg-green-600 hover:bg-green-700 text-white font-medium text-lg"
              >
                <User className="h-6 w-6 mr-3" />
                <div className="text-left">
                  <div className="font-semibold">Enter User Dashboard</div>
                  <div className="text-sm opacity-90">Access to essential features</div>
                </div>
              </button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;