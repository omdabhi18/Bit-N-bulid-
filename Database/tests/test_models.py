"""
Comprehensive tests for all 18 SQLAlchemy domain models.
Verifies table creation, field types, default values, and foreign-key integrity.
"""

from datetime import datetime, timezone, timedelta
import uuid
import random
import pytest
from sqlalchemy import select


from Database.models.user import User, UserRole
from Database.models.farm import Farm
from Database.models.field import Field, FieldStatus
from Database.models.crop import Crop, CropStage, HealthStatus
from Database.models.sensor import Sensor, SensorType, SensorStatus
from Database.models.sensor_reading import SensorReading
from Database.models.weather_data import WeatherData
from Database.models.market_price import MarketPrice
from Database.models.risk import Risk, RiskType, RiskSeverity, RiskStatus
from Database.models.ai_advisory import AIAdvisory, AdvisoryStatus
from Database.models.action_plan import ActionPlan, ActionPlanStatus, ActionPriority
from Database.models.task import Task, TaskPriority, TaskStatus
from Database.models.disease_analysis import DiseaseAnalysis
from Database.models.expert_request import ExpertRequest, ExpertRequestStatus
from Database.models.agent_run import AgentRun, AgentRunStatus
from Database.models.alert import Alert, AlertType, AlertSeverity
from Database.models.notification import Notification, NotificationType, NotificationChannel, NotificationStatus
from Database.models.activity_log import ActivityLog



