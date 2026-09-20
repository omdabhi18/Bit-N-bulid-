from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.sensor_service import sensor_service
from app.schemas.sensor import ValveTriggerRequest, ValveTriggerResponse
from app.integrations.mock_iot import mock_iot_service

router = APIRouter(prefix="/sensors", tags=["Sensors & IoT"])

from app.services.iot_service import iot_service
from app.integrations.mqtt_client import SensorTelemetryPayload

@router.post("/telemetry")
async def ingest_telemetry(
    payload: SensorTelemetryPayload,
    farmId: str = "farm-greenvalley-01",
    fieldId: str = "field-cotton-01",
    sensorId: str = "SN-Cotton-01",
    db: AsyncSession = Depends(get_db)
):
    """Ingest, validate, and broadcast real-time IoT sensor telemetry."""
    return await iot_service.process_sensor_payload(
        farm_id=farmId,
        field_id=fieldId,
        sensor_id=sensorId,
        payload_data=payload.model_dump(),
        db=db
    )

@router.post("/valve/trigger", response_model=ValveTriggerResponse)
async def trigger_valve(req: ValveTriggerRequest, db: AsyncSession = Depends(get_db)):
    return await sensor_service.trigger_valve(db, "farm-greenvalley-01", req.fieldId, req.minutes)

@router.post("/valve/stop")
async def stop_valve(req: ValveTriggerRequest):
    mock_iot_service.stop_valve("farm-greenvalley-01", req.fieldId)
    return {"success": True, "message": f"Irrigation stopped for {req.fieldId}"}
