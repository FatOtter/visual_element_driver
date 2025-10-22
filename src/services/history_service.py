from src.models.productline_object import ProductlineObject
from src.models.object_history import ObjectHistory
from src.app_logging import get_logger
from datetime import datetime

logger = get_logger(__name__)

class HistoryService:
    """Service for retrieving historical object data."""
    
    def get_object_at_timestamp(self, object_id, timestamp):
        """Get object data at specific timestamp."""
        try:
            # Parse timestamp
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            # Get object
            obj = ProductlineObject.find_by_id(object_id)
            if not obj:
                logger.warning(f"Object not found: {object_id}")
                return None
            
            # Get historical data
            history = ObjectHistory.find_by_object_before_timestamp(object_id, timestamp)
            
            if history:
                # Build response from historical data
                response = {
                    'object_id': obj.id,
                    'name': obj.name,
                    'status': history.status or obj.status,
                    'metadata': history.metadata or obj.metadata,
                    'created_at': obj.created_at.isoformat() + 'Z',
                    'updated_at': history.timestamp.isoformat() + 'Z',
                    'coordinates': {
                        'position': {
                            'x': history.position_x,
                            'y': history.position_y,
                            'z': history.position_z
                        },
                        'height': history.height,
                        'direction': {
                            'x': history.direction_x,
                            'y': history.direction_y,
                            'z': history.direction_z
                        },
                        'rotation': history.rotation
                    }
                }
            else:
                # No historical data, return current data
                from src.services.data_service import DataService
                data_service = DataService()
                response = data_service.get_object(object_id)
                if response:
                    response['timestamp'] = timestamp.isoformat() + 'Z'
            
            logger.info(f"Retrieved historical data for {object_id} at {timestamp}")
            return response
            
        except Exception as e:
            logger.error(f"Error retrieving historical data for {object_id}: {str(e)}")
            raise
