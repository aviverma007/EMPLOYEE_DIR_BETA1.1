import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { 
  MapPin,
  BookOpen,
  Users,
  Clock,
  User,
  Check,
  X,
  Building,
  Plus,
  CalendarDays,
  Trash2,
  Calendar
} from "lucide-react";

const MeetingRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [selectedLocation, setSelectedLocation] = useState("all");
  const [selectedFloor, setSelectedFloor] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  
  // Form state
  const [bookingForm, setBookingForm] = useState({
    employee_id: "",
    start_time: "",
    end_time: "",
    remarks: ""
  });
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [showBookingDialog, setShowBookingDialog] = useState(false);
  const [employeeSearch, setEmployeeSearch] = useState("");

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Define locations with floors and rooms - updated to match backend
  const locationConfig = {
    "IFC": {
      floors: ["11", "12", "14"],
      rooms: ["Conference Room A", "Meeting Room B", "Executive Room", "Board Room", "Training Room"]
    },
    "Central Office 75": {
      floors: ["1"],
      rooms: ["Meeting Room"]
    },
    "Office 75": {
      floors: ["1"],
      rooms: ["Conference Room"]
    },
    "Noida": {
      floors: ["1"],
      rooms: ["Meeting Room"]
    },
    "Project Office": {
      floors: ["1"],
      rooms: ["Meeting Room"]
    }
  };

  // Fetch data
  useEffect(() => {
    fetchRooms();
    fetchEmployees();
    fetchLocations();
  }, []);

  const fetchRooms = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/meeting-rooms`);
      if (response.ok) {
        const data = await response.json();
        setRooms(data);
      }
    } catch (error) {
      console.error('Error fetching rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/employees`);
      if (response.ok) {
        const data = await response.json();
        setEmployees(data);
      }
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const fetchLocations = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/locations`);
      if (response.ok) {
        const data = await response.json();
        // Filter relevant locations
        const relevantLocations = data.locations.filter(loc => 
          locationConfig.hasOwnProperty(loc) || 
          ['IFC', 'Central Office 75', 'Office 75', 'Noida', 'Project Office'].includes(loc)
        );
        setLocations(relevantLocations);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const handleBookRoom = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/meeting-rooms/${selectedRoom.id}/book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingForm),
      });

      if (response.ok) {
        setShowBookingDialog(false);
        setBookingForm({
          employee_id: "",
          start_time: "",
          end_time: "",
          remarks: ""
        });
        setEmployeeSearch("");
        fetchRooms();
        alert('Room booked successfully!');
      } else {
        const error = await response.json();
        alert(`Error booking room: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error booking room:', error);
      alert('Failed to book room');
    }
  };

  const handleCancelBooking = async (roomId) => {
    if (window.confirm('Are you sure you want to cancel this booking?')) {
      try {
        const response = await fetch(`${backendUrl}/api/meeting-rooms/${roomId}/booking`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchRooms();
          alert('Booking cancelled successfully!');
        } else {
          alert('Failed to cancel booking');
        }
      } catch (error) {
        console.error('Error cancelling booking:', error);
        alert('Failed to cancel booking');
      }
    }
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const filteredEmployees = employees.filter(emp =>
    emp.name.toLowerCase().includes(employeeSearch.toLowerCase()) ||
    emp.id.toLowerCase().includes(employeeSearch.toLowerCase())
  );

  const getSelectedEmployee = () => {
    return employees.find(emp => emp.id === bookingForm.employee_id);
  };

  const filteredRooms = rooms.filter(room => {
    if (selectedLocation && selectedLocation !== "all" && room.location !== selectedLocation) return false;
    if (selectedFloor && selectedFloor !== "all" && room.floor !== selectedFloor) return false;
    if (selectedStatus && selectedStatus !== "all" && room.status !== selectedStatus) return false;
    return true;
  });

  const getAvailableFloors = () => {
    if (!selectedLocation || selectedLocation === "all" || !locationConfig[selectedLocation]) return [];
    return locationConfig[selectedLocation].floors;
  };

  const getMinDateTime = () => {
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    return `${today}T09:00`;
  };

  const getMaxDateTime = () => {
    // Allow booking up to 30 days in the future
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 30);
    const maxDate = futureDate.toISOString().split('T')[0];
    return `${maxDate}T20:00`;
  };

  const formatTime12Hour = (time24) => {
    if (!time24) return '';
    const [hours, minutes] = time24.split(':');
    const hour12 = hours % 12 || 12;
    const ampm = hours < 12 ? 'AM' : 'PM';
    return `${hour12}:${minutes} ${ampm}`;
  };

  const clearAllBookings = async () => {
    if (window.confirm('Are you sure you want to clear ALL bookings from ALL meeting rooms? This action cannot be undone.')) {
      try {
        const response = await fetch(`${backendUrl}/meeting-rooms/clear-all-bookings`, {
          method: 'DELETE',
        });

        if (response.ok) {
          const result = await response.json();
          fetchRooms(); // Refresh room data
          alert(`Success! ${result.message}`);
        } else {
          const error = await response.json();
          alert(`Error clearing bookings: ${error.detail || 'Unknown error'}`);
        }
      } catch (error) {
        console.error('Error clearing all bookings:', error);
        alert('Failed to clear bookings');
      }
    }
  };

  const getTimeOptions = () => {
    const times = [];
    for (let hour = 9; hour <= 20; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const time24 = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        const time12 = formatTime12Hour(time24);
        times.push({ value: time24, label: time12 });
      }
    }
    return times;
  };

  return (
    <div className="h-full flex flex-col space-y-4 p-4 sm:p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-2 sm:space-y-0">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Meeting Rooms</h1>
        <div className="flex items-center text-sm text-gray-600">
          <Calendar className="h-4 w-4 mr-1" />
          Single booking per room policy
        </div>
      </div>

      {/* Location and Floor Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base sm:text-lg flex items-center gap-2">
            <Building className="h-4 w-4 sm:h-5 sm:w-5" />
            Location & Floor Selection
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <Select value={selectedLocation} onValueChange={(value) => {
              setSelectedLocation(value);
              setSelectedFloor("all"); // Reset floor when location changes
            }}>
              <SelectTrigger className="h-10">
                <SelectValue placeholder="Select Location" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Locations</SelectItem>
                {Object.keys(locationConfig).map((location) => (
                  <SelectItem key={location} value={location}>
                    {location}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select 
              value={selectedFloor} 
              onValueChange={setSelectedFloor}
              disabled={!selectedLocation || selectedLocation === "all"}
            >
              <SelectTrigger className="h-10">
                <SelectValue placeholder="Select Floor" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Floors</SelectItem>
                {getAvailableFloors().map((floor) => (
                  <SelectItem key={floor} value={floor}>
                    Floor {floor}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger className="h-10">
                <SelectValue placeholder="Room Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Rooms</SelectItem>
                <SelectItem value="vacant">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    Vacant
                  </div>
                </SelectItem>
                <SelectItem value="occupied">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                    Occupied
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>

            <Button
              variant="outline"
              className="h-10"
              onClick={() => {
                setSelectedLocation("all");
                setSelectedFloor("all");
                setSelectedStatus("all");
              }}
            >
              Clear Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Rooms Grid */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-gray-500">Loading meeting rooms...</div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {filteredRooms.map((room) => (
              <Card key={room.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="min-w-0 flex-1">
                      <CardTitle className="text-base sm:text-lg truncate">{room.name}</CardTitle>
                      <div className="flex flex-wrap items-center gap-2 text-xs sm:text-sm text-gray-500 mt-1">
                        <div className="flex items-center gap-1">
                          <MapPin className="h-3 w-3 sm:h-4 sm:w-4" />
                          <span className="truncate">{room.location}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Building className="h-3 w-3 sm:h-4 sm:w-4" />
                          <span>Floor {room.floor}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Users className="h-3 w-3 sm:h-4 sm:w-4" />
                          <span>{room.capacity}</span>
                        </div>
                      </div>
                    </div>
                    <Badge className={`
                      ${room.status === 'vacant' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                      border-0 text-xs whitespace-nowrap ml-2
                    `}>
                      {room.status.toUpperCase()}
                    </Badge>
                  </div>
                </CardHeader>

                <CardContent className="space-y-3">
                  {/* Room Features */}
                  <div className="text-sm text-gray-600">
                    <div className="font-medium mb-1">Amenities:</div>
                    <div className="flex flex-wrap gap-1">
                      {room.amenities && room.amenities.map((amenity, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {amenity}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Booking Details - Show for any occupied room with bookings */}
                  {room.status === 'occupied' && room.bookings && room.bookings.length > 0 && (
                    <div className="bg-red-50 rounded-lg p-3 space-y-2">
                      <div className="flex items-center gap-2 text-sm font-medium text-red-800">
                        <User className="h-4 w-4" />
                        Booked by: {room.bookings[0].employee_name}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-red-600">
                        <Clock className="h-3 w-3" />
                        {formatDateTime(room.bookings[0].start_time)} - {formatDateTime(room.bookings[0].end_time)}
                      </div>
                      {room.bookings[0].remarks && (
                        <div className="text-xs text-red-600 bg-white/50 p-2 rounded">
                          <span className="font-medium">Notes: </span>
                          {room.bookings[0].remarks}
                        </div>
                      )}
                      <div className="text-xs text-red-500 opacity-75">
                        Booking ID: {room.bookings[0].id}
                      </div>
                      <div className="text-xs text-red-500 opacity-75">
                        Booked on: {formatDateTime(room.bookings[0].created_at)}
                      </div>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCancelBooking(room.id)}
                        className="w-full text-red-600 border-red-300 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Cancel Booking
                      </Button>
                    </div>
                  )}
                  
                  {/* Show current active booking info separately if exists */}
                  {room.current_booking && (
                    <div className="bg-orange-50 border border-orange-200 rounded-lg p-2">
                      <div className="text-xs font-medium text-orange-800 flex items-center gap-1">
                        <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
                        Currently Active Meeting
                      </div>
                    </div>
                  )}

                  {/* Book Button */}
                  {room.status === 'vacant' && (
                    <Dialog open={showBookingDialog && selectedRoom?.id === room.id} onOpenChange={setShowBookingDialog}>
                      <DialogTrigger asChild>
                        <Button 
                          className="w-full bg-green-600 hover:bg-green-700"
                          onClick={() => setSelectedRoom(room)}
                        >
                          <BookOpen className="h-4 w-4 mr-2" />
                          Book Room
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-md">
                        <DialogHeader>
                          <DialogTitle>Book {room.name}</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          {/* Employee Selection */}
                          <div>
                            <Label>Employee</Label>
                            <div className="space-y-2">
                              <Input
                                placeholder="Search by name or ID..."
                                value={employeeSearch}
                                onChange={(e) => setEmployeeSearch(e.target.value)}
                              />
                              {employeeSearch && (
                                <div className="max-h-32 overflow-y-auto border rounded-md">
                                  {filteredEmployees.slice(0, 5).map((emp) => (
                                    <div
                                      key={emp.id}
                                      className="p-2 hover:bg-gray-100 cursor-pointer flex justify-between items-center"
                                      onClick={() => {
                                        setBookingForm(prev => ({ ...prev, employee_id: emp.id }));
                                        setEmployeeSearch("");
                                      }}
                                    >
                                      <div>
                                        <div className="font-medium">{emp.name}</div>
                                        <div className="text-sm text-gray-500">{emp.id} - {emp.department}</div>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}
                              {getSelectedEmployee() && (
                                <div className="bg-blue-50 p-2 rounded-md flex justify-between items-center">
                                  <div>
                                    <div className="font-medium">{getSelectedEmployee().name}</div>
                                    <div className="text-sm text-gray-500">{getSelectedEmployee().id}</div>
                                  </div>
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    onClick={() => setBookingForm(prev => ({ ...prev, employee_id: "" }))}
                                  >
                                    <X className="h-4 w-4" />
                                  </Button>
                                </div>
                              )}
                            </div>
                          </div>

                          {/* Date & Time Selection with 12-hour format */}
                          <div className="space-y-4">
                            <div>
                              <Label>Booking Date</Label>
                              <Input
                                type="date"
                                value={bookingForm.start_time ? bookingForm.start_time.split('T')[0] : ''}
                                onChange={(e) => {
                                  const date = e.target.value;
                                  const startTime = bookingForm.start_time ? bookingForm.start_time.split('T')[1] : '09:00';
                                  const endTime = bookingForm.end_time ? bookingForm.end_time.split('T')[1] : '10:00';
                                  setBookingForm(prev => ({
                                    ...prev,
                                    start_time: `${date}T${startTime}`,
                                    end_time: `${date}T${endTime}`
                                  }));
                                }}
                                min={new Date().toISOString().split('T')[0]}
                                max={(() => {
                                  const futureDate = new Date();
                                  futureDate.setDate(futureDate.getDate() + 30);
                                  return futureDate.toISOString().split('T')[0];
                                })()}
                              />
                            </div>
                            
                            <div className="grid grid-cols-2 gap-3">
                              <div>
                                <Label>Start Time</Label>
                                <Select 
                                  value={bookingForm.start_time ? bookingForm.start_time.split('T')[1] || '' : ''}
                                  onValueChange={(time) => {
                                    const date = bookingForm.start_time ? bookingForm.start_time.split('T')[0] : new Date().toISOString().split('T')[0];
                                    setBookingForm(prev => ({ ...prev, start_time: `${date}T${time}` }));
                                  }}
                                >
                                  <SelectTrigger>
                                    <SelectValue placeholder="Start time" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {getTimeOptions().map((time) => (
                                      <SelectItem key={time.value} value={time.value}>
                                        {time.label}
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                              </div>
                              
                              <div>
                                <Label>End Time</Label>
                                <Select 
                                  value={bookingForm.end_time ? bookingForm.end_time.split('T')[1] || '' : ''}
                                  onValueChange={(time) => {
                                    const date = bookingForm.end_time ? bookingForm.end_time.split('T')[0] : new Date().toISOString().split('T')[0];
                                    setBookingForm(prev => ({ ...prev, end_time: `${date}T${time}` }));
                                  }}
                                >
                                  <SelectTrigger>
                                    <SelectValue placeholder="End time" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {getTimeOptions().map((time) => (
                                      <SelectItem key={time.value} value={time.value}>
                                        {time.label}
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                              </div>
                            </div>
                          </div>

                          {/* Business Hours Notice */}
                          <div className="bg-blue-50 p-3 rounded-md">
                            <div className="text-sm text-blue-800">
                              <strong>Business Hours:</strong> 9:00 AM - 8:00 PM<br/>
                              <strong>Policy:</strong> Single booking per room<br/>
                              <strong>Advance Booking:</strong> Up to 30 days
                            </div>
                          </div>

                          {/* Meeting Details */}
                          <div>
                            <Label>Meeting Purpose / Notes</Label>
                            <Textarea
                              placeholder="e.g., Team standup, Client presentation, Training session..."
                              value={bookingForm.remarks}
                              onChange={(e) => setBookingForm(prev => ({ ...prev, remarks: e.target.value }))}
                              rows={3}
                            />
                          </div>

                          <div className="flex gap-2">
                            <Button
                              onClick={handleBookRoom}
                              disabled={!bookingForm.employee_id || !bookingForm.start_time || !bookingForm.end_time}
                              className="flex-1 bg-blue-600 hover:bg-blue-700"
                            >
                              <Check className="h-4 w-4 mr-2" />
                              Confirm Booking
                            </Button>
                            <Button
                              variant="outline"
                              onClick={() => {
                                setShowBookingDialog(false);
                                setBookingForm({
                                  employee_id: "",
                                  start_time: "",
                                  end_time: "",
                                  remarks: ""
                                });
                                setEmployeeSearch("");
                              }}
                            >
                              Cancel
                            </Button>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && filteredRooms.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No meeting rooms found</div>
            <div className="text-gray-400 text-sm mt-2">Try adjusting your location and floor filters</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MeetingRooms;