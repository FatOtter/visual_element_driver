"""
Database indexes configuration for performance optimization.
This module defines database indexes to improve query performance.
"""

from src.database import db
from sqlalchemy import Index, text

def create_indexes():
    """Create all database indexes for performance optimization."""
    
    try:
        # Create indexes for ProductlineObject table
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_objects_status 
            ON productline_objects(status)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_objects_updated_at 
            ON productline_objects(updated_at)
        """))
        
        # Create indexes for Coordinates table
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_coordinates_position 
            ON coordinates(position_x, position_y, position_z)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_coordinates_updated_at 
            ON coordinates(updated_at)
        """))
        
        # Create indexes for ObjectHistory table
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_history_object_timestamp 
            ON object_history(object_id, timestamp)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_history_timestamp 
            ON object_history(timestamp)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_history_object_id 
            ON object_history(object_id)
        """))
        
        # Create composite indexes for common queries
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_objects_status_updated 
            ON productline_objects(status, updated_at)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_history_object_status_timestamp 
            ON object_history(object_id, status, timestamp)
        """))
        
        db.session.commit()
        return True, "Database indexes created successfully"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Failed to create indexes: {str(e)}"

def drop_indexes():
    """Drop all database indexes."""
    
    try:
        # Drop indexes for ProductlineObject table
        db.session.execute(text("DROP INDEX IF EXISTS idx_objects_status"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_objects_updated_at"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_objects_status_updated"))
        
        # Drop indexes for Coordinates table
        db.session.execute(text("DROP INDEX IF EXISTS idx_coordinates_position"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_coordinates_updated_at"))
        
        # Drop indexes for ObjectHistory table
        db.session.execute(text("DROP INDEX IF EXISTS idx_history_object_timestamp"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_history_timestamp"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_history_object_id"))
        db.session.execute(text("DROP INDEX IF EXISTS idx_history_object_status_timestamp"))
        
        db.session.commit()
        return True, "Database indexes dropped successfully"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Failed to drop indexes: {str(e)}"

def analyze_query_performance():
    """Analyze query performance and suggest optimizations."""
    
    try:
        # Analyze table statistics
        tables = ['productline_objects', 'coordinates', 'object_history']
        results = {}
        
        for table in tables:
            # Get table statistics
            result = db.session.execute(text(f"""
                SELECT 
                    table_name,
                    table_rows,
                    avg_row_length,
                    data_length,
                    index_length
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = '{table}'
            """)).fetchone()
            
            if result:
                results[table] = {
                    'rows': result[1],
                    'avg_row_length': result[2],
                    'data_length': result[3],
                    'index_length': result[4]
                }
        
        return True, results
        
    except Exception as e:
        return False, f"Failed to analyze performance: {str(e)}"
