from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.activity_log import ActivityLog
from Database.repositories.base_repository import BaseRepository

class ActivityLogRepository(BaseRepository[ActivityLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(ActivityLog, session)

    async def get_logs_for_farm(self, farm_id: str, limit: int = 50) -> List[ActivityLog]:
        res = await self.session.execute(
            select(ActivityLog)
            .filter(ActivityLog.farm_id == farm_id)
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
        )
        return list(res.scalars().all())

    async def log_activity(
        self,
        event_type: str = "SYSTEM_EVENT",
        description: str = "",
        user_id: Optional[str] = None,
        farm_id: Optional[str] = "farm-greenvalley-01",
        field_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        severity: str = "info",
        agent: str = "System",
    ) -> ActivityLog:
        log = ActivityLog(
            user_id=user_id,
            farm_id=farm_id,
            field_id=field_id,
            agent=agent,
            event=description or event_type,
            description=description,
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=metadata or {},
            severity=severity,
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def list_recent(self, limit: int = 20) -> List[ActivityLog]:
        res = await self.session.execute(
            select(ActivityLog)
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
        )
        return list(res.scalars().all())

    async def log_event(
        self,
        agent: str,
        event: str,
        farm_id: Optional[str] = "farm-greenvalley-01",
        field_id: Optional[str] = None,
        severity: str = "info",
        event_type: str = "SYSTEM_EVENT"
    ) -> ActivityLog:
        log = ActivityLog(
            agent=agent,
            event=event,
            farm_id=farm_id,
            field_id=field_id,
            severity=severity,
            event_type=event_type
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

