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
  Calendar,
  Clock,
  MapPin,
  Users,
  Monitor,
  Wifi,
  Search,
  Filter,
  Building,
  BookOpen,
  X,
  Check,
  User
} from "lucide-react";

const MeetingRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [filteredRooms, setFilteredRooms] = useState([]);
  const [locations, setLocations] = useState([]);
  const [floors, setFloors] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedLocation, setSelectedLocation] = useState("");
  const [selectedFloor, setSelectedFloor] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  
  // Booking form
  const [bookingForm, setBookingForm] = useState({
    employee_id: "",
    start_time: "",
    end_time: "",
    remarks: ""
  });
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [showBookingDialog, setShowBookingDialog] = useState(false);
  const [employeeSearch, setEmployeeSearch] = useState("");

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch initial data
  useEffect(() => {
    fetchRooms();
    fetchLocations();
    fetchEmployees();
  }, []);

  // Update floors when location changes
  useEffect(() => {
    if (selectedLocation) {
      fetchFloors(selectedLocation);
    } else {
      setFloors([]);
      setSelectedFloor("");
    }
  }, [selectedLocation]);

  // Apply filters
  useEffect(() => {
    let filtered = rooms;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(room =>
        room.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        room.id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Location filter
    if (selectedLocation) {
      filtered = filtered.filter(room => room.location === selectedLocation);
    }

    // Floor filter
    if (selectedFloor) {
      filtered = filtered.filter(room => room.floor === selectedFloor);
    }

    // Status filter
    if (statusFilter !== "all") {
      filtered = filtered.filter(room => room.status === statusFilter);
    }

    setFilteredRooms(filtered);
  }, [rooms, searchTerm, selectedLocation, selectedFloor, statusFilter]);

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

  const fetchLocations = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/meeting-rooms/locations`);
      if (response.ok) {
        const data = await response.json();
        setLocations(data.locations || []);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const fetchFloors = async (location) => {
    try {
      const response = await fetch(`${backendUrl}/api/meeting-rooms/floors?location=${encodeURIComponent(location)}`);
      if (response.ok) {
        const data = await response.json();
        setFloors(data.floors || []);
      }
    } catch (error) {
      console.error('Error fetching floors:', error);
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
        fetchRooms(); // Refresh rooms
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
    try {
      const response = await fetch(`${backendUrl}/api/meeting-rooms/${roomId}/booking`, {
        method: 'DELETE',
      });

      if (response.ok) {
        fetchRooms(); // Refresh rooms
        alert('Booking cancelled successfully!');
      } else {
        alert('Failed to cancel booking');
      }
    } catch (error) {
      console.error('Error cancelling booking:', error);
      alert('Failed to cancel booking');
    }
  };

  const formatDateTime = (dateTimeString) => {
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    return status === 'vacant' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
  };

  const filteredEmployees = employees.filter(emp => 
    employeeSearch === "" || 
    emp.name.toLowerCase().includes(employeeSearch.toLowerCase()) ||
    emp.id.toLowerCase().includes(employeeSearch.toLowerCase())
  );

  const getSelectedEmployee = () => {
    return employees.find(emp => emp.id === bookingForm.employee_id);
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Meeting Rooms</h1>
        <div className="text-sm text-gray-500">
          {filteredRooms.length} rooms found
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search rooms..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Location Dropdown */}
            <Select value={selectedLocation} onValueChange={setSelectedLocation}>
              <SelectTrigger>
                <Building className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Select Location" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Locations</SelectItem>
                {locations.map((location) => (
                  <SelectItem key={location} value={location}>
                    {location}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Floor Dropdown */}
            <Select value={selectedFloor} onValueChange={setSelectedFloor} disabled={!selectedLocation}>
              <SelectTrigger>
                <MapPin className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Select Floor" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Floors</SelectItem>
                {floors.map((floor) => (
                  <SelectItem key={floor} value={floor}>
                    {floor}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Status Filter */}
            <div className="flex gap-2">
              <Button
                variant={statusFilter === "all" ? "default" : "outline"}
                size="sm"
                onClick={() => setStatusFilter("all")}
              >
                All
              </Button>
              <Button
                variant={statusFilter === "vacant" ? "default" : "outline"}
                size="sm"
                onClick={() => setStatusFilter("vacant")}
                className="bg-green-600 hover:bg-green-700 border-green-600 text-white"
              >
                Vacant
              </Button>
              <Button
                variant={statusFilter === "occupied" ? "default" : "outline"}
                size="sm"
                onClick={() => setStatusFilter("occupied")}
                className="bg-red-600 hover:bg-red-700 border-red-600 text-white"
              >
                Occupied
              </Button>
            </div>

            {/* Clear Filters */}
            <Button
              variant="outline"
              onClick={() => {
                setSearchTerm("");
                setSelectedLocation("");
                setSelectedFloor("");
                setStatusFilter("all");
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRooms.map((room) => (
              <Card key={room.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">{room.name}</CardTitle>
                      <div className="flex items-center gap-2 text-sm text-gray-500 mt-1">
                        <Building className="h-4 w-4" />
                        {room.location} - {room.floor}
                      </div>
                    </div>
                    <Badge className={`${getStatusColor(room.status)} border-0`}>
                      {room.status === 'vacant' ? 'Vacant' : 'Occupied'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Room Details */}
                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    <div className="flex items-center gap-1">
                      <Users className="h-4 w-4" />
                      {room.capacity} people
                    </div>
                    <div className="flex items-center gap-1">
                      <Monitor className="h-4 w-4" />
                      {room.equipment?.length || 0} equipment
                    </div>
                  </div>

                  {/* Equipment List */}
                  {room.equipment && room.equipment.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {room.equipment.slice(0, 3).map((item, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {item}
                        </Badge>
                      ))}
                      {room.equipment.length > 3 && (
                        <Badge variant="secondary" className="text-xs">
                          +{room.equipment.length - 3} more
                        </Badge>
                      )}
                    </div>
                  )}

                  {/* Current Booking */}
                  {room.status === 'occupied' && room.current_booking && (
                    <div className="bg-red-50 rounded-lg p-3 space-y-2">
                      <div className="flex items-center gap-2 text-sm font-medium text-red-800">
                        <User className="h-4 w-4" />
                        {room.current_booking.employee_name}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-red-600">
                        <Clock className="h-3 w-3" />
                        {formatDateTime(room.current_booking.start_time)} - {formatDateTime(room.current_booking.end_time)}
                      </div>
                      {room.current_booking.remarks && (
                        <div className="text-xs text-red-600">
                          {room.current_booking.remarks}
                        </div>
                      )}
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCancelBooking(room.id)}
                        className="w-full text-red-600 border-red-300 hover:bg-red-50"
                      >
                        Cancel Booking
                      </Button>
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

                          {/* Date & Time */}
                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <Label>Start Time</Label>
                              <Input
                                type="datetime-local"
                                value={bookingForm.start_time}
                                onChange={(e) => setBookingForm(prev => ({ ...prev, start_time: e.target.value }))}
                              />
                            </div>
                            <div>
                              <Label>End Time</Label>
                              <Input
                                type="datetime-local"
                                value={bookingForm.end_time}
                                onChange={(e) => setBookingForm(prev => ({ ...prev, end_time: e.target.value }))}
                              />
                            </div>
                          </div>

                          {/* Remarks */}
                          <div>
                            <Label>Remarks</Label>
                            <Textarea
                              placeholder="Meeting purpose, notes..."
                              value={bookingForm.remarks}
                              onChange={(e) => setBookingForm(prev => ({ ...prev, remarks: e.target.value }))}
                              rows={3}
                            />
                          </div>

                          <div className="flex gap-2">
                            <Button
                              onClick={handleBookRoom}
                              disabled={!bookingForm.employee_id || !bookingForm.start_time || !bookingForm.end_time}
                              className="flex-1"
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
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filters</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MeetingRooms;