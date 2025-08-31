#!/usr/bin/env python3
"""
TrackFlow User Checker
Lists all users in the database
"""

import os
import sys
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

def list_users(engine):
    """List all users in the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, username, email, role, created_at
                FROM users
                ORDER BY id
            """))
            
            users = result.fetchall()
            
            if not users:
                print("No users found in the database.")
                return
            
            print(f"Found {len(users)} user(s) in the database:")
            print("-" * 80)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<10} {'Created'}")
            print("-" * 80)
            
            admin_count = 0
            for user in users:
                user_id, username, email, role, created_at = user
                print(f"{user_id:<5} {username:<20} {email:<30} {role:<10} {created_at}")
                if role == 'admin':
                    admin_count += 1
            
            print("-" * 80)
            print(f"Total users: {len(users)}")
            print(f"Admin users: {admin_count}")
            print(f"Regular users: {len(users) - admin_count}")
            
            if admin_count == 0:
                print("\nWARNING: No admin users found!")
                print("Run 'python create_admin.py' to create an admin user.")
            
            return True
            
    except Exception as e:
        print(f"Error listing users: {e}")
        return False

def main():
    """Main function"""
    print("TrackFlow User Checker")
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
        
        # List users
        if list_users(engine):
            print("\nUser check completed successfully!")
        else:
            print("Failed to list users.")
            sys.exit(1)
            
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 