#!/usr/bin/env python3
"""
Simple test script to verify Flask application can start
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from flask import Flask, jsonify
from flask_cors import CORS

def create_simple_app():
    """Create a simple Flask app for testing."""
    
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS
    CORS(app)
    
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Productline 3D Data Retrieval API',
            'version': '1.0.0',
            'status': 'running',
            'message': 'Application is working!'
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': '2025-01-27T16:35:00Z'
        })
    
    @app.route('/test')
    def test_interface():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Interface</title>
        </head>
        <body>
            <h1>Test Interface</h1>
            <p>Application is running successfully!</p>
            <p><a href="/">API Info</a> | <a href="/health">Health Check</a></p>
        </body>
        </html>
        '''
    
    return app

if __name__ == '__main__':
    print("Creating simple test application...")
    app = create_simple_app()
    
    print("Starting Flask application on http://localhost:5566")
    print("Available endpoints:")
    print("  - http://localhost:5566/ (API info)")
    print("  - http://localhost:5566/health (Health check)")
    print("  - http://localhost:5566/test (Test interface)")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5566, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
