from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_database_engine(config):
    """Create database engine with connection pooling."""
    
    # Get database configuration
    db_uri = config.get('SQLALCHEMY_DATABASE_URI')
    engine_options = config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
    
    # Create engine with connection pooling
    engine = create_engine(
        db_uri,
        poolclass=QueuePool,
        pool_size=engine_options.get('pool_size', 10),
        max_overflow=engine_options.get('max_overflow', 20),
        pool_recycle=engine_options.get('pool_recycle', 120),
        pool_pre_ping=engine_options.get('pool_pre_ping', True),
        echo=config.get('DEBUG', False)
    )
    
    return engine

def init_database(app):
    """Initialize database connection for Flask app."""
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Create engine for direct queries if needed
    app.database_engine = create_database_engine(app.config)
    
    # Create session factory
    app.session_factory = sessionmaker(bind=app.database_engine)
    
    return db

def get_db_session():
    """Get a database session."""
    from flask import current_app
    return current_app.session_factory()

def test_database_connection():
    """Test database connection."""
    try:
        from flask import current_app
        from sqlalchemy import text
        with current_app.database_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

def create_tables():
    """Create all database tables."""
    try:
        db.create_all()
        return True, "Tables created successfully"
    except Exception as e:
        return False, f"Failed to create tables: {str(e)}"

def drop_tables():
    """Drop all database tables."""
    try:
        db.drop_all()
        return True, "Tables dropped successfully"
    except Exception as e:
        return False, f"Failed to drop tables: {str(e)}"
