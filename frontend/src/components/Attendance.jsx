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

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

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
        record.employee_name.toLowerCase().startsWith(searchTerm.toLowerCase()) ||
        record.employee_id.toLowerCase().startsWith(searchTerm.toLowerCase())
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
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filters</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Attendance;