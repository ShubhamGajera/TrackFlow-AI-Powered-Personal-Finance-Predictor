#!/usr/bin/env python3
"""
Database Schema Fix Script for TrackFlow
This script adds missing columns to the goals table
"""

from app import app, db
from sqlalchemy import text

def fix_database_schema():
    with app.app_context():
        try:
            print("🔧 Fixing database schema...")
            
            # Check if goals table exists and has required columns
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'goals'
            """))
            
            existing_columns = [row[0] for row in result]
            print(f"Current columns in goals table: {existing_columns}")
            
            # Add missing columns if they don't exist
            if 'name' not in existing_columns:
                print("➕ Adding 'name' column...")
                db.session.execute(text("ALTER TABLE goals ADD COLUMN name VARCHAR(100) DEFAULT 'Monthly Savings'"))
            
            if 'target_amount' not in existing_columns:
                print("➕ Adding 'target_amount' column...")
                db.session.execute(text("ALTER TABLE goals ADD COLUMN target_amount FLOAT DEFAULT 0.0"))
            
            if 'achieved' not in existing_columns:
                print("➕ Adding 'achieved' column...")
                db.session.execute(text("ALTER TABLE goals ADD COLUMN achieved FLOAT DEFAULT 0.0"))
            
            # Commit changes
            db.session.commit()
            print("✅ Database schema updated successfully!")
            
            # Verify the changes
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'goals'
                ORDER BY column_name
            """))
            
            updated_columns = [row[0] for row in result]
            print(f"Updated columns in goals table: {updated_columns}")
            
        except Exception as e:
            print(f"❌ Error fixing database schema: {e}")
            db.session.rollback()
            print("Rolling back changes...")

if __name__ == "__main__":
    print("🔧 TrackFlow Database Schema Fixer")
    print("=" * 40)
    fix_database_schema() 