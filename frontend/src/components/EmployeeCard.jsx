import React, { useState } from "react";
import { User, Phone, Mail, MapPin, Calendar, Briefcase, Camera, Upload } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { toast } from "sonner";

const EmployeeCard = ({ employees, onImageUpdate }) => {
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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {employees.map((employee) => (
        <Card key={employee.id} className="hover:shadow-lg transition-all duration-300 border-0 shadow-sm bg-white group">
          <CardContent className="p-6">
            <div className="flex flex-col items-center space-y-4">
              {/* Profile Image */}
              <div className="relative">
                <div className="w-20 h-20 rounded-full overflow-hidden bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
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
                  <User className="h-10 w-10 text-gray-500" style={{display: employee.profileImage && employee.profileImage !== "/api/placeholder/150/150" ? 'none' : 'block'}} />
                </div>
                
                <Dialog>
                  <DialogTrigger asChild>
                    <Button
                      size="sm"
                      className="absolute -bottom-1 -right-1 h-8 w-8 rounded-full p-0 bg-slate-900 hover:bg-slate-800 opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={() => setSelectedEmployee(employee)}
                    >
                      <Camera className="h-4 w-4" />
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

              {/* Employee Info */}
              <div className="text-center space-y-2">
                <h3 className="font-semibold text-lg text-slate-900">{employee.name}</h3>
                <Badge variant="secondary" className="text-xs">
                  {employee.id}
                </Badge>
                <p className="text-sm font-medium text-slate-600">{employee.grade}</p>
              </div>

              {/* Contact Info */}
              <div className="w-full space-y-3 text-sm">
                <div className="flex items-center space-x-2">
                  <Briefcase className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">{employee.department}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">{employee.location}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">{employee.mobile}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Mail className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600 text-xs">{employee.email}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">Joined {new Date(employee.dateOfJoining).toLocaleDateString()}</span>
                </div>

                {employee.reportingManager && employee.reportingManager !== "*" && (
                  <div className="pt-2 border-t border-gray-100">
                    <p className="text-xs text-gray-500">Reports to:</p>
                    <p className="text-sm font-medium text-slate-600">{employee.reportingManager}</p>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default EmployeeCard;