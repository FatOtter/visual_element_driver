# Data Model: Productline 3D Data Retrieval

**Created**: 2025-01-27  
**Purpose**: Define data entities, relationships, and validation rules for the productline 3D data system

## Core Entities

### ProductlineObject
**Purpose**: Represents a single element in the productline with 3D spatial data

**Attributes**:
- `id` (string, primary key): Unique identifier for the object
- `name` (string, optional): Human-readable name for the object
- `status` (enum): Current state (active, inactive, processing, error)
- `created_at` (datetime): Object creation timestamp
- `updated_at` (datetime): Last modification timestamp
- `metadata` (json): Additional object properties

**Validation Rules**:
- `id` must be non-empty string, max 100 characters
- `status` must be one of: active, inactive, processing, error
- `created_at` and `updated_at` must be valid datetime objects
- `metadata` must be valid JSON structure

**Relationships**:
- One-to-many with ObjectHistory (temporal data)
- One-to-one with 3DCoordinates (current spatial data)

### 3DCoordinates
**Purpose**: Represents current spatial data for an object

**Attributes**:
- `object_id` (string, foreign key): Reference to ProductlineObject
- `position_x` (float): X coordinate in 3D space
- `position_y` (float): Y coordinate in 3D space  
- `position_z` (float): Z coordinate in 3D space
- `height` (float): Object height dimension
- `direction_x` (float): X component of direction vector
- `direction_y` (float): Y component of direction vector
- `direction_z` (float): Z component of direction vector
- `rotation` (float): Rotation angle in degrees
- `updated_at` (datetime): Last coordinate update

**Validation Rules**:
- All position coordinates must be finite numbers
- Height must be non-negative
- Direction vector components must be normalized (sum of squares = 1)
- Rotation must be between 0 and 360 degrees
- `object_id` must reference existing ProductlineObject

**Relationships**:
- Many-to-one with ProductlineObject

### ObjectHistory
**Purpose**: Represents historical state of an object at specific timestamps

**Attributes**:
- `id` (integer, primary key): Auto-incrementing history record ID
- `object_id` (string, foreign key): Reference to ProductlineObject
- `timestamp` (datetime): Point in time for this historical record
- `position_x` (float): Historical X coordinate
- `position_y` (float): Historical Y coordinate
- `position_z` (float): Historical Z coordinate
- `height` (float): Historical height
- `direction_x` (float): Historical X direction component
- `direction_y` (float): Historical Y direction component
- `direction_z` (float): Historical Z direction component
- `rotation` (float): Historical rotation angle
- `status` (enum): Historical status at this timestamp
- `metadata` (json): Historical metadata snapshot

**Validation Rules**:
- `timestamp` must be valid datetime
- All coordinate values must be finite numbers
- `object_id` must reference existing ProductlineObject
- `status` must be valid enum value
- `metadata` must be valid JSON

**Relationships**:
- Many-to-one with ProductlineObject

## Data Relationships

```
ProductlineObject (1) ←→ (1) 3DCoordinates
     │
     │ (1)
     │
     ↓ (many)
ObjectHistory
```

**Relationship Rules**:
- Each ProductlineObject has exactly one current 3DCoordinates record
- Each ProductlineObject can have many ObjectHistory records
- ObjectHistory records are immutable once created
- Deleting a ProductlineObject cascades to delete related 3DCoordinates and ObjectHistory

## State Transitions

### ProductlineObject Status Flow
```
created → active → inactive
   ↓        ↓        ↓
processing → error → inactive
```

**Transition Rules**:
- New objects start in 'active' status
- Objects can transition to 'processing' during updates
- Objects can transition to 'error' if processing fails
- Objects can be set to 'inactive' to disable them
- Error objects can be reactivated after fixing issues

### Coordinate Updates
```
3DCoordinates.updated_at changes → New ObjectHistory record created
```

**Update Rules**:
- Every coordinate change creates a new ObjectHistory record
- Historical records are never modified
- Current coordinates are always in 3DCoordinates table
- Historical queries use ObjectHistory table

## Data Validation

### Input Validation
- Object ID format: Alphanumeric string, 1-100 characters
- Coordinate values: Finite numbers within reasonable bounds (-1000 to 1000)
- Timestamps: Valid ISO 8601 format or Unix timestamp
- Status values: Must match predefined enum values
- JSON metadata: Valid JSON structure, max 10KB

### Business Rules
- Objects cannot be deleted if they have active references
- Historical data is retained for minimum 1 year
- Coordinate updates must include all spatial dimensions
- Status changes are logged in ObjectHistory
- Batch operations must handle partial failures gracefully

## Performance Considerations

### Database Indexes
- Primary key on ProductlineObject.id
- Index on ObjectHistory.object_id for historical queries
- Index on ObjectHistory.timestamp for time-based queries
- Composite index on (object_id, timestamp) for efficient historical lookups

### Query Optimization
- Use connection pooling for concurrent requests
- Implement query result caching for frequently accessed objects
- Batch historical data queries to minimize database round trips
- Use database views for complex coordinate calculations

## Data Migration

### Initial Data Setup
- Create tables with proper indexes
- Insert sample ProductlineObject records
- Generate initial 3DCoordinates for all objects
- Create ObjectHistory records for initial states

### Schema Evolution
- Add new columns with default values
- Migrate existing data to new schema
- Update indexes as needed
- Maintain backward compatibility for API responses

## Security Considerations

### Data Access
- All database access through service layer
- Input sanitization for all user inputs
- SQL injection prevention through parameterized queries
- Access logging for audit trails

### Data Integrity
- Foreign key constraints enforce referential integrity
- Check constraints validate coordinate ranges
- Unique constraints prevent duplicate records
- Transaction management for data consistency
