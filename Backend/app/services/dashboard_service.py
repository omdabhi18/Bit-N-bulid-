from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any
from app.models.farm import Farm, Field
from app.models.risk import Risk
from app.models.advisory import AIAdvisory
from app.models.task import FarmTask
from app.integrations.mock_iot import mock_iot_service
from app.schemas.dashboard import DashboardResponse
from app.schemas.farm import FieldDetail, Coordinate
from app.schemas.advisory import AdvisoryResponse
from app.schemas.task import TaskResponse

class DashboardService:
    async def get_dashboard(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> DashboardResponse:
        # 1. Fetch Farm Fields
        field_res = await db.execute(select(Field).filter(Field.farm_id == farm_id))
        fields = field_res.scalars().all()
        field_details = [
            FieldDetail(
                id=f.id,
                name=f.name,
                crop=f.crop,
                area=f.area,
                stage=f.stage,
                healthScore=f.health_score,
                soilMoisture=f.soil_moisture,
                status=f.status,
                riskCategory=f.risk_category,
                pestRisk=f.pest_risk,
                soilPH=f.soil_ph,
                nitrogen=f.nitrogen,
                phosphorus=f.phosphorus,
                potassium=f.potassium,
                sensorNode=f.sensor_node,
                sensorStatus=f.sensor_status,
                coordinates=[Coordinate(**c) for c in (f.coordinates or [])],
                color=f.color,
                dripStatus=f.drip_status,
                recommendation=f.recommendation
            ) for f in fields
        ]

        # 2. Fetch Primary Advisory
        adv_res = await db.execute(select(AIAdvisory).filter(AIAdvisory.farm_id == farm_id).order_by(AIAdvisory.created_at.desc()))
        advisories = adv_res.scalars().all()
        primary_adv = None
        if advisories:
            a = advisories[0]
            primary_adv = AdvisoryResponse(
                id=a.id,
                title=a.title,
                titleGu=a.title_gu,
                titleHi=a.title_hi,
                field=a.field,
                priority=a.priority,
                confidenceScore=a.confidence_score,
                status=a.status,
                timestamp=a.timestamp,
                orchestratorSummary=a.orchestrator_summary,
                explainability=a.explainability or {},
                actionDetails=a.action_details or {}
            )

        # 3. Fetch Pending Tasks
        task_res = await db.execute(select(FarmTask).filter(FarmTask.farm_id == farm_id, FarmTask.status == "todo").limit(4))
        tasks = task_res.scalars().all()
        pending_tasks = [TaskResponse.model_validate(t) for t in tasks]

        # 4. Fetch Live Telemetry from Mock IoT
        telemetry = mock_iot_service.get_current_telemetry()
        valves = mock_iot_service.get_valve_status()

        # 5. Count Risks
        risk_res = await db.execute(select(Risk).filter(Risk.farm_id == farm_id))
        risks = risk_res.scalars().all()

        return DashboardResponse(
            farmHealthScore=telemetry.get("farmHealthScore", 82),
            soilMoisture=telemetry.get("soilMoisture", 31.4),
            soilMoistureStatus=telemetry.get("soilMoistureStatus", "Deficit (પાણીની જરૂર)"),
            soilTemperature=telemetry.get("soilTemperature", 27.8),
            airTemperature=telemetry.get("airTemperature", 33.2),
            airHumidity=telemetry.get("airHumidity", 58.0),
            rainfallProb24h=telemetry.get("rainfallProb24h", 12),
            windSpeed=telemetry.get("windSpeed", 14.0),
            overallRisk="High" if any(r.severity in ["High", "Critical"] for r in risks) else "Normal",
            activeRisksCount=len(risks),
            primaryAdvisory=primary_adv,
            fields=field_details,
            pendingTasks=pending_tasks,
            activeValve=valves
        )

dashboard_service = DashboardService()
