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

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017/smartworld_db
PORT=8001
ENVIRONMENT=development
```

#### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Excel Data Files

The system uses Excel files for data import:
- `backend/employee_directory.xlsx` - Employee data
- `backend/attendance_data.xlsx` - Attendance records

### Default Admin Access

- **Login**: Admin Access button (no password required in development)
- **Role**: Administrator with full system access

## 🌐 Accessing the Application

Once everything is running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📊 System Features

### Core Modules
1. **Employee Directory** - Complete employee management
2. **Hierarchy Builder** - Organizational structure
3. **Attendance System** - Punch in/out tracking
4. **Task Management** - Project and task tracking
5. **News Feed** - Company announcements
6. **Knowledge Base** - Company documentation
7. **Help/Support** - Support ticket system
8. **Meeting Rooms** - Room booking system
9. **Policies** - Company policy management

### Data Management
- **Excel Integration** - Import/export employee data
- **Real-time Updates** - Live data synchronization
- **Search & Filter** - Advanced search capabilities
- **File Upload** - Profile images and documents

## 🛠️ Troubleshooting

### Common Issues

#### MongoDB Connection Issues
```bash
# Check MongoDB status
sudo systemctl status mongodb

# Check MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log

# Restart MongoDB
sudo systemctl restart mongodb
```

#### Port Already in Use
```bash
# Find process using port 8001
sudo lsof -i :8001

# Kill process
sudo kill -9 <PID>
```

#### Python Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Node.js Dependencies Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Service Management

#### Using Supervisor
```bash
# Check all services
sudo supervisorctl status

# Restart specific service
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

# View logs
sudo supervisorctl tail -f backend
sudo supervisorctl tail -f frontend
```

#### Manual Process Management
```bash
# Check processes
ps aux | grep python  # Backend
ps aux | grep node     # Frontend

# Stop processes
pkill -f "uvicorn"    # Stop backend
pkill -f "react"      # Stop frontend
```

## 🔐 Security Considerations

### Production Settings
1. **Change default MongoDB port**
2. **Enable MongoDB authentication**
3. **Use HTTPS with SSL certificates**
4. **Set strong environment variables**
5. **Configure firewall rules**
6. **Enable CORS properly**

### Example Production Environment
```env
# Backend .env (production)
MONGO_URL=mongodb://username:password@localhost:27017/smartworld_db
PORT=8001
ENVIRONMENT=production
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

## 📝 API Documentation

The system provides automatic API documentation:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Key API Endpoints
- `GET /api/employees` - Employee directory
- `GET /api/attendance` - Attendance records
- `GET /api/tasks` - Task management
- `GET /api/news` - Company news
- `GET /api/knowledge` - Knowledge base

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Documentation**: Check this README
- **Issues**: Create GitHub issue
- **Email**: contact@smartworlddevelopers.com

## 🔄 Updates

### Latest Version Features
- ✅ Real estate project banner integration
- ✅ Enhanced search functionality (starts-with pattern)
- ✅ Scrollable todo lists
- ✅ External quick links integration
- ✅ Improved UI/UX design

---

**Made with ❤️ by SmartWorld Developers**
