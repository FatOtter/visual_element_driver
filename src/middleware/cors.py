from flask_cors import CORS
from src.app_logging import get_logger

logger = get_logger(__name__)

def init_cors(app):
    """Initialize CORS for the Flask application."""
    
    # Get CORS configuration from app config
    cors_origins = app.config.get('CORS_ORIGINS', ['*'])
    cors_methods = app.config.get('CORS_METHODS', ['GET', 'POST', 'OPTIONS'])
    cors_headers = app.config.get('CORS_HEADERS', ['Content-Type', 'Authorization'])
    
    # Configure CORS
    CORS(app, 
         origins=cors_origins,
         methods=cors_methods,
         allow_headers=cors_headers,
         supports_credentials=True)
    
    logger.info("CORS configured", 
               origins=cors_origins, 
               methods=cors_methods, 
               headers=cors_headers)
    
    # Add custom CORS headers for Unreal Engine
    @app.after_request
    def after_request(response):
        """Add custom headers for Unreal Engine integration."""
        
        # Add custom headers for Unreal Engine
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
        
        # Add custom headers for API versioning
        response.headers['X-API-Version'] = app.config.get('API_VERSION', 'v1')
        response.headers['X-Service'] = 'Productline-3D-Data-API'
        
        return response
    
    logger.info("Custom CORS headers configured for Unreal Engine integration")
