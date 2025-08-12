import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Checkbox } from "./ui/checkbox";
import { 
  ChevronLeft, 
  ChevronRight, 
  Image, 
  Users, 
  PartyPopper, 
  CheckSquare, 
  Workflow, 
  Newspaper,
  Plus,
  X
} from "lucide-react";

const Home = () => {
  const [currentBannerIndex, setCurrentBannerIndex] = useState(0);
  const [todoItems, setTodoItems] = useState([
    { id: 1, text: "Review monthly reports", completed: false },
    { id: 2, text: "Schedule team meeting", completed: true },
    { id: 3, text: "Update employee profiles", completed: false }
  ]);
  const [newTodoText, setNewTodoText] = useState("");
  const [showAddTodo, setShowAddTodo] = useState(false);
  const [currentJoineeIndex, setCurrentJoineeIndex] = useState(0);
  const [employees, setEmployees] = useState([]);

  // Sample banner images (you can replace with actual company images)
  const bannerImages = [
    "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1200&h=300&fit=crop&crop=center"
  ];

  // Fetch employees data for new joinees
  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
        const response = await fetch(`${backendUrl}/api/employees`);
        if (response.ok) {
          const data = await response.json();
          // Filter employees who joined in July 2025 or later
          const recentJoinees = data.filter(emp => {
            const joinDate = new Date(emp.dateOfJoining);
            const july2025 = new Date('2025-07-01');
            return joinDate >= july2025;
          }).sort((a, b) => new Date(b.dateOfJoining) - new Date(a.dateOfJoining));
          
          setEmployees(recentJoinees.slice(0, 15)); // Show latest 15 employees
        }
      } catch (error) {
        console.error('Error fetching employees:', error);
        // Fallback data for demonstration - none as we want real data from July 2025
        setEmployees([]);
      }
    };
    
    fetchEmployees();
  }, []);

  // Auto-scroll banner every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentBannerIndex(prev => (prev + 1) % bannerImages.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [bannerImages.length]);

  // Auto-scroll new joinees every 2 seconds
  useEffect(() => {
    if (employees.length > 1) {
      const interval = setInterval(() => {
        setCurrentJoineeIndex(prev => (prev + 1) % employees.length);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [employees.length]);

  // Navigate banner manually
  const navigateBanner = (direction) => {
    if (direction === 'next') {
      setCurrentBannerIndex(prev => (prev + 1) % bannerImages.length);
    } else {
      setCurrentBannerIndex(prev => (prev - 1 + bannerImages.length) % bannerImages.length);
    }
  };

  // Todo list functions
  const addTodoItem = () => {
    if (newTodoText.trim()) {
      const newItem = {
        id: Date.now(),
        text: newTodoText.trim(),
        completed: false
      };
      setTodoItems([...todoItems, newItem]);
      setNewTodoText("");
      setShowAddTodo(false);
      localStorage.setItem('userTodos', JSON.stringify([...todoItems, newItem]));
    }
  };

  const toggleTodoItem = (id) => {
    const updatedItems = todoItems.map(item =>
      item.id === id ? { ...item, completed: !item.completed } : item
    );
    setTodoItems(updatedItems);
    localStorage.setItem('userTodos', JSON.stringify(updatedItems));
  };

  const removeTodoItem = (id) => {
    const updatedItems = todoItems.filter(item => item.id !== id);
    setTodoItems(updatedItems);
    localStorage.setItem('userTodos', JSON.stringify(updatedItems));
  };

  // Load todos from localStorage on component mount
  useEffect(() => {
    const savedTodos = localStorage.getItem('userTodos');
    if (savedTodos) {
      setTodoItems(JSON.parse(savedTodos));
    }
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const tiles = [
    {
      title: "PICTURES",
      icon: <Image className="h-6 w-6" />,
      description: "Company gallery and events",
      color: "bg-blue-600",
      textColor: "text-white"
    },
    {
      title: "NEW JOINEES",
      icon: <Users className="h-6 w-6" />,
      description: "Welcome our new team members",
      color: "bg-white border-2 border-blue-200",
      textColor: "text-blue-900",
      interactive: true
    },
    {
      title: "CELEBRATIONS",
      icon: <PartyPopper className="h-6 w-6" />,
      description: "Birthdays, anniversaries & achievements",
      color: "bg-blue-600",
      textColor: "text-white"
    },
    {
      title: "TO DO LIST",
      icon: <CheckSquare className="h-6 w-6" />,
      description: "Your personal task manager",
      color: "bg-white border-2 border-blue-200",
      textColor: "text-blue-900",
      interactive: true
    },
    {
      title: "WORKFLOW",
      icon: <Workflow className="h-6 w-6" />,
      description: "Process management & tracking",
      color: "bg-blue-600",
      textColor: "text-white"
    },
    {
      title: "DAILY COMPANY NEWS",
      icon: <Newspaper className="h-6 w-6" />,
      description: "Latest updates and announcements",
      color: "bg-white border-2 border-blue-200",
      textColor: "text-blue-900"
    }
  ];

  return (
    <div className="h-full flex flex-col space-y-4">
      {/* Compact Banner Section */}
      <div className="relative w-full h-48 rounded-lg shadow-md overflow-hidden">
        <div 
          className="flex transition-transform duration-500 ease-in-out h-full"
          style={{ transform: `translateX(-${currentBannerIndex * 100}%)` }}
        >
          {bannerImages.map((image, index) => (
            <div
              key={index}
              className="min-w-full h-full relative"
              style={{
                backgroundImage: `url(${image})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
            >
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
                <div className="text-center text-white">
                  <h2 className="text-3xl font-bold mb-2">Welcome to SmartWorld</h2>
                  <p className="text-lg">Building Tomorrow's Workforce Today</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Navigation Arrows */}
        <button
          onClick={() => navigateBanner('prev')}
          className="absolute left-3 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-1.5 transition-all"
        >
          <ChevronLeft className="h-5 w-5 text-gray-800" />
        </button>
        <button
          onClick={() => navigateBanner('next')}
          className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-1.5 transition-all"
        >
          <ChevronRight className="h-5 w-5 text-gray-800" />
        </button>
        
        {/* Dots Indicator */}
        <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 flex space-x-1.5">
          {bannerImages.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentBannerIndex(index)}
              className={`w-2.5 h-2.5 rounded-full transition-all ${
                index === currentBannerIndex ? 'bg-white' : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Tiles Section - Equal Height Grid */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tiles.map((tile, index) => (
          <Card 
            key={index}
            className={`${tile.color} ${tile.textColor} shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105 cursor-pointer h-full flex flex-col`}
          >
            <CardHeader className="pb-2 flex-shrink-0">
              <div className="flex items-center space-x-2">
                {tile.icon}
                <CardTitle className="text-base font-bold">{tile.title}</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="pt-0 flex-1 flex flex-col">
              {tile.interactive && tile.title === "NEW JOINEES" ? (
                <div className="flex-1 flex flex-col">
                  <p className="text-xs opacity-90 mb-3">{tile.description}</p>
                  
                  {/* New Joinees Dynamic Display */}
                  {employees.length > 0 ? (
                    <div className="flex-1 flex items-center justify-center">
                      <div className="text-center bg-blue-50 rounded-lg p-4 w-full">
                        <div className="transition-all duration-500">
                          <h3 className="font-semibold text-blue-900 text-lg mb-1">
                            {employees[currentJoineeIndex]?.name}
                          </h3>
                          <p className="text-blue-700 text-sm mb-1">
                            ID: {employees[currentJoineeIndex]?.id}
                          </p>
                          <p className="text-blue-600 text-xs">
                            Joined: {formatDate(employees[currentJoineeIndex]?.date_of_joining)}
                          </p>
                        </div>
                        <div className="flex justify-center mt-2 space-x-1">
                          {employees.map((_, idx) => (
                            <div
                              key={idx}
                              className={`w-1.5 h-1.5 rounded-full transition-all ${
                                idx === currentJoineeIndex ? 'bg-blue-600' : 'bg-blue-300'
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="flex-1 flex items-center justify-center text-blue-700">
                      <p className="text-sm">Loading new joinees...</p>
                    </div>
                  )}
                </div>
              ) : tile.interactive && tile.title === "TO DO LIST" ? (
                <div className="flex-1 flex flex-col">
                  <p className="text-xs opacity-90 mb-2">{tile.description}</p>
                  
                  {/* Todo Items - Compact version */}
                  <div className="flex-1 space-y-1.5 max-h-24 overflow-y-auto">
                    {todoItems.slice(0, 3).map((item) => (
                      <div key={item.id} className="flex items-center space-x-2 bg-blue-50 rounded p-1.5">
                        <Checkbox
                          checked={item.completed}
                          onCheckedChange={() => toggleTodoItem(item.id)}
                          className="border-blue-400 h-3 w-3"
                        />
                        <span className={`flex-1 text-xs text-blue-900 ${item.completed ? 'line-through opacity-70' : ''}`}>
                          {item.text}
                        </span>
                        <button
                          onClick={() => removeTodoItem(item.id)}
                          className="text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ))}
                  </div>

                  {/* Add Todo - Compact */}
                  {showAddTodo ? (
                    <div className="mt-auto space-y-1.5">
                      <Input
                        value={newTodoText}
                        onChange={(e) => setNewTodoText(e.target.value)}
                        placeholder="Enter new task..."
                        className="bg-blue-50 text-blue-900 placeholder-blue-500 border-blue-200 h-8 text-xs"
                        onKeyPress={(e) => e.key === 'Enter' && addTodoItem()}
                      />
                      <div className="flex space-x-1">
                        <Button 
                          size="sm" 
                          onClick={addTodoItem}
                          className="bg-blue-600 text-white hover:bg-blue-700 h-7 px-2 text-xs"
                        >
                          Add
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => {
                            setShowAddTodo(false);
                            setNewTodoText("");
                          }}
                          className="border-blue-400 text-blue-600 hover:bg-blue-50 h-7 px-2 text-xs"
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <Button
                      size="sm"
                      onClick={() => setShowAddTodo(true)}
                      className="mt-auto bg-blue-50 hover:bg-blue-100 text-blue-600 border-blue-200 border h-7 text-xs"
                    >
                      <Plus className="h-3 w-3 mr-1" />
                      Add Task
                    </Button>
                  )}
                </div>
              ) : (
                <div className="flex-1 flex items-start">
                  <p className="text-xs opacity-90">{tile.description}</p>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Home;