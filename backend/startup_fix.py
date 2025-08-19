#!/usr/bin/env python3
"""
Startup fix script - modifies server.py to always load Excel data in development mode
Usage: python startup_fix.py
"""
import os
import re
from pathlib import Path

def fix_startup_behavior():
    """Modify server.py to always reload Excel data in development"""
    
    server_file = Path(__file__).parent / 'server.py'
    
    if not server_file.exists():
        print(f"Error: server.py not found at {server_file}")
        return False
    
    # Read current content
    with open(server_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the startup logic
    old_pattern = r'if count == 0:\s*logger\.info\("Database empty, loading Excel data\.\.\."\)'
    new_pattern = '''# Force reload in development mode
        force_reload = os.environ.get('FORCE_EXCEL_RELOAD', 'false').lower() == 'true'
        
        if count == 0 or force_reload:
            if force_reload:
                logger.info("Force reload enabled, clearing and reloading Excel data...")
                await db.employees.delete_many({})
                await db.attendance.delete_many({})
            else:
                logger.info("Database empty, loading Excel data...")'''
    
    # Replace the pattern
    new_content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE | re.DOTALL)
    
    # Also update the skip message
    skip_pattern = r'logger\.info\(f"Database already has {count} employees, skipping Excel load"\)'
    new_skip = '''if not force_reload:
                logger.info(f"Database already has {count} employees, skipping Excel load (set FORCE_EXCEL_RELOAD=true to override)")
            else:
                logger.info("Force reload disabled, keeping existing data")'''
    
    new_content = re.sub(skip_pattern, new_skip, new_content)
    
    # Write back the modified content
    try:
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✓ Successfully updated server.py startup behavior")
        print("✓ Set FORCE_EXCEL_RELOAD=true in .env to always reload Excel data")
        return True
        
    except Exception as e:
        print(f"✗ Error writing to server.py: {e}")
        return False

def update_env_file():
    """Add force reload option to .env file"""
    env_file = Path(__file__).parent / '.env'
    
    # Read existing .env or create new
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Add force reload option if not present
    if 'FORCE_EXCEL_RELOAD' not in env_content:
        env_content += '\n# Force reload Excel data on startup (for development)\nFORCE_EXCEL_RELOAD=true\n'
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✓ Added FORCE_EXCEL_RELOAD=true to .env file")
    else:
        print("✓ FORCE_EXCEL_RELOAD already exists in .env file")

if __name__ == "__main__":
    print("Fixing startup behavior for development...")
    
    if fix_startup_behavior():
        update_env_file()
        print("\nSetup completed! The server will now:")
        print("- Always reload Excel data when FORCE_EXCEL_RELOAD=true in .env")
        print("- Skip reload when FORCE_EXCEL_RELOAD=false or not set")
        print("\nRestart your server to apply changes.")
    else:
        print("\nFailed to update startup behavior. Please check the file manually.")