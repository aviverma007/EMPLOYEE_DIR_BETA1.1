import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { 
  Clock,
  Search,
  Filter,
  Calendar,
  User,
  MapPin
} from "lucide-react";

const Attendance = () => {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [filteredRecords, setFilteredRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedEmployee, setSelectedEmployee] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  
  // Form state
  const [attendanceForm, setAttendanceForm] = useState({
    employee_id: "",
    date: "",
    punch_in: "",
    punch_out: "",
    punch_in_location: "",
    punch_out_location: "",
    status: "present",
    remarks: ""
  });
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [showViewDialog, setShowViewDialog] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  const statuses = ["present", "absent", "half_day", "late"];
  const locations = ["Office", "Remote", "Client Site", "Branch Office"];

  // Fetch attendance records and employees
  useEffect(() => {
    fetchAttendanceRecords();
    fetchEmployees();
  }, []);

  // Apply filters
  useEffect(() => {
    let filtered = attendanceRecords;

    if (searchTerm) {
      filtered = filtered.filter(record =>
        record.employee_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.employee_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedEmployee && selectedEmployee !== "all") {
      filtered = filtered.filter(record => record.employee_id === selectedEmployee);
    }

    if (selectedDate) {
      filtered = filtered.filter(record => record.date === selectedDate);
    }

    setFilteredRecords(filtered);
  }, [attendanceRecords, searchTerm, selectedEmployee, selectedDate]);

  const fetchAttendanceRecords = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/attendance`);
      if (response.ok) {
        const data = await response.json();
        setAttendanceRecords(data);
      }
    } catch (error) {
      console.error('Error fetching attendance records:', error);
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

  const handleCreateAttendance = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/attendance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(attendanceForm),
      });

      if (response.ok) {
        setShowCreateDialog(false);
        resetForm();
        fetchAttendanceRecords();
        alert('Attendance record created successfully!');
      } else {
        const error = await response.json();
        alert(`Error creating attendance: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error creating attendance:', error);
      alert('Failed to create attendance record');
    }
  };

  const handleUpdateAttendance = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/attendance/${selectedRecord.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          punch_in: attendanceForm.punch_in,
          punch_out: attendanceForm.punch_out,
          punch_in_location: attendanceForm.punch_in_location,
          punch_out_location: attendanceForm.punch_out_location,
          status: attendanceForm.status,
          remarks: attendanceForm.remarks
        }),
      });

      if (response.ok) {
        setShowEditDialog(false);
        resetForm();
        setSelectedRecord(null);
        fetchAttendanceRecords();
        alert('Attendance record updated successfully!');
      } else {
        const error = await response.json();
        alert(`Error updating attendance: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error updating attendance:', error);
      alert('Failed to update attendance record');
    }
  };

  const handleDeleteAttendance = async (recordId) => {
    if (window.confirm('Are you sure you want to delete this attendance record?')) {
      try {
        const response = await fetch(`${backendUrl}/api/attendance/${recordId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchAttendanceRecords();
          alert('Attendance record deleted successfully!');
        } else {
          alert('Failed to delete attendance record');
        }
      } catch (error) {
        console.error('Error deleting attendance:', error);
        alert('Failed to delete attendance record');
      }
    }
  };

  const resetForm = () => {
    setAttendanceForm({
      employee_id: "",
      date: "",
      punch_in: "",
      punch_out: "",
      punch_in_location: "",
      punch_out_location: "",
      status: "present",
      remarks: ""
    });
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return 'Not recorded';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short', 
      day: 'numeric'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      present: 'bg-green-100 text-green-800',
      absent: 'bg-red-100 text-red-800',
      half_day: 'bg-yellow-100 text-yellow-800',
      late: 'bg-orange-100 text-orange-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'present':
        return <CheckCircle className="h-4 w-4" />;
      case 'absent':
        return <XCircle className="h-4 w-4" />;
      case 'half_day':
        return <AlertCircle className="h-4 w-4" />;
      case 'late':
        return <Clock className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const startEdit = (record) => {
    setSelectedRecord(record);
    setAttendanceForm({
      employee_id: record.employee_id,
      date: record.date,
      punch_in: record.punch_in ? new Date(record.punch_in).toISOString().slice(0, 16) : "",
      punch_out: record.punch_out ? new Date(record.punch_out).toISOString().slice(0, 16) : "",
      punch_in_location: record.punch_in_location || "",
      punch_out_location: record.punch_out_location || "",
      status: record.status,
      remarks: record.remarks || ""
    });
    setShowEditDialog(true);
  };

  const viewRecord = (record) => {
    setSelectedRecord(record);
    setShowViewDialog(true);
  };

  const getEmployeeName = (employeeId) => {
    const employee = employees.find(emp => emp.id === employeeId);
    return employee ? employee.name : 'Unknown Employee';
  };

  const calculateWorkingHours = (punchIn, punchOut) => {
    if (!punchIn || !punchOut) return 'N/A';
    const start = new Date(punchIn);
    const end = new Date(punchOut);
    const diffHours = (end - start) / (1000 * 60 * 60);
    return `${diffHours.toFixed(1)} hrs`;
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Employee Attendance</h1>
        <div className="text-sm text-gray-500">
          Attendance records are auto-synced from punch-in/out systems
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
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search employees..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={selectedEmployee} onValueChange={setSelectedEmployee}>
              <SelectTrigger>
                <SelectValue placeholder="Select Employee" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Employees</SelectItem>
                {employees.map((emp) => (
                  <SelectItem key={emp.id} value={emp.id}>
                    {emp.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              placeholder="Select Date"
            />

            <Button
              variant="outline"
              onClick={() => {
                setSearchTerm("");
                setSelectedEmployee("all");
                setSelectedDate("");
              }}
            >
              Clear Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Attendance Records */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-gray-500">Loading attendance records...</div>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredRecords.map((record) => (
              <Card key={record.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{record.employee_name}</CardTitle>
                      <div className="flex items-center gap-4 text-sm text-gray-500 mt-2">
                        <div className="flex items-center gap-1">
                          <User className="h-4 w-4" />
                          {record.employee_id}
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {formatDate(record.date)}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Punch In:</span>
                      <div className="font-medium">{formatDateTime(record.punch_in)}</div>
                      {record.punch_in_location && (
                        <div className="flex items-center gap-1 text-gray-400 text-xs">
                          <MapPin className="h-3 w-3" />
                          {record.punch_in_location}
                        </div>
                      )}
                    </div>
                    <div>
                      <span className="text-gray-500">Punch Out:</span>
                      <div className="font-medium">{formatDateTime(record.punch_out)}</div>
                      {record.punch_out_location && (
                        <div className="flex items-center gap-1 text-gray-400 text-xs">
                          <MapPin className="h-3 w-3" />
                          {record.punch_out_location}
                        </div>
                      )}
                    </div>
                    <div>
                      <span className="text-gray-500">Working Hours:</span>
                      <div className="font-medium">{calculateWorkingHours(record.punch_in, record.punch_out)}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && filteredRecords.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No attendance records found</div>
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filters or add a new record</div>
          </div>
        )}
      </div>

      {/* Edit Dialog */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Edit Attendance Record</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Employee</Label>
                <Input value={getEmployeeName(attendanceForm.employee_id)} disabled />
              </div>
              
              <div>
                <Label>Date</Label>
                <Input type="date" value={attendanceForm.date} disabled />
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Punch In</Label>
                <Input
                  type="datetime-local"
                  value={attendanceForm.punch_in}
                  onChange={(e) => setAttendanceForm(prev => ({ ...prev, punch_in: e.target.value }))}
                />
              </div>
              
              <div>
                <Label>Punch Out</Label>
                <Input
                  type="datetime-local"
                  value={attendanceForm.punch_out}
                  onChange={(e) => setAttendanceForm(prev => ({ ...prev, punch_out: e.target.value }))}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Punch In Location</Label>
                <Select value={attendanceForm.punch_in_location} onValueChange={(value) => setAttendanceForm(prev => ({ ...prev, punch_in_location: value }))}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select location" />
                  </SelectTrigger>
                  <SelectContent>
                    {locations.map((loc) => (
                      <SelectItem key={loc} value={loc}>
                        {loc}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label>Punch Out Location</Label>
                <Select value={attendanceForm.punch_out_location} onValueChange={(value) => setAttendanceForm(prev => ({ ...prev, punch_out_location: value }))}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select location" />
                  </SelectTrigger>
                  <SelectContent>
                    {locations.map((loc) => (
                      <SelectItem key={loc} value={loc}>
                        {loc}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label>Status</Label>
              <Select value={attendanceForm.status} onValueChange={(value) => setAttendanceForm(prev => ({ ...prev, status: value }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {statuses.map((status) => (
                    <SelectItem key={status} value={status}>
                      {status.replace('_', ' ').toUpperCase()}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Remarks</Label>
              <Textarea
                value={attendanceForm.remarks}
                onChange={(e) => setAttendanceForm(prev => ({ ...prev, remarks: e.target.value }))}
                placeholder="Additional notes..."
                rows={3}
              />
            </div>
            
            <div className="flex gap-2">
              <Button onClick={handleUpdateAttendance}>
                Update Attendance
              </Button>
              <Button variant="outline" onClick={() => setShowEditDialog(false)}>
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* View Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Attendance Details</DialogTitle>
          </DialogHeader>
          {selectedRecord && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-gray-500">Employee:</Label>
                  <div className="font-medium">{selectedRecord.employee_name}</div>
                  <div className="text-sm text-gray-400">{selectedRecord.employee_id}</div>
                </div>
                
                <div>
                  <Label className="text-gray-500">Date:</Label>
                  <div className="font-medium">{formatDate(selectedRecord.date)}</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-gray-500">Punch In:</Label>
                  <div className="font-medium">{formatDateTime(selectedRecord.punch_in)}</div>
                  {selectedRecord.punch_in_location && (
                    <div className="flex items-center gap-1 text-gray-500 text-sm">
                      <MapPin className="h-3 w-3" />
                      {selectedRecord.punch_in_location}
                    </div>
                  )}
                </div>
                
                <div>
                  <Label className="text-gray-500">Punch Out:</Label>
                  <div className="font-medium">{formatDateTime(selectedRecord.punch_out)}</div>
                  {selectedRecord.punch_out_location && (
                    <div className="flex items-center gap-1 text-gray-500 text-sm">
                      <MapPin className="h-3 w-3" />
                      {selectedRecord.punch_out_location}
                    </div>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-gray-500">Status:</Label>
                  <Badge className={`${getStatusColor(selectedRecord.status)} border-0 flex items-center gap-1 w-fit`}>
                    {getStatusIcon(selectedRecord.status)}
                    {selectedRecord.status.replace('_', ' ').toUpperCase()}
                  </Badge>
                </div>
                
                <div>
                  <Label className="text-gray-500">Working Hours:</Label>
                  <div className="font-medium">{calculateWorkingHours(selectedRecord.punch_in, selectedRecord.punch_out)}</div>
                </div>
              </div>

              {selectedRecord.remarks && (
                <div>
                  <Label className="text-gray-500">Remarks:</Label>
                  <div className="font-medium bg-gray-50 p-3 rounded-md">{selectedRecord.remarks}</div>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Attendance;