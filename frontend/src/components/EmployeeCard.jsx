import React, { useState } from "react";
import { User, Camera, Upload, Eye } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { toast } from "sonner";

const EmployeeCard = ({ employees, onImageUpdate, onEmployeeClick }) => {
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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {employees.map((employee) => (
        <Card key={employee.id} className="hover:shadow-lg transition-all duration-300 border-0 shadow-sm bg-white group cursor-pointer">
          <CardContent className="p-6">
            <div className="flex flex-col items-center space-y-4">
              {/* Profile Image */}
              <div className="relative">
                <div className="w-16 h-16 rounded-full overflow-hidden bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
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
                  <User className="h-8 w-8 text-gray-500" style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
                </div>
                
                <Dialog>
                  <DialogTrigger asChild>
                    <Button
                      size="sm"
                      className="absolute -bottom-1 -right-1 h-7 w-7 rounded-full p-0 bg-slate-900 hover:bg-slate-800 opacity-0 group-hover:opacity-100 transition-opacity"
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

              {/* Employee Info - Condensed View */}
              <div className="text-center space-y-2" onClick={() => onEmployeeClick(employee)}>
                <h3 className="font-semibold text-lg text-slate-900 hover:text-blue-600 transition-colors">{employee.name}</h3>
                <Badge variant="secondary" className="text-xs">
                  {employee.id}
                </Badge>
                <p className="text-sm font-medium text-slate-600">{employee.department}</p>
                
                {/* View Details Button */}
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity flex items-center space-x-2"
                  onClick={(e) => {
                    e.stopPropagation();
                    onEmployeeClick(employee);
                  }}
                >
                  <Eye className="h-4 w-4" />
                  <span>View Details</span>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default EmployeeCard;