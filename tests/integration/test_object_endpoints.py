"""
Integration tests for object retrieval endpoints.
Tests the complete flow from API request to database response.
"""

import pytest
import json
from flask import Flask
from src.app import create_app
from src.database import db

class TestObjectEndpointsIntegration:
    """Integration tests for object endpoints."""
    
    @pytest.fixture
    def app(self):
        """Create test application with database."""
        app = create_app('testing')
        
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()
    
    def test_get_object_complete_flow(self, client, app):
        """Test complete object retrieval flow."""
        # This test should FAIL initially (no data)
        response = client.get('/api/v1/objects/OBJ_001')
        
        # Initially should return 404 (no data)
        assert response.status_code == 404
        
        # TODO: Add test data and verify successful retrieval
        # This will be implemented after data models are created
    
    def test_database_connection(self, app):
        """Test database connection is working."""
        with app.app_context():
            # Test database connection
            result = db.engine.execute("SELECT 1").fetchone()
            assert result[0] == 1
    
    def test_api_health_check(self, client):
        """Test API health check endpoint."""
        response = client.get('/api/v1/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
