"""
End-to-end integration test simulating the entire autonomous platform pipeline:
Sensor reading -> Risk detection -> Action plan proposal ->
Farmer approval -> Task creation -> Execution -> Completion -> Immutable activity audit log.
"""

from datetime import datetime, timezone
import pytest
from sqlalchemy import select

from Database.models.user import User, UserRole
from Database.models.farm import Farm
from Database.models.field import Field, FieldStatus
from Database.models.sensor import Sensor, SensorType
from Database.models.sensor_reading import SensorReading
from Database.models.risk import Risk, RiskType, RiskSeverity, RiskStatus
from Database.models.ai_advisory import AIAdvisory, AdvisoryStatus
from Database.models.action_plan import ActionPlan, ActionPlanStatus, ActionPriority
from Database.models.task import Task, TaskStatus, TaskPriority
from Database.models.activity_log import ActivityLog
from Database.repositories.action_plan_repository import ActionPlanRepository
from Database.repositories.task_repository import TaskRepository
from Database.repositories.activity_log_repository import ActivityLogRepository



@pytest.mark.asyncio
async def test_full_pipeline_e2e(db_session):
    """
    Simulate full platform flow:
    1. Sensor reading indicates severe drought / moisture drop.
    2. Risk Agent records WATER_STRESS risk.
    3. Action Planner generates AI advisory and Action Plan.
    4. Farmer approves action plan (atomic transaction creates Task).
    5. IoT/Worker picks up task and marks it IN_PROGRESS, then COMPLETED.
    6. System logs immutable audit trail in activity_logs.
    """
    # Step 0: Setup Farmer, Farm, Field, Sensor
    farmer = User(
        id="usr-e2e-01",
        name="Kishanbhai Patel",
        email="kishan@e2e.test",
        phone="+919876543210",
        password_hash="pwd",
        role=UserRole.FARMER,
    )
    farm = Farm(
        id="farm-e2e-01",
        owner_id=farmer.id,
        name="GreenValley Smart Farm",
        location="Rajkot, Gujarat",
        latitude=22.3039,
        longitude=70.8022,
        area=10.0,
    )
    field = Field(
        id="field-e2e-01",
        farm_id=farm.id,
        name="Field A (Cotton South)",
        area=3.5,
        status=FieldStatus.ACTIVE,
    )
    sensor = Sensor(
        id="sns-e2e-01",
        field_id=field.id,
        device_id="ESP32-NODE-SOIL-01",
        sensor_type=SensorType.SOIL_MOISTURE,
    )
    db_session.add_all([farmer, farm, field, sensor])
    await db_session.flush()

    # Step 1: Telemetry ingestion (Moisture drops to 14.8% < threshold 25%)
    reading = SensorReading(
        sensor_id=sensor.id,
        timestamp=datetime.now(timezone.utc),
        value=14.8,
        unit="%",
        reading_metadata={"rssi": -65, "battery": 3.8},
    )
    db_session.add(reading)
    await db_session.flush()
    assert reading.id is not None

    # Step 2: Risk Agent flags WATER_STRESS
    risk = Risk(
        id="rsk-e2e-01",
        field_id=field.id,
        risk_type=RiskType.WATER_STRESS,
        severity=RiskSeverity.HIGH,
        confidence=0.96,
        evidence={"sensor_reading": 14.8, "threshold": 25.0, "deficiency": 10.2},
        explanation="Field A root zone moisture dropped below wilting point (15%).",
        status=RiskStatus.ACTIVE,
    )
    db_session.add(risk)
    await db_session.flush()
    assert risk.id == "rsk-e2e-01"

    # Step 3: AI Advisory & Action Plan generation
    advisory = AIAdvisory(
        id="adv-e2e-01",
        field_id=field.id,
        risk_id=risk.id,
        title="Emergency Drip Irrigation",
        recommendation="Activate Solenoid Valve 1 for 45 minutes to restore root zone moisture to 35%.",
        reasoning="Weather forecast confirms 0% precipitation for the next 48 hours; irrigation is required.",
        confidence=0.95,
        status=AdvisoryStatus.ACTIVE,
    )
    action_plan = ActionPlan(
        id="act-e2e-01",
        field_id=field.id,
        risk_id=risk.id,
        advisory_id=advisory.id,
        action="Initiate 45-minute pressurized drip cycle on Field A",
        duration="45 mins",
        estimated_cost=250.0,
        required_resources={"water_volume_liters": 1500, "power_source": "Solar/Grid"},
        weather_window="Clear sky, low wind",
        priority=ActionPriority.HIGH,
        confidence=0.95,
        status=ActionPlanStatus.PENDING_APPROVAL,
    )
    db_session.add_all([advisory, action_plan])
    await db_session.flush()

    # Step 4: Farmer Approves Plan -> Atomic Task Creation
    plan_repo = ActionPlanRepository(db_session)
    approved_plan, task = await plan_repo.approve_and_dispatch_task(
        action_plan_id=action_plan.id,
        user_id=farmer.id,
    )
    assert approved_plan.status == ActionPlanStatus.APPROVED
    assert task is not None
    assert task.action_plan_id == action_plan.id
    assert task.status == TaskStatus.PENDING

    # Step 5: IoT/Worker Executes Task
    task_repo = TaskRepository(db_session)
    executing_task = await task_repo.update_status(task.id, TaskStatus.IN_PROGRESS)
    assert executing_task.status == TaskStatus.IN_PROGRESS
    assert executing_task.started_at is not None

    completed_task = await task_repo.update_status(task.id, TaskStatus.COMPLETED)
    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.completed_at is not None

    # Step 6: Verify Immutable Activity Audit Trail
    act_repo = ActivityLogRepository(db_session)
    log_entry = await act_repo.log_activity(
        user_id=farmer.id,
        farm_id=farm.id,
        field_id=field.id,
        event_type="TASK_COMPLETED",
        description=f"Automated drip cycle completed successfully for {completed_task.title}.",
        entity_type="Task",
        entity_id=completed_task.id,
        metadata={"duration_mins": 45, "liters_delivered": 1500},
    )
    assert log_entry.id is not None
    assert log_entry.event_type == "TASK_COMPLETED"

    # Step 7: Final Query Verification
    res = await db_session.execute(
        select(ActivityLog).where(ActivityLog.entity_id == completed_task.id)
    )
    saved_log = res.scalar_one()
    assert saved_log.description.startswith("Automated drip cycle completed")
    assert saved_log.metadata_json["liters_delivered"] == 1500
