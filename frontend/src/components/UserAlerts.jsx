import React, { useState, useEffect } from "react";
import { 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Clock,
  Bell
} from "lucide-react";
import dataService from "../services/dataService";

const UserAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [currentAlertIndex, setCurrentAlertIndex] = useState(0);
  const [dismissedAlerts, setDismissedAlerts] = useState(new Set());
  const [showAlert, setShowAlert] = useState(false);
  const [isCloudVisible, setIsCloudVisible] = useState(true); // Control cloud visibility
  const [buttonPosition, setButtonPosition] = useState({ top: 16, right: 16 }); // Button position
  const [isDragging, setIsDragging] = useState(false);

  // Load alerts on component mount
  useEffect(() => {
    const checkAndLoadAlerts = async () => {
      // Wait for dataService to be loaded
      if (!dataService.isLoaded) {
        console.log('Waiting for dataService to load...');
        // Check every 500ms if dataService is loaded
        const checkInterval = setInterval(() => {
          if (dataService.isLoaded) {
            clearInterval(checkInterval);
            console.log('DataService loaded, loading alerts now...');
            loadActiveAlerts();
          }
        }, 500);
        
        // Timeout after 10 seconds
        setTimeout(() => {
          clearInterval(checkInterval);
          console.log('Timeout waiting for dataService, loading alerts anyway...');
          loadActiveAlerts();
        }, 10000);
      } else {
        console.log('DataService already loaded, loading alerts...');
        loadActiveAlerts();
      }
    };

    checkAndLoadAlerts();
    
    // Refresh alerts every 30 seconds to check for new ones
    const refreshInterval = setInterval(() => {
      if (dataService.isLoaded) {
        loadActiveAlerts();
      }
    }, 30000);

    return () => clearInterval(refreshInterval);
  }, []);

  const loadActiveAlerts = () => {
    try {
      const activeAlerts = dataService.getActiveAlerts();
      console.log('Loading active alerts:', activeAlerts); // Debug log
      
      // Filter out dismissed alerts
      const newAlerts = activeAlerts.filter(alert => !dismissedAlerts.has(alert.id));
      console.log('Filtered alerts (after dismissal):', newAlerts); // Debug log
      
      if (newAlerts.length > 0) {
        setAlerts(newAlerts);
        setCurrentAlertIndex(0);
        setShowAlert(true);
        console.log('Showing alerts:', newAlerts.length); // Debug log
      } else {
        setShowAlert(false);
        console.log('No alerts to show'); // Debug log
      }
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  // Auto-cycle through alerts every 4 seconds if there are multiple alerts
  useEffect(() => {
    if (alerts.length > 1 && showAlert) {
      const cycleInterval = setInterval(() => {
        setCurrentAlertIndex(prev => (prev + 1) % alerts.length);
      }, 4000);

      return () => clearInterval(cycleInterval);
    }
  }, [alerts.length, showAlert]);

  // Reload alerts when dismissed alerts change
  useEffect(() => {
    if (alerts.length > 0) {
      const activeAlerts = alerts.filter(alert => !dismissedAlerts.has(alert.id));
      if (activeAlerts.length === 0) {
        setShowAlert(false);
      } else if (activeAlerts.length !== alerts.length) {
        setAlerts(activeAlerts);
        setCurrentAlertIndex(0);
      }
    }
  }, [dismissedAlerts, alerts]);

  const handleDismiss = (alertId) => {
    // Removed dismiss functionality - alerts can't be closed individually
    console.log('Alert dismiss disabled');
  };

  const toggleCloudVisibility = () => {
    setIsCloudVisible(!isCloudVisible);
  };

  // Handle dragging functionality
  const handleMouseDown = (e) => {
    setIsDragging(true);
    const startY = e.clientY;
    const startTop = buttonPosition.top;

    const handleMouseMove = (e) => {
      const deltaY = e.clientY - startY;
      const newTop = Math.max(16, Math.min(window.innerHeight - 100, startTop + deltaY));
      setButtonPosition(prev => ({ ...prev, top: newTop }));
    };

    const handleMouseUp = () => {
      setIsDragging(false);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error': return <AlertTriangle className="h-5 w-5" />;
      case 'warning': return <AlertTriangle className="h-5 w-5" />;
      case 'success': return <CheckCircle className="h-5 w-5" />;
      default: return <Info className="h-5 w-5" />;
    }
  };

  const getAlertColors = (type) => {
    switch (type) {
      case 'error': return {
        bg: 'bg-red-100',
        text: 'text-red-800',
        border: 'border-red-200',
        icon: 'text-red-600'
      };
      case 'warning': return {
        bg: 'bg-yellow-100',
        text: 'text-yellow-800',
        border: 'border-yellow-200',
        icon: 'text-yellow-600'
      };
      case 'success': return {
        bg: 'bg-green-100',
        text: 'text-green-800',
        border: 'border-green-200',
        icon: 'text-green-600'
      };
      default: return {
        bg: 'bg-blue-50',
        text: 'text-blue-800',
        border: 'border-blue-200',
        icon: 'text-blue-600'
      };
    }
  };

  if (!showAlert || alerts.length === 0) {
    return (
      <>
        {/* Floating Cloud Button - Always visible when there are dismissed alerts */}
        {dismissedAlerts.size > 0 && (
          <div className="fixed top-4 right-4 z-50">
            <button
              onClick={toggleCloudVisibility}
              className="relative group"
            >
              {/* Blinking Animation */}
              <div className="absolute inset-0 bg-blue-400 rounded-full opacity-75 animate-ping"></div>
              
              {/* Cloud Button */}
              <div className="relative bg-gradient-to-br from-gray-700 via-gray-800 to-black rounded-full p-4 shadow-2xl border-2 border-gray-600 hover:scale-110 transition-all duration-300 backdrop-blur-sm bg-opacity-90">
                <div className="flex items-center justify-center">
                  <Cloud className="h-6 w-6 text-blue-300 filter drop-shadow-lg" />
                  <Bell className="h-4 w-4 text-white absolute top-2 right-2 animate-bounce" />
                </div>
              </div>
              
              {/* Notification Badge */}
              <div className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold animate-pulse">
                {dismissedAlerts.size}
              </div>
            </button>
          </div>
        )}
      </>
    );
  }

  if (!showAlert || alerts.length === 0) {
    return (
      <>
        {/* Floating Bell Button - Always visible when there are dismissed alerts */}
        {dismissedAlerts.size > 0 && (
          <div 
            className="fixed z-50"
            style={{ top: `${buttonPosition.top}px`, right: `${buttonPosition.right}px` }}
          >
            <button
              onClick={toggleCloudVisibility}
              onMouseDown={handleMouseDown}
              className={`relative group cursor-${isDragging ? 'grabbing' : 'grab'}`}
            >
              {/* Blinking Animation Ring */}
              <div className="absolute inset-0 bg-blue-400 rounded-full opacity-50 animate-ping"></div>
              
              {/* Bell Button - Smaller */}
              <div className="relative bg-white rounded-full p-2 shadow-lg border-2 border-blue-400 hover:scale-105 transition-all duration-300 backdrop-blur-sm">
                <Bell className="h-4 w-4 text-blue-600 animate-bounce" />
              </div>
              
              {/* Notification Badge - Smaller */}
              <div className="absolute -top-1 -right-1 bg-blue-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center font-bold animate-pulse">
                {dismissedAlerts.size}
              </div>
            </button>
          </div>
        )}
      </>
    );
  }

  const currentAlert = alerts[currentAlertIndex];
  const colors = getAlertColors(currentAlert.type);

  return (
    <>
      {/* Floating Bell Button - Draggable */}
      <div 
        className="fixed z-50"
        style={{ top: `${buttonPosition.top}px`, right: `${buttonPosition.right}px` }}
      >
        <button
          onClick={toggleCloudVisibility}
          onMouseDown={handleMouseDown}
          className={`relative group cursor-${isDragging ? 'grabbing' : 'grab'}`}
        >
          {/* Blinking Animation Ring */}
          <div className="absolute inset-0 bg-blue-400 rounded-full opacity-50 animate-ping"></div>
          
          {/* Bell Button - Smaller */}
          <div className="relative bg-white rounded-full p-2 shadow-lg border-2 border-blue-400 hover:scale-105 transition-all duration-300 backdrop-blur-sm">
            <Bell className="h-4 w-4 text-blue-600 animate-bounce" />
          </div>
          
          {/* Notification Badge - Smaller */}
          <div className="absolute -top-1 -right-1 bg-blue-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center font-bold animate-pulse">
            {alerts.length}
          </div>
        </button>
      </div>

      {/* Compact White-Blue Alert Popup */}
      {isCloudVisible && (
        <div 
          className="fixed z-40 max-w-xs w-full animate-in slide-in-from-right duration-300"
          style={{ 
            top: `${buttonPosition.top + 60}px`, 
            right: `${buttonPosition.right}px` 
          }}
        >
          {/* Compact Alert Container */}
          <div className="relative">
            {/* Alert Shadow */}
            <div className="absolute inset-0 bg-gray-300 opacity-20 rounded-2xl transform translate-x-1 translate-y-1 blur-sm"></div>
            
            {/* Main Alert Body - White & Blue Theme */}
            <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-200 backdrop-blur-md">
              {/* Alert Content - Compact */}
              <div className="p-4">
                {/* Alert Header - Compact */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <div className={`p-1.5 rounded-full ${colors.bg}`}>
                      <div className={colors.icon}>
                        {getAlertIcon(currentAlert.type)}
                      </div>
                    </div>
                    <div>
                      <h3 className={`font-semibold text-sm ${colors.text}`}>
                        {currentAlert.title}
                      </h3>
                      {currentAlert.priority === 'high' && (
                        <span className="bg-blue-500 text-white px-2 py-0.5 rounded text-xs font-medium">
                          HIGH
                        </span>
                      )}
                    </div>
                  </div>
                  {/* Removed X button - no dismiss functionality */}
                </div>

                {/* Alert Message - Compact */}
                <div className="mb-3 p-2 bg-blue-50 rounded-lg border border-blue-100">
                  <p className={`text-sm leading-relaxed ${colors.text}`}>
                    {currentAlert.message}
                  </p>
                </div>
                
                {/* Alert Footer - Compact */}
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Clock className="h-3 w-3" />
                    <span>
                      {new Date(currentAlert.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  
                  {alerts.length > 1 && (
                    <div className="flex items-center space-x-2">
                      <span className="text-blue-600 font-medium text-xs">
                        {currentAlertIndex + 1} of {alerts.length}
                      </span>
                      {/* Progress indicators - Smaller */}
                      <div className="flex space-x-1">
                        {alerts.map((_, index) => (
                          <div
                            key={index}
                            className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                              index === currentAlertIndex 
                                ? 'bg-blue-500 ring-1 ring-blue-300' 
                                : 'bg-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Blue accent glow - Subtle */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-100 to-blue-200 opacity-5 pointer-events-none"></div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default UserAlerts;