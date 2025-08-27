# Shared Network Storage Setup Guide

## Overview
This guide explains how to set up shared network storage for real-time data synchronization across multiple systems running the SmartWorld application.

## 🎯 What This Accomplishes
- **Real-time sync**: Alerts, meeting room bookings, and other data sync instantly across all systems
- **No cloud dependency**: Uses your local network infrastructure
- **Automatic polling**: Checks for updates every 2 seconds
- **Visual indicators**: Shows sync status and connection health
- **Cross-platform**: Works on Windows, Linux, and macOS

## 📁 Files Modified/Added

### New Files Created:
1. **`/app/frontend/src/services/sharedNetworkStorage.js`** - Core sync service
2. **`/app/frontend/src/config/sharedStorageConfig.js`** - Configuration file (EDIT THIS!)
3. **`/app/frontend/src/hooks/useSharedDataSync.js`** - React hook for sync
4. **`/app/frontend/src/components/SyncStatus.jsx`** - Status indicator component

### Modified Files:
1. **`/app/frontend/src/services/dataService.js`** - Added sync to all CRUD operations
2. **`/app/frontend/src/App.js`** - Added SyncStatus component
3. **`/app/frontend/src/components/MeetingRooms.jsx`** - Added real-time updates
4. **`/app/frontend/src/components/AlertManagement.jsx`** - Added real-time updates
5. **`/app/frontend/src/components/UserAlerts.jsx`** - Added real-time updates

## 🛠️ Setup Instructions

### Step 1: Configure the Shared Path
Edit `/app/frontend/src/config/sharedStorageConfig.js`:

```javascript
// UPDATE THIS PATH FOR YOUR SETUP:
export const SHARED_DATA_PATH = "YOUR_SHARED_NETWORK_PATH";
```

**Examples:**
- Windows Network: `"\\\\192.168.1.100\\SharedData\\SmartWorld"`
- Windows Local: `"C:\\SharedSmartWorldData"`
- Linux: `"/mnt/shared/smartworld"`
- macOS: `"/Volumes/SharedData/SmartWorld"`

### Step 2: Create the Shared Directory Structure

#### Option A: Windows Network Share
1. On your main system (always-on), create folder: `C:\SharedSmartWorldData`
2. Right-click → Properties → Sharing → Advanced Sharing
3. Check "Share this folder"
4. Set permissions for all users (Read/Write)
5. Update config to: `"\\\\MAIN-SYSTEM-IP\\SharedSmartWorldData"`

#### Option B: Linux Network Share
1. Create directory: `sudo mkdir -p /mnt/shared/smartworld`
2. Set up Samba or NFS sharing
3. Mount on other systems: `sudo mount -t cifs //main-system-ip/share /mnt/shared`
4. Update config to: `"/mnt/shared/smartworld"`

#### Option C: Local Testing (Single Machine)
1. Create folder: `C:\SharedSmartWorldData` (Windows) or `/tmp/smartworld` (Unix)
2. Keep default config for testing
3. Open multiple browser tabs/windows to test sync

### Step 3: Verify Network Access
Ensure all systems can:
- Read and write to the shared location
- Access each other on the network
- Have the same folder structure

### Step 4: Restart the Application
```bash
sudo supervisorctl restart frontend
```

## 🎛️ Configuration Options

### Polling Frequency
Edit `POLL_INTERVAL` in config file:
- `1000` = 1 second (high responsiveness)
- `2000` = 2 seconds (balanced - default)
- `5000` = 5 seconds (conservative)

### Data Types to Sync
Edit `SYNCED_DATA_TYPES` in config file:
```javascript
export const SYNCED_DATA_TYPES = {
  alerts: true,           // System alerts ✅
  meetingRooms: true,     // Room bookings ✅
  news: true,             // Company news ✅
  tasks: true,            // Tasks ✅
  knowledge: true,        // Knowledge base ✅
  help: true,             // Help requests ✅
  hierarchy: true,        // Org chart ✅
  attendance: true,       // Attendance ✅
  policies: false,        // Static data ❌
  workflows: false        // Static data ❌
};
```

## 📊 How It Works

### Data Flow
1. **User Action**: User creates alert/booking on System A
2. **Local Storage**: Data saved to local state immediately
3. **Shared Storage**: Data written to shared JSON file
4. **Network Sync**: Other systems detect file change via polling
5. **Real-time Update**: System B/C automatically refresh UI

### File Structure
```
SharedSmartWorldData/
├── alerts.json          # System alerts
├── meetingRooms.json    # Room bookings
├── news.json            # Company news
├── tasks.json           # Task management
├── knowledge.json       # Knowledge base
├── help.json            # Support requests
├── hierarchy.json       # Organization chart
├── attendance.json      # Attendance records
└── metadata.json        # System metadata
```

