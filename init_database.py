#!/usr/bin/env python3
"""
Database initialization script for Productline 3D Data API
Creates all necessary tables and adds sample data.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.app import create_app
from src.database import db
from src.models.productline_object import ProductlineObject
from src.models.coordinates import Coordinates
from src.models.object_history import ObjectHistory
from datetime import datetime

def init_database():
    """Initialize database with tables and sample data."""
    
    print("Creating Flask application...")
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
        
        # Check if data already exists
        existing_objects = ProductlineObject.query.count()
        if existing_objects > 0:
            print(f"✅ Database already has {existing_objects} objects")
            return True
        
        print("Adding sample data...")
        
        # Create sample objects
        sample_objects = [
            {
                'id': 'OBJ_001',
                'name': 'Conveyor Belt A',
                'status': 'active',
                'metadata': {'type': 'conveyor', 'speed': 1.5, 'length': 10.0}
            },
            {
                'id': 'OBJ_002', 
                'name': 'Robot Arm B',
                'status': 'active',
                'metadata': {'type': 'robot', 'payload': 5.0, 'reach': 2.5}
            },
            {
                'id': 'OBJ_003',
                'name': 'Quality Station C',
                'status': 'processing',
                'metadata': {'type': 'station', 'capacity': 100, 'cycle_time': 30}
            }
        ]
        
        for obj_data in sample_objects:
            try:
                obj = ProductlineObject(
                    id=obj_data['id'],
                    name=obj_data['name'],
                    status=obj_data['status'],
                    metadata=obj_data['metadata']
                )
                db.session.add(obj)
                
                # Add coordinates for each object
                coords = Coordinates(
                    object_id=obj_data['id'],
                    position_x=float(sample_objects.index(obj_data) * 2.0),
                    position_y=0.0,
                    position_z=0.0,
                    height=1.0,
                    direction_x=1.0,
                    direction_y=0.0,
                    direction_z=0.0,
                    rotation=0.0
                )
                db.session.add(coords)
                
                print(f"✅ Created object {obj_data['id']}")
                
            except Exception as e:
                print(f"❌ Error creating object {obj_data['id']}: {e}")
        
        try:
            db.session.commit()
            print("✅ Sample data added successfully")
            return True
        except Exception as e:
            print(f"❌ Error committing data: {e}")
            db.session.rollback()
            return False

def test_database():
    """Test database connection and data retrieval."""
    
    print("\nTesting database connection...")
    app = create_app('development')
    
    with app.app_context():
        try:
            # Test basic query
            objects = ProductlineObject.query.all()
            print(f"✅ Found {len(objects)} objects in database")
            
            for obj in objects:
                print(f"  - {obj.id}: {obj.name} ({obj.status})")
                
                # Test coordinates
                coords = Coordinates.query.filter_by(object_id=obj.id).first()
                if coords:
                    print(f"    Coordinates: ({coords.position_x}, {coords.position_y}, {coords.position_z})")
                else:
                    print(f"    No coordinates found")
            
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == '__main__':
    print("=== Productline 3D Data API - Database Initialization ===")
    
    # Initialize database
    if init_database():
        print("\n=== Database Initialization Complete ===")
        
        # Test database
        if test_database():
            print("\n✅ Database initialization and testing successful!")
            print("You can now start the application with: python run.py")
        else:
            print("\n❌ Database testing failed")
            sys.exit(1)
    else:
        print("\n❌ Database initialization failed")
        sys.exit(1)
