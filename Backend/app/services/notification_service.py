from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.models.audit import ActivityLog, AlertNotification
from app.models.farm import Farm
from app.schemas.notification import ActivityLogResponse, AlertNotificationResponse, AuditCertificateResponse

class NotificationService:
    async def get_activity_logs(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[ActivityLogResponse]:
        res = await db.execute(select(ActivityLog).filter(ActivityLog.farm_id == farm_id).order_by(ActivityLog.created_at.desc()))
        logs = res.scalars().all()
        return [ActivityLogResponse.model_validate(l) for l in logs]

    async def get_audit_certificate(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> AuditCertificateResponse:
        res_farm = await db.execute(select(Farm).filter(Farm.id == farm_id))
        farm = res_farm.scalars().first()

        logs = await self.get_activity_logs(db, farm_id)

        return AuditCertificateResponse(
            farmName=farm.name if farm else "GreenValley Smart Farms",
            farmerName=farm.farmer_name if farm else "Kishanbhai Patel",
            healthScore=82,
            village=farm.village if farm else "Ribda",
            district=farm.district if farm else "Rajkot",
            generatedAt=datetime.now().strftime("%d-%m-%Y %H:%M:%S IST"),
            verifiedAgentsCount=8,
            totalDecisionsLogged=len(logs),
            recentAuditLogs=logs[:10]
        )

notification_service = NotificationService()
