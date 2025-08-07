import React, { useState } from "react";
import { User, Camera, Upload, Eye } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { toast } from "sonner";

const EmployeeList = ({ employees, onImageUpdate, onEmployeeClick }) => {
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [imageUrl, setImageUrl] = useState("");

  const handleImageSubmit = () => {
    if (imageUrl && selectedEmployee) {
      onImageUpdate(selectedEmployee.id, imageUrl);
      toast.success("Profile image updated successfully!");
      setImageUrl("");
      setSelectedEmployee(null);
    }
  };

  if (employees.length === 0) {
    return (
      <Card className="p-8 text-center">
        <div className="text-gray-500">
          <User className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>No employees found matching your criteria.</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="border-0 shadow-sm bg-white">
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow className="bg-slate-50">
              <TableHead className="w-16">Photo</TableHead>
              <TableHead>Employee</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Location</TableHead>
              <TableHead className="w-32">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {employees.map((employee) => (
              <TableRow key={employee.id} className="hover:bg-slate-50 cursor-pointer">
                <TableCell>
                  <div className="relative group">
                    <div className="w-10 h-10 rounded-full overflow-hidden bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
                      {employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? (
                        <img 
                          src={employee.profileImage} 
                          alt={employee.name}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'flex';
                          }}
                        />
                      ) : null}
                      <User className="h-5 w-5 text-gray-500" style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
                    </div>
                    
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          size="sm"
                          className="absolute -top-1 -right-1 h-6 w-6 rounded-full p-0 bg-slate-900 hover:bg-slate-800 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedEmployee(employee);
                          }}
                        >
                          <Camera className="h-3 w-3" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="sm:max-w-md">
                        <DialogHeader>
                          <DialogTitle>Update Profile Image</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          <div className="space-y-2">
                            <Label htmlFor="image-url">Image URL</Label>
                            <Input
                              id="image-url"
                              placeholder="Enter image URL..."
                              value={imageUrl}
                              onChange={(e) => setImageUrl(e.target.value)}
                            />
                          </div>
                          <Button onClick={handleImageSubmit} className="w-full">
                            <Upload className="h-4 w-4 mr-2" />
                            Update Image
                          </Button>
                        </div>
                      </DialogContent>
                    </Dialog>
                  </div>
                </TableCell>
                
                <TableCell onClick={() => onEmployeeClick(employee)}>
                  <div>
                    <p className="font-semibold text-slate-900 hover:text-blue-600 transition-colors">{employee.name}</p>
                    <Badge variant="outline" className="text-xs mt-1">{employee.id}</Badge>
                  </div>
                </TableCell>
                
                <TableCell onClick={() => onEmployeeClick(employee)}>
                  <span className="text-sm text-gray-700">{employee.department}</span>
                </TableCell>
                
                <TableCell onClick={() => onEmployeeClick(employee)}>
                  <span className="text-sm text-gray-700">{employee.location}</span>
                </TableCell>
                
                <TableCell>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      onEmployeeClick(employee);
                    }}
                    className="flex items-center space-x-2"
                  >
                    <Eye className="h-4 w-4" />
                    <span>Details</span>
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default EmployeeList;