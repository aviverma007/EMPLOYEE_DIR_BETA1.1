import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Building2, User, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';

const LoginForm = () => {
  const { login } = useAuth();

  const handleLogin = () => {
    const userData = {
      name: 'Administrator',
      role: 'admin',
      employeeId: 'ADMIN001',
      loginTime: new Date().toISOString()
    };
    login(userData);
    toast.success('Welcome Administrator!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-6">
          <div className="flex items-center justify-center">
            <div className="p-6 bg-blue-600 rounded-2xl shadow-lg">
              <Building2 className="h-16 w-16 text-white" />
            </div>
          </div>
          <div>
            <p className="text-lg text-blue-600 font-medium">
              Employee Management System
            </p>
          </div>
        </div>

        {/* Login Button */}
        <Card className="border-blue-200 shadow-lg">
          <CardHeader className="bg-blue-50">
            <CardTitle className="text-blue-900 text-center">Administrator Access</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <Button
              onClick={handleLogin}
              className="w-full h-16 bg-blue-600 hover:bg-blue-700 text-white font-medium text-lg"
            >
              <Shield className="h-6 w-6 mr-3" />
              <div className="text-left">
                <div className="font-semibold">Enter Admin Dashboard</div>
                <div className="text-sm opacity-90">Full access to all features</div>
              </div>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginForm;