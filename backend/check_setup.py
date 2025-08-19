#!/usr/bin/env python3
"""
Setup checker script - verifies all dependencies and file paths
Usage: python check_setup.py
"""
import os
import sys
from pathlib import Path
import importlib

def check_imports():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pymongo', 'motor', 'pandas', 'openpyxl', 
        'et_xmlfile', 'python-dotenv', 'pydantic', 'python-multipart'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Handle different import names
            import_name = package
            if package == 'python-dotenv':
                import_name = 'dotenv'
            elif package == 'python-multipart':
                import_name = 'multipart'
            
            importlib.import_module(import_name)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def check_files():
    """Check if required files exist"""
    current_dir = Path(__file__).parent
    app_dir = current_dir.parent
    
    required_files = [
        ('Excel file (backend)', current_dir / 'employee_directory.xlsx'),
        ('Excel file (app root)', app_dir / 'employee_directory.xlsx'),
        ('Environment file', current_dir / '.env'),
        ('Server file', current_dir / 'server.py'),
        ('Models file', current_dir / 'models.py'),
        ('Excel parser', current_dir / 'excel_parser.py'),
        ('Requirements', current_dir / 'requirements.txt')
    ]
    
    missing_files = []
    
    for name, filepath in required_files:
        if filepath.exists():
            print(f"✓ {name}: {filepath}")
        else:
            print(f"✗ {name}: {filepath} - MISSING")
            missing_files.append((name, filepath))
    
    return missing_files

def check_mongodb():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        
        print(f"Attempting to connect to MongoDB: {mongo_url}")
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ismaster')
        print("✓ MongoDB connection successful")
        
        # Check database
        db_name = os.environ.get('DB_NAME', 'test_database')
        db = client[db_name]
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✓ Database '{db_name}' accessible, collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("  Make sure MongoDB is installed and running on your system")
        print("  Install MongoDB Community: https://docs.mongodb.com/manual/installation/")
        return False

def check_directories():
    """Check and create necessary directories"""
    current_dir = Path(__file__).parent
    
    directories = [
        current_dir / 'uploads',
        current_dir / 'uploads' / 'images'
    ]
    
    for directory in directories:
        if directory.exists():
            print(f"✓ Directory exists: {directory}")
        else:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created directory: {directory}")
            except Exception as e:
                print(f"✗ Failed to create directory {directory}: {e}")

def main():
    """Main setup checker"""
    print("=" * 60)
    print("Employee Directory Application Setup Checker")
    print("=" * 60)
    
    print("\n1. Checking Python packages:")
    missing_packages = check_imports()
    
    print("\n2. Checking required files:")
    missing_files = check_files()
    
    print("\n3. Checking directories:")
    check_directories()
    
    print("\n4. Checking MongoDB connection:")
    mongodb_ok = check_mongodb()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    
    if missing_packages:
        print(f"✗ Missing packages: {', '.join(missing_packages)}")
        print("  Run: pip install -r requirements.txt")
    
    if missing_files:
        print("✗ Missing files:")
        for name, filepath in missing_files:
            print(f"  - {name}: {filepath}")
    
    if not mongodb_ok:
        print("✗ MongoDB not accessible")
        print("  Install and start MongoDB service")
    
    if not missing_packages and not missing_files and mongodb_ok:
        print("✓ All checks passed! Application should work correctly.")
        print("\nTo run the application:")
        print("1. Backend: uvicorn server:app --reload --host 0.0.0.0 --port 8001")
        print("2. Frontend: npm start (in frontend directory)")
    else:
        print("✗ Some issues found. Please fix them before running the application.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()