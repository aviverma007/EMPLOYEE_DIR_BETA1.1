# 🏢 Employee Directory System - Complete Setup Guide

A comprehensive full-stack employee management system built with React, FastAPI, and MongoDB. This system provides complete employee directory management, attendance tracking, task management, and more.

## 🎯 **CRITICAL: Excel Data Loading Solution**

**If you're experiencing "Database already has employees, skipping Excel load" - this section solves it completely!**

### ⚡ Quick Fix Commands
```bash
# Backend - Force Excel Reload
cd backend
python force_excel_load.py

# OR set environment variable
set FORCE_EXCEL_RELOAD=true  # Windows
export FORCE_EXCEL_RELOAD=true  # Linux/Mac
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

## 🏗️ Project Overview

This is a modern employee management system that includes:
- **Employee Directory** (640+ employees from Excel)
- **Hierarchy Builder** for organizational structure  
- **Task Management** system
- **News Feed** for company updates
- **Knowledge Base** for company information
- **Help/Support** system with threaded replies
- **Meeting Room Booking** (32 rooms across multiple locations)
- **Attendance Management** with punch in/out tracking
- **Policy Management** with categorization

## 🛠️ Technology Stack

- **Frontend**: React 18+ with Tailwind CSS
- **Backend**: FastAPI (Python 3.8+)  
- **Database**: MongoDB 4.4+
- **UI Components**: Radix UI + Custom Components
- **Excel Integration**: openpyxl + pandas
- **Process Management**: Supervisor (Linux) / Manual (Windows)

## 📋 Prerequisites & Installation

### 🖥️ **Windows Users** (Complete Guide)

#### **Required Software:**
1. **Node.js 16+** - [Download](https://nodejs.org/)
2. **Python 3.8+** - [Download](https://python.org/)  
3. **MongoDB Community** - [Download](https://www.mongodb.com/download-center/community)
4. **Git** - [Download](https://git-scm.com/)

#### **Step-by-Step Windows Setup:**

```cmd
# 1. Clone Repository
git clone <your-repo-url>
cd <repository-folder>

# 2. Run Automated Setup (Recommended)
setup_windows.bat

# 3. OR Manual Setup - Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy local_env_template.env .env

# 4. Manual Setup - Frontend  
cd ../frontend
npm install --legacy-peer-deps
echo REACT_APP_BACKEND_URL=http://localhost:8001 > .env
```

### 🐧 **Linux/Mac Users**

```bash
# 1. Clone Repository
git clone <your-repo-url>
cd <repository-folder>

# 2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure as needed

# 3. Frontend Setup
cd ../frontend  
npm install --legacy-peer-deps
echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
```

## 🚨 **Excel Data Loading - Complete Solution**

### **The Problem:**
Your backend shows: `"Database already has 640 employees, skipping Excel load"`

### **💡 Solution 1: Force Reload Script (Recommended)**

```cmd
cd backend
python force_excel_load.py
```

**What this does:**
- Clears all existing data (employees, attendance, etc.)
- Reloads fresh data from Excel files
- Initializes meeting rooms and other data
- Provides detailed logging

### **💡 Solution 2: Environment Variable**

**Windows:**
```cmd  
cd backend
.venv\Scripts\activate
set FORCE_EXCEL_RELOAD=true
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Linux/Mac:**
```bash
cd backend
source venv/bin/activate
export FORCE_EXCEL_RELOAD=true
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### **💡 Solution 3: Quick Batch File (Windows)**

```cmd
cd backend
run_server.bat
```

### **💡 Solution 4: Check Setup & Force Load**

```cmd
cd backend
python check_setup.py      # Verify all dependencies
python force_excel_load.py # Clear & reload Excel data  
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

## 🚀 **Running the Application**

### **Windows - Method 1 (Automated)**

```cmd
# Terminal 1 - Backend
cd backend
run_server.bat

# Terminal 2 - Frontend  
cd frontend
simple_start.bat
```

### **Windows - Method 2 (Manual)**

```cmd  
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
set FORCE_EXCEL_RELOAD=true
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm start
```

### **Linux/Mac**

```bash
# Terminal 1 - Backend  
cd backend
source venv/bin/activate
export FORCE_EXCEL_RELOAD=true
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm start
```

## 🔧 **Frontend Dependency Issues (Windows)**

### **Problem:** 
NPM errors with React 19, ESLint 9, date-fns conflicts

### **Solutions:**

#### **Method 1: Legacy Peer Dependencies**
```cmd
cd frontend
rmdir /S /Q node_modules
del package-lock.json  
npm install --legacy-peer-deps
npm start
```

#### **Method 2: Force Install**
```cmd
cd frontend
npm install --force
npm start
```

#### **Method 3: Use Yarn**  
```cmd
cd frontend
npm install -g yarn
yarn install
yarn start
```

#### **Method 4: Nuclear Fix (Guaranteed)**
```cmd
cd frontend
nuclear_fix.bat
```

#### **Method 5: Minimal Dependencies**
```cmd
cd frontend
copy package_minimal.json package.json
npm install
npm start
```

## 📁 **Project Structure**

