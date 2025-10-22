from flask import jsonify, request
from src.app_logging import get_logger
import traceback

logger = get_logger(__name__)

def register_error_handlers(app):
    """Register error handlers for the Flask application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        logger.warning(f"Bad request: {error.description}", 
                      path=request.path, method=request.method)
        return jsonify({
            'error': 'Bad Request',
            'code': 'BAD_REQUEST',
            'message': error.description or 'Invalid request format'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        logger.warning(f"Not found: {error.description}", 
                      path=request.path, method=request.method)
        return jsonify({
            'error': 'Not Found',
            'code': 'NOT_FOUND',
            'message': error.description or 'Resource not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        logger.warning(f"Method not allowed: {error.description}", 
                      path=request.path, method=request.method)
        return jsonify({
            'error': 'Method Not Allowed',
            'code': 'METHOD_NOT_ALLOWED',
            'message': f'Method {request.method} not allowed for this endpoint'
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        logger.error(f"Internal server error: {error.description}", 
                    path=request.path, method=request.method,
                    error=str(error), traceback=traceback.format_exc())
        return jsonify({
            'error': 'Internal Server Error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(error)}", 
                    path=request.path, method=request.method,
                    error=str(error), traceback=traceback.format_exc())
        return jsonify({
            'error': 'Internal Server Error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.before_request
    def log_request():
        """Log incoming requests."""
        logger.info(f"Request received", 
                   method=request.method, path=request.path,
                   remote_addr=request.remote_addr)
    
    @app.after_request
    def log_response(response):
        """Log outgoing responses."""
        logger.info(f"Response sent", 
                   method=request.method, path=request.path,
                   status_code=response.status_code)
        return response