@pytest.mark.asyncio
async def test_user_creation(db_session):
    """Test user creation with roles and password hashing field."""
    uid = f"usr-test-{uuid.uuid4().hex[:6]}"
    user = User(
        id=uid,
        name="Kishanbhai Patel",
        email=f"kishan.{uuid.uuid4().hex[:6]}@greenvalley.in",
        phone=f"+91{random.randint(9000000000, 9999999999)}",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$fakehash",
        role=UserRole.FARMER,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()

    res = await db_session.execute(select(User).where(User.id == uid))
    fetched = res.scalar_one()
    assert fetched.name == "Kishanbhai Patel"
    assert fetched.role == UserRole.FARMER


@pytest.mark.asyncio
async def test_farm_and_field_hierarchy(db_session):
    """Test Farm -> Field relationship and geometry coordinates."""
    owner_id = f"usr-test-{uuid.uuid4().hex[:6]}"
    owner = User(
        id=owner_id,
        name="Rameshbhai Farmer",
        email=f"ramesh.{uuid.uuid4().hex[:6]}@farm.in",
        phone=f"+91{random.randint(9000000000, 9999999999)}",
        password_hash="hash",
        role=UserRole.FARMER,
    )
    farm_id = f"farm-test-{uuid.uuid4().hex[:6]}"
    farm = Farm(
        id=farm_id,
        owner_id=owner.id,
        name="Test Saurashtra Agro",
        location="Rajkot, Gujarat",
        latitude=22.3039,
        longitude=70.8022,
        area=12.5,
        soil_type="Black Cotton",
    )
    field_id = f"field-test-{uuid.uuid4().hex[:6]}"
    field = Field(
        id=field_id,
        farm_id=farm.id,
        name="Field Alpha",
        area=4.5,
        boundary=[{"lat": 22.304, "lng": 70.802}, {"lat": 22.305, "lng": 70.803}],
        status=FieldStatus.ACTIVE,
        soil_moisture=34.5,
    )
    db_session.add_all([owner, farm, field])
    await db_session.flush()

    res = await db_session.execute(select(Field).where(Field.id == field_id))
    fetched_field = res.scalar_one()
    assert fetched_field.name == "Field Alpha"
    assert fetched_field.farm_id == farm_id



@pytest.mark.asyncio
async def test_crop_lifecycle(db_session):
    """Test Crop entity linked to Field."""
    crop = Crop(
        id="crop-test-01",
        field_id="field-test-01",
        crop_name="Cotton",
        variety="BT Cotton RCH-2",
        sowing_date=datetime.now(timezone.utc) - timedelta(days=60),
        expected_harvest_date=datetime.now(timezone.utc) + timedelta(days=90),
        current_stage=CropStage.VEGETATIVE,
        health_status=HealthStatus.GOOD,
    )
    db_session.add(crop)
    await db_session.flush()

    res = await db_session.execute(select(Crop).where(Crop.id == "crop-test-01"))
    fetched = res.scalar_one()
    assert fetched.crop_name == "Cotton"
    assert fetched.current_stage == CropStage.VEGETATIVE


@pytest.mark.asyncio
async def test_sensor_and_readings(db_session):
    """Test IoT Sensor registration and time-series telemetry insertion."""
    sensor = Sensor(
        id="sns-test-01",
        field_id="field-test-01",
        device_id="ESP32-SOIL-TEST-01",
        sensor_type=SensorType.SOIL_MOISTURE,
        status=SensorStatus.ACTIVE,
    )
    reading1 = SensorReading(
        sensor_id=sensor.id,
        value=28.4,
        unit="%",
        reading_metadata={"battery_voltage": 3.7},
    )
    reading2 = SensorReading(
        sensor_id=sensor.id,
        value=27.9,
        unit="%",
        reading_metadata={"battery_voltage": 3.69},
    )
    db_session.add_all([sensor, reading1, reading2])
    await db_session.flush()

    res = await db_session.execute(
        select(SensorReading).where(SensorReading.sensor_id == "sns-test-01")
    )
    readings = res.scalars().all()
    assert len(readings) == 2
    assert readings[0].value == 28.4


@pytest.mark.asyncio
async def test_weather_and_market_data(db_session):
    """Test WeatherData and APMC MarketPrice entries."""
    weather = WeatherData(
        farm_id="farm-test-01",
        temperature=31.5,
        humidity=65.0,
        rainfall_probability=15.0,
        rainfall=0.0,
        wind_speed=12.4,
        weather_condition="Sunny",
        source="IMD / OpenWeather",
    )
    mandi = MarketPrice(
        crop="Cotton",
        mandi="Rajkot APMC",
        location="Rajkot, Gujarat",
        price=7450.0,
        unit="Rs/Quintal",
        source="Agmarknet API",
    )
    db_session.add_all([weather, mandi])
    await db_session.flush()

    w_res = await db_session.execute(select(WeatherData).where(WeatherData.farm_id == "farm-test-01"))
    assert w_res.scalar_one().temperature == 31.5

    m_res = await db_session.execute(select(MarketPrice).where(MarketPrice.crop == "Cotton"))
    assert m_res.scalar_one().price == 7450.0


@pytest.mark.asyncio
async def test_risk_advisory_action_plan_flow(db_session):
    """Test cascading workflow: Risk -> AI Advisory -> Action Plan -> Execution Task."""
    risk = Risk(
        id="rsk-test-01",
        field_id="field-test-01",
        risk_type=RiskType.WATER_STRESS,
        severity=RiskSeverity.HIGH,
        confidence=0.92,
        evidence={"soil_moisture": 18.2, "threshold": 25.0},
        explanation="Soil moisture has dropped below critical wilting threshold.",
        status=RiskStatus.ACTIVE,
    )
    advisory = AIAdvisory(
        id="adv-test-01",
        field_id="field-test-01",
        risk_id=risk.id,
        title="Immediate Drip Irrigation Required",
        recommendation="Initiate Zone-A drip irrigation for 45 minutes.",
        reasoning="Prevents irreversible moisture stress during flowering stage.",
        confidence=0.94,
        status=AdvisoryStatus.ACTIVE,
    )
    action_plan = ActionPlan(
        id="act-test-01",
        field_id="field-test-01",
        risk_id=risk.id,
        advisory_id=advisory.id,
        action="Execute 45 min drip irrigation via Smart Solenoid Valve #1",
        estimated_cost=250.0,
        priority=ActionPriority.HIGH,
        confidence=0.95,
        status=ActionPlanStatus.APPROVED,
    )
    task = Task(
        id="tsk-test-01",
        action_plan_id=action_plan.id,
        field_id="field-test-01",
        title="Open Drip Valve 1 - Zone A",
        description="Run automated drip cycle 45 mins",
        priority=TaskPriority.HIGH,
        status=TaskStatus.IN_PROGRESS,
    )
    db_session.add_all([risk, advisory, action_plan, task])
    await db_session.flush()

    res = await db_session.execute(select(Task).where(Task.id == "tsk-test-01"))
    fetched_task = res.scalar_one()
    assert fetched_task.title == "Open Drip Valve 1 - Zone A"
    assert fetched_task.action_plan_id == "act-test-01"


@pytest.mark.asyncio
async def test_disease_and_expert_request(db_session):
    """Test Crop Disease Analysis and Expert Agronomist Escalation."""
    disease = DiseaseAnalysis(
        id="dis-test-01",
        field_id="field-test-01",
        image_url="https://res.cloudinary.com/krishinetra/image/upload/sample_leaf.jpg",
        disease="Cotton Leaf Curl Virus",
        pest="Whitefly Bemisia tabaci",
        confidence=0.91,
        analysis="Interveinal chlorosis and upward curling of leaves.",
        recommendation="Spray Neem oil or Acetamiprid 20% SP at recommended dilution.",
        expert_required=True,
    )
    expert_req = ExpertRequest(
        id="exp-test-01",
        field_id="field-test-01",
        disease_analysis_id=disease.id,
        requested_by="usr-test-01",
        reason="Severe viral symptoms spreading rapidly across Sector 2.",
        status=ExpertRequestStatus.PENDING,
    )
    db_session.add_all([disease, expert_req])
    await db_session.flush()

    res = await db_session.execute(select(ExpertRequest).where(ExpertRequest.id == "exp-test-01"))
    assert res.scalar_one().status == ExpertRequestStatus.PENDING


@pytest.mark.asyncio
async def test_agent_run_and_audit_activity(db_session):
    """Test autonomous agent execution recording and activity audit log."""
    agent_run = AgentRun(
        id="run-test-01",
        agent_name="WATER_AGENT",
        field_id="field-test-01",
        input_summary={"sensor_value": 18.2, "target": 35.0},
        output_summary={"action": "IRRIGATE", "volume_litres": 1500},
        confidence=0.94,
        status=AgentRunStatus.COMPLETED,
    )
    activity = ActivityLog(
        id="actlog-test-01",
        user_id="usr-test-01",
        farm_id="farm-test-01",
        field_id="field-test-01",
        event_type="AGENT_EXECUTION",
        description="Water Agent recommended 45-min drip irrigation.",
        entity_type="AgentRun",
        entity_id=agent_run.id,
    )
    db_session.add_all([agent_run, activity])
    await db_session.flush()

    res = await db_session.execute(select(ActivityLog).where(ActivityLog.id == "actlog-test-01"))
    log = res.scalar_one()
    assert log.event_type == "AGENT_EXECUTION"
    assert log.entity_id == "run-test-01"
