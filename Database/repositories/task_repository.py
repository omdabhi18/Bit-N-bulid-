from typing import List, Optional, Any

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.task import Task
from Database.models.activity_log import ActivityLog
from Database.repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_tasks_for_farm(self, farm_id: str) -> List[Task]:
        res = await self.session.execute(
            select(Task)
            .filter(Task.farm_id == farm_id)
            .order_by(Task.created_at.desc())
        )
        return list(res.scalars().all())

    async def update_status(self, task_id: str, new_status: Any) -> Optional[Task]:
        task = await self.get_by_id(task_id)
        if not task:
            return None

        status_str = new_status.value if hasattr(new_status, "value") else str(new_status)
        task.status = status_str

        if status_str.upper() in ("IN_PROGRESS", "RUNNING", "EXECUTING"):
            if not task.started_at:
                task.started_at = datetime.now(timezone.utc)
        elif status_str.upper() == "COMPLETED":
            if not task.started_at:
                task.started_at = datetime.now(timezone.utc)
            task.completed_at = datetime.now(timezone.utc)
            # Log completion activity
            log = ActivityLog(
                farm_id=task.farm_id,
                field_id=task.field_id,
                agent="Task Execution Engine",
                event=f"Task #{task.id} (\"{task.title}\") marked COMPLETED",
                event_type="TASK_COMPLETED",
                severity="success"
            )
            self.session.add(log)

        await self.session.commit()
        await self.session.refresh(task)
        return task

