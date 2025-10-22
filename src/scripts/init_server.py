#!/usr/bin/env python3
"""
Server initialization script for Productline 3D Data Retrieval API.
This script performs comprehensive server setup including dependency checking,
database configuration, and health monitoring.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import test_database_connection, create_tables
from src.app_logging import get_logger

logger = get_logger(__name__)

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        logger.error(f"Python 3.8+ required, found {sys.version}")
        return False, f"Python 3.8+ required, found {sys.version}"
    
    logger.info(f"Python version check passed: {sys.version}")
    return True, f"Python version: {sys.version}"

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'flask', 'flask_cors', 'flask_sqlalchemy', 'pymysql',
        'pytest', 'python_dotenv', 'structlog'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"Package {package} found")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"Package {package} not found")
    
    if missing_packages:
        return False, f"Missing packages: {', '.join(missing_packages)}"
    
    logger.info("All required dependencies found")
    return True, "All dependencies satisfied"

def check_database_connection():
    """Test database connection."""
    try:
        success, message = test_database_connection()
        if success:
            logger.info("Database connection successful")
            return True, message
        else:
            logger.error(f"Database connection failed: {message}")
            return False, message
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False, f"Database connection test failed: {str(e)}"

def setup_database():
    """Setup database tables."""
    try:
        success, message = create_tables()
        if success:
            logger.info("Database tables created successfully")
            return True, message
        else:
            logger.error(f"Failed to create database tables: {message}")
            return False, message
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        return False, f"Database setup failed: {str(e)}"

def check_port_availability():
    """Check if port 5566 is available."""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 5566))
            logger.info("Port 5566 is available")
            return True, "Port 5566 is available"
    except OSError:
        logger.warning("Port 5566 is already in use")
        return False, "Port 5566 is already in use"

def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'data', 'tests/contract', 'tests/integration', 'tests/unit']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created/verified: {directory}")
    
    return True, "Directories created successfully"

def main():
    """Main initialization function."""
    logger.info("Starting server initialization...")
    
    # Check Python version
    success, message = check_python_version()
    if not success:
        logger.error(f"Python version check failed: {message}")
        return False
    
    # Check dependencies
    success, message = check_dependencies()
    if not success:
        logger.error(f"Dependency check failed: {message}")
        logger.info("Run: pip install -r requirements.txt")
        return False
    
    # Create directories
    success, message = create_directories()
    if not success:
        logger.error(f"Directory creation failed: {message}")
        return False
    
    # Check database connection
    success, message = check_database_connection()
    if not success:
        logger.error(f"Database connection failed: {message}")
        logger.info("Please ensure MySQL is running and accessible")
        return False
    
    # Setup database
    success, message = setup_database()
    if not success:
        logger.error(f"Database setup failed: {message}")
        return False
    
    # Check port availability
    success, message = check_port_availability()
    if not success:
        logger.warning(f"Port check failed: {message}")
        logger.info("You may need to stop other services using port 5566")
    
    logger.info("Server initialization completed successfully!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
