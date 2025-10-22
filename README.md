# Productline 3D Data Retrieval API

A Flask-based RESTful API service for providing 3D coordinate data to Unreal Engine applications. This service enables real-time retrieval of productline object data including position, height, direction, and status information.

## Features

- **3D Object Data Retrieval**: Get complete 3D visualization data for productline elements
- **Batch Processing**: Retrieve multiple objects in a single request
- **Historical Data**: Access object data at specific timestamps
- **Developer Testing Interface**: Web-based testing interface for API validation
- **MySQL Integration**: Robust database backend with connection pooling
- **RESTful API**: Standard JSON API endpoints for Unreal Engine integration

## API Endpoints

### Core Endpoints

- `GET /` - API information and service status
- `GET /api/v1/health` - Health check with database status
- `GET /api/v1/objects/{id}` - Retrieve single object data
- `POST /api/v1/objects/batch` - Retrieve multiple objects
- `GET /test` - Developer testing interface

### Response Format

```json
{
  "object_id": "OBJ_001",
  "name": "Conveyor Belt A",
  "status": "active",
  "coordinates": {
    "position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "height": 1.0,
    "direction": {"x": 1.0, "y": 0.0, "z": 0.0},
    "rotation": 0.0
  },
  "metadata": {
    "type": "conveyor",
    "speed": 1.5,
    "length": 10.0
  },
  "created_at": "2025-10-22T08:49:05Z",
  "updated_at": "2025-10-22T08:49:05Z"
}
```

## Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd visual_element_driver
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**:
   ```bash
   # Update config in src/config.py with your MySQL credentials
   # Default: test_admin / 1qaz2wsxE @ localhost:3306
   ```

4. **Initialize database**:
   ```bash
   python init_database.py
   ```

5. **Start the application**:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5566`

### Testing

Access the developer testing interface at `http://localhost:5566/test`

## Configuration

### Environment Variables

- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 3306)
- `DB_USER` - Database username (default: test_admin)
- `DB_PASSWORD` - Database password (set via environment variable)
- `DB_NAME` - Database name (default: productline_3d)
- `PORT` - API port (default: 5566)
- `HOST` - Bind address (default: 0.0.0.0)

### Database Schema

- **productline_objects**: Main object table with status and metadata
- **coordinates**: 3D position and direction data
- **object_history**: Historical snapshots for timeline visualization

## Development

### Project Structure

```
src/
├── api/           # API routes and endpoints
├── models/        # Database models
├── services/      # Business logic
├── middleware/    # CORS, error handling
├── scripts/       # Initialization scripts
└── app.py         # Flask application

tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── contract/      # API contract tests
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/contract/
```

## API Usage Examples

### Retrieve Single Object

```bash
curl http://localhost:5566/api/v1/objects/OBJ_001
```

### Batch Object Retrieval

```bash
curl -X POST http://localhost:5566/api/v1/objects/batch \
  -H "Content-Type: application/json" \
  -d '{"object_ids": ["OBJ_001", "OBJ_002", "OBJ_003"]}'
```

### Health Check

```bash
curl http://localhost:5566/api/v1/health
```

## Unreal Engine Integration

This API is designed for seamless integration with Unreal Engine applications:

- **JSON Response Format**: All responses are in JSON format
- **CORS Enabled**: Cross-origin requests supported
- **Fast Response Times**: Optimized for real-time 3D applications
- **Batch Support**: Efficient multi-object retrieval
- **Error Handling**: Comprehensive error responses

## License

Private Repository - All Rights Reserved

## Support

For technical support or questions, please contact the development team.