from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
import random
from app.models.risk import Risk
from app.models.action_plan import ActionPlan
from app.models.audit import ActivityLog
from app.schemas.risk import RiskResponse

class RiskService:
    async def get_risks(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[RiskResponse]:
        res = await db.execute(select(Risk).filter(Risk.farm_id == farm_id))
        risks = res.scalars().all()
        return [
            RiskResponse(
                id=r.id,
                category=r.category,
                icon=r.icon,
                severity=r.severity,
                field=r.field,
                probability=r.probability,
                indicators=r.indicators or [],
                recommendedAction=r.recommended_action,
                planGenerated=r.plan_generated,
                planId=r.plan_id
            ) for r in risks
        ]

    async def generate_plan_from_risk(self, db: AsyncSession, farm_id: str, risk_id: str) -> Optional[str]:
        res = await db.execute(select(Risk).filter(Risk.id == risk_id))
        risk = res.scalars().first()
        if not risk:
            return None

        new_plan_id = f"PLAN-{random.randint(1000, 9999)}"
        new_plan = ActionPlan(
            id=new_plan_id,
            farm_id=farm_id,
            title=f"{risk.category.split('(')[0].strip()} Mitigation Plan",
            target_field=risk.field,
            action_type=risk.recommended_action,
            scheduled_time="Today • 18:00 IST",
            status="Draft",
            priority=risk.severity,
            estimated_cost=150.0,
            water_volume="1,500 L",
            constraints={
                "costBudget": "Max ₹250",
                "weatherWindow": "Safe Window (Wind < 15 km/h)",
                "waterAvailability": "Adequate Level (88%)",
                "safetyProtocols": "Standard field PPE"
            },
            hardware_target="Zone Drip & Sprayer Node",
            assigned_to="Kishanbhai Patel"
        )
        db.add(new_plan)

        risk.plan_generated = True
        risk.plan_id = new_plan_id

        # Log event
        log = ActivityLog(
            farm_id=farm_id,
            time=datetime.now().strftime("%I:%M %p"),
            agent="Constrained Action Planner",
            event=f"Action Plan #{new_plan_id} generated for {risk.category}",
            severity="info"
        )
        db.add(log)
        await db.commit()

        return new_plan_id

risk_service = RiskService()
