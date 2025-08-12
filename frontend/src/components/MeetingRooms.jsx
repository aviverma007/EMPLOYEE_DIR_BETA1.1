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
        {
          id: 'global-center',
          name: 'Global Center Meeting Room',
          capacity: 5,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Marker', 'Glass Board']
        },
        {
          id: 'louvre',
          name: 'Louvre Meeting Room',
          capacity: 5,
          location: 'Main Building',
          status: 'occupied',
          occupiedBy: 'Team Planning Session',
          occupiedUntil: '15:30',
          equipment: ['TV Screen', 'Marker', 'Glass Board']
        },
        {
          id: 'golden-gate',
          name: 'Golden Gate Meeting Room',
          capacity: 10,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['TV Screen', 'Marker', 'Glass Board']
        },
        {
          id: 'empire-state',
          name: 'Empire State Meeting Room',
          capacity: 5,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['TV Screen', 'Marker', 'Glass Board']
        },
        {
          id: 'marina-bay',
          name: 'Marina Bay Meeting Room',
          capacity: 4,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Marker', 'Glass Board']
        },
        {
          id: 'burj',
          name: 'Burj Meeting Room',
          capacity: 5,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Marker', 'Glass Board']
        },
        {
          id: 'board-room',
          name: 'Board Room',
          capacity: 25,
          location: 'Executive Floor',
          status: 'occupied',
          occupiedBy: 'Board Meeting - Q3 Review',
          occupiedUntil: '17:00',
          equipment: ['Screen', 'Marker', 'Glass Board']
        }
      ];
      
      setRooms(companyRooms);
      setLoading(false);
    };

    initializeRooms();
  }, []);

  const handleStatusChange = (roomId, newStatus, reason = '') => {
    setRooms(prev => prev.map(room => 
      room.id === roomId 
        ? { 
            ...room, 
            status: newStatus,
            occupiedBy: newStatus === 'occupied' ? reason : '',
            occupiedUntil: newStatus === 'occupied' ? getCurrentTime() : ''
          }
        : room
    ));
    
    setEditingRoom(null);
    setOccupancyReason('');
    
    toast.success(
      newStatus === 'occupied' 
        ? `Room marked as occupied: ${reason}` 
        : 'Room marked as vacant'
    );
  };

  const getCurrentTime = () => {
    const now = new Date();
    const oneHour = new Date(now.getTime() + 60 * 60 * 1000);
    return oneHour.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const startEditing = (room) => {
    setEditingRoom(room.id);
    setOccupancyReason(room.occupiedBy || '');
  };

  const cancelEditing = () => {
    setEditingRoom(null);
    setOccupancyReason('');
  };

  const saveOccupancyReason = (roomId) => {
    if (!occupancyReason.trim()) {
      toast.error('Please enter a reason for occupancy');
      return;
    }
    handleStatusChange(roomId, 'occupied', occupancyReason.trim());
  };

  const getStatusColor = (status) => {
    return status === 'vacant' 
      ? 'bg-green-100 text-green-800 border-green-200' 
      : 'bg-red-100 text-red-800 border-red-200';
  };

  const getStatusIcon = (status) => {
    return status === 'vacant' 
      ? <CheckCircle className="h-3 w-3" />
      : <XCircle className="h-3 w-3" />;
  };

  const vacantRooms = rooms.filter(room => room.status === 'vacant').length;
  const occupiedRooms = rooms.filter(room => room.status === 'occupied').length;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-blue-600 text-sm">Loading meeting rooms...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto space-y-4">
      {/* Compact Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-blue-900">Meeting Room Management</h2>
          <p className="text-blue-600 text-sm">Track room availability and occupancy</p>
        </div>
        <div className="flex gap-2">
          <Badge className="px-3 py-1 bg-green-100 text-green-800 border-green-200 text-xs">
            <CheckCircle className="h-3 w-3 mr-1" />
            {vacantRooms} Vacant
          </Badge>
          <Badge className="px-3 py-1 bg-red-100 text-red-800 border-red-200 text-xs">
            <XCircle className="h-3 w-3 mr-1" />
            {occupiedRooms} Occupied
          </Badge>
        </div>
      </div>

      {/* Compact Room Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {rooms.map((room) => (
          <Card 
            key={room.id} 
            className={`hover:shadow-md transition-all duration-200 border ${
              room.status === 'vacant' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
            } h-full flex flex-col`}
          >
            <CardHeader className="pb-2 flex-shrink-0">
              <div className="flex justify-between items-start">
                <CardTitle className="text-sm font-semibold text-gray-900 leading-tight">
                  {room.name}
                </CardTitle>
                <Badge className={`${getStatusColor(room.status)} border font-medium text-xs px-2 py-1`}>
                  {getStatusIcon(room.status)}
                  <span className="ml-1 capitalize">{room.status}</span>
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="flex-1 flex flex-col space-y-2 text-xs">
              {/* Room Details */}
              <div className="space-y-1">
                <div className="flex items-center gap-1 text-gray-600">
                  <Users className="h-3 w-3 text-blue-500" />
                  <span>{room.capacity} people</span>
                </div>
                <div className="flex items-center gap-1 text-gray-600">
                  <MapPin className="h-3 w-3 text-blue-500" />
                  <span>{room.location}</span>
                </div>
                {room.status === 'occupied' && room.occupiedUntil && (
                  <div className="flex items-center gap-1 text-gray-600">
                    <Clock className="h-3 w-3 text-blue-500" />
                    <span>Until: {room.occupiedUntil}</span>
                  </div>
                )}
              </div>

              {/* Equipment */}
              <div>
                <p className="font-medium text-gray-600 mb-1">Equipment:</p>
                <div className="flex flex-wrap gap-1">
                  {room.equipment.map((item, index) => (
                    <Badge key={index} variant="outline" className="text-xs px-1 py-0">
                      {item === 'TV Screen' || item === 'Screen' ? (
                        <Monitor className="h-2 w-2 mr-1" />
                      ) : item === 'Marker' || item === 'Glass Board' ? (
                        <PenTool className="h-2 w-2 mr-1" />
                      ) : null}
                      {item}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Occupancy Information */}
              {room.status === 'occupied' && room.occupiedBy && editingRoom !== room.id && (
                <div className="bg-white p-2 rounded border border-red-200 flex-shrink-0">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-medium text-red-600 mb-1 text-xs">Currently occupied:</p>
                      <p className="text-gray-800 text-xs">{room.occupiedBy}</p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => startEditing(room)}
                      className="text-gray-500 hover:text-gray-700 p-1 h-auto"
                    >
                      <Edit3 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              )}

              {/* Editing Form */}
              {editingRoom === room.id && (
                <div className="bg-white p-2 rounded border border-blue-200 flex-shrink-0">
                  <p className="font-medium text-blue-600 mb-1 text-xs">Occupancy reason:</p>
                  <Textarea
                    value={occupancyReason}
                    onChange={(e) => setOccupancyReason(e.target.value)}
                    placeholder="Enter reason..."
                    rows={2}
                    className="text-xs mb-2"
                  />
                  <div className="flex gap-1">
                    <Button
                      onClick={() => saveOccupancyReason(room.id)}
                      size="sm"
                      className="bg-blue-600 hover:bg-blue-700 text-white h-6 px-2 text-xs"
                    >
                      <Save className="h-2 w-2 mr-1" />
                      Save
                    </Button>
                    <Button
                      onClick={cancelEditing}
                      variant="outline"
                      size="sm"
                      className="h-6 px-2 text-xs"
                    >
                      <X className="h-2 w-2 mr-1" />
                      Cancel
                    </Button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="mt-auto pt-2">
                {room.status === 'vacant' ? (
                  <Button
                    onClick={() => startEditing(room)}
                    className="w-full bg-red-600 hover:bg-red-700 text-white h-6 text-xs"
                    size="sm"
                  >
                    <XCircle className="h-3 w-3 mr-1" />
                    Mark Occupied
                  </Button>
                ) : (
                  <Button
                    onClick={() => handleStatusChange(room.id, 'vacant')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white h-6 text-xs"
                    size="sm"
                  >
                    <CheckCircle className="h-3 w-3 mr-1" />
                    Mark Vacant
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Compact Quick Stats */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="p-4">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-xl font-bold text-blue-600">{rooms.length}</div>
              <div className="text-xs text-blue-700">Total Rooms</div>
            </div>
            <div>
              <div className="text-xl font-bold text-green-600">{vacantRooms}</div>
              <div className="text-xs text-green-700">Available</div>
            </div>
            <div>
              <div className="text-xl font-bold text-red-600">{occupiedRooms}</div>
              <div className="text-xs text-red-700">Occupied</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MeetingRooms;