-- ============================================================
-- KrishiNetra AI - PostgreSQL Initialization Script
-- Executed automatically on initial container startup
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Verification notice
DO $$
BEGIN
    RAISE NOTICE 'KrishiNetra PostgreSQL initialized successfully with UUID & Trigram extensions.';
END $$;
