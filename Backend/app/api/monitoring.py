from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.sensor_service import sensor_service
from app.schemas.sensor import MonitoringResponse

router = APIRouter(prefix="/monitoring", tags=["Live Monitoring"])

@router.get("/telemetry", response_model=MonitoringResponse)
async def get_monitoring_telemetry(db: AsyncSession = Depends(get_db)):
    return await sensor_service.get_monitoring_data(db)
