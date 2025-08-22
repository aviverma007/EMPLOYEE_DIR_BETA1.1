import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Calendar, MapPin, Users, Clock, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';
import { meetingRoomAPI, employeeAPI, utilityAPI } from '../services/api';
import SearchableEmployeeDropdown from './ui/SearchableEmployeeDropdown';

const MeetingRooms = () => {
  const { isAdmin } = useAuth();
  const [rooms, setRooms] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [locations, setLocations] = useState([]);
  const [filters, setFilters] = useState({
    location: '',
    floor: '',
    status: ''
  });
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [bookingData, setBookingData] = useState({
    employee_name: '',
    employee_id: '',
    start_time: '',
    end_time: '',
    purpose: ''
  });
  const [loading, setLoading] = useState(true);

  // Set user-specific filters after component mounts
  useEffect(() => {
    if (!isAdmin()) {
      setFilters({
        location: 'IFC',
        floor: '14th Floor',
        status: ''
      });
    }
  }, [isAdmin]);

  useEffect(() => {
    fetchRooms();
    fetchEmployees();
    fetchLocations();
  }, []);

  useEffect(() => {
    fetchRooms();
  }, [filters]);

  const fetchRooms = async () => {
    try {
      setLoading(true);
      const data = await meetingRoomAPI.getAll(filters);
      setRooms(data);
    } catch (error) {
      console.error('Error fetching rooms:', error);
      toast.error('Failed to load meeting rooms');
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const data = await employeeAPI.getAll();
      setEmployees(data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const fetchLocations = async () => {
    try {
      const data = await utilityAPI.getLocations();
      setLocations(data.filter(loc => loc !== 'All Locations'));
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const handleBookRoom = async () => {
    if (!selectedRoom || !bookingData.employee_id || !bookingData.start_time || !bookingData.end_time) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      const employee = employees.find(emp => emp.id === bookingData.employee_id);
      const bookingPayload = {
        ...bookingData,
        employee_name: employee ? employee.name : bookingData.employee_name,
        room_name: selectedRoom.name
      };

      await meetingRoomAPI.book(selectedRoom.id, bookingPayload);
      toast.success('Room booked successfully!');
      
      setSelectedRoom(null);
      setBookingData({
        employee_name: '',
        employee_id: '',
        start_time: '',
        end_time: '',
        purpose: ''
      });
      fetchRooms();
    } catch (error) {
      console.error('Error booking room:', error);
      toast.error(error.message || 'Failed to book room');
    }
  };

  const handleCancelBooking = async (roomId) => {
    if (window.confirm('Are you sure you want to cancel this booking?')) {
      try {
        await meetingRoomAPI.cancelBooking(roomId);
        toast.success('Booking cancelled successfully');
        fetchRooms();
      } catch (error) {
        console.error('Error cancelling booking:', error);
        toast.error('Failed to cancel booking');
      }
    }
  };

  const handleClearAllBookings = async () => {
    if (window.confirm('Are you sure you want to clear all bookings? This action cannot be undone.')) {
      try {
        const result = await meetingRoomAPI.clearAllBookings();
        toast.success(result.message || 'All bookings cleared successfully');
        fetchRooms();
      } catch (error) {
        console.error('Error clearing all bookings:', error);
        toast.error('Failed to clear all bookings');
      }
    }
  };

  const handleEmployeeSelect = (employeeId) => {
    const employee = employees.find(emp => emp.id === employeeId);
    setBookingData({
      ...bookingData,
      employee_id: employeeId,
      employee_name: employee ? employee.name : ''
    });
  };

  const clearFilters = () => {
    if (isAdmin()) {
      setFilters({
        location: '',
        floor: '',
        status: ''
      });
    } else {
      setFilters({
        location: 'IFC',
        floor: '14th Floor',
        status: ''
      });
    }
  };

  const getUniqueFloors = () => {
    const floors = [...new Set(rooms.map(room => room.floor))];
    return floors.sort();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading meeting rooms...</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Meeting Rooms</h1>
        <Button onClick={handleClearAllBookings} variant="outline">
          Clear All Bookings
        </Button>
      </div>

      {/* Filters - Only show for Admin */}
      {isAdmin() && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Location & Floor Selection</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Location Filter</label>
                <select
                  value={filters.location}
                  onChange={(e) => setFilters({...filters, location: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">All Locations</option>
                  {locations.map(location => (
                    <option key={location} value={location}>
                      {location}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Floor Filter</label>
                <select
                  value={filters.floor}
                  onChange={(e) => setFilters({...filters, floor: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">All Floors</option>
                  {getUniqueFloors().map(floor => (
                    <option key={floor} value={floor}>
                      {floor}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Room Status Filter</label>
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({...filters, status: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">All Status</option>
                  <option value="vacant">Vacant</option>
                  <option value="occupied">Occupied</option>
                </select>
              </div>

              <div className="flex items-end">
                <Button variant="outline" onClick={clearFilters} className="w-full">
                  Clear Filters
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* For Users - Show info about 14th floor IFC rooms */}
      {!isAdmin() && (
        <Card className="mb-6 bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <MapPin className="h-5 w-5 text-blue-600" />
              <div>
                <h3 className="font-semibold text-blue-900">Meeting Rooms - IFC 14th Floor</h3>
                <p className="text-sm text-blue-700">Showing available meeting rooms on the 14th floor at IFC location (9 rooms available)</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Booking Modal */}
      {selectedRoom && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold mb-4">Book {selectedRoom.name}</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Employee</label>
                <SearchableEmployeeDropdown
                  employees={employees}
                  selectedEmployeeId={bookingData.employee_id}
                  onEmployeeSelect={handleEmployeeSelect}
                  placeholder="Search by employee name or ID..."
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Start Time</label>
                  <Input
                    type="datetime-local"
                    value={bookingData.start_time}
                    onChange={(e) => setBookingData({...bookingData, start_time: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">End Time</label>
                  <Input
                    type="datetime-local"
                    value={bookingData.end_time}
                    onChange={(e) => setBookingData({...bookingData, end_time: e.target.value})}
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Purpose</label>
                <Input
                  value={bookingData.purpose}
                  onChange={(e) => setBookingData({...bookingData, purpose: e.target.value})}
                  placeholder="Meeting purpose"
                />
              </div>
            </div>

            <div className="flex space-x-2 mt-6">
              <Button onClick={handleBookRoom}>
                Book Room
              </Button>
              <Button variant="outline" onClick={() => setSelectedRoom(null)}>
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Room Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {rooms.map(room => (
          <Card key={room.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg">{room.name}</CardTitle>
                <Badge 
                  className={room.status === 'vacant' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'}
                >
                  {room.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center text-sm text-gray-600">
                  <MapPin className="mr-2 h-4 w-4" />
                  {room.location} - {room.floor}
                </div>

                <div className="flex items-center text-sm text-gray-600">
                  <Users className="mr-2 h-4 w-4" />
                  Capacity: {room.capacity} people
                </div>

                <div className="text-sm text-gray-600">
                  <strong>Amenities:</strong> {room.amenities || 'Basic facilities'}
                </div>

                {room.current_booking && (
                  <div className="bg-blue-50 p-3 rounded-md">
                    <div className="flex items-center text-sm text-blue-800 mb-2">
                      <Clock className="mr-1 h-4 w-4" />
                      Current Booking
                    </div>
                    <div className="text-sm">
                      <p><strong>Employee:</strong> {room.current_booking.employee_name}</p>
                      <p><strong>Time:</strong> {new Date(room.current_booking.start_time).toLocaleString()} - {new Date(room.current_booking.end_time).toLocaleString()}</p>
                      {room.current_booking.purpose && (
                        <p><strong>Purpose:</strong> {room.current_booking.purpose}</p>
                      )}
                    </div>
                  </div>
                )}

                <div className="flex space-x-2">
                  {room.status === 'vacant' ? (
                    <Button 
                      onClick={() => setSelectedRoom(room)}
                      className="flex-1"
                    >
                      <CheckCircle className="mr-1 h-4 w-4" />
                      Book Room
                    </Button>
                  ) : (
                    <Button 
                      variant="outline"
                      onClick={() => handleCancelBooking(room.id)}
                      className="flex-1"
                    >
                      <XCircle className="mr-1 h-4 w-4" />
                      Cancel Booking
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {rooms.length === 0 && (
        <div className="text-center py-12">
          <Calendar className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No meeting rooms found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Try adjusting your filter criteria to see available rooms.
          </p>
        </div>
      )}
    </div>
  );
};

export default MeetingRooms;