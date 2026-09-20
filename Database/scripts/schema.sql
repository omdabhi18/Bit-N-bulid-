-- ====================================================================
-- KrishiNetra AI: Complete PostgreSQL Production Schema
-- Autonomous Farm-to-Field Advisory & Action Orchestration Platform
-- ====================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(30) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'FARMER' CHECK (role IN ('FARMER', 'EXPERT', 'ADMIN')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);

-- 2. FARMS TABLE
CREATE TABLE IF NOT EXISTS farms (
    id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    farmer_name VARCHAR(120) NOT NULL,
    village VARCHAR(100) DEFAULT 'Ribda',
    taluka VARCHAR(100) DEFAULT 'Gondal',
    district VARCHAR(100) DEFAULT 'Rajkot',
    state VARCHAR(100) DEFAULT 'Gujarat',
    latitude DOUBLE PRECISION DEFAULT 21.9619,
    longitude DOUBLE PRECISION DEFAULT 70.7923,
    area DOUBLE PRECISION DEFAULT 12.5,
    soil_type VARCHAR(150) DEFAULT 'Medium Black Clayey Loam (કાળી જમીન)',
    irrigation_method VARCHAR(150) DEFAULT 'Drip Automation + Tube Well',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_farms_owner ON farms(owner_id);

-- 3. FIELDS TABLE
CREATE TABLE IF NOT EXISTS fields (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    area VARCHAR(50) DEFAULT '5.0 Acres',
    crop_name VARCHAR(100) NOT NULL,
    stage VARCHAR(100) DEFAULT 'Flowering',
    health_score INTEGER DEFAULT 80 CHECK (health_score BETWEEN 0 AND 100),
    soil_moisture DOUBLE PRECISION DEFAULT 35.0,
    status VARCHAR(30) DEFAULT 'WARNING' CHECK (status IN ('HEALTHY', 'WARNING', 'CRITICAL')),
    risk_category VARCHAR(100) DEFAULT 'Water Stress',
    pest_risk VARCHAR(50) DEFAULT 'Low (15%)',
    soil_ph DOUBLE PRECISION DEFAULT 6.8,
    nitrogen VARCHAR(50) DEFAULT 'Normal',
    phosphorus VARCHAR(50) DEFAULT 'Optimal',
    potassium VARCHAR(50) DEFAULT 'High',
    boundary JSONB DEFAULT '[]'::jsonb,
    color VARCHAR(20) DEFAULT '#eab308',
    drip_status VARCHAR(50) DEFAULT 'Ready',
    recommendation VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_fields_farm ON fields(farm_id);
CREATE INDEX IF NOT EXISTS idx_fields_status ON fields(status);

-- 4. CROPS TABLE
CREATE TABLE IF NOT EXISTS crops (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    crop_name VARCHAR(100) NOT NULL,
    variety VARCHAR(100) NOT NULL,
    sowing_date VARCHAR(50) DEFAULT '2026-06-15',
    expected_harvest_date VARCHAR(50) DEFAULT '2026-11-20',
    current_stage VARCHAR(100) NOT NULL,
    health_status VARCHAR(50) DEFAULT 'Good',
    area DOUBLE PRECISION DEFAULT 5.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_crops_farm ON crops(farm_id);

-- 5. SENSORS TABLE
CREATE TABLE IF NOT EXISTS sensors (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    device_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    sensor_type VARCHAR(50) DEFAULT 'SOIL_MOISTURE',
    battery INTEGER DEFAULT 95 CHECK (battery BETWEEN 0 AND 100),
    signal_strength VARCHAR(50) DEFAULT 'Excellent (4G IoT)',
    status VARCHAR(30) DEFAULT 'ONLINE' CHECK (status IN ('ONLINE', 'OFFLINE', 'STANDBY')),
    last_seen VARCHAR(50) DEFAULT 'Just now',
    configuration JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_sensors_device ON sensors(device_id);
CREATE INDEX IF NOT EXISTS idx_sensors_farm ON sensors(farm_id);

-- 6. SENSOR READINGS TABLE (HIGH VOLUME TIME-SERIES)
CREATE TABLE IF NOT EXISTS sensor_readings (
    id VARCHAR(36) PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    field_id VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    soil_moisture DOUBLE PRECISION DEFAULT 31.4,
    soil_temperature DOUBLE PRECISION DEFAULT 27.8,
    soil_ph DOUBLE PRECISION DEFAULT 6.8,
    soil_ec DOUBLE PRECISION DEFAULT 0.42,
    nitrogen DOUBLE PRECISION DEFAULT 82.0,
    phosphorus DOUBLE PRECISION DEFAULT 14.0,
    potassium DOUBLE PRECISION DEFAULT 185.0,
    air_temperature DOUBLE PRECISION DEFAULT 33.2,
    air_humidity DOUBLE PRECISION DEFAULT 58.0,
    value DOUBLE PRECISION,
    unit VARCHAR(30) DEFAULT '%',
    reading_metadata JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_timestamp ON sensor_readings(sensor_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);

-- 7. WEATHER DATA TABLE
CREATE TABLE IF NOT EXISTS weather_data (
    id VARCHAR(36) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    location VARCHAR(120) DEFAULT 'Rajkot, Gujarat',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    temperature DOUBLE PRECISION DEFAULT 33.0,
    humidity DOUBLE PRECISION DEFAULT 58.0,
    rainfall_probability INTEGER DEFAULT 12,
    rainfall DOUBLE PRECISION DEFAULT 0.0,
    wind_speed DOUBLE PRECISION DEFAULT 14.0,
    wind_direction VARCHAR(30) DEFAULT 'SW',
    weather_condition VARCHAR(100) DEFAULT 'Mostly Sunny',
    uv_index INTEGER DEFAULT 8,
    dew_point DOUBLE PRECISION DEFAULT 22.0,
    et0 VARCHAR(30) DEFAULT '5.8 mm/day',
    advisory VARCHAR(255) DEFAULT 'Favorable conditions for drip irrigation this evening.',
    source VARCHAR(50) DEFAULT 'IMD / Hyperlocal Station',
    hourly_forecast JSONB DEFAULT '[]'::jsonb,
    daily_forecast JSONB DEFAULT '[]'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_weather_farm ON weather_data(farm_id);

-- 8. MARKET PRICES TABLE
CREATE TABLE IF NOT EXISTS market_prices (
    id VARCHAR(50) PRIMARY KEY,
    crop VARCHAR(100) NOT NULL,
    mandi VARCHAR(100) DEFAULT 'Rajkot APMC',
    location VARCHAR(100) DEFAULT 'Rajkot, Gujarat',
    price DOUBLE PRECISION DEFAULT 7380.0,
    unit VARCHAR(50) DEFAULT '₹ / Quintal (100 kg)',
    change_7d DOUBLE PRECISION DEFAULT 4.2,
    trend VARCHAR(20) DEFAULT 'UP',
    msp_price DOUBLE PRECISION DEFAULT 7122.0,
    ai_recommendation VARCHAR(255) DEFAULT '',
    nearby_markets JSONB DEFAULT '[]'::jsonb,
    price_history JSONB DEFAULT '[]'::jsonb,
    source VARCHAR(50) DEFAULT 'Agmarknet',
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_market_crop ON market_prices(crop);

-- 9. RISKS TABLE
CREATE TABLE IF NOT EXISTS risks (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    category VARCHAR(120) NOT NULL,
    risk_type VARCHAR(50) NOT NULL DEFAULT 'WATER_STRESS' CHECK (risk_type IN ('WATER_STRESS', 'PEST', 'DISEASE', 'NUTRIENT_DEFICIENCY', 'WEATHER', 'MARKET')),
    severity VARCHAR(20) NOT NULL DEFAULT 'HIGH' CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    confidence INTEGER DEFAULT 85 CHECK (confidence BETWEEN 0 AND 100),
    evidence JSONB DEFAULT '[]'::jsonb,
    explanation VARCHAR(500) DEFAULT '',
    recommended_action VARCHAR(255) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'RESOLVED', 'MITIGATED')),
    plan_generated BOOLEAN DEFAULT FALSE,
    plan_id VARCHAR(50),
    icon VARCHAR(50) DEFAULT 'Droplets',
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_risks_farm ON risks(farm_id);
CREATE INDEX IF NOT EXISTS idx_risks_type_status ON risks(risk_type, status);

-- 10. AI ADVISORIES TABLE
CREATE TABLE IF NOT EXISTS ai_advisories (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    risk_id VARCHAR(50) REFERENCES risks(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    title_gu VARCHAR(200),
    title_hi VARCHAR(200),
    recommendation VARCHAR(500) NOT NULL,
    reasoning VARCHAR(1000) DEFAULT '',
    priority VARCHAR(30) DEFAULT 'High',
    confidence INTEGER DEFAULT 90,
    status VARCHAR(30) DEFAULT 'PENDING_APPROVAL' CHECK (status IN ('PENDING_APPROVAL', 'APPROVED', 'REJECTED')),
    timestamp VARCHAR(50) DEFAULT 'Today',
    orchestrator_summary VARCHAR(500) NOT NULL,
    explainability JSONB DEFAULT '{}'::jsonb,
    action_details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_advisories_farm ON ai_advisories(farm_id);

-- 11. ACTION PLANS TABLE
CREATE TABLE IF NOT EXISTS action_plans (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    risk_id VARCHAR(50) REFERENCES risks(id) ON DELETE SET NULL,
    advisory_id VARCHAR(50) REFERENCES ai_advisories(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    target_field VARCHAR(150) DEFAULT 'Field A (Cotton - 5.2 Acres)',
    action VARCHAR(200) NOT NULL,
    action_type VARCHAR(150) NOT NULL,
    scheduled_time VARCHAR(100) DEFAULT 'Today • 18:00 IST',
    duration VARCHAR(50) DEFAULT '35 Minutes',
    estimated_cost DOUBLE PRECISION DEFAULT 45.0,
    water_volume VARCHAR(50) DEFAULT '2,500 L',
    required_resources VARCHAR(200) DEFAULT '2,500 L water, tube well pump',
    weather_window VARCHAR(150) DEFAULT 'Safe (Rain prob 12%, Wind 14 km/h)',
    safety_constraints VARCHAR(200) DEFAULT 'Electrical line grounding verified',
    constraints JSONB DEFAULT '{}'::jsonb,
    hardware_target VARCHAR(120) DEFAULT 'Solenoid Valve SV-01 (Field A)',
    assigned_to VARCHAR(120) DEFAULT 'Kishanbhai Patel',
    priority VARCHAR(30) DEFAULT 'High',
    confidence INTEGER DEFAULT 92,
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'PENDING_APPROVAL', 'APPROVED', 'SCHEDULED', 'EXECUTING', 'COMPLETED', 'FAILED', 'CANCELLED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_plans_farm_status ON action_plans(farm_id, status);

-- 12. TASKS TABLE
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(36) NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE CASCADE,
    action_plan_id VARCHAR(50) REFERENCES action_plans(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(500) DEFAULT '',
    assigned_to VARCHAR(120) DEFAULT 'Kishanbhai Patel',
    priority VARCHAR(30) DEFAULT 'High',
    status VARCHAR(30) NOT NULL DEFAULT 'TODO' CHECK (status IN ('TODO', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    due_at VARCHAR(50) DEFAULT 'Today 18:00',
    due_time VARCHAR(50) DEFAULT 'Today 18:00',
    icon VARCHAR(50) DEFAULT 'CheckCircle',
    notes VARCHAR(500) DEFAULT '',
    failure_reason VARCHAR(255),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_tasks_farm_status ON tasks(farm_id, status);

-- 13. DISEASE ANALYSES TABLE
CREATE TABLE IF NOT EXISTS disease_analyses (
    id VARCHAR(50) PRIMARY KEY,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE SET NULL,
    crop VARCHAR(100) NOT NULL,
    disease VARCHAR(150) NOT NULL,
    disease_name VARCHAR(150) NOT NULL,
    disease_name_gu VARCHAR(150),
    pest VARCHAR(150),
    confidence INTEGER DEFAULT 85 CHECK (confidence BETWEEN 0 AND 100),
    severity VARCHAR(30) DEFAULT 'High',
    image_url VARCHAR(500) NOT NULL,
    analysis VARCHAR(1000) DEFAULT '',
    symptoms JSONB DEFAULT '[]'::jsonb,
    recommendation VARCHAR(1000) DEFAULT '',
    recommended_remedy JSONB DEFAULT '{}'::jsonb,
    expert_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_disease_crop ON disease_analyses(crop);

-- 14. EXPERT REQUESTS TABLE
CREATE TABLE IF NOT EXISTS expert_requests (
    id VARCHAR(50) PRIMARY KEY,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE SET NULL,
    disease_analysis_id VARCHAR(50) REFERENCES disease_analyses(id) ON DELETE SET NULL,
    risk_id VARCHAR(50) REFERENCES risks(id) ON DELETE SET NULL,
    requested_by VARCHAR(120) DEFAULT 'Kishanbhai Patel',
    assigned_expert VARCHAR(150) DEFAULT 'Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)',
    field_name VARCHAR(100) DEFAULT 'Field B (Wheat)',
    crop VARCHAR(100) DEFAULT 'Wheat',
    issue VARCHAR(255) NOT NULL,
    ai_confidence INTEGER DEFAULT 58,
    reason VARCHAR(500) DEFAULT '',
    status VARCHAR(30) DEFAULT 'REVIEW_PENDING' CHECK (status IN ('REVIEW_PENDING', 'IN_REVIEW', 'RESOLVED')),
    expert_response VARCHAR(1000) DEFAULT '',
    agronomist_notes VARCHAR(1000) DEFAULT '',
    telemetry_snapshot JSONB DEFAULT '{}'::jsonb,
    submitted_at VARCHAR(50) DEFAULT 'Just now',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_expert_status ON expert_requests(status);

-- 15. AGENT RUNS TABLE
CREATE TABLE IF NOT EXISTS agent_runs (
    id VARCHAR(36) PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    field_id VARCHAR(50),
    role VARCHAR(150) DEFAULT 'Specialized Autonomous Agent',
    status VARCHAR(30) DEFAULT 'COMPLETED' CHECK (status IN ('ACTIVE', 'COMPLETED', 'FAILED')),
    confidence INTEGER DEFAULT 95,
    input_summary VARCHAR(500) DEFAULT '',
    output_summary VARCHAR(500) DEFAULT '',
    inputs JSONB DEFAULT '[]'::jsonb,
    outputs JSONB DEFAULT '[]'::jsonb,
    execution_time_ms INTEGER DEFAULT 120,
    error_message VARCHAR(500),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_agent_runs_name ON agent_runs(agent_name);

-- 16. ALERTS TABLE
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE SET NULL,
    type VARCHAR(50) DEFAULT 'WATER_DEFICIT',
    severity VARCHAR(30) DEFAULT 'WARNING' CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
    title VARCHAR(200) NOT NULL,
    message VARCHAR(500) NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_alerts_user_read ON alerts(user_id, read);

-- 17. NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) DEFAULT 'ACTION_REQUIRED',
    channel VARCHAR(30) DEFAULT 'WEB' CHECK (channel IN ('WEB', 'SMS', 'WHATSAPP', 'EMAIL')),
    title VARCHAR(200) NOT NULL,
    message VARCHAR(500) NOT NULL,
    status VARCHAR(30) DEFAULT 'SENT' CHECK (status IN ('PENDING', 'SENT', 'FAILED')),
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);

-- 18. ACTIVITY LOGS TABLE (AUDIT TRAIL)
CREATE TABLE IF NOT EXISTS activity_logs (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    farm_id VARCHAR(36) REFERENCES farms(id) ON DELETE CASCADE,
    field_id VARCHAR(50) REFERENCES fields(id) ON DELETE SET NULL,
    agent VARCHAR(100) DEFAULT 'Master Orchestrator',
    event VARCHAR(500) NOT NULL,
    event_type VARCHAR(100) DEFAULT 'ORCHESTRATION_DECISION',
    description VARCHAR(500) DEFAULT '',
    entity_type VARCHAR(50),
    entity_id VARCHAR(50),
    time VARCHAR(50) DEFAULT 'Just now',
    severity VARCHAR(20) DEFAULT 'info' CHECK (severity IN ('info', 'success', 'warning', 'error')),
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_activity_logs_farm ON activity_logs(farm_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_activity_logs_event_type ON activity_logs(event_type);
