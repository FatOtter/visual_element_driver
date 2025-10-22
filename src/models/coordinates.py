from src.database import db
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
import math

class Coordinates3D:
    """3D Coordinates class for testing and calculations."""
    
    def __init__(self, x=0.0, y=0.0, z=0.0, height=0.0, 
                 direction_x=0.0, direction_y=0.0, direction_z=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.direction_z = direction_z
        
        # Normalize direction vector
        self._normalize_direction()
    
    def _normalize_direction(self):
        """Normalize direction vector to unit length."""
        magnitude = math.sqrt(
            self.direction_x**2 + self.direction_y**2 + self.direction_z**2
        )
        
        if magnitude > 0:
            self.direction_x /= magnitude
            self.direction_y /= magnitude
            self.direction_z /= magnitude
    
    @property
    def position(self):
        """Get position as dictionary."""
        return {'x': self.x, 'y': self.y, 'z': self.z}
    
    @property
    def direction(self):
        """Get direction as dictionary."""
        return {'x': self.direction_x, 'y': self.direction_y, 'z': self.direction_z}
    
    def is_valid(self):
        """Check if coordinates are valid."""
        return self.height >= 0
    
    def distance_to(self, other):
        """Calculate distance to another coordinate."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'position': self.position,
            'height': self.height,
            'direction': self.direction
        }

class Coordinates(db.Model):
    """3DCoordinates model representing current spatial data for an object."""
    
    __tablename__ = 'coordinates'
    
    # Foreign key to ProductlineObject
    object_id = Column(String(100), ForeignKey('productline_objects.id', ondelete='CASCADE'), 
                       primary_key=True)
    
    # Position coordinates
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    position_z = Column(Float, nullable=False)
    
    # Object dimensions
    height = Column(Float, nullable=False)
    
    # Direction vector (normalized)
    direction_x = Column(Float, nullable=False)
    direction_y = Column(Float, nullable=False)
    direction_z = Column(Float, nullable=False)
    
    # Rotation angle in degrees
    rotation = Column(Float, nullable=True)
    
    # Timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    object = relationship("ProductlineObject", back_populates="coordinates")
    
    # Indexes and constraints
    __table_args__ = (
        Index('idx_position', 'position_x', 'position_y', 'position_z'),
        Index('idx_updated_at', 'updated_at'),
        CheckConstraint('height >= 0', name='check_height_positive'),
        CheckConstraint('rotation >= 0 AND rotation <= 360', name='check_rotation_range'),
    )
    
    def __init__(self, object_id, position_x=0.0, position_y=0.0, position_z=0.0, 
                 height=0.0, direction_x=1.0, direction_y=0.0, direction_z=0.0, rotation=0.0):
        self.object_id = object_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.height = height
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.direction_z = direction_z
        self.rotation = rotation
        
        # Normalize direction vector
        self._normalize_direction()
    
    def _normalize_direction(self):
        """Normalize direction vector to unit length."""
        magnitude = math.sqrt(
            self.direction_x**2 + self.direction_y**2 + self.direction_z**2
        )
        
        if magnitude > 0:
            self.direction_x /= magnitude
            self.direction_y /= magnitude
            self.direction_z /= magnitude
    
    def to_dict(self):
        """Convert coordinates to dictionary for JSON serialization."""
        return {
            'position': {
                'x': self.position_x,
                'y': self.position_y,
                'z': self.position_z
            },
            'height': self.height,
            'direction': {
                'x': self.direction_x,
                'y': self.direction_y,
                'z': self.direction_z
            },
            'rotation': self.rotation
        }
    
    def update_position(self, x, y, z):
        """Update position coordinates."""
        self.position_x = x
        self.position_y = y
        self.position_z = z
        self.updated_at = datetime.utcnow()
    
    def update_direction(self, x, y, z):
        """Update direction vector and normalize."""
        self.direction_x = x
        self.direction_y = y
        self.direction_z = z
        self._normalize_direction()
        self.updated_at = datetime.utcnow()
    
    def update_rotation(self, rotation):
        """Update rotation angle."""
        if rotation < 0 or rotation > 360:
            raise ValueError("Rotation must be between 0 and 360 degrees")
        
        self.rotation = rotation
        self.updated_at = datetime.utcnow()
    
    def get_distance_to(self, other_coordinates):
        """Calculate distance to another set of coordinates."""
        dx = self.position_x - other_coordinates.position_x
        dy = self.position_y - other_coordinates.position_y
        dz = self.position_z - other_coordinates.position_z
        
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def is_within_bounds(self, min_x, max_x, min_y, max_y, min_z, max_z):
        """Check if coordinates are within specified bounds."""
        return (min_x <= self.position_x <= max_x and
                min_y <= self.position_y <= max_y and
                min_z <= self.position_z <= max_z)
    
    @classmethod
    def find_by_object_id(cls, object_id):
        """Find coordinates by object ID."""
        return cls.query.filter_by(object_id=object_id).first()
    
    @classmethod
    def find_within_bounds(cls, min_x, max_x, min_y, max_y, min_z, max_z):
        """Find all coordinates within specified bounds."""
        return cls.query.filter(
            cls.position_x.between(min_x, max_x),
            cls.position_y.between(min_y, max_y),
            cls.position_z.between(min_z, max_z)
        ).all()
    
    def __repr__(self):
        return f'<Coordinates {self.object_id}: ({self.position_x}, {self.position_y}, {self.position_z})>'
