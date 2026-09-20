from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List
from datetime import datetime
from app.models.sensor import SensorNode
from app.models.audit import ActivityLog
from app.integrations.mock_iot import mock_iot_service
from app.agents.execution_agent import execution_agent
from app.schemas.sensor import (
    TelemetryCurrent,
    MonitoringResponse,
    TimeSeriesPoint,
    NPKRadarPoint,
    HardwareSensorResponse,
    ValveTriggerResponse
)

class SensorService:
    async def get_monitoring_data(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> MonitoringResponse:
        telemetry = mock_iot_service.get_current_telemetry()

        # 24h Time Series
        time_series = [
            TimeSeriesPoint(time="00:00", moisture=38.0, temp=23.0, humidity=75.0, ec=0.40),
            TimeSeriesPoint(time="03:00", moisture=37.0, temp=22.0, humidity=79.0, ec=0.40),
            TimeSeriesPoint(time="06:00", moisture=36.0, temp=24.0, humidity=82.0, ec=0.41),
            TimeSeriesPoint(time="09:00", moisture=34.0, temp=28.0, humidity=68.0, ec=0.41),
            TimeSeriesPoint(time="12:00", moisture=33.0, temp=32.0, humidity=55.0, ec=0.42),
            TimeSeriesPoint(time="15:00", moisture=31.0, temp=34.0, humidity=50.0, ec=0.42),
            TimeSeriesPoint(time="18:00", moisture=telemetry.get("soilMoisture", 31.4), temp=30.0, humidity=58.0, ec=0.42),
            TimeSeriesPoint(time="21:00", moisture=30.0, temp=26.0, humidity=65.0, ec=0.41)
        ]

        # NPK Radar data
        npk_radar = [
            NPKRadarPoint(nutrient="Nitrogen (N)", actual=telemetry.get("nitrogenLevel", 82.0), optimal=75.0, fullMark=100.0),
            NPKRadarPoint(nutrient="Phosphorus (P)", actual=telemetry.get("phosphorusLevel", 14.0), optimal=70.0, fullMark=100.0),
            NPKRadarPoint(nutrient="Potassium (K)", actual=telemetry.get("potassiumLevel", 185.0), optimal=80.0, fullMark=100.0),
            NPKRadarPoint(nutrient="Organic Carbon", actual=65.0, optimal=70.0, fullMark=100.0),
            NPKRadarPoint(nutrient="Zinc (Zn)", actual=70.0, optimal=65.0, fullMark=100.0),
            NPKRadarPoint(nutrient="Boron (B)", actual=60.0, optimal=60.0, fullMark=100.0)
        ]

        # Fetch Hardware Sensors
        res = await db.execute(select(SensorNode).filter(SensorNode.farm_id == farm_id))
        nodes = res.scalars().all()
        hardware_list = [
            HardwareSensorResponse(
                id=n.id,
                name=n.name,
                field=n.field_name,
                battery=n.battery,
                signal=n.signal_strength,
                status=n.status,
                lastSync=n.last_sync,
                type=n.sensor_type
            ) for n in nodes
        ]

        return MonitoringResponse(
            telemetry=TelemetryCurrent(**telemetry),
            timeSeries=time_series,
            npkRadar=npk_radar,
            sensors=hardware_list
        )

    async def trigger_valve(self, db: AsyncSession, farm_id: str, field_id: str, minutes: int = 35) -> ValveTriggerResponse:
        # Actuate via Execution Agent & Mock IoT
        res = await execution_agent.trigger_valve(farm_id, field_id, minutes)

        # Log Activity
        log = ActivityLog(
            farm_id=farm_id,
            time=datetime.now().strftime("%I:%M %p"),
            agent="Execution Agent",
            event=f"⚡ Solenoid Valve opened for {field_id.upper()} ({minutes} min run scheduled)",
            severity="success"
        )
        db.add(log)
        await db.commit()

        return ValveTriggerResponse(
            success=True,
            fieldId=field_id,
            minutes=minutes,
            status="Running",
            message=f"Drip Irrigation Valve activated for {field_id.upper()}! 💧 Running for {minutes} mins."
        )

sensor_service = SensorService()
