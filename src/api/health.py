from flask import Blueprint, jsonify, current_app
from src.database import test_database_connection
from src.app_logging import get_logger
import time
import psutil
import os

# Create health check blueprint
health_bp = Blueprint('health', __name__)
logger = get_logger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint."""
    try:
        start_time = time.time()
        
        # Test database connection
        db_success, db_message = test_database_connection()
        
        # Get system information
        system_info = get_system_info()
        
        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Determine overall health status
        overall_status = 'healthy' if db_success else 'unhealthy'
        
        health_data = {
            'status': overall_status,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'version': '1.0.0',
            'service': 'Productline 3D Data Retrieval API',
            'response_time_ms': round(response_time, 2),
            'database': {
                'status': 'connected' if db_success else 'disconnected',
                'message': db_message
            },
            'system': system_info
        }
        
        # Log health check
        logger.info(f"Health check completed", 
                   status=overall_status, 
                   response_time_ms=response_time,
                   db_status='connected' if db_success else 'disconnected')
        
        # Return appropriate status code
        status_code = 200 if overall_status == 'healthy' else 503
        return jsonify(health_data), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'error': str(e)
        }), 503

@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check for Kubernetes/Docker."""
    try:
        # Test database connection
        db_success, db_message = test_database_connection()
        
        if db_success:
            return jsonify({'status': 'ready'}), 200
        else:
            return jsonify({
                'status': 'not ready',
                'message': db_message
            }), 503
            
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return jsonify({
            'status': 'not ready',
            'error': str(e)
        }), 503

@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Liveness check for Kubernetes/Docker."""
    try:
        # Simple liveness check - just return OK if the service is running
        return jsonify({'status': 'alive'}), 200
        
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        return jsonify({
            'status': 'not alive',
            'error': str(e)
        }), 503

def get_system_info():
    """Get system information for health check."""
    try:
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'uptime_seconds': time.time() - psutil.boot_time(),
            'python_version': os.sys.version,
            'process_id': os.getpid()
        }
    except Exception as e:
        logger.warning(f"Failed to get system info: {str(e)}")
        return {
            'error': 'Unable to retrieve system information'
        }
