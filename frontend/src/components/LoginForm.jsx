import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Building2, User, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    employeeId: ''
  });
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.role) {
      toast.error('Please fill in all fields');
      return;
    }

    const userData = {
      name: formData.name,
      role: formData.role,
      employeeId: formData.employeeId || `EMP${Date.now()}`,
      loginTime: new Date().toISOString()
    };

    login(userData);
    toast.success(`Welcome ${formData.name}! Logged in as ${formData.role}`);
  };

  const handleQuickLogin = (role, name, empId) => {
    const userData = {
      name,
      role,
      employeeId: empId,
      loginTime: new Date().toISOString()
    };
    login(userData);
    toast.success(`Welcome ${name}! Logged in as ${role}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-3">
            <div className="p-3 bg-blue-600 rounded-lg">
              <Building2 className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-blue-900">
                SMARTWORLD DEVELOPERS Pvt. Ltd.
              </h1>
              <p className="text-sm text-blue-600">
                Employee Management System
              </p>
            </div>
          </div>
        </div>

        {/* Login Form */}
        <Card className="border-blue-200 shadow-lg">
          <CardHeader className="bg-blue-50">
            <CardTitle className="text-blue-900 text-center">Login to Continue</CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-blue-900">Full Name</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="border-blue-200 focus:border-blue-400"
                  placeholder="Enter your full name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="role" className="text-blue-900">Role</Label>
                <Select value={formData.role} onValueChange={(value) => setFormData({...formData, role: value})}>
                  <SelectTrigger className="border-blue-200 focus:border-blue-400">
                    <SelectValue placeholder="Select your role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">
                      <div className="flex items-center space-x-2">
                        <Shield className="h-4 w-4 text-blue-600" />
                        <span>Administrator</span>
                      </div>
                    </SelectItem>
                    <SelectItem value="user">
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4 text-blue-600" />
                        <span>Employee</span>
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="employeeId" className="text-blue-900">Employee ID (Optional)</Label>
                <Input
                  id="employeeId"
                  type="text"
                  value={formData.employeeId}
                  onChange={(e) => setFormData({...formData, employeeId: e.target.value})}
                  className="border-blue-200 focus:border-blue-400"
                  placeholder="Enter employee ID"
                />
              </div>

              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                Login
              </Button>
            </form>

            <div className="space-y-3 pt-4 border-t border-blue-100">
              <p className="text-sm text-blue-600 text-center">Quick Login (Demo)</p>
              <div className="grid grid-cols-2 gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleQuickLogin('admin', 'Admin User', 'ADMIN001')}
                  className="border-blue-200 text-blue-700 hover:bg-blue-50"
                >
                  <Shield className="h-4 w-4 mr-2" />
                  Admin
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleQuickLogin('user', 'Employee User', 'EMP001')}
                  className="border-blue-200 text-blue-700 hover:bg-blue-50"
                >
                  <User className="h-4 w-4 mr-2" />
                  Employee
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginForm;