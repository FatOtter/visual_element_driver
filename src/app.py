"""
Productline 3D Data Retrieval API
Flask application for providing 3D coordinate data to Unreal Engine applications.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import config
from dotenv import load_dotenv
from src.database import init_database
from src.app_logging import setup_logging, get_logger
from src.middleware.error_handler import register_error_handlers
from src.middleware.cors import init_cors
from src.api.routes import api_bp
from src.api.health import health_bp

def load_environment_config():
    """Load environment variables from configuration file."""
    # Simply load from config/env.example
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    env_example_path = os.path.join(config_dir, 'env.example')
    if os.path.exists(env_example_path):
        load_dotenv(env_example_path)

def create_app(config_name=None):
    """Create and configure Flask application."""
    
    # Load environment variables from config files
    load_environment_config()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize logging
    setup_logging(app)
    logger = get_logger(__name__)
    
    # Initialize database
    init_database(app)
    
    # Initialize CORS
    init_cors(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(health_bp)
    
    # Add test interface route
    @app.route('/test')
    def test_interface():
        """Developer testing interface."""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Productline 3D Data API - Test Interface</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .form-group { margin: 20px 0; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, textarea { width: 100%; padding: 8px; margin-bottom: 10px; }
                button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
                .response { background: #f8f9fa; padding: 15px; margin: 20px 0; border-left: 4px solid #007bff; }
                .error { border-left-color: #dc3545; background: #f8d7da; }
                .success { border-left-color: #28a745; background: #d4edda; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Productline 3D Data API - Test Interface</h1>
                
                <div class="form-group">
                    <label for="objectId">Object ID:</label>
                    <input type="text" id="objectId" placeholder="e.g., OBJ_001" value="OBJ_001">
                </div>
                
                <div class="form-group">
                    <label for="timestamp">Timestamp (optional):</label>
                    <input type="datetime-local" id="timestamp">
                </div>
                
                <button onclick="getObjectData()">Get Object Data</button>
                <button onclick="getHistoricalData()">Get Historical Data</button>
                <button onclick="testBatchRequest()">Test Batch Request</button>
                
                <div id="response" class="response" style="display: none;">
                    <h3>Response:</h3>
                    <pre id="responseContent"></pre>
                </div>
            </div>
            
            <script>
                const API_BASE = '/api/v1';
                
                function showResponse(data, isError = false) {
                    const responseDiv = document.getElementById('response');
                    const responseContent = document.getElementById('responseContent');
                    
                    responseDiv.className = 'response ' + (isError ? 'error' : 'success');
                    responseContent.textContent = JSON.stringify(data, null, 2);
                    responseDiv.style.display = 'block';
                }
                
                async function getObjectData() {
                    const objectId = document.getElementById('objectId').value;
                    if (!objectId) {
                        showResponse({error: 'Object ID is required'}, true);
                        return;
                    }
                    
                    try {
                        const response = await fetch(`${API_BASE}/objects/${objectId}`);
                        const data = await response.json();
                        showResponse(data, !response.ok);
                    } catch (error) {
                        showResponse({error: error.message}, true);
                    }
                }
                
                async function getHistoricalData() {
                    const objectId = document.getElementById('objectId').value;
                    const timestamp = document.getElementById('timestamp').value;
                    
                    if (!objectId) {
                        showResponse({error: 'Object ID is required'}, true);
                        return;
                    }
                    
                    try {
                        let url = `${API_BASE}/objects/${objectId}`;
                        if (timestamp) {
                            url += `?timestamp=${timestamp}`;
                        }
                        
                        const response = await fetch(url);
                        const data = await response.json();
                        showResponse(data, !response.ok);
                    } catch (error) {
                        showResponse({error: error.message}, true);
                    }
                }
                
                async function testBatchRequest() {
                    try {
                        const response = await fetch(`${API_BASE}/objects/batch`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                object_ids: ['OBJ_001', 'OBJ_002', 'OBJ_003']
                            })
                        });
                        const data = await response.json();
                        showResponse(data, !response.ok);
                    } catch (error) {
                        showResponse({error: error.message}, true);
                    }
                }
            </script>
        </body>
        </html>
        '''
    
    # Health check endpoint
    @app.route('/')
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'service': 'Productline 3D Data Retrieval API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/api/v1/health',
                'objects': '/api/v1/objects/{id}',
                'batch': '/api/v1/objects/batch',
                'test': '/test'
            }
        })
    
    logger.info(f"Flask application created with {config_name} configuration")
    return app

def main():
    """Main application entry point."""
    app = create_app()
    
    # Get configuration
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5566)
    debug = app.config.get('DEBUG', False)
    
    logger = get_logger(__name__)
    logger.info(f"Starting Productline 3D Data Retrieval API on {host}:{port}")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
