from src.models.productline_object import ProductlineObject
from src.models.coordinates import Coordinates
from src.app_logging import get_logger

logger = get_logger(__name__)

class DataService:
    """Service for retrieving object data."""
    
    def get_object(self, object_id):
        """Get complete object data by ID."""
        try:
            # Get object
            obj = ProductlineObject.find_by_id(object_id)
            if not obj:
                logger.warning(f"Object not found: {object_id}")
                return None
            
            # Get coordinates
            coords = Coordinates.find_by_object_id(object_id)
            
            # Build response
            response = obj.to_dict()
            if coords:
                response['coordinates'] = coords.to_dict()
            else:
                # Return default coordinates if none exist
                response['coordinates'] = {
                    'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                    'height': 0.0,
                    'direction': {'x': 1.0, 'y': 0.0, 'z': 0.0},
                    'rotation': 0.0
                }
            
            logger.info(f"Retrieved object data for {object_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error retrieving object {object_id}: {str(e)}")
            raise