```
employee-directory/
├── backend/                    # FastAPI Backend
│   ├── server.py              # Main application
│   ├── models.py              # Database models
│   ├── excel_parser.py        # Excel data processing  
│   ├── attendance_parser.py   # Attendance processing
│   ├── force_excel_load.py    # Force data reload
│   ├── check_setup.py         # Setup verification
│   ├── run_server.bat         # Windows server starter
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── employee_directory.xlsx # Employee data (640 records)
│   └── attendance_data.xlsx   # Attendance data
├── frontend/                   # React Frontend  
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── context/           # Authentication context
│   │   └── App.js            # Main app with 5-tab layout
│   ├── package.json          # Dependencies
│   ├── package_minimal.json  # Minimal dependencies backup
│   ├── nuclear_fix.bat       # Windows dependency fix
│   ├── simple_start.bat      # Windows starter
│   └── .env                  # Frontend environment
├── setup_windows.bat         # Complete Windows setup
├── WINDOWS_SETUP_GUIDE.md    # Detailed Windows guide
├── QUICK_START_WINDOWS.md    # Quick start instructions
└── README.md                # This file
```

## 🌐 **Accessing the Application**

Once everything is running:

- **Frontend**: http://localhost:3000  
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Admin Login**: Use "Admin Access" button (no password required)

## 📊 **System Features**

### **5-Tab Navigation System**
1. **Home** - Daily news management and company updates
2. **Employee Directory** - 640+ employees with search, filters, hierarchy builder
3. **Work** - Task management and assignment system  
4. **Knowledge** - Company policies, procedures, and documentation
5. **Help** - Support ticketing system with threaded replies

### **Advanced Features**
- **Excel Integration** - 640 employees loaded from `employee_directory.xlsx`
- **Meeting Room Booking** - 32 rooms across multiple locations (IFC, Noida, etc.)
- **Attendance Tracking** - Punch in/out with location tracking
- **Image Upload** - Profile pictures with base64 and file upload support
- **Hierarchy Management** - Organizational structure visualization
- **Search Functionality** - "Starts with" pattern across all fields
- **Real-time Updates** - Live data synchronization

### **Meeting Room System**
- **IFC Location**: 11 rooms (floors 11, 12, 14)
  - Floor 14: 9 conference rooms (OVAL, PETRONAS, BOARD ROOM, etc.)
- **Other Locations**: Noida, Central Office, Project Offices
- **Single Booking Policy** - One booking per room at a time
- **Status Tracking** - Real-time vacant/occupied status

## 🛠️ **Troubleshooting**

### **Excel Data Issues**

#### **Problem**: "Database already has employees, skipping Excel load"
```cmd
# Solution 1: Force reload script  
python force_excel_load.py

# Solution 2: Environment variable
set FORCE_EXCEL_RELOAD=true
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Solution 3: Check and verify
python check_setup.py
```

#### **Problem**: "Excel file not found"
```cmd
# Verify file location
dir employee_directory.xlsx  # Should be in backend folder

# Check parser configuration
python -c "from excel_parser import ExcelParser; print(ExcelParser().file_path)"
```

### **MongoDB Issues**

#### **Windows MongoDB Setup**
```cmd
# Install MongoDB Community Server
# Start MongoDB service
net start MongoDB

# Verify connection
mongo --eval "db.runCommand({connectionStatus: 1})"
```

#### **Connection Problems**
```cmd
# Check MongoDB status  
# Windows:
sc query MongoDB

# Linux:  
sudo systemctl status mongodb

# Test connection
python -c "from pymongo import MongoClient; print(MongoClient().admin.command('ismaster'))"
```

### **Frontend Dependency Conflicts**

#### **React 19 + ESLint 9 Issues**
```cmd
# Method 1: Legacy peer deps
npm install --legacy-peer-deps

# Method 2: Force install
npm install --force  

# Method 3: Use Yarn
npm install -g yarn
yarn install

# Method 4: Nuclear option
nuclear_fix.bat  # Windows
```

#### **Date-fns Version Conflicts**
```cmd
# Fix react-day-picker compatibility
npm install date-fns@3.6.0 --legacy-peer-deps
npm install react-day-picker@8.8.0 --legacy-peer-deps
```

### **Backend Issues**

#### **Server Won't Start**
```cmd
# Check Python version
python --version  # Should be 3.8+

# Verify dependencies
pip list | findstr fastapi
pip list | findstr uvicorn  
pip list | findstr pymongo

# Check virtual environment
.venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux

# Check logs
uvicorn server:app --host 0.0.0.0 --port 8001 --log-level debug
```

#### **Import Errors**
```cmd
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Install missing packages
pip install openpyxl et_xmlfile pandas motor
```

### **Port Conflicts**

#### **Port 8001 Already in Use**
```cmd
# Windows - Find process
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Linux - Find and kill process  
lsof -i :8001
kill -9 <PID>

# Use different port
uvicorn server:app --host 0.0.0.0 --port 8002 --reload
```

#### **Port 3000 Already in Use**
```cmd
# Kill React process
# Windows:
taskkill /f /im node.exe

# Linux:  
pkill -f react-scripts

# Use different port
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # Linux
```

