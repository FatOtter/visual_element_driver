import re
from datetime import datetime
from src.app_logging import get_logger

logger = get_logger(__name__)

def validate_object_id(object_id):
    """Validate object ID format."""
    if not object_id or not isinstance(object_id, str):
        return False
    
    # Check length (1-100 characters)
    if len(object_id) < 1 or len(object_id) > 100:
        return False
    
    # Check for valid characters (alphanumeric and underscore)
    if not re.match(r'^[a-zA-Z0-9_]+$', object_id):
        return False
    
    return True

def validate_timestamp(timestamp):
    """Validate timestamp format."""
    if not timestamp:
        return True  # Optional parameter
    
    try:
        # Try to parse ISO 8601 format
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        try:
            # Try to parse Unix timestamp
            datetime.fromtimestamp(float(timestamp))
            return True
        except (ValueError, TypeError):
            return False

def validate_batch_request(data):
    """Validate batch request data."""
    if not isinstance(data, dict):
        return False
    
    # Check for required object_ids
    if 'object_ids' not in data:
        return False
    
    object_ids = data.get('object_ids', [])
    if not isinstance(object_ids, list):
        return False
    
    # Check array size (max 50 objects)
    if len(object_ids) > 50:
        return False
    
    # Validate each object ID
    for object_id in object_ids:
        if not validate_object_id(object_id):
            return False
    
    # Validate optional timestamp
    if 'timestamp' in data:
        if not validate_timestamp(data['timestamp']):
            return False
    
    return True

def validate_coordinates(coords):
    """Validate coordinate data."""
    if not isinstance(coords, dict):
        return False
    
    required_fields = ['position', 'height', 'direction', 'rotation']
    for field in required_fields:
        if field not in coords:
            return False
    
    # Validate position
    position = coords.get('position', {})
    if not isinstance(position, dict):
        return False
    
    for axis in ['x', 'y', 'z']:
        if axis not in position or not isinstance(position[axis], (int, float)):
            return False
    
    # Validate height
    height = coords.get('height')
    if not isinstance(height, (int, float)) or height < 0:
        return False
    
    # Validate direction
    direction = coords.get('direction', {})
    if not isinstance(direction, dict):
        return False
    
    for axis in ['x', 'y', 'z']:
        if axis not in direction or not isinstance(direction[axis], (int, float)):
            return False
    
    # Validate rotation
    rotation = coords.get('rotation')
    if not isinstance(rotation, (int, float)) or rotation < 0 or rotation > 360:
        return False
    
    return True