### Sync Status Indicator
- **Green "Synced"**: Connected and syncing
- **Orange "Local"**: Fallback to localStorage only
- **Sync count**: Number of successful syncs
- **Last sync time**: When data was last synchronized

## 🔍 Monitoring and Troubleshooting

### Check Sync Status
1. Look for sync indicator in bottom-right corner
2. Click settings icon for detailed status
3. Check browser console for sync logs

### Common Issues and Solutions

#### "Local" Status (Orange Badge)
**Problem**: Not connecting to shared storage
**Solutions**:
1. Verify shared path exists and is accessible
2. Check network connectivity between systems
3. Ensure read/write permissions on shared folder
4. Restart frontend service

#### No Real-time Updates
**Problem**: Changes not appearing on other systems
**Solutions**:
1. Check if shared files are being created/updated
2. Verify polling is active in sync status dialog
3. Ensure other systems are running and accessing same shared path
4. Check browser console for JavaScript errors

#### File Permission Errors
**Problem**: Cannot write to shared location
**Solutions**:
1. Set folder permissions to allow read/write for all users
2. Run application with appropriate user permissions
3. Check if antivirus is blocking file operations
4. Verify network share configuration

### Debug Logging
Open browser console to see detailed sync logs:
```
[SharedStorage] Initializing shared storage at: C:\SharedSmartWorldData
[DataService] Alert created and synced to shared storage
[SharedStorage] Detected change in alerts from another system
[MeetingRooms] Received real-time update from another system
```

## 🚀 Testing the Setup

### Single System Test
1. Open two browser tabs
2. Login as Admin in tab 1, User in tab 2
3. Create an alert in tab 1
4. Verify alert appears in tab 2

### Multi-System Test
1. Set up shared folder accessible from both systems
2. Update config on both systems to point to shared folder
3. Create meeting room booking on System A
4. Verify booking appears on System B within 2 seconds

### Performance Test
1. Monitor sync status counter
2. Create multiple alerts/bookings rapidly
3. Verify all changes sync without errors
4. Check shared folder for JSON file updates

## 🔧 Advanced Configuration

### Custom System Names
Update `SYSTEM_NAME` in config for better identification:
```javascript
export const SYSTEM_NAME = "Reception-Computer";
```

### Environment Detection
Enable `AUTO_DETECT_ENVIRONMENT` to automatically choose best path:
```javascript
export const AUTO_DETECT_ENVIRONMENT = true;
```

### Retry Settings
Configure retry behavior for failed operations:
```javascript
export const MAX_RETRY_ATTEMPTS = 3;
export const RETRY_DELAY = 1000;
```

## 📱 User Experience

### What Users See
1. **Immediate feedback**: Local changes appear instantly
2. **Sync notifications**: Toast messages when data updates from other systems
3. **Status indicator**: Always-visible sync status in corner
4. **No interruption**: Sync happens transparently in background

### What Admins See
- All user features plus:
- Detailed sync statistics in status dialog
- Configuration validation warnings
- Error logs and troubleshooting info

## 🛡️ Security Considerations

### Network Security
- Shared folder should be on internal network only
- Use VPN for remote access if needed
- Consider encrypting shared drive

### Data Privacy
- JSON files contain application data in plain text
- Ensure appropriate network access controls
- Regular backup of shared data folder

### File Locking
- Service handles concurrent access automatically
- Uses timestamp-based conflict resolution
- Last write wins in case of simultaneous updates

## 📞 Support

If you encounter issues:

1. **Check the sync status dialog** - Click the settings icon in the sync indicator
2. **Review browser console logs** - Look for error messages or warnings
3. **Verify network connectivity** - Ensure all systems can access the shared path
4. **Test file operations** - Manually create/edit files in shared folder
5. **Restart services** - Use `sudo supervisorctl restart frontend`

## 🎉 Success Confirmation

You'll know the setup is working when:
- ✅ Sync status shows "Synced" (green badge)
- ✅ Changes on one system appear on others within 2-5 seconds
- ✅ JSON files are created/updated in shared folder
- ✅ No error messages in browser console
- ✅ Sync counter increments with each change

## 📋 Quick Setup Checklist

- [ ] Create shared network folder
- [ ] Update `SHARED_DATA_PATH` in config file
- [ ] Verify network access from all systems
- [ ] Restart frontend service
- [ ] Test with alert creation/booking
- [ ] Confirm sync status shows "Synced"
- [ ] Verify real-time updates between systems

---

**Note**: This setup enables frontend-only synchronization without requiring a backend database server. All data is managed through the shared network storage system.