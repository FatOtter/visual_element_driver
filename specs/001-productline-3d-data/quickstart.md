# Quick Start Guide: Productline 3D Data Retrieval API

**Created**: 2025-01-27  
**Purpose**: Get the API service running quickly for development and testing

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd visual_element_driver
pip install -r requirements.txt
```

### 2. Server Initialization (First Time Setup)
```bash
# Run the comprehensive initialization script
./scripts/init.sh

# This script will:
# - Check all dependencies and system requirements
# - Verify database connectivity
# - Create and configure database schema (DDL)
# - Set up environment configuration
# - Run health checks
# - Initialize sample data (optional)
```

### 3. Manual Configuration (Alternative)
```bash
# Environment Configuration
cp config/development.py.example config/development.py

# Set environment variables (optional)
export PORT=5566
export DATABASE_URL=sqlite:///data/productline.db

# Check Dependencies
python src/scripts/check_dependencies.py

# Setup Database
python src/scripts/setup_database.py

# Health Check
python src/scripts/health_check.py
```

## Running the Service

### Development Mode
```bash
# Start the Flask development server
python src/app.py

# Service will be available at:
# - API: http://localhost:5566/api/v1/
# - Test Interface: http://localhost:5566/test
```

### Production Mode
```bash
# Using Gunicorn (recommended)
gunicorn -w 4 -b 0.0.0.0:5566 src.app:app

# Using Docker
docker-compose up -d
```

## API Usage Examples

### 1. Get Single Object
```bash
# Retrieve object by ID
curl -X GET "http://localhost:5566/api/v1/objects/OBJ_001"

# Response:
{
  "object_id": "OBJ_001",
  "name": "Conveyor Belt Section A",
  "status": "active",
  "coordinates": {
    "position": {"x": 10.5, "y": 20.3, "z": 5.0},
    "height": 2.5,
    "direction": {"x": 1.0, "y": 0.0, "z": 0.0},
    "rotation": 0.0
  },
  "metadata": {"type": "conveyor", "speed": 1.2},
  "created_at": "2025-01-27T10:00:00Z",
  "updated_at": "2025-01-27T15:30:00Z"
}
```

### 2. Get Historical Data
```bash
# Retrieve object at specific timestamp
curl -X GET "http://localhost:5566/api/v1/objects/OBJ_001?timestamp=2025-01-27T12:00:00Z"
```

### 3. Batch Object Retrieval
```bash
# Get multiple objects at once
curl -X POST "http://localhost:5566/api/v1/objects/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "object_ids": ["OBJ_001", "OBJ_002", "OBJ_003"],
    "timestamp": "2025-01-27T12:00:00Z"
  }'
```

### 4. Health Check
```bash
# Check service health
curl -X GET "http://localhost:5566/api/v1/health"
```

## Testing Interface

### Access the Web Interface
1. Open browser to `http://localhost:5566/test`
2. Enter object ID in the form field
3. Click "Get Object Data" to retrieve information
4. View JSON response for comparison with Unreal Engine

### Testing Historical Data
1. Enter object ID and timestamp
2. Click "Get Historical Data"
3. Compare response with current data

## Unreal Engine Integration

### C++ Example
```cpp
// HTTP request to get object data
FString ObjectId = TEXT("OBJ_001");
FString ApiUrl = TEXT("http://localhost:5566/api/v1/objects/") + ObjectId;

// Make HTTP request
TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
Request->SetURL(ApiUrl);
Request->SetVerb(TEXT("GET"));
Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
Request->OnProcessRequestComplete().BindLambda([this](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    if (bWasSuccessful && Response.IsValid())
    {
        FString ResponseString = Response->GetContentAsString();
        // Parse JSON response and extract 3D coordinates
        ParseObjectData(ResponseString);
    }
});
Request->ProcessRequest();
```

### Blueprint Integration
1. Create HTTP Request node
2. Set URL to `http://localhost:5566/api/v1/objects/{ObjectID}`
3. Set Method to GET
4. Parse JSON response for coordinates
5. Apply to 3D object transform

## Configuration Options

### Port Configuration
```bash
# Default port 5566
export PORT=5566

# Custom port
export PORT=8080
```

### Database Configuration
```bash
# SQLite (development)
export DATABASE_URL=sqlite:///data/productline.db

# PostgreSQL (production)
export DATABASE_URL=postgresql://user:pass@localhost:5432/productline
```

### CORS Configuration
```python
# In config/development.py
CORS_ORIGINS = ["*"]  # Development only
CORS_METHODS = ["GET", "POST"]
CORS_HEADERS = ["Content-Type"]
```

## Initialization Scripts

### Main Initialization Script (`./scripts/init.sh`)
The main initialization script performs comprehensive server setup:

```bash
#!/bin/bash
# Comprehensive server initialization script

echo "=== Productline 3D Data API - Server Initialization ==="

# 1. Check system requirements
echo "Checking system requirements..."
python src/scripts/check_dependencies.py

# 2. Setup environment
echo "Setting up environment configuration..."
./scripts/setup_env.sh

# 3. Database setup
echo "Configuring database..."
python src/scripts/setup_database.py

# 4. Health check
echo "Running health checks..."
python src/scripts/health_check.py

# 5. Load sample data (optional)
read -p "Load sample data? (y/n): " load_sample
if [[ $load_sample == "y" ]]; then
    python src/scripts/load_sample_data.py
fi

echo "=== Initialization Complete ==="
```

### Individual Scripts

**Dependency Checker (`src/scripts/check_dependencies.py`)**:
- Verifies Python version (3.8+)
- Checks required packages (Flask, SQLAlchemy, etc.)
- Validates system resources
- Tests network connectivity

**Database Setup (`src/scripts/setup_database.py`)**:
- Creates database connection
- Executes DDL scripts
- Sets up indexes
- Configures connection pooling
- Runs migration scripts

**Health Check (`src/scripts/health_check.py`)**:
- Tests database connectivity
- Verifies API endpoints
- Checks port availability
- Validates configuration

**Environment Setup (`./scripts/setup_env.sh`)**:
- Creates configuration files
- Sets up logging
- Configures CORS settings
- Sets default environment variables

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using port 5566
lsof -i :5566

# Kill process or use different port
export PORT=8080
```

**Database connection failed:**
```bash
# Check database URL
echo $DATABASE_URL

# Recreate database
rm data/productline.db
python -m src.models.init_db
```

**CORS errors in Unreal Engine:**
```bash
# Check CORS configuration
curl -H "Origin: http://localhost" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:5566/api/v1/objects/OBJ_001
```

### Performance Testing
```bash
# Test response times
time curl -X GET "http://localhost:5566/api/v1/objects/OBJ_001"

# Load testing (install Apache Bench)
ab -n 1000 -c 10 http://localhost:5566/api/v1/objects/OBJ_001
```

### Logs and Debugging
```bash
# Enable debug logging
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG

# View logs
tail -f logs/app.log
```

## Next Steps

1. **API Testing**: Use the web interface to test all endpoints
2. **Unreal Engine Integration**: Implement HTTP client in your UE project
3. **Data Population**: Add your productline objects to the database
4. **Performance Tuning**: Monitor response times and optimize as needed
5. **Production Deployment**: Configure for production environment

## Support

- API Documentation: `http://localhost:5566/api/v1/docs`
- Health Check: `http://localhost:5566/api/v1/health`
- Test Interface: `http://localhost:5566/test`
- Logs: Check `logs/app.log` for detailed information
