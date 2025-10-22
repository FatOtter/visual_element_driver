from src.services.data_service import DataService
from src.services.history_service import HistoryService
from src.app_logging import get_logger

logger = get_logger(__name__)

class BatchService:
    """Service for batch object data retrieval."""
    
    def get_objects_batch(self, object_ids, timestamp=None):
        """Get multiple objects in a single request."""
        try:
            objects = []
            errors = []
            
            for object_id in object_ids:
                try:
                    if timestamp:
                        # Get historical data
                        history_service = HistoryService()
                        obj_data = history_service.get_object_at_timestamp(object_id, timestamp)
                    else:
                        # Get current data
                        data_service = DataService()
                        obj_data = data_service.get_object(object_id)
                    
                    if obj_data:
                        objects.append(obj_data)
                    else:
                        errors.append({
                            'object_id': object_id,
                            'error': 'Object not found',
                            'code': 'OBJECT_NOT_FOUND'
                        })
                        
                except Exception as e:
                    logger.warning(f"Error retrieving object {object_id}: {str(e)}")
                    errors.append({
                        'object_id': object_id,
                        'error': str(e),
                        'code': 'RETRIEVAL_ERROR'
                    })
            
            response = {
                'objects': objects,
                'errors': errors
            }
            
            logger.info(f"Batch request processed: {len(objects)} objects, {len(errors)} errors")
            return response
            
        except Exception as e:
            logger.error(f"Error processing batch request: {str(e)}")
            raise
