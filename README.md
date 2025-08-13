# SmartWorld Employee Management System

A comprehensive full-stack employee management system built with React, FastAPI, and MongoDB. This system provides complete employee directory management, attendance tracking, task management, and more.

## 🏗️ Project Overview

This is a modern employee management system that includes:
- **Employee Directory** with search and filtering
- **Hierarchy Builder** for organizational structure
- **Attendance Management** with punch in/out tracking
- **Task Management** system
- **News Feed** for company updates
- **Knowledge Base** for company information
- **Help/Support** system with threaded replies
- **Meeting Room Booking** system
- **Policy Management**

## 🛠️ Technology Stack

- **Frontend**: React 18+ with Vite
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **UI Components**: Custom components with Tailwind CSS
- **Process Management**: Supervisor (for production)

## 📋 Prerequisites

Before installing, ensure you have the following installed on your server:

### Required Software:
- **Node.js** (v16 or higher) - [Download Node.js](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download Python](https://python.org/)
- **MongoDB** (v4.4 or higher) - [Download MongoDB](https://mongodb.com/try/download/community)
- **Git** (for cloning) - [Download Git](https://git-scm.com/)

### Package Managers:
- **npm** or **yarn** (comes with Node.js)
- **pip** (comes with Python)

## 🚀 Installation Guide

### Method 1: Automatic Setup (Recommended)

1. **Clone the Repository**
```bash
git clone <your-repository-url>
cd smartworld-employee-system
```

2. **Run Setup Script**
```bash
# Make setup script executable
chmod +x setup.sh

# Run the setup script (installs all dependencies)
./setup.sh
```

### Method 2: Manual Setup

#### Step 1: Clone and Navigate
```bash
git clone <your-repository-url>
cd smartworld-employee-system
```

#### Step 2: Backend Setup

1. **Navigate to Backend Directory**
```bash
cd backend
```

2. **Create Python Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Additional Dependencies** (if needed)
```bash
pip install fastapi uvicorn motor pymongo pandas openpyxl python-multipart python-dotenv
```

#### Step 3: Frontend Setup

1. **Navigate to Frontend Directory**
```bash
cd ../frontend
```

2. **Install Node.js Dependencies**
```bash
# Using npm
npm install

# OR using yarn (recommended)
yarn install
```

#### Step 4: Database Setup

1. **Install MongoDB**
   - **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install mongodb
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   ```
   
   - **CentOS/RHEL:**
   ```bash
   sudo yum install mongodb-org
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```
   
   - **macOS (using Homebrew):**
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb/brew/mongodb-community
   ```

2. **Verify MongoDB Installation**
```bash
mongo --version
```

#### Step 5: Environment Configuration

1. **Backend Environment (.env)**
```bash
cd backend
cp .env.example .env  # If available, or create new
```

Edit `backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017/smartworld_db
PORT=8001
ENVIRONMENT=development
```

2. **Frontend Environment (.env)**
```bash
cd ../frontend
cp .env.example .env  # If available, or create new
```

Edit `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🏃‍♂️ Running the Application

### Development Mode

#### Method 1: Using Individual Commands

1. **Start MongoDB** (if not running as service)
```bash
# Start MongoDB
sudo systemctl start mongodb
# OR
mongod --dbpath /your/db/path
```

2. **Start Backend Server**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

3. **Start Frontend Development Server** (in new terminal)
```bash
cd frontend
npm start
# OR
yarn start
```

#### Method 2: Using Process Manager (Recommended for Production)

1. **Install Supervisor**
```bash
# Ubuntu/Debian
sudo apt install supervisor

# CentOS/RHEL
sudo yum install supervisor
```

2. **Configure Supervisor**
Create supervisor configuration files or use the existing ones:

```bash
# Copy supervisor configs (if available)
sudo cp scripts/supervisor/*.conf /etc/supervisor/conf.d/

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
```

3. **Start All Services**
```bash
sudo supervisorctl start all
```

### Production Deployment

#### Using Docker (Optional)

1. **Build and Run with Docker Compose**
```bash
# If docker-compose.yml exists
docker-compose up -d
```

#### Manual Production Setup

1. **Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx
```

Create Nginx config (`/etc/nginx/sites-available/smartworld`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/smartworld /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 📁 Project Structure

```
smartworld-employee-system/
├── backend/                    # FastAPI Backend
│   ├── server.py              # Main FastAPI application
│   ├── excel_parser.py        # Excel data processing
│   ├── attendance_parser.py   # Attendance data processing
│   ├── models.py              # Database models
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Backend environment variables
│   ├── employee_directory.xlsx # Employee data file
│   └── attendance_data.xlsx   # Attendance data file
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   ├── context/           # React context
│   │   └── App.js            # Main React app
│   ├── public/               # Static files
│   ├── package.json          # Node.js dependencies
│   └── .env                  # Frontend environment variables
├── scripts/                   # Utility scripts
├── supervisor/               # Supervisor configuration
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
