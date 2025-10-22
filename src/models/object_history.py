from src.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum, Index
from sqlalchemy.orm import relationship

class ObjectHistory(db.Model):
    """ObjectHistory model representing historical state of an object at specific timestamps."""
    
    __tablename__ = 'object_history'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to ProductlineObject
    object_id = Column(String(100), ForeignKey('productline_objects.id', ondelete='CASCADE'), 
                       nullable=False)
    
    # Timestamp for this historical record
    timestamp = Column(DateTime, nullable=False)
    
    # Historical position coordinates
    position_x = Column(Float, nullable=True)
    position_y = Column(Float, nullable=True)
    position_z = Column(Float, nullable=True)
    
    # Historical object dimensions
    height = Column(Float, nullable=True)
    
    # Historical direction vector
    direction_x = Column(Float, nullable=True)
    direction_y = Column(Float, nullable=True)
    direction_z = Column(Float, nullable=True)
    
    # Historical rotation angle
    rotation = Column(Float, nullable=True)
    
    # Historical status
    status = Column(Enum('active', 'inactive', 'processing', 'error', name='history_status_enum'), 
                     nullable=True)
    
    # Historical metadata snapshot
    object_metadata = Column(JSON, nullable=True)
    
    # Record creation timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    object = relationship("ProductlineObject", back_populates="history")
    
    # Indexes
    __table_args__ = (
        Index('idx_object_timestamp', 'object_id', 'timestamp'),
        Index('idx_timestamp', 'timestamp'),
        Index('idx_object_id', 'object_id'),
    )
    
    def __init__(self, object_id, timestamp, position_x=None, position_y=None, position_z=None,
                 height=None, direction_x=None, direction_y=None, direction_z=None, 
                 rotation=None, status=None, metadata=None):
        self.object_id = object_id
        self.timestamp = timestamp
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.height = height
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.direction_z = direction_z
        self.rotation = rotation
        self.status = status
        self.object_metadata = metadata
    
    def to_dict(self):
        """Convert history record to dictionary for JSON serialization."""
        return {
            'object_id': self.object_id,
            'timestamp': self.timestamp.isoformat() + 'Z' if self.timestamp else None,
            'position': {
                'x': self.position_x,
                'y': self.position_y,
                'z': self.position_z
            } if self.position_x is not None else None,
            'height': self.height,
            'direction': {
                'x': self.direction_x,
                'y': self.direction_y,
                'z': self.direction_z
            } if self.direction_x is not None else None,
            'rotation': self.rotation,
            'status': self.status,
            'metadata': self.object_metadata,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None
        }
    
    @classmethod
    def find_by_object_id(cls, object_id):
        """Find all history records for an object."""
        return cls.query.filter_by(object_id=object_id).order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def find_by_object_at_timestamp(cls, object_id, timestamp):
        """Find history record for an object at specific timestamp."""
        return cls.query.filter_by(object_id=object_id, timestamp=timestamp).first()
    
    @classmethod
    def find_by_object_before_timestamp(cls, object_id, timestamp):
        """Find history record for an object before specific timestamp."""
        return cls.query.filter(
            cls.object_id == object_id,
            cls.timestamp <= timestamp
        ).order_by(cls.timestamp.desc()).first()
    
    @classmethod
    def find_by_object_after_timestamp(cls, object_id, timestamp):
        """Find history record for an object after specific timestamp."""
        return cls.query.filter(
            cls.object_id == object_id,
            cls.timestamp >= timestamp
        ).order_by(cls.timestamp.asc()).first()
    
    @classmethod
    def find_by_timestamp_range(cls, start_timestamp, end_timestamp):
        """Find all history records within timestamp range."""
        return cls.query.filter(
            cls.timestamp.between(start_timestamp, end_timestamp)
        ).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def create_from_coordinates(cls, object_id, coordinates, timestamp=None):
        """Create history record from current coordinates."""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        return cls(
            object_id=object_id,
            timestamp=timestamp,
            position_x=coordinates.position_x,
            position_y=coordinates.position_y,
            position_z=coordinates.position_z,
            height=coordinates.height,
            direction_x=coordinates.direction_x,
            direction_y=coordinates.direction_y,
            direction_z=coordinates.direction_z,
            rotation=coordinates.rotation,
            status=coordinates.object.status if coordinates.object else None,
            metadata=coordinates.object.metadata if coordinates.object else None
        )
    
    def __repr__(self):
        return f'<ObjectHistory {self.object_id} at {self.timestamp}>'
