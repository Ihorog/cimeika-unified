#!/usr/bin/env python3
"""
Database initialization script
Creates all tables in the database
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config.database import init_db, engine, Base
from app.config.canon import CANON_BUNDLE_ID


def main():
    """Initialize database tables"""
    print("=" * 60)
    print("CIMEIKA Database Initialization")
    print("=" * 60)
    print(f"Canon Bundle ID: {CANON_BUNDLE_ID}")
    print(f"Database URL: {engine.url}")
    print()
    
    try:
        # Initialize database
        print("Creating database tables...")
        init_db()
        print("✓ Database tables created successfully!")
        print()
        
        # List all tables
        print("Created tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
        print()
        print("=" * 60)
        print("Database initialization completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
