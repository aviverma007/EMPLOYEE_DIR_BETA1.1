import { useEffect, useState } from 'react';
import sharedNetworkStorage from '../services/sharedNetworkStorage';

/**
 * React hook for shared data synchronization
 * 
 * This hook:
 * 1. Listens for data changes from other systems
 * 2. Provides manual sync functionality
 * 3. Shows sync status and statistics
 * 4. Handles real-time UI updates
 */

export const useSharedDataSync = (dataTypes = []) => {
  const [syncStatus, setSyncStatus] = useState({
    isConnected: false,
    lastSync: null,
    syncCount: 0,
    errors: []
  });
  
  const [dataUpdates, setDataUpdates] = useState({});
  
  useEffect(() => {
    // Listen for shared data updates
    const handleDataUpdate = (event) => {
      const { dataType, timestamp } = event.detail;
      
      setDataUpdates(prev => ({
        ...prev,
        [dataType]: timestamp
      }));
      
      setSyncStatus(prev => ({
        ...prev,
        lastSync: timestamp,
        syncCount: prev.syncCount + 1
      }));
      
      console.log(`[useSharedDataSync] Data updated: ${dataType} at ${timestamp}`);
    };
    
    // Add event listener
    window.addEventListener('sharedDataUpdate', handleDataUpdate);
    
    // Initialize sync status
    const status = sharedNetworkStorage.getStatus();
    setSyncStatus(prev => ({
      ...prev,
      isConnected: status.polling
    }));
    
    // Cleanup
    return () => {
      window.removeEventListener('sharedDataUpdate', handleDataUpdate);
    };
  }, []);
  
  // Manual sync function
  const syncNow = async () => {
    try {
      setSyncStatus(prev => ({
        ...prev,
        errors: []
      }));
      
      const changes = await sharedNetworkStorage.syncNow();
      
      setSyncStatus(prev => ({
        ...prev,
        lastSync: new Date().toISOString(),
        syncCount: prev.syncCount + changes.length
      }));
      
      return changes;
    } catch (error) {
      console.error('[useSharedDataSync] Sync error:', error);
      
      setSyncStatus(prev => ({
        ...prev,
        errors: [...prev.errors, error.message]
      }));
      
      throw error;
    }
  };
  
  // Get sync statistics
  const getSyncStats = () => {
    const status = sharedNetworkStorage.getStatus();
    return {
      ...syncStatus,
      ...status,
      dataUpdates
    };
  };
  
  return {
    syncStatus,
    dataUpdates,
    syncNow,
    getSyncStats
  };
};

export default useSharedDataSync;