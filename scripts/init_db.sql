-- Initialize database for Productline 3D Data Retrieval API
-- MySQL database initialization script

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS productline_3d CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE productline_3d;

-- Create ProductlineObject table
CREATE TABLE IF NOT EXISTS productline_objects (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    status ENUM('active', 'inactive', 'processing', 'error') NOT NULL DEFAULT 'active',
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create 3DCoordinates table
CREATE TABLE IF NOT EXISTS coordinates (
    object_id VARCHAR(100) PRIMARY KEY,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    height FLOAT NOT NULL CHECK (height >= 0),
    direction_x FLOAT NOT NULL,
    direction_y FLOAT NOT NULL,
    direction_z FLOAT NOT NULL,
    rotation FLOAT CHECK (rotation >= 0 AND rotation <= 360),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES productline_objects(id) ON DELETE CASCADE,
    INDEX idx_position (position_x, position_y, position_z),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create ObjectHistory table
CREATE TABLE IF NOT EXISTS object_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
    status ENUM('active', 'inactive', 'processing', 'error'),
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES productline_objects(id) ON DELETE CASCADE,
    INDEX idx_object_timestamp (object_id, timestamp),
    INDEX idx_timestamp (timestamp),
    INDEX idx_object_id (object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create trigger to ensure direction vector normalization
DELIMITER //
CREATE TRIGGER IF NOT EXISTS check_direction_normalization
BEFORE INSERT ON coordinates
FOR EACH ROW
BEGIN
    DECLARE magnitude FLOAT;
    SET magnitude = SQRT(NEW.direction_x * NEW.direction_x + NEW.direction_y * NEW.direction_y + NEW.direction_z * NEW.direction_z);
    IF magnitude > 0 THEN
        SET NEW.direction_x = NEW.direction_x / magnitude;
        SET NEW.direction_y = NEW.direction_y / magnitude;
        SET NEW.direction_z = NEW.direction_z / magnitude;
    END IF;
END//
DELIMITER ;

-- Create trigger for updating coordinates
DELIMITER //
CREATE TRIGGER IF NOT EXISTS update_direction_normalization
BEFORE UPDATE ON coordinates
FOR EACH ROW
BEGIN
    DECLARE magnitude FLOAT;
    SET magnitude = SQRT(NEW.direction_x * NEW.direction_x + NEW.direction_y * NEW.direction_y + NEW.direction_z * NEW.direction_z);
    IF magnitude > 0 THEN
        SET NEW.direction_x = NEW.direction_x / magnitude;
        SET NEW.direction_y = NEW.direction_y / magnitude;
        SET NEW.direction_z = NEW.direction_z / magnitude;
    END IF;
END//
DELIMITER ;

-- Insert sample data
INSERT INTO productline_objects (id, name, status, metadata) VALUES
('OBJ_001', 'Conveyor Belt Section A', 'active', '{"type": "conveyor", "speed": 1.2, "capacity": 100}'),
('OBJ_002', 'Robot Arm Station 1', 'active', '{"type": "robot", "model": "KUKA", "payload": 50}'),
('OBJ_003', 'Quality Check Station', 'active', '{"type": "inspection", "camera_count": 4}'),
('OBJ_004', 'Packaging Station', 'processing', '{"type": "packaging", "rate": 30}'),
('OBJ_005', 'Storage Rack A1', 'active', '{"type": "storage", "capacity": 200, "levels": 5}');

INSERT INTO coordinates (object_id, position_x, position_y, position_z, height, direction_x, direction_y, direction_z, rotation) VALUES
('OBJ_001', 10.5, 20.3, 5.0, 2.5, 1.0, 0.0, 0.0, 0.0),
('OBJ_002', 15.0, 25.0, 5.5, 3.0, 0.0, 1.0, 0.0, 90.0),
('OBJ_003', 20.0, 30.0, 6.0, 2.8, 0.707, 0.707, 0.0, 45.0),
('OBJ_004', 25.0, 35.0, 5.2, 2.2, -1.0, 0.0, 0.0, 180.0),
('OBJ_005', 30.0, 40.0, 4.0, 4.0, 0.0, 0.0, 1.0, 0.0);

-- Insert historical data
INSERT INTO object_history (object_id, timestamp, position_x, position_y, position_z, height, direction_x, direction_y, direction_z, rotation, status, metadata) VALUES
('OBJ_001', '2025-01-27 10:00:00', 10.0, 20.0, 5.0, 2.5, 1.0, 0.0, 0.0, 0.0, 'active', '{"type": "conveyor", "speed": 1.0}'),
('OBJ_001', '2025-01-27 11:00:00', 10.2, 20.1, 5.0, 2.5, 1.0, 0.0, 0.0, 0.0, 'active', '{"type": "conveyor", "speed": 1.1}'),
('OBJ_002', '2025-01-27 10:30:00', 14.8, 24.8, 5.5, 3.0, 0.0, 1.0, 0.0, 90.0, 'active', '{"type": "robot", "model": "KUKA", "payload": 50}'),
('OBJ_004', '2025-01-27 09:00:00', 25.0, 35.0, 5.2, 2.2, -1.0, 0.0, 0.0, 180.0, 'inactive', '{"type": "packaging", "rate": 0}'),
('OBJ_004', '2025-01-27 10:00:00', 25.0, 35.0, 5.2, 2.2, -1.0, 0.0, 0.0, 180.0, 'processing', '{"type": "packaging", "rate": 30}');
