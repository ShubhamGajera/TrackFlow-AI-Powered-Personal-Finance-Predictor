#!/usr/bin/env python3
"""
Simple script to create an admin user for TrackFlow
Run this script to create an admin user in your database
"""

from app import app, db
from models import User

def create_admin_user():
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(role='admin').first()
        if admin_user:
            print(f"Admin user already exists: {admin_user.username} ({admin_user.email})")
            return
        
        # Create admin user
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
        
        # Validate input
        if not username or not email or not password:
            print("All fields are required!")
            return
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print(f"User with username '{username}' or email '{email}' already exists!")
            return
        
        # Create admin user
        admin_user = User(username=username, email=email, role='admin')
        admin_user.set_password(password)
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Admin user '{username}' created successfully!")
            print(f"   Email: {email}")
            print(f"   Role: {admin_user.role}")
            print("\nYou can now login with these credentials.")
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("🔐 TrackFlow Admin User Creator")
    print("=" * 40)
    create_admin_user() 