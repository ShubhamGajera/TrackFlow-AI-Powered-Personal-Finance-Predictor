#!/usr/bin/env python3
"""
Script to check current users in TrackFlow database
"""

from app import app, db
from models import User

def check_users():
    with app.app_context():
        try:
            users = User.query.all()
            print("👥 Current Users in Database:")
            print("=" * 50)
            
            if not users:
                print("No users found in database.")
                return
            
            for user in users:
                status = "🟢 Active" if user.role == 'admin' else "🔵 User"
                print(f"{status} | {user.username} | {user.email} | Role: {user.role}")
            
            print(f"\nTotal users: {len(users)}")
            
            # Check for admin users
            admin_users = [u for u in users if u.role == 'admin']
            if admin_users:
                print(f"✅ Admin users: {len(admin_users)}")
            else:
                print("❌ No admin users found!")
                print("Run 'python create_admin.py' to create an admin user.")
                
        except Exception as e:
            print(f"❌ Error checking users: {e}")

if __name__ == "__main__":
    check_users() 