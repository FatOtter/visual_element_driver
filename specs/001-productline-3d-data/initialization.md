# Server Initialization Guide

**Created**: 2025-01-27  
**Purpose**: Comprehensive guide for initializing the Productline 3D Data API server

## Overview

The initialization system ensures proper server setup with dependency checking, database configuration, and health monitoring. This is essential for first-time deployment and ensures consistent server state.

## Initialization Scripts

### Main Initialization Script (`./scripts/init.sh`)

**Purpose**: Comprehensive server setup for first-time deployment

**Features**:
- System requirements validation
- Dependency checking
- Database setup and DDL execution
- Environment configuration
- Health monitoring setup
- Sample data loading (optional)

**Usage**:
```bash
# Make executable
chmod +x ./scripts/init.sh

# Run initialization
./scripts/init.sh
```

**Output**:
- System requirements report
- Dependency status
- Database setup confirmation
- Health check results
- Configuration files created

### Individual Scripts

#### 1. Dependency Checker (`src/scripts/check_dependencies.py`)

**Purpose**: Verify system requirements and dependencies

**Checks**:
- Python version (3.8+)
- Required packages (Flask, SQLAlchemy, pytest, etc.)
- System resources (memory, disk space)
- Network connectivity
- Port availability

**Usage**:
```bash
python src/scripts/check_dependencies.py
```

**Output**:
```
=== Dependency Check Report ===
✓ Python 3.8.10 detected
✓ Flask 2.3.0 installed
✓ SQLAlchemy 2.0.0 installed
✓ pytest 7.4.0 installed
✓ System memory: 8GB available
✓ Port 5566 available
✓ Network connectivity: OK
```

#### 2. Database Setup (`src/scripts/setup_database.py`)

**Purpose**: Configure database and execute DDL scripts

**Features**:
- Database connection testing
- DDL script execution
- Index creation
- Connection pooling setup
- Migration execution
- Sample data loading

**Usage**:
```bash
python src/scripts/setup_database.py
```

**Configuration**:
```python
# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/productline.db')
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
```

**DDL Scripts**:
- `src/models/schema.sql` - Table creation
- `src/models/indexes.sql` - Index creation
- `src/models/constraints.sql` - Constraint setup

#### 3. Health Check (`src/scripts/health_check.py`)

**Purpose**: Verify system health and functionality

**Checks**:
- Database connectivity
- API endpoint availability
- Port binding
- Configuration validation
- Service readiness

**Usage**:
```bash
python src/scripts/health_check.py
```

**Output**:
```
=== Health Check Report ===
✓ Database connection: OK
✓ API endpoints: OK
✓ Port 5566: Available
✓ Configuration: Valid
✓ Service ready: OK
```

#### 4. Environment Setup (`./scripts/setup_env.sh`)

**Purpose**: Configure environment and settings

**Features**:
- Configuration file creation
- Logging setup
- CORS configuration
- Environment variable setup
- Security settings

**Usage**:
```bash
chmod +x ./scripts/setup_env.sh
./scripts/setup_env.sh
```

**Configuration Files Created**:
- `config/development.py` - Development settings
- `config/production.py` - Production settings
- `config/init_config.yaml` - Initialization settings
- `logs/` directory - Logging setup

## Database Schema Initialization

### DDL Scripts

#### Table Creation (`src/models/schema.sql`)
```sql
-- ProductlineObject table
CREATE TABLE productline_objects (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'processing', 'error')),
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3DCoordinates table
CREATE TABLE coordinates (
    object_id VARCHAR(100) PRIMARY KEY,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    height FLOAT NOT NULL CHECK (height >= 0),
    direction_x FLOAT NOT NULL,
    direction_y FLOAT NOT NULL,
    direction_z FLOAT NOT NULL,
    rotation FLOAT CHECK (rotation >= 0 AND rotation <= 360),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES productline_objects(id)
);

-- ObjectHistory table
CREATE TABLE object_history (
    id SERIAL PRIMARY KEY,
    object_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    position_x FLOAT,
    position_y FLOAT,
    position_z FLOAT,
    height FLOAT,
    direction_x FLOAT,
    direction_y FLOAT,
    direction_z FLOAT,
    rotation FLOAT,
    status VARCHAR(20),
    metadata JSON,
    FOREIGN KEY (object_id) REFERENCES productline_objects(id)
);
```

#### Index Creation (`src/models/indexes.sql`)
```sql
-- Performance indexes
CREATE INDEX idx_object_history_object_id ON object_history(object_id);
CREATE INDEX idx_object_history_timestamp ON object_history(timestamp);
CREATE INDEX idx_object_history_composite ON object_history(object_id, timestamp);
CREATE INDEX idx_objects_status ON productline_objects(status);
CREATE INDEX idx_objects_updated_at ON productline_objects(updated_at);
```

