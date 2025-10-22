import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    
    # Database configuration - using MySQL as specified
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'test_admin')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '1qaz2wsxE')
    DB_NAME = os.environ.get('DB_NAME', 'productline_3d')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
    
    # Server configuration
    PORT = int(os.environ.get('PORT', 5566))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # CORS configuration
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']
    CORS_HEADERS = ['Content-Type', 'Authorization']
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'logs/app.log'
    
    # API configuration
    API_VERSION = 'v1'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
