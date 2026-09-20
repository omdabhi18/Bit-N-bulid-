"""001_initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-20 13:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('phone', sa.String(length=30), unique=True, nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='FARMER'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 2. farms
    op.create_table(
        'farms',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('owner_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('farmer_name', sa.String(length=120), nullable=False),
        sa.Column('village', sa.String(length=100), server_default='Ribda'),
        sa.Column('taluka', sa.String(length=100), server_default='Gondal'),
        sa.Column('district', sa.String(length=100), server_default='Rajkot'),
        sa.Column('state', sa.String(length=100), server_default='Gujarat'),
        sa.Column('latitude', sa.Float(), server_default='21.9619'),
        sa.Column('longitude', sa.Float(), server_default='70.7923'),
        sa.Column('area', sa.Float(), server_default='12.5'),
        sa.Column('soil_type', sa.String(length=150), server_default='Medium Black Clayey Loam (કાળી જમીન)'),
        sa.Column('irrigation_method', sa.String(length=150), server_default='Drip Automation + Tube Well'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 3. fields
    op.create_table(
        'fields',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('area', sa.String(length=50), server_default='5.0 Acres'),
        sa.Column('crop_name', sa.String(length=100), nullable=False),
        sa.Column('stage', sa.String(length=100), server_default='Flowering'),
        sa.Column('health_score', sa.Integer(), server_default='80'),
        sa.Column('soil_moisture', sa.Float(), server_default='35.0'),
        sa.Column('status', sa.String(length=30), server_default='WARNING'),
        sa.Column('risk_category', sa.String(length=100), server_default='Water Stress'),
        sa.Column('pest_risk', sa.String(length=50), server_default='Low (15%)'),
        sa.Column('soil_ph', sa.Float(), server_default='6.8'),
        sa.Column('nitrogen', sa.String(length=50), server_default='Normal'),
        sa.Column('phosphorus', sa.String(length=50), server_default='Optimal'),
        sa.Column('potassium', sa.String(length=50), server_default='High'),
        sa.Column('boundary', sa.JSON(), nullable=True),
        sa.Column('color', sa.String(length=20), server_default='#eab308'),
        sa.Column('drip_status', sa.String(length=50), server_default='Ready'),
        sa.Column('recommendation', sa.String(length=255), server_default=''),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 4. crops
    op.create_table(
        'crops',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('crop_name', sa.String(length=100), nullable=False),
        sa.Column('variety', sa.String(length=100), nullable=False),
        sa.Column('sowing_date', sa.String(length=50), server_default='2026-06-15'),
        sa.Column('expected_harvest_date', sa.String(length=50), server_default='2026-11-20'),
        sa.Column('current_stage', sa.String(length=100), nullable=False),
        sa.Column('health_status', sa.String(length=50), server_default='Good'),
        sa.Column('area', sa.Float(), server_default='5.0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 5. sensors
    op.create_table(
        'sensors',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('device_id', sa.String(length=100), unique=True, nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('sensor_type', sa.String(length=50), server_default='SOIL_MOISTURE'),
        sa.Column('battery', sa.Integer(), server_default='95'),
        sa.Column('signal_strength', sa.String(length=50), server_default='Excellent (4G IoT)'),
        sa.Column('status', sa.String(length=30), server_default='ONLINE'),
        sa.Column('last_seen', sa.String(length=50), server_default='Just now'),
        sa.Column('configuration', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 6. sensor_readings
    op.create_table(
        'sensor_readings',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('sensor_id', sa.String(length=50), sa.ForeignKey('sensors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('soil_moisture', sa.Float(), server_default='31.4'),
        sa.Column('soil_temperature', sa.Float(), server_default='27.8'),
        sa.Column('soil_ph', sa.Float(), server_default='6.8'),
        sa.Column('soil_ec', sa.Float(), server_default='0.42'),
        sa.Column('nitrogen', sa.Float(), server_default='82.0'),
        sa.Column('phosphorus', sa.Float(), server_default='14.0'),
        sa.Column('potassium', sa.Float(), server_default='185.0'),
        sa.Column('air_temperature', sa.Float(), server_default='33.2'),
        sa.Column('air_humidity', sa.Float(), server_default='58.0'),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=30), server_default='%'),
        sa.Column('reading_metadata', sa.JSON(), nullable=True)
    )
    op.create_index('idx_sensor_readings_sensor_timestamp', 'sensor_readings', ['sensor_id', 'timestamp'])

    # 7. weather_data
    op.create_table(
        'weather_data',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('location', sa.String(length=120), server_default='Rajkot, Gujarat'),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('temperature', sa.Float(), server_default='33.0'),
        sa.Column('humidity', sa.Float(), server_default='58.0'),
        sa.Column('rainfall_probability', sa.Integer(), server_default='12'),
        sa.Column('rainfall', sa.Float(), server_default='0.0'),
        sa.Column('wind_speed', sa.Float(), server_default='14.0'),
        sa.Column('wind_direction', sa.String(length=30), server_default='SW'),
        sa.Column('weather_condition', sa.String(length=100), server_default='Mostly Sunny'),
        sa.Column('uv_index', sa.Integer(), server_default='8'),
        sa.Column('dew_point', sa.Float(), server_default='22.0'),
        sa.Column('et0', sa.String(length=30), server_default='5.8 mm/day'),
        sa.Column('advisory', sa.String(length=255), server_default='Favorable conditions for drip irrigation this evening.'),
        sa.Column('source', sa.String(length=50), server_default='IMD / Hyperlocal Station'),
        sa.Column('hourly_forecast', sa.JSON(), nullable=True),
        sa.Column('daily_forecast', sa.JSON(), nullable=True)
    )

    # 8. market_prices
    op.create_table(
        'market_prices',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('crop', sa.String(length=100), nullable=False),
        sa.Column('mandi', sa.String(length=100), server_default='Rajkot APMC'),
        sa.Column('location', sa.String(length=100), server_default='Rajkot, Gujarat'),
        sa.Column('price', sa.Float(), server_default='7380.0'),
        sa.Column('unit', sa.String(length=50), server_default='₹ / Quintal (100 kg)'),
        sa.Column('change_7d', sa.Float(), server_default='4.2'),
        sa.Column('trend', sa.String(length=20), server_default='UP'),
        sa.Column('msp_price', sa.Float(), server_default='7122.0'),
        sa.Column('ai_recommendation', sa.String(length=255), server_default=''),
        sa.Column('nearby_markets', sa.JSON(), nullable=True),
        sa.Column('price_history', sa.JSON(), nullable=True),
        sa.Column('source', sa.String(length=50), server_default='Agmarknet'),
        sa.Column('date', sa.DateTime(), nullable=True)
    )

    # 9. risks
    op.create_table(
        'risks',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('category', sa.String(length=120), nullable=False),
        sa.Column('risk_type', sa.String(length=50), server_default='WATER_STRESS'),
        sa.Column('severity', sa.String(length=20), server_default='HIGH'),
        sa.Column('confidence', sa.Integer(), server_default='85'),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.Column('explanation', sa.String(length=500), server_default=''),
        sa.Column('recommended_action', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=30), server_default='ACTIVE'),
        sa.Column('plan_generated', sa.Boolean(), server_default=sa.false()),
        sa.Column('plan_id', sa.String(length=50), nullable=True),
        sa.Column('icon', sa.String(length=50), server_default='Droplets'),
        sa.Column('detected_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True)
    )

    # 10. ai_advisories
    op.create_table(
        'ai_advisories',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('risk_id', sa.String(length=50), sa.ForeignKey('risks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('title_gu', sa.String(length=200), nullable=True),
        sa.Column('title_hi', sa.String(length=200), nullable=True),
        sa.Column('recommendation', sa.String(length=500), nullable=False),
        sa.Column('reasoning', sa.String(length=1000), server_default=''),
        sa.Column('priority', sa.String(length=30), server_default='High'),
        sa.Column('confidence', sa.Integer(), server_default='90'),
        sa.Column('status', sa.String(length=30), server_default='PENDING_APPROVAL'),
        sa.Column('timestamp', sa.String(length=50), server_default='Today'),
        sa.Column('orchestrator_summary', sa.String(length=500), nullable=False),
        sa.Column('explainability', sa.JSON(), nullable=True),
        sa.Column('action_details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True)
    )

    # 11. action_plans
    op.create_table(
        'action_plans',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('risk_id', sa.String(length=50), sa.ForeignKey('risks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('advisory_id', sa.String(length=50), sa.ForeignKey('ai_advisories.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('target_field', sa.String(length=150), server_default='Field A (Cotton - 5.2 Acres)'),
        sa.Column('action', sa.String(length=200), nullable=False),
        sa.Column('action_type', sa.String(length=150), nullable=False),
        sa.Column('scheduled_time', sa.String(length=100), server_default='Today • 18:00 IST'),
        sa.Column('duration', sa.String(length=50), server_default='35 Minutes'),
        sa.Column('estimated_cost', sa.Float(), server_default='45.0'),
        sa.Column('water_volume', sa.String(length=50), server_default='2,500 L'),
        sa.Column('required_resources', sa.String(length=200), server_default='2,500 L water, tube well pump'),
        sa.Column('weather_window', sa.String(length=150), server_default='Safe (Rain prob 12%, Wind 14 km/h)'),
        sa.Column('safety_constraints', sa.String(length=200), server_default='Electrical line grounding verified'),
        sa.Column('constraints', sa.JSON(), nullable=True),
        sa.Column('hardware_target', sa.String(length=120), server_default='Solenoid Valve SV-01 (Field A)'),
        sa.Column('assigned_to', sa.String(length=120), server_default='Kishanbhai Patel'),
        sa.Column('priority', sa.String(length=30), server_default='High'),
        sa.Column('confidence', sa.Integer(), server_default='92'),
        sa.Column('status', sa.String(length=30), server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 12. tasks
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='CASCADE'), nullable=True),
        sa.Column('action_plan_id', sa.String(length=50), sa.ForeignKey('action_plans.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=500), server_default=''),
        sa.Column('assigned_to', sa.String(length=120), server_default='Kishanbhai Patel'),
        sa.Column('priority', sa.String(length=30), server_default='High'),
        sa.Column('status', sa.String(length=30), server_default='TODO'),
        sa.Column('due_at', sa.String(length=50), server_default='Today 18:00'),
        sa.Column('due_time', sa.String(length=50), server_default='Today 18:00'),
        sa.Column('icon', sa.String(length=50), server_default='CheckCircle'),
        sa.Column('notes', sa.String(length=500), server_default=''),
        sa.Column('failure_reason', sa.String(length=255), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # 13. disease_analyses
    op.create_table(
        'disease_analyses',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True),
        sa.Column('crop', sa.String(length=100), nullable=False),
        sa.Column('disease', sa.String(length=150), nullable=False),
        sa.Column('disease_name', sa.String(length=150), nullable=False),
        sa.Column('disease_name_gu', sa.String(length=150), nullable=True),
        sa.Column('pest', sa.String(length=150), nullable=True),
        sa.Column('confidence', sa.Integer(), server_default='85'),
        sa.Column('severity', sa.String(length=30), server_default='High'),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('analysis', sa.String(length=1000), server_default=''),
        sa.Column('symptoms', sa.JSON(), nullable=True),
        sa.Column('recommendation', sa.String(length=1000), server_default=''),
        sa.Column('recommended_remedy', sa.JSON(), nullable=True),
        sa.Column('expert_required', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # 14. expert_requests
    op.create_table(
        'expert_requests',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True),
        sa.Column('disease_analysis_id', sa.String(length=50), sa.ForeignKey('disease_analyses.id', ondelete='SET NULL'), nullable=True),
        sa.Column('risk_id', sa.String(length=50), sa.ForeignKey('risks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('requested_by', sa.String(length=120), server_default='Kishanbhai Patel'),
        sa.Column('assigned_expert', sa.String(length=150), server_default='Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)'),
        sa.Column('field_name', sa.String(length=100), server_default='Field B (Wheat)'),
        sa.Column('crop', sa.String(length=100), server_default='Wheat'),
        sa.Column('issue', sa.String(length=255), nullable=False),
        sa.Column('ai_confidence', sa.Integer(), server_default='58'),
        sa.Column('reason', sa.String(length=500), server_default=''),
        sa.Column('status', sa.String(length=30), server_default='REVIEW_PENDING'),
        sa.Column('expert_response', sa.String(length=1000), server_default=''),
        sa.Column('agronomist_notes', sa.String(length=1000), server_default=''),
        sa.Column('telemetry_snapshot', sa.JSON(), nullable=True),
        sa.Column('submitted_at', sa.String(length=50), server_default='Just now'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True)
    )

    # 15. agent_runs
    op.create_table(
        'agent_runs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('agent_name', sa.String(length=50), nullable=False),
        sa.Column('field_id', sa.String(length=50), nullable=True),
        sa.Column('role', sa.String(length=150), server_default='Specialized Autonomous Agent'),
        sa.Column('status', sa.String(length=30), server_default='COMPLETED'),
        sa.Column('confidence', sa.Integer(), server_default='95'),
        sa.Column('input_summary', sa.String(length=500), server_default=''),
        sa.Column('output_summary', sa.String(length=500), server_default=''),
        sa.Column('inputs', sa.JSON(), nullable=True),
        sa.Column('outputs', sa.JSON(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), server_default='120'),
        sa.Column('error_message', sa.String(length=500), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True)
    )

    # 16. alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True),
        sa.Column('type', sa.String(length=50), server_default='WATER_DEFICIT'),
        sa.Column('severity', sa.String(length=30), server_default='WARNING'),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.String(length=500), nullable=False),
        sa.Column('read', sa.Boolean(), server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # 17. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('type', sa.String(length=50), server_default='ACTION_REQUIRED'),
        sa.Column('channel', sa.String(length=30), server_default='WEB'),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=30), server_default='SENT'),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # 18. activity_logs
    op.create_table(
        'activity_logs',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('farm_id', sa.String(length=36), sa.ForeignKey('farms.id', ondelete='CASCADE'), nullable=True),
        sa.Column('field_id', sa.String(length=50), sa.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True),
        sa.Column('agent', sa.String(length=100), server_default='Master Orchestrator'),
        sa.Column('event', sa.String(length=500), nullable=False),
        sa.Column('event_type', sa.String(length=100), server_default='ORCHESTRATION_DECISION'),
        sa.Column('description', sa.String(length=500), server_default=''),
        sa.Column('entity_type', sa.String(length=50), nullable=True),
        sa.Column('entity_id', sa.String(length=50), nullable=True),
        sa.Column('time', sa.String(length=50), server_default='Just now'),
        sa.Column('severity', sa.String(length=20), server_default='info'),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

def downgrade() -> None:
    for tbl in [
        'activity_logs', 'notifications', 'alerts', 'agent_runs',
        'expert_requests', 'disease_analyses', 'tasks', 'action_plans',
        'ai_advisories', 'risks', 'market_prices', 'weather_data',
        'sensor_readings', 'sensors', 'crops', 'fields', 'farms', 'users'
    ]:
        op.drop_table(tbl)
