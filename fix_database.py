#!/usr/bin/env python3
"""
TrackFlow Database Schema Fixer
Fixes missing columns in the goals table
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

def fix_database_schema():
    """Fix missing columns in the goals table"""
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
        
        # Check if goals table exists
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'goals'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                print("Goals table does not exist. Creating it...")
                conn.execute(text("""
                    CREATE TABLE goals (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER UNIQUE,
                        name VARCHAR(100) DEFAULT 'Monthly Savings',
                        target_amount FLOAT DEFAULT 0.0,
                        achieved FLOAT DEFAULT 0.0,
                        monthly_savings_target FLOAT DEFAULT 0.0
                    );
                """))
                conn.commit()
                print("Goals table created successfully!")
                return True
        
        # Check for missing columns
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'goals';
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            print("Existing columns:", existing_columns)
            
            # Add missing columns
            if 'name' not in existing_columns:
                print("Adding 'name' column...")
                conn.execute(text("ALTER TABLE goals ADD COLUMN name VARCHAR(100) DEFAULT 'Monthly Savings'"))
            
            if 'target_amount' not in existing_columns:
                print("Adding 'target_amount' column...")
                conn.execute(text("ALTER TABLE goals ADD COLUMN target_amount FLOAT DEFAULT 0.0"))
            
            if 'achieved' not in existing_columns:
                print("Adding 'achieved' column...")
                conn.execute(text("ALTER TABLE goals ADD COLUMN achieved FLOAT DEFAULT 0.0"))
            
            conn.commit()
            print("All missing columns added successfully!")
            
            # Verify the fix
            result = conn.execute(text("SELECT * FROM goals LIMIT 1"))
            print("Schema verification successful!")
            
            return True
            
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("TrackFlow Database Schema Fixer")
    print("=" * 50)
    
    success = fix_database_schema()
    
    if success:
        print("Database schema fixed successfully!")
    else:
        print("Failed to fix database schema. Please check the errors above.")
        sys.exit(1) 