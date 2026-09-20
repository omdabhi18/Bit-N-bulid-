import pytest
from datetime import datetime, timezone
from Database.models.user import User, UserRole
from Database.models.farm import Farm
from Database.models.field import Field, FieldStatus
from Database.models.sensor import Sensor, SensorType
from Database.models.task import Task, TaskPriority, TaskStatus
from Database.repositories.user_repository import UserRepository
from Database.repositories.farm_repository import FarmRepository
from Database.repositories.sensor_repository import SensorRepository
from Database.repositories.task_repository import TaskRepository
from Database.repositories.activity_log_repository import ActivityLogRepository



@pytest.mark.asyncio
async def test_user_repository(db_session):
    repo = UserRepository(db_session)
    user = await repo.create(
        id="usr-repo-01",
        name="Agronomist Dr. Mehta",
        email="mehta@krishinetra.in",
        phone="+919876543299",
        password_hash="secret_hash",
        role=UserRole.EXPERT,
    )
    assert user.id == "usr-repo-01"

    found = await repo.find_by_email("mehta@krishinetra.in")
    assert found is not None
    assert found.name == "Agronomist Dr. Mehta"

    experts = await repo.list_by_role(UserRole.EXPERT)
    assert len(experts) >= 1


@pytest.mark.asyncio
async def test_farm_repository(db_session):
    repo = FarmRepository(db_session)
    farm = await repo.create(
        id="farm-repo-01",
        owner_id="usr-repo-01",
        name="Saurashtra High-Tech Drip Farm",
        location="Junagadh, Gujarat",
        latitude=21.5222,
        longitude=70.4579,
        area=25.0,
    )
    assert farm.name == "Saurashtra High-Tech Drip Farm"

    farms = await repo.list_by_owner("usr-repo-01")
    assert len(farms) == 1
    assert farms[0].id == "farm-repo-01"


@pytest.mark.asyncio
async def test_sensor_repository_telemetry(db_session):
    repo = SensorRepository(db_session)
    sensor = await repo.create(
        id="sns-repo-01",
        field_id="field-repo-01",
        device_id="NODE-TEST-99",
        sensor_type=SensorType.SOIL_MOISTURE,
    )

    # Ingest multiple telemetry points
    reading1 = await repo.add_reading(sensor_id="sns-repo-01", value=32.0, unit="%")
    reading2 = await repo.add_reading(sensor_id="sns-repo-01", value=31.5, unit="%")

    assert reading1.id is not None
    assert reading2.id is not None

    recent = await repo.get_recent_readings(sensor_id="sns-repo-01", limit=10)
    assert len(recent) == 2
    # Newest reading first
    assert recent[0].value == 31.5


@pytest.mark.asyncio
async def test_task_repository_lifecycle(db_session):
    repo = TaskRepository(db_session)
    task = await repo.create(
        id="tsk-repo-01",
        title="Check Drip Lateral Filters",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
    )
    assert task.status == TaskStatus.PENDING

    # Transition to IN_PROGRESS
    updated = await repo.update_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.started_at is not None

    # Transition to COMPLETED
    completed = await repo.update_status(task.id, TaskStatus.COMPLETED)
    assert completed.status == TaskStatus.COMPLETED
    assert completed.completed_at is not None


@pytest.mark.asyncio
async def test_activity_log_repository(db_session):
    repo = ActivityLogRepository(db_session)
    log = await repo.log_activity(
        user_id="usr-repo-01",
        farm_id="farm-repo-01",
        event_type="DISPATCH_TASK",
        description="Task tsk-repo-01 dispatched to field worker.",
        entity_type="Task",
        entity_id="tsk-repo-01",
    )
    assert log.id is not None

    recent_logs = await repo.list_recent(limit=5)
    assert len(recent_logs) >= 1
    assert recent_logs[0].event_type == "DISPATCH_TASK"
