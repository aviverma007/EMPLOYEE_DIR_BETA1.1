import React, { useState, useEffect } from "react";
import { 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  X, 
  Clock,
  Cloud,
  Bell
} from "lucide-react";
import dataService from "../services/dataService";

const UserAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [currentAlertIndex, setCurrentAlertIndex] = useState(0);
  const [dismissedAlerts, setDismissedAlerts] = useState(new Set());
  const [showAlert, setShowAlert] = useState(false);
  const [isCloudVisible, setIsCloudVisible] = useState(true); // Control cloud visibility

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
    setDismissedAlerts(prev => new Set([...prev, alertId]));
    
    // If this was the last alert, hide the popup
    const remainingAlerts = alerts.filter(alert => alert.id !== alertId && !dismissedAlerts.has(alert.id));
    if (remainingAlerts.length === 0) {
      setShowAlert(false);
    }
  };

  const handleDismissAll = () => {
    const allAlertIds = alerts.map(alert => alert.id);
    setDismissedAlerts(prev => new Set([...prev, ...allAlertIds]));
    setShowAlert(false);
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
        bg: 'bg-red-500',
        text: 'text-white',
        border: 'border-red-600'
      };
      case 'warning': return {
        bg: 'bg-yellow-500',
        text: 'text-white',
        border: 'border-yellow-600'
      };
      case 'success': return {
        bg: 'bg-green-500',
        text: 'text-white',
        border: 'border-green-600'
      };
      default: return {
        bg: 'bg-blue-500',
        text: 'text-white',
        border: 'border-blue-600'
      };
    }
  };

  if (!showAlert || alerts.length === 0) {
    return null;
  }

  const currentAlert = alerts[currentAlertIndex];
  const colors = getAlertColors(currentAlert.type);

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm w-full animate-in slide-in-from-right duration-300">
      <div className={`${colors.bg} ${colors.text} rounded-lg shadow-2xl border-2 ${colors.border} overflow-hidden`}>
        {/* Alert Header */}
        <div className="px-4 py-3 border-b border-white border-opacity-20">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {getAlertIcon(currentAlert.type)}
              <span className="font-semibold text-sm">
                {currentAlert.title}
              </span>
              {currentAlert.priority === 'high' && (
                <span className="bg-white bg-opacity-20 px-2 py-1 rounded text-xs font-medium">
                  HIGH
                </span>
              )}
            </div>
            <button
              onClick={() => handleDismiss(currentAlert.id)}
              className="text-white hover:text-gray-200 transition-colors p-1 rounded-full hover:bg-white hover:bg-opacity-20"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Alert Content */}
        <div className="px-4 py-3">
          <p className="text-sm leading-relaxed mb-3">
            {currentAlert.message}
          </p>
          
          {/* Alert Footer */}
          <div className="flex items-center justify-between text-xs opacity-90">
            <div className="flex items-center space-x-1">
              <Clock className="h-3 w-3" />
              <span>
                {new Date(currentAlert.created_at).toLocaleDateString()}
              </span>
            </div>
            
            {alerts.length > 1 && (
              <div className="flex items-center space-x-2">
                <span>
                  {currentAlertIndex + 1} of {alerts.length}
                </span>
                {/* Progress indicators */}
                <div className="flex space-x-1">
                  {alerts.map((_, index) => (
                    <div
                      key={index}
                      className={`w-2 h-2 rounded-full ${
                        index === currentAlertIndex 
                          ? 'bg-white' 
                          : 'bg-white bg-opacity-40'
                      }`}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        {alerts.length > 1 && (
          <div className="px-4 py-2 border-t border-white border-opacity-20">
            <button
              onClick={handleDismissAll}
              className="w-full text-xs bg-white bg-opacity-20 hover:bg-opacity-30 px-3 py-2 rounded text-white font-medium transition-all duration-200"
            >
              Dismiss All Alerts
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserAlerts;