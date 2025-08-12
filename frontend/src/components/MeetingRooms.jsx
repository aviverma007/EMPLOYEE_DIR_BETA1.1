import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
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
  Monitor,
  PenTool
} from 'lucide-react';
import { toast } from 'sonner';

const MeetingRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingRoom, setEditingRoom] = useState(null);
  const [occupancyReason, setOccupancyReason] = useState('');

  // Initialize with specific meeting rooms as requested
  useEffect(() => {
    const initializeRooms = () => {
      const companyRooms = [
        {
          id: 'oval-14',
          name: 'OVAL MEETING ROOM',
          capacity: 10,
          location: 'Floor 14',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['TV Screen', 'Marker', 'Glass Board']
        },
        {
          id: 'petronas',
          name: 'Petronas Meeting Room',
          capacity: 5,
          location: 'Main Building',
          status: 'vacant',
          occupiedBy: '',
          occupiedUntil: '',
          equipment: ['Marker', 'Glass Board']
        },
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