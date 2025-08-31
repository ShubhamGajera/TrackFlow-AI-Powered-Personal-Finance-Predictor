#!/usr/bin/env python3
"""
TrackFlow Admin User Creator
Creates an admin user for the TrackFlow application
"""

import os
import sys
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_database_url():
    """Get database URL from environment or config"""
    # Try to get from environment
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        return db_url
    
    # Fallback to config
    try:
        from config import Config
        return Config.SQLALCHEMY_DATABASE_URI
    except ImportError:
        pass
    
    # Final fallback
    return "postgresql://postgres:password@localhost:5432/trackflow"

def check_admin_exists(engine):
    """Check if admin user already exists"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'"))
            count = result.scalar()
            return count > 0
    except Exception as e:
        print(f"Error checking admin existence: {e}")
        return False

def create_admin_user(engine):
    """Create admin user"""
    try:
        print("Creating admin user...")
        
        # Get admin details
        username = input("Enter admin username (default: admin): ").strip() or "admin"
        email = input("Enter admin email (default: admin@trackflow.com): ").strip() or "admin@trackflow.com"
        password = input("Enter admin password (default: admin123): ").strip() or "admin123"
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Check if user already exists
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM users WHERE username = :username"), {"username": username})
            existing_user = result.fetchone()
            
            if existing_user:
                print(f"User '{username}' already exists. Updating to admin role...")
                conn.execute(text("UPDATE users SET role = 'admin' WHERE username = :username"), {"username": username})
                conn.commit()
                print(f"User '{username}' is now an admin!")
                return True
            
            # Create new admin user
            conn.execute(text("""
                INSERT INTO users (username, email, password_hash, role, created_at)
                VALUES (:username, :email, :password_hash, 'admin', CURRENT_DATE)
            """), {
                "username": username,
                "email": email,
                "password_hash": password_hash
            })
            conn.commit()
            
            print(f"Admin user '{username}' created successfully!")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print(f"Role: admin")
            
            return True
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

def main():
    """Main function"""
    print("TrackFlow Admin User Creator")
    print("=" * 50)
    
    try:
        # Get database URL
        db_url = get_database_url()
        print("Database URL:", db_url)
        
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
        
        # Check if admin exists
        if check_admin_exists(engine):
            print("Admin user already exists!")
            return
        
        # Create admin user
        if create_admin_user(engine):
            print("Admin user setup completed successfully!")
        else:
            print("Failed to create admin user.")
            sys.exit(1)
            
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 