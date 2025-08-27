import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';
import { 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Database, 
  Clock, 
  Activity,
  Settings,
  CheckCircle,
  AlertCircle,
  Network
} from 'lucide-react';
import useSharedDataSync from '../hooks/useSharedDataSync';

/**
 * Sync Status Component
 * 
 * Shows real-time synchronization status across systems:
 * - Connection status to shared network storage
 * - Last sync time and sync count
 * - Manual sync button
 * - Detailed sync statistics
 * - Configuration status
 */

const SyncStatus = ({ isAdmin = false }) => {
  const { syncStatus, dataUpdates, syncNow, getSyncStats } = useSharedDataSync();
  const [isLoading, setIsLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  
  const handleManualSync = async () => {
    setIsLoading(true);
    try {
      const changes = await syncNow();
      console.log(`Manual sync completed: ${changes.length} changes`);
    } catch (error) {
      console.error('Manual sync failed:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const formatTime = (timestamp) => {
    if (!timestamp) return 'Never';
    return new Date(timestamp).toLocaleTimeString();
  };
  
  const formatDate = (timestamp) => {
    if (!timestamp) return 'Never';
    return new Date(timestamp).toLocaleString();
  };
  
  const stats = getSyncStats();
  
  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Compact Status Indicator */}
      <div className="flex items-center gap-2">
        {/* Main Status Card */}
        <Card className="shadow-lg border-2 bg-white/95 backdrop-blur-sm">
          <CardContent className="p-3">
            <div className="flex items-center gap-3">
              {/* Connection Status */}
              <div className="flex items-center gap-2">
                {syncStatus.isConnected ? (
                  <div className="flex items-center gap-1">
                    <Wifi className="h-4 w-4 text-green-600" />
                    <Badge variant="success" className="bg-green-100 text-green-700 text-xs">
                      Synced
                    </Badge>
                  </div>
                ) : (
                  <div className="flex items-center gap-1">
                    <WifiOff className="h-4 w-4 text-orange-600" />
                    <Badge variant="warning" className="bg-orange-100 text-orange-700 text-xs">
                      Local
                    </Badge>
                  </div>
                )}
              </div>
              
              {/* Sync Count */}
              <div className="flex items-center gap-1 text-sm text-gray-600">
                <Activity className="h-3 w-3" />
                <span>{syncStatus.syncCount}</span>
              </div>
              
              {/* Last Sync Time */}
              <div className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="h-3 w-3" />
                <span>{formatTime(syncStatus.lastSync)}</span>
              </div>
              
              {/* Manual Sync Button */}
              <Button
                variant="outline"
                size="sm"
                onClick={handleManualSync}
                disabled={isLoading}
                className="h-6 px-2 text-xs"
              >
                <RefreshCw className={`h-3 w-3 ${isLoading ? 'animate-spin' : ''}`} />
              </Button>
              
              {/* Details Button */}
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                    <Settings className="h-3 w-3" />
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                      <Network className="h-5 w-5" />
                      Shared Network Storage Status
                    </DialogTitle>
                    <DialogDescription>
                      Real-time synchronization status across all systems
                    </DialogDescription>
                  </DialogHeader>
                  
                  <SyncDetailsContent stats={stats} dataUpdates={dataUpdates} />
                </DialogContent>
              </Dialog>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

const SyncDetailsContent = ({ stats, dataUpdates }) => {
  return (
    <div className="space-y-4">
      {/* Connection Information */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">Connection Status</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Database className="h-4 w-4 text-blue-600" />
              <span>Shared Path:</span>
            </div>
            <div className="font-mono text-xs bg-gray-100 p-1 rounded">
              {stats.sharedPath}
            </div>
            
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-green-600" />
              <span>Polling:</span>
            </div>
            <div className="flex items-center gap-1">
              {stats.polling ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-orange-600" />
              )}
              <span>{stats.polling ? 'Active' : 'Inactive'}</span>
              <Badge variant="outline" className="text-xs">
                {stats.pollInterval}ms
              </Badge>
            </div>
            
            <div className="flex items-center gap-2">
              <Settings className="h-4 w-4 text-purple-600" />
              <span>System ID:</span>
            </div>
            <div className="font-mono text-xs bg-gray-100 p-1 rounded truncate">
              {stats.systemId}
            </div>
            
            <div className="flex items-center gap-2">
              <Wifi className="h-4 w-4 text-blue-600" />
              <span>File System API:</span>
            </div>
            <div className="flex items-center gap-1">
              {stats.hasFileSystemAPI ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-orange-600" />
              )}
              <span>{stats.hasFileSystemAPI ? 'Available' : 'Fallback Mode'}</span>
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Sync Statistics */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">Synchronization Statistics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.syncCount}</div>
              <div className="text-xs text-gray-500">Total Syncs</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {Object.keys(dataUpdates).length}
              </div>
              <div className="text-xs text-gray-500">Data Types</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {stats.callbacksRegistered?.length || 0}
              </div>
              <div className="text-xs text-gray-500">Active Listeners</div>
            </div>
          </div>
          
          {/* Last Sync Time */}
          <div className="text-center text-sm text-gray-600">
            Last Sync: {stats.lastSync ? new Date(stats.lastSync).toLocaleString() : 'Never'}
          </div>
        </CardContent>
      </Card>
      
      {/* Data Types Status */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">Data Types Synchronization</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-2">
            {[
              'alerts', 'meetingRooms', 'news', 'tasks', 
              'knowledge', 'help', 'hierarchy', 'attendance'
            ].map(dataType => (
              <div key={dataType} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <span className="text-sm font-medium capitalize">
                  {dataType.replace(/([A-Z])/g, ' $1')}
                </span>
                <div className="flex items-center gap-1">
                  {dataUpdates[dataType] ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <div className="h-4 w-4 border-2 border-gray-300 rounded-full" />
                  )}
                  <span className="text-xs text-gray-500">
                    {dataUpdates[dataType] ? 
                      new Date(dataUpdates[dataType]).toLocaleTimeString() : 
                      'No updates'
                    }
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
      
      {/* Configuration Guide */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-blue-800">Configuration Guide</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-blue-700 space-y-2">
          <div className="space-y-1">
            <div className="font-medium">To set up shared network storage:</div>
            <ol className="list-decimal list-inside space-y-1 text-xs">
              <li>Create a shared folder on your network (e.g., C:\SharedSmartWorldData)</li>
              <li>Update the SHARED_DATA_PATH in sharedNetworkStorage.js</li>
              <li>Ensure all systems can read/write to this location</li>
              <li>Restart the application after configuration</li>
            </ol>
          </div>
          <div className="mt-3 p-2 bg-blue-100 rounded text-xs">
            <strong>Current Path:</strong> 
            <div className="font-mono mt-1">{stats.sharedPath}</div>
          </div>
        </CardContent>
      </Card>
      
      {/* Errors */}
      {stats.errors && stats.errors.length > 0 && (
        <Card className="bg-red-50 border-red-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-red-800">Synchronization Errors</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {stats.errors.map((error, index) => (
              <div key={index} className="text-sm text-red-700 bg-red-100 p-2 rounded">
                {error}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SyncStatus;