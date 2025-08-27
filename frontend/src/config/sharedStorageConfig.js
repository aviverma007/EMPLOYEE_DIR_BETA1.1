/**
 * Shared Network Storage Configuration
 * 
 * IMPORTANT: Update the SHARED_DATA_PATH to match your network setup
 * 
 * This file contains the configuration for shared network storage
 * that allows data synchronization across multiple systems.
 */

// =============================================================================
// CONFIGURATION SECTION - UPDATE THESE PATHS FOR YOUR NETWORK
// =============================================================================

/**
 * SHARED_DATA_PATH: The network location where all systems will store shared data
 * 
 * Examples:
 * - Windows Network Share: "\\\\SERVER-NAME\\SharedFolder\\SmartWorldData"
 * - Windows Local Share: "C:\\SharedSmartWorldData"
 * - Linux/Unix: "/mnt/shared/SmartWorldData"
 * - macOS: "/Volumes/SharedFolder/SmartWorldData"
 * 
 * Requirements:
 * 1. All systems must have read/write access to this location
 * 2. The folder should exist and be accessible before starting the application
 * 3. Ensure network connectivity between all systems using the application
 */

// UPDATE THIS PATH FOR YOUR SETUP:
export const SHARED_DATA_PATH = "C:\\SharedSmartWorldData";

// Alternative paths for different environments:
export const SHARED_DATA_PATHS = {
  // Development/Testing (local)
  development: "C:\\SharedSmartWorldData",
  
  // Production Windows Network
  windowsNetwork: "\\\\192.168.1.100\\SharedData\\SmartWorld",
  
  // Production Linux/Unix
  linuxNetwork: "/mnt/shared/smartworld",
  
  // Production macOS
  macNetwork: "/Volumes/SharedData/SmartWorld",
  
  // Cloud storage simulation (still uses localStorage but with network prefix)
  cloudSimulation: "localStorage_network_simulation"
};

// =============================================================================
// POLLING CONFIGURATION
// =============================================================================

/**
 * POLL_INTERVAL: How often to check for changes from other systems (in milliseconds)
 * 
 * Recommended values:
 * - Real-time: 1000ms (1 second) - High responsiveness, more network activity
 * - Balanced: 2000ms (2 seconds) - Good balance of responsiveness and performance
 * - Conservative: 5000ms (5 seconds) - Lower network activity, slower updates
 */
export const POLL_INTERVAL = 2000; // 2 seconds

/**
 * MAX_RETRY_ATTEMPTS: Number of times to retry failed operations
 */
export const MAX_RETRY_ATTEMPTS = 3;

/**
 * RETRY_DELAY: Delay between retry attempts (in milliseconds)
 */
export const RETRY_DELAY = 1000; // 1 second

// =============================================================================
// DATA TYPES CONFIGURATION
// =============================================================================

/**
 * SYNCED_DATA_TYPES: Which data types should be synchronized across systems
 * Set to false to disable synchronization for specific data types
 */
export const SYNCED_DATA_TYPES = {
  alerts: true,           // System alerts and notifications
  meetingRooms: true,     // Meeting room bookings
  news: true,             // Company news and announcements
  tasks: true,            // Task management
  knowledge: true,        // Knowledge base articles
  help: true,             // Help requests and support tickets
  hierarchy: true,        // Organization hierarchy
  attendance: true,       // Attendance records
  policies: false,        // Policies (usually static, disable if not needed)
  workflows: false        // Workflows (usually static, disable if not needed)
};

// =============================================================================
// SYSTEM IDENTIFICATION
// =============================================================================

/**
 * SYSTEM_NAME: A friendly name for this system (optional)
 * This helps identify which system made changes in logs
 */
export const SYSTEM_NAME = window.location.hostname || "Unknown System";

/**
 * AUTO_DETECT_ENVIRONMENT: Try to auto-detect the best configuration
 */
export const AUTO_DETECT_ENVIRONMENT = true;

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get the appropriate shared data path based on environment
 */
export const getSharedDataPath = () => {
  if (!AUTO_DETECT_ENVIRONMENT) {
    return SHARED_DATA_PATH;
  }
  
  // Try to detect the best path based on the environment
  const platform = navigator.platform.toLowerCase();
  const userAgent = navigator.userAgent.toLowerCase();
  
  if (platform.includes('win')) {
    // Windows environment
    return SHARED_DATA_PATHS.windowsNetwork;
  } else if (platform.includes('mac')) {
    // macOS environment
    return SHARED_DATA_PATHS.macNetwork;
  } else if (platform.includes('linux')) {
    // Linux environment
    return SHARED_DATA_PATHS.linuxNetwork;
  }
  
  // Fallback to default
  return SHARED_DATA_PATH;
};

/**
 * Get configuration summary for display
 */
export const getConfigSummary = () => {
  return {
    sharedPath: getSharedDataPath(),
    pollInterval: POLL_INTERVAL,
    systemName: SYSTEM_NAME,
    syncedDataTypes: Object.entries(SYNCED_DATA_TYPES)
      .filter(([, enabled]) => enabled)
      .map(([type]) => type),
    autoDetect: AUTO_DETECT_ENVIRONMENT
  };
};

/**
 * Validate configuration
 */
export const validateConfig = () => {
  const issues = [];
  
  if (!SHARED_DATA_PATH || SHARED_DATA_PATH.trim() === '') {
    issues.push('SHARED_DATA_PATH is not configured');
  }
  
  if (POLL_INTERVAL < 500) {
    issues.push('POLL_INTERVAL is too low (minimum 500ms recommended)');
  }
  
  if (POLL_INTERVAL > 30000) {
    issues.push('POLL_INTERVAL is too high (maximum 30000ms recommended)');
  }
  
  const enabledTypes = Object.values(SYNCED_DATA_TYPES).filter(Boolean);
  if (enabledTypes.length === 0) {
    issues.push('No data types are enabled for synchronization');
  }
  
  return {
    isValid: issues.length === 0,
    issues
  };
};

// =============================================================================
// USAGE EXAMPLES
// =============================================================================

/*
SETUP EXAMPLES:

1. Local Development (Single Machine Testing):
   - Set SHARED_DATA_PATH to "C:\\SharedSmartWorldData"
   - Create the folder manually
   - Test with multiple browser tabs/windows

2. Windows Network Setup:
   - Create shared folder on server: \\SERVER\SharedData\SmartWorld
   - Give all computers read/write access
   - Set SHARED_DATA_PATH to "\\\\SERVER\\SharedData\\SmartWorld"

3. Linux Network Setup:
   - Mount shared folder: sudo mount -t cifs //server/share /mnt/shared
   - Set SHARED_DATA_PATH to "/mnt/shared/smartworld"

4. Cloud Storage Simulation (No Network Share):
   - Keep AUTO_DETECT_ENVIRONMENT = true
   - Uses enhanced localStorage with network simulation
   - Good for testing without network setup
*/

export default {
  SHARED_DATA_PATH,
  SHARED_DATA_PATHS,
  POLL_INTERVAL,
  MAX_RETRY_ATTEMPTS,
  RETRY_DELAY,
  SYNCED_DATA_TYPES,
  SYSTEM_NAME,
  AUTO_DETECT_ENVIRONMENT,
  getSharedDataPath,
  getConfigSummary,
  validateConfig
};