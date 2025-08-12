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

  // Sample banner images (you can replace with actual company images)
  const bannerImages = [
    "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=300&fit=crop&crop=center",
    "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1200&h=300&fit=crop&crop=center"
  ];

  // Auto-scroll banner every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentBannerIndex(prev => (prev + 1) % bannerImages.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [bannerImages.length]);

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
      // Save to localStorage (profile storage)
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

  const tiles = [
    {
      title: "PICTURES",
      icon: <Image className="h-6 w-6" />,
      description: "Company gallery and events",
      color: "bg-gradient-to-br from-purple-500 to-pink-500",
      textColor: "text-white"
    },
    {
      title: "NEW JOINEES",
      icon: <Users className="h-6 w-6" />,
      description: "Welcome our new team members",
      color: "bg-gradient-to-br from-green-500 to-teal-500",
      textColor: "text-white"
    },
    {
      title: "CELEBRATIONS",
      icon: <PartyPopper className="h-6 w-6" />,
      description: "Birthdays, anniversaries & achievements",
      color: "bg-gradient-to-br from-orange-500 to-red-500",
      textColor: "text-white"
    },
    {
      title: "TO DO LIST",
      icon: <CheckSquare className="h-6 w-6" />,
      description: "Your personal task manager",
      color: "bg-gradient-to-br from-blue-500 to-cyan-500",
      textColor: "text-white",
      interactive: true
    },
    {
      title: "WORKFLOW",
      icon: <Workflow className="h-6 w-6" />,
      description: "Process management & tracking",
      color: "bg-gradient-to-br from-indigo-500 to-purple-500",
      textColor: "text-white"
    },
    {
      title: "DAILY COMPANY NEWS",
      icon: <Newspaper className="h-6 w-6" />,
      description: "Latest updates and announcements",
      color: "bg-gradient-to-br from-yellow-500 to-orange-500",
      textColor: "text-white"
    }
  ];

  return (
    <div className="space-y-4">
      {/* Compact Banner Section - Reduced height */}
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

      {/* Compact Tiles Section - Optimized for single screen view */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tiles.map((tile, index) => (
          <Card 
            key={index}
            className={`${tile.color} ${tile.textColor} shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105 cursor-pointer h-auto`}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center space-x-2">
                {tile.icon}
                <CardTitle className="text-base font-bold">{tile.title}</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              {tile.interactive && tile.title === "TO DO LIST" ? (
                <div className="space-y-2">
                  <p className="text-xs opacity-90 mb-2">{tile.description}</p>
                  
                  {/* Todo Items - Compact version */}
                  <div className="space-y-1.5 max-h-24 overflow-y-auto">
                    {todoItems.slice(0, 3).map((item) => (
                      <div key={item.id} className="flex items-center space-x-2 bg-white bg-opacity-20 rounded p-1.5">
                        <Checkbox
                          checked={item.completed}
                          onCheckedChange={() => toggleTodoItem(item.id)}
                          className="border-white h-3 w-3"
                        />
                        <span className={`flex-1 text-xs ${item.completed ? 'line-through opacity-70' : ''}`}>
                          {item.text}
                        </span>
                        <button
                          onClick={() => removeTodoItem(item.id)}
                          className="text-white hover:text-red-200 transition-colors"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ))}
                  </div>

                  {/* Add Todo - Compact */}
                  {showAddTodo ? (
                    <div className="space-y-1.5">
                      <Input
                        value={newTodoText}
                        onChange={(e) => setNewTodoText(e.target.value)}
                        placeholder="Enter new task..."
                        className="bg-white text-gray-800 placeholder-gray-500 h-8 text-xs"
                        onKeyPress={(e) => e.key === 'Enter' && addTodoItem()}
                      />
                      <div className="flex space-x-1">
                        <Button 
                          size="sm" 
                          onClick={addTodoItem}
                          className="bg-white text-blue-600 hover:bg-gray-100 h-7 px-2 text-xs"
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
                          className="border-white text-white hover:bg-white hover:text-blue-600 h-7 px-2 text-xs"
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <Button
                      size="sm"
                      onClick={() => setShowAddTodo(true)}
                      className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white border-white border h-7 text-xs"
                    >
                      <Plus className="h-3 w-3 mr-1" />
                      Add Task
                    </Button>
                  )}
                </div>
              ) : (
                <p className="text-xs opacity-90">{tile.description}</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Home;