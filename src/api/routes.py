from flask import Blueprint, request, jsonify, current_app
from src.services.data_service import DataService
from src.services.history_service import HistoryService
from src.services.batch_service import BatchService
from src.api.validation import validate_object_id, validate_timestamp, validate_batch_request
from src.app_logging import get_logger

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
logger = get_logger(__name__)

@api_bp.route('/objects/<object_id>', methods=['GET'])
def get_object(object_id):
    """Get object data by ID with optional timestamp."""
    try:
        # Validate object ID
        if not validate_object_id(object_id):
            return jsonify({
                'error': 'Invalid object ID format',
                'code': 'INVALID_OBJECT_ID',
                'message': 'Object ID must be 1-100 characters'
            }), 400
        
        # Get timestamp parameter
        timestamp = request.args.get('timestamp')
        if timestamp and not validate_timestamp(timestamp):
            return jsonify({
                'error': 'Invalid timestamp format',
                'code': 'INVALID_TIMESTAMP',
                'message': 'Timestamp must be valid ISO 8601 format'
            }), 400
        
        # Get object data
        if timestamp:
            data_service = HistoryService()
            result = data_service.get_object_at_timestamp(object_id, timestamp)
        else:
            data_service = DataService()
            result = data_service.get_object(object_id)
        
        if result is None:
            return jsonify({
                'error': 'Object not found',
                'code': 'OBJECT_NOT_FOUND',
                'message': f'Object with ID \'{object_id}\' does not exist'
            }), 404
        
        logger.info(f"Retrieved object {object_id}", object_id=object_id, timestamp=timestamp)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error retrieving object {object_id}", error=str(e), object_id=object_id)
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500

@api_bp.route('/objects/batch', methods=['POST'])
def get_objects_batch():
    """Get multiple objects in a single request."""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'code': 'INVALID_CONTENT_TYPE'
            }), 400
        
        data = request.get_json()
        if not validate_batch_request(data):
            return jsonify({
                'error': 'Invalid batch request',
                'code': 'INVALID_BATCH_REQUEST',
                'message': 'Request must contain object_ids array'
            }), 400
        
        # Get objects
        batch_service = BatchService()
        result = batch_service.get_objects_batch(
            data.get('object_ids', []),
            data.get('timestamp')
        )
        
        logger.info(f"Batch request processed", 
                   object_count=len(data.get('object_ids', [])),
                   timestamp=data.get('timestamp'))
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing batch request", error=str(e))
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        from src.database import test_database_connection
        
        # Test database connection
        db_ok, db_message = test_database_connection()
        
        status = 'healthy' if db_ok else 'unhealthy'
        
        return jsonify({
            'status': status,
            'timestamp': current_app.config.get('TIMESTAMP', ''),
            'version': '1.0.0',
            'database': {
                'status': 'connected' if db_ok else 'disconnected',
                'message': db_message
            }
        }), 200 if db_ok else 503
        
    except Exception as e:
        logger.error(f"Health check failed", error=str(e))
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
