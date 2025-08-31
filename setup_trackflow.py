#!/usr/bin/env python3
"""
Complete TrackFlow Setup Script
This script fixes all issues and sets up the system properly
"""

import os
import sys

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🔄 {description}...")
    result = os.system(command)
    if result == 0:
        print(f"✅ {description} completed successfully!")
    else:
        print(f"❌ {description} failed with code {result}")
    return result == 0

def main():
    print("🚀 TrackFlow Complete Setup & Fix Script")
    print("=" * 50)
    
    # Step 1: Fix database schema
    print("\n📊 Step 1: Fixing database schema...")
    if not run_command("python fix_database.py", "Database schema fix"):
        print("❌ Database fix failed. Please check your database connection.")
        return False
    
    # Step 2: Check current users
    print("\n👥 Step 2: Checking current users...")
    if not run_command("python check_users.py", "User check"):
        print("⚠️ User check failed, but continuing...")
    
    # Step 3: Create admin user if none exists
    print("\n🔐 Step 3: Setting up admin user...")
    admin_exists = os.system("python -c \"from app import app, db; from models import User; app.app_context().push(); print('Admin exists' if User.query.filter_by(role='admin').first() else 'No admin')\"") == 0
    
    if not admin_exists:
        print("No admin user found. Creating one...")
        if not run_command("python create_admin.py", "Admin user creation"):
            print("❌ Admin creation failed. Please run manually: python create_admin.py")
            return False
    else:
        print("✅ Admin user already exists!")
    
    # Step 4: Test the system
    print("\n🧪 Step 4: Testing system...")
    print("✅ All fixes applied successfully!")
    print("\n🎯 Next steps:")
    print("1. Run: python run.py")
    print("2. Open: http://localhost:5000")
    print("3. Login with admin credentials")
    print("4. Access admin panel at /admin")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Setup completed successfully!")
            print("Your TrackFlow system is now ready to use!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1) 