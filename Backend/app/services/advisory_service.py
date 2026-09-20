from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
from app.models.advisory import AIAdvisory
from app.models.audit import ActivityLog
from app.schemas.advisory import AdvisoryResponse

class AdvisoryService:
    async def get_advisories(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[AdvisoryResponse]:
        res = await db.execute(select(AIAdvisory).filter(AIAdvisory.farm_id == farm_id).order_by(AIAdvisory.created_at.desc()))
        advisories = res.scalars().all()
        return [
            AdvisoryResponse(
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
            ) for a in advisories
        ]

    async def approve_advisory(self, db: AsyncSession, advisory_id: str) -> bool:
        res = await db.execute(select(AIAdvisory).filter(AIAdvisory.id == advisory_id))
        adv = res.scalars().first()
        if not adv:
            return False

        adv.status = "Approved"

        log = ActivityLog(
            farm_id=adv.farm_id,
            time=datetime.now().strftime("%I:%M %p"),
            agent="Farmer Interaction",
            event=f"Farmer approved recommendation: \"{adv.title}\"",
            severity="success"
        )
        db.add(log)
        await db.commit()
        return True

    async def reject_advisory(self, db: AsyncSession, advisory_id: str, reason: str = "Farmer decided to delay") -> bool:
        res = await db.execute(select(AIAdvisory).filter(AIAdvisory.id == advisory_id))
        adv = res.scalars().first()
        if not adv:
            return False

        adv.status = "Rejected"

        log = ActivityLog(
            farm_id=adv.farm_id,
            time=datetime.now().strftime("%I:%M %p"),
            agent="Farmer Interaction",
            event=f"Farmer dismissed advisory #{advisory_id}: Reason - {reason}",
            severity="warning"
        )
        db.add(log)
        await db.commit()
        return True

advisory_service = AdvisoryService()
