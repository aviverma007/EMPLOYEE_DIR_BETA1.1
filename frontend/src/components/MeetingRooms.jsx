import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { 
  Calendar, 
  Clock, 
  Users, 
  MapPin, 
  CheckCircle, 
  XCircle, 
  Edit3, 
  Save,
  X,
  PlusCircle
} from 'lucide-react';
import { toast } from 'sonner';

const MeetingRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingRoom, setEditingRoom] = useState(null);
  const [occupancyReason, setOccupancyReason] = useState('');

  // Initialize with sample meeting rooms
  useEffect(() => {
    const initializeRooms = () => {
      const sampleRooms = [
        {
          id: 'room-001',
          name: 'Conference Room A',
          capacity: 12,
          location: 'Floor 1, East Wing',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Projector', 'Whiteboard', 'Video Conferencing']
        },
        {
          id: 'room-002',
          name: 'Meeting Room B',
          capacity: 8,
          location: 'Floor 2, West Wing',
          status: 'occupied',
          occupiedBy: 'Marketing Team - Q1 Planning Meeting',
          occupiedUntil: '15:30',
          equipment: ['TV Screen', 'Whiteboard']
        },
        {
          id: 'room-003',
          name: 'Boardroom',
          capacity: 16,
          location: 'Floor 3, Executive Wing',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Large Screen', 'Conference Phone', 'Whiteboard']
        },
        {
          id: 'room-004',
          name: 'Training Room',
          capacity: 25,
          location: 'Floor 1, North Wing',
          status: 'occupied',
          occupiedBy: 'Employee Onboarding Session',
          occupiedUntil: '17:00',
          equipment: ['Projector', 'Sound System', 'Flipcharts']
        },
        {
          id: 'room-005',
          name: 'Small Meeting Room C',
          capacity: 4,
          location: 'Floor 2, East Wing',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['TV Screen', 'Whiteboard']
        },
        {
          id: 'room-006',
          name: 'Innovation Lab',
          capacity: 10,
          location: 'Floor 3, Creative Wing',
          status: 'occupied',
          occupiedBy: 'Product Development Sprint Review',
          occupiedUntil: '16:45',
          equipment: ['Interactive Whiteboard', 'Brainstorming Tools']
        }
      ];
      
      setRooms(sampleRooms);
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
      ? <CheckCircle className="h-4 w-4" />
      : <XCircle className="h-4 w-4" />;
  };

  const vacantRooms = rooms.filter(room => room.status === 'vacant').length;
  const occupiedRooms = rooms.filter(room => room.status === 'occupied').length;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-blue-600">Loading meeting rooms...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-blue-900">Meeting Room Management</h2>
          <p className="text-blue-600">Manage room availability and track occupancy</p>
        </div>
        <div className="flex gap-4">
          <Badge className="px-4 py-2 bg-green-100 text-green-800 border-green-200">
            <CheckCircle className="h-4 w-4 mr-2" />
            {vacantRooms} Vacant
          </Badge>
          <Badge className="px-4 py-2 bg-red-100 text-red-800 border-red-200">
            <XCircle className="h-4 w-4 mr-2" />
            {occupiedRooms} Occupied
          </Badge>
        </div>
      </div>

      {/* Room Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {rooms.map((room) => (
          <Card 
            key={room.id} 
            className={`hover:shadow-lg transition-all duration-300 border-2 ${
              room.status === 'vacant' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
            }`}
          >
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg font-semibold text-gray-900">
                  {room.name}
                </CardTitle>
                <Badge className={`${getStatusColor(room.status)} border font-medium`}>
                  {getStatusIcon(room.status)}
                  <span className="ml-1 capitalize">{room.status}</span>
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Room Details */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Users className="h-4 w-4 text-blue-500" />
                  <span>Capacity: {room.capacity} people</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPin className="h-4 w-4 text-blue-500" />
                  <span>{room.location}</span>
                </div>
                {room.status === 'occupied' && room.occupiedUntil && (
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Clock className="h-4 w-4 text-blue-500" />
                    <span>Until: {room.occupiedUntil}</span>
                  </div>
                )}
              </div>

              {/* Equipment */}
              <div>
                <p className="text-xs font-medium text-gray-600 mb-2">Equipment:</p>
                <div className="flex flex-wrap gap-1">
                  {room.equipment.map((item, index) => (
                    <Badge key={index} variant="outline" className="text-xs px-2 py-1">
                      {item}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Occupancy Information */}
              {room.status === 'occupied' && room.occupiedBy && editingRoom !== room.id && (
                <div className="bg-white p-3 rounded-lg border border-red-200">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="text-xs font-medium text-red-600 mb-1">Currently occupied for:</p>
                      <p className="text-sm text-gray-800">{room.occupiedBy}</p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => startEditing(room)}
                      className="text-gray-500 hover:text-gray-700 p-1"
                    >
                      <Edit3 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              )}

              {/* Editing Form */}
              {editingRoom === room.id && (
                <div className="bg-white p-3 rounded-lg border border-blue-200">
                  <p className="text-xs font-medium text-blue-600 mb-2">Occupancy reason:</p>
                  <Textarea
                    value={occupancyReason}
                    onChange={(e) => setOccupancyReason(e.target.value)}
                    placeholder="Enter reason for room occupancy..."
                    rows={2}
                    className="text-sm mb-3"
                  />
                  <div className="flex gap-2">
                    <Button
                      onClick={() => saveOccupancyReason(room.id)}
                      size="sm"
                      className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                      <Save className="h-3 w-3 mr-1" />
                      Save
                    </Button>
                    <Button
                      onClick={cancelEditing}
                      variant="outline"
                      size="sm"
                    >
                      <X className="h-3 w-3 mr-1" />
                      Cancel
                    </Button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-2 pt-2">
                {room.status === 'vacant' ? (
                  <Button
                    onClick={() => startEditing(room)}
                    className="w-full bg-red-600 hover:bg-red-700 text-white"
                    size="sm"
                  >
                    <XCircle className="h-4 w-4 mr-2" />
                    Mark as Occupied
                  </Button>
                ) : (
                  <Button
                    onClick={() => handleStatusChange(room.id, 'vacant')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white"
                    size="sm"
                  >
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Mark as Vacant
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Stats */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">{rooms.length}</div>
              <div className="text-sm text-blue-700">Total Rooms</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">{vacantRooms}</div>
              <div className="text-sm text-green-700">Available Now</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-red-600">{occupiedRooms}</div>
              <div className="text-sm text-red-700">Currently Occupied</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MeetingRooms;