#### Constraints (`src/models/constraints.sql`)
```sql
-- Data integrity constraints
ALTER TABLE coordinates ADD CONSTRAINT chk_direction_normalized 
    CHECK (direction_x*direction_x + direction_y*direction_y + direction_z*direction_z = 1);

ALTER TABLE object_history ADD CONSTRAINT chk_historical_timestamp 
    CHECK (timestamp <= CURRENT_TIMESTAMP);

-- Triggers for updated_at
CREATE TRIGGER update_objects_updated_at 
    BEFORE UPDATE ON productline_objects 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_coordinates_updated_at 
    BEFORE UPDATE ON coordinates 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

## Configuration Management

### Environment Variables

**Required Variables**:
```bash
# Database
export DATABASE_URL="sqlite:///data/productline.db"  # Development
export DATABASE_URL="postgresql://user:pass@localhost:5432/productline"  # Production

# Server
export PORT=5566
export FLASK_ENV=development  # or production
export LOG_LEVEL=INFO

# Security (optional)
export API_KEY=your-secret-key
export CORS_ORIGINS="*"  # Development only
```

**Optional Variables**:
```bash
# Performance
export DB_POOL_SIZE=10
export DB_MAX_OVERFLOW=20
export REQUEST_TIMEOUT=30

# Logging
export LOG_FILE=logs/app.log
export LOG_MAX_SIZE=10MB
export LOG_BACKUP_COUNT=5
```

### Configuration Files

#### Development Configuration (`config/development.py`)
```python
import os

class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/productline.db')
    PORT = int(os.environ.get('PORT', 5566))
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['*']
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
```

#### Production Configuration (`config/production.py`)
```python
import os

class ProductionConfig:
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    PORT = int(os.environ.get('PORT', 5566))
    LOG_LEVEL = 'INFO'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    DB_POOL_SIZE = 20
    DB_MAX_OVERFLOW = 30
    API_KEY = os.environ.get('API_KEY')
```

## Initialization Process

### Step-by-Step Process

1. **System Requirements Check**
   ```bash
   python src/scripts/check_dependencies.py
   ```

2. **Environment Setup**
   ```bash
   ./scripts/setup_env.sh
   ```

3. **Database Initialization**
   ```bash
   python src/scripts/setup_database.py
   ```

4. **Health Verification**
   ```bash
   python src/scripts/health_check.py
   ```

5. **Service Start**
   ```bash
   python src/app.py
   ```

### Automated Initialization

**One-Command Setup**:
```bash
./scripts/init.sh
```

**Docker Initialization**:
```bash
docker-compose up -d
docker-compose exec app python src/scripts/init_server.py
```

## Troubleshooting

### Common Initialization Issues

**Database Connection Failed**:
```bash
# Check database URL
echo $DATABASE_URL

# Test connection manually
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('Connection OK')"
```

**Port Already in Use**:
```bash
# Check port usage
lsof -i :5566

# Kill process or change port
export PORT=8080
```

**Missing Dependencies**:
```bash
# Install missing packages
pip install -r requirements.txt

# Check specific package
python -c "import flask; print('Flask OK')"
```

**Permission Issues**:
```bash
# Fix script permissions
chmod +x ./scripts/*.sh

# Fix directory permissions
chmod 755 logs/
chmod 755 data/
```

### Initialization Logs

**Log Location**: `logs/initialization.log`

**Log Levels**:
- INFO: Normal initialization steps
- WARNING: Non-critical issues
- ERROR: Critical failures
- DEBUG: Detailed debugging information

**Log Rotation**: Configured for 10MB max size with 5 backup files

## Security Considerations

### Initialization Security

- Database credentials stored in environment variables
- No hardcoded secrets in configuration files
- Proper file permissions on sensitive files
- CORS configuration for production
- API key authentication (optional)

### Production Deployment

- Use production configuration
- Set secure environment variables
- Configure proper CORS origins
- Enable API key authentication
- Set up monitoring and alerting

## Monitoring and Maintenance

### Health Monitoring

**Health Check Endpoint**: `GET /api/v1/health`

**Monitoring Scripts**:
- `src/scripts/health_check.py` - Comprehensive health check
- `src/scripts/check_dependencies.py` - Dependency monitoring
- `src/scripts/setup_database.py` - Database health

**Automated Monitoring**:
```bash
# Cron job for health checks
*/5 * * * * /path/to/health_check.py
```

### Maintenance Tasks

**Regular Maintenance**:
- Database backup
- Log rotation
- Performance monitoring
- Security updates
- Dependency updates

**Maintenance Scripts**:
- `scripts/backup_database.sh` - Database backup
- `scripts/rotate_logs.sh` - Log rotation
- `scripts/update_dependencies.sh` - Dependency updates
