from src.database import db
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, JSON, Index
from sqlalchemy.orm import relationship
import json

class ProductlineObject(db.Model):
    """ProductlineObject model representing a single element in the productline."""
    
    __tablename__ = 'productline_objects'
    
    # Primary key
    id = Column(String(100), primary_key=True)
    
    # Basic attributes
    name = Column(String(255), nullable=True)
    status = Column(Enum('active', 'inactive', 'processing', 'error', name='status_enum'), 
                   nullable=False, default='active')
    object_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    coordinates = relationship("Coordinates", back_populates="object", uselist=False, cascade="all, delete-orphan")
    history = relationship("ObjectHistory", back_populates="object", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_updated_at', 'updated_at'),
    )
    
    def __init__(self, id, name=None, status='active', metadata=None):
        self.id = id
        self.name = name
        self.status = status
        self.object_metadata = metadata
    
    def to_dict(self):
        """Convert object to dictionary for JSON serialization."""
        return {
            'object_id': self.id,
            'name': self.name,
            'status': self.status,
            'metadata': self.object_metadata,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
    
    def update_status(self, new_status):
        """Update object status."""
        if new_status not in ['active', 'inactive', 'processing', 'error']:
            raise ValueError(f"Invalid status: {new_status}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def update_metadata(self, metadata_dict):
        """Update object metadata."""
        if self.object_metadata is None:
            self.object_metadata = {}
        
        self.object_metadata.update(metadata_dict)
        self.updated_at = datetime.utcnow()
    
    def is_active(self):
        """Check if object is active."""
        return self.status == 'active'
    
    def can_be_retrieved(self):
        """Check if object can be retrieved (not in error state)."""
        return self.status in ['active', 'inactive', 'processing']
    
    @classmethod
    def find_by_id(cls, object_id):
        """Find object by ID."""
        return cls.query.filter_by(id=object_id).first()
    
    @classmethod
    def find_active_objects(cls):
        """Find all active objects."""
        return cls.query.filter_by(status='active').all()
    
    @classmethod
    def find_by_status(cls, status):
        """Find objects by status."""
        return cls.query.filter_by(status=status).all()
    
    def __repr__(self):
        return f'<ProductlineObject {self.id}: {self.name} ({self.status})>'
