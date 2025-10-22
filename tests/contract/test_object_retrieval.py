"""
Contract tests for object retrieval API endpoint.
Tests the API contract as defined in OpenAPI specification.
"""

import pytest
import json
from flask import Flask
from src.app import create_app

class TestObjectRetrievalContract:
    """Test the GET /api/v1/objects/{id} endpoint contract."""
    
    @pytest.fixture
    def app(self):
        """Create test application."""
        app = create_app('testing')
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()
    
    def test_get_object_by_id_success(self, client):
        """Test successful object retrieval by ID."""
        # This test should FAIL initially (no data in database)
        response = client.get('/api/v1/objects/OBJ_001')
        
        # Expected response structure
        assert response.status_code == 200
        data = response.get_json()
        
        # Required fields per OpenAPI spec
        assert 'object_id' in data
        assert 'name' in data
        assert 'status' in data
        assert 'coordinates' in data
        assert 'metadata' in data
        assert 'timestamp' in data
        
        # Coordinate structure
        coords = data['coordinates']
        assert 'position' in coords
        assert 'height' in coords
        assert 'direction' in coords
        
        # Position structure
        position = coords['position']
        assert 'x' in position
        assert 'y' in position
        assert 'z' in position
        
        # Direction structure
        direction = coords['direction']
        assert 'x' in direction
        assert 'y' in direction
        assert 'z' in direction
    
    def test_get_object_by_id_not_found(self, client):
        """Test object not found scenario."""
        response = client.get('/api/v1/objects/NONEXISTENT')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
    
    def test_get_object_by_id_invalid_format(self, client):
        """Test invalid object ID format."""
        response = client.get('/api/v1/objects/')
        
        assert response.status_code == 404
    
    def test_response_content_type(self, client):
        """Test response content type is JSON."""
        response = client.get('/api/v1/objects/OBJ_001')
        
        assert response.content_type == 'application/json'
    
    def test_response_headers(self, client):
        """Test CORS headers are present."""
        response = client.get('/api/v1/objects/OBJ_001')
        
        # CORS headers should be present
        assert 'Access-Control-Allow-Origin' in response.headers