## 🔧 **Configuration Files**

### **Backend Environment (.env)**
```env
# MongoDB Configuration  
MONGO_URL="mongodb://localhost:27017"
DB_NAME="employee_directory_db"

# Excel Configuration
FORCE_EXCEL_RELOAD=true
EXCEL_FILE_PATH="employee_directory.xlsx"

# Server Configuration
HOST="0.0.0.0"
PORT=8001
DEBUG=true
```

### **Frontend Environment (.env)**
```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001

# Development Configuration  
WDS_SOCKET_PORT=3000
GENERATE_SOURCEMAP=false
```

## 📚 **API Documentation**

### **Excel Data Endpoints**
- `POST /api/refresh-excel` - Force reload Excel data
- `GET /api/stats` - System statistics (employee count, etc.)
- `GET /api/departments` - List all departments (24 total)
- `GET /api/locations` - List all locations (23 total)

### **Employee Management**
- `GET /api/employees` - List all employees (640 records)
- `GET /api/employees?search=John` - Search employees (starts-with)
- `PUT /api/employees/{id}/image` - Update profile image (base64)
- `POST /api/employees/{id}/upload-image` - Upload image file

### **Meeting Rooms**
- `GET /api/meeting-rooms` - List all rooms (32 total)
- `GET /api/meeting-rooms?location=IFC` - Filter by location
- `POST /api/meeting-rooms/{id}/book` - Book room (single booking)
- `DELETE /api/meeting-rooms/{room_id}/booking/{booking_id}` - Cancel booking

### **Complete API Documentation**
Visit: http://localhost:8001/docs for interactive API documentation

## 🔐 **Security & Production**

### **Production Environment Variables**
```env
# Backend Production
MONGO_URL="mongodb://username:password@localhost:27017/production_db"
ENVIRONMENT="production"
ALLOWED_ORIGINS=["https://yourdomain.com"]
DEBUG=false

# Frontend Production  
REACT_APP_BACKEND_URL=https://api.yourdomain.com
```

### **Production Deployment**
1. **Build Frontend**: `npm run build`
2. **Serve Static Files**: Configure nginx/apache
3. **Process Manager**: Use PM2 or supervisor
4. **SSL Certificate**: Configure HTTPS
5. **Database Security**: Enable MongoDB authentication
6. **Firewall**: Configure proper ports (80, 443, not 3000/8001)

## 📋 **Quick Reference Commands**

### **Daily Development Workflow**
```cmd
# Start everything (Windows)
cd backend && run_server.bat
cd frontend && simple_start.bat

# Start everything (Linux)
cd backend && source venv/bin/activate && uvicorn server:app --reload --host 0.0.0.0 --port 8001
cd frontend && npm start

# Force refresh Excel data
cd backend && python force_excel_load.py

# Check system health  
cd backend && python check_setup.py
```

### **Reset Everything**
```cmd
# Clear database and reload
cd backend && python force_excel_load.py

# Reset frontend dependencies  
cd frontend && nuclear_fix.bat  # Windows
cd frontend && rm -rf node_modules package-lock.json && npm install --legacy-peer-deps  # Linux
```

## 🆘 **Getting Help**

### **Common Error Messages & Solutions**

| Error | Solution |
|-------|----------|
| "Database already has employees" | Run `python force_excel_load.py` |
| "Excel file not found" | Ensure `employee_directory.xlsx` is in backend folder |
| "MongoDB connection failed" | Start MongoDB service: `net start MongoDB` |
| "Cannot find module 'ajv/dist/compile/codegen'" | Run `npm install --legacy-peer-deps` |
| "ERESOLVE could not resolve" | Use `npm install --force` or `yarn install` |
| "Port 8001 is already in use" | Kill process: `netstat -ano \| findstr :8001` |

### **System Requirements Verification**
```cmd
# Check all requirements
node --version    # Should be 16+
python --version  # Should be 3.8+
mongo --version   # Should be 4.4+
npm --version     # Should be 8+
```

### **Emergency Reset (Nuclear Option)**
```cmd
# Complete reset - Windows
setup_windows.bat

# Complete reset - Linux  
./setup.sh
```

## 📄 **File Checklist**

Before running, ensure these files exist:
- ✅ `backend/employee_directory.xlsx` (640 employees)
- ✅ `backend/attendance_data.xlsx` (attendance records)
- ✅ `backend/.env` (environment variables)  
- ✅ `frontend/.env` (backend URL configuration)
- ✅ `backend/requirements.txt` (Python dependencies)
- ✅ `frontend/package.json` (Node.js dependencies)

## 🎉 **Success Indicators**

You'll know everything is working when you see:
- **Backend**: "Successfully loaded 640 employees from Excel"
- **Frontend**: "Compiled successfully!" 
- **Browser**: Application loads at http://localhost:3000
- **API Docs**: Available at http://localhost:8001/docs
- **Data**: Employee directory shows 640 employees
- **Meeting Rooms**: 32 rooms available for booking

---

**🚀 Made with ❤️ for SmartWorld Developers | Complete Windows & Linux Support**
