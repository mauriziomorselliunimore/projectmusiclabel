-- Drop all tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Grant privileges
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
