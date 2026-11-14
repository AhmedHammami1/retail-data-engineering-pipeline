CREATE SCHEMA IF NOT EXISTS dw;

-- Set the default schema for this session
SET search_path TO dw;

-- Verify schema creation
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'dw';