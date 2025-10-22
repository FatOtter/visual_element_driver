"""
Unit tests for 3DCoordinates model.
Tests coordinate calculations and validation.
"""

import pytest
import math
from src.models.coordinates import Coordinates3D

class TestCoordinates3D:
    """Test 3DCoordinates model functionality."""
    
    def test_coordinate_creation(self):
        """Test basic coordinate creation."""
        # This test should FAIL initially (model not implemented)
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        
        assert coords.x == 1.0
        assert coords.y == 2.0
        assert coords.z == 3.0
        assert coords.height == 4.0
        assert coords.direction_x == 0.0
        assert coords.direction_y == 0.0
        assert coords.direction_z == 1.0
    
    def test_position_property(self):
        """Test position property."""
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        
        position = coords.position
        assert position['x'] == 1.0
        assert position['y'] == 2.0
        assert position['z'] == 3.0
    
    def test_direction_property(self):
        """Test direction property."""
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        
        direction = coords.direction
        assert direction['x'] == 0.0
        assert direction['y'] == 0.0
        assert direction['z'] == 1.0
    
    def test_direction_normalization(self):
        """Test direction vector normalization."""
        coords = Coordinates3D(
            x=0.0, y=0.0, z=0.0,
            height=0.0,
            direction_x=3.0, direction_y=4.0, direction_z=0.0
        )
        
        # Direction should be normalized
        magnitude = math.sqrt(coords.direction_x**2 + coords.direction_y**2 + coords.direction_z**2)
        assert abs(magnitude - 1.0) < 0.001
    
    def test_coordinate_validation(self):
        """Test coordinate validation."""
        # Test valid coordinates
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        assert coords.is_valid()
        
        # Test invalid coordinates (negative height)
        coords.height = -1.0
        assert not coords.is_valid()
    
    def test_distance_calculation(self):
        """Test distance calculation between coordinates."""
        coords1 = Coordinates3D(
            x=0.0, y=0.0, z=0.0,
            height=0.0,
            direction_x=1.0, direction_y=0.0, direction_z=0.0
        )
        
        coords2 = Coordinates3D(
            x=3.0, y=4.0, z=0.0,
            height=0.0,
            direction_x=1.0, direction_y=0.0, direction_z=0.0
        )
        
        distance = coords1.distance_to(coords2)
        assert abs(distance - 5.0) < 0.001  # 3-4-5 triangle
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        coords = Coordinates3D(
            x=1.0, y=2.0, z=3.0,
            height=4.0,
            direction_x=0.0, direction_y=0.0, direction_z=1.0
        )
        
        data = coords.to_dict()
        assert data['position']['x'] == 1.0
        assert data['position']['y'] == 2.0
        assert data['position']['z'] == 3.0
        assert data['height'] == 4.0
        assert data['direction']['x'] == 0.0
        assert data['direction']['y'] == 0.0
        assert data['direction']['z'] == 1.0
