#!/usr/bin/env python3
"""
Run script for Productline 3D Data Retrieval API
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.app import create_app

if __name__ == '__main__':
    # Set environment
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Create and run app
    app = create_app()
    app.run(host='0.0.0.0', port=5566, debug=True)
