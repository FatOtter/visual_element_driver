"""
Unit tests for ProductlineObject model.
Tests model creation, validation, and relationships.
"""

import pytest
from datetime import datetime
from src.models.productline_object import ProductlineObject
from src.models.coordinates import Coordinates3D
from src.database import db

class TestProductlineObject:
    """Test ProductlineObject model functionality."""
    
    def test_object_creation(self):
        """Test basic object creation."""
        # This test should FAIL initially (model not implemented)
        obj = ProductlineObject(
            id='OBJ_001',
            name='Test Object',
            status='active'
        )
        
        assert obj.id == 'OBJ_001'
        assert obj.name == 'Test Object'
        assert obj.status == 'active'
    
    def test_object_validation(self):
        """Test object validation rules."""
        # Test required fields
        with pytest.raises(ValueError):
            ProductlineObject()  # Missing required fields
    
    def test_status_enum(self):
        """Test status enum validation."""
        obj = ProductlineObject(
            id='OBJ_001',
            status='active'
        )
        assert obj.status == 'active'
        
        # Test invalid status
        with pytest.raises(ValueError):
            obj.status = 'invalid_status'
    
    def test_coordinates_relationship(self):
        """Test coordinates relationship."""
        obj = ProductlineObject(
            id='OBJ_001',
            name='Test Object'
        )
        
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        
        obj.coordinates = coords
        assert obj.coordinates.x == 1.0
        assert obj.coordinates.y == 2.0
        assert obj.coordinates.z == 3.0
    
    def test_metadata_handling(self):
        """Test metadata JSON handling."""
        obj = ProductlineObject(
            id='OBJ_001',
            metadata={'type': 'conveyor', 'speed': 1.5}
        )
        
        assert obj.metadata['type'] == 'conveyor'
        assert obj.metadata['speed'] == 1.5
    
    def test_string_representation(self):
        """Test string representation."""
        obj = ProductlineObject(
            id='OBJ_001',
            name='Test Object',
            status='active'
        )
        
        str_repr = str(obj)
        assert 'OBJ_001' in str_repr
        assert 'Test Object' in str_repr
        assert 'active' in str_repr
