-- Create n8n database for docker-compose setup
-- Run this in PostgreSQL container or via psql

CREATE DATABASE n8n;

-- Grant permissions (adjust as needed)
GRANT ALL PRIVILEGES ON DATABASE n8n TO postgres;

