from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
import random
from app.models.task import FarmTask
from app.models.audit import ActivityLog
from app.schemas.task import TaskResponse, TaskCreate

class TaskService:
    async def get_tasks(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[TaskResponse]:
        res = await db.execute(select(FarmTask).filter(FarmTask.farm_id == farm_id).order_by(FarmTask.created_at.desc()))
        tasks = res.scalars().all()
        return [TaskResponse.model_validate(t) for t in tasks]

    async def update_status(self, db: AsyncSession, task_id: str, new_status: str) -> Optional[TaskResponse]:
        res = await db.execute(select(FarmTask).filter(FarmTask.id == task_id))
        task = res.scalars().first()
        if not task:
            return None

        old_status = task.status
        task.status = new_status

        # If completed, log activity
        if new_status == "completed":
            log = ActivityLog(
                farm_id=task.farm_id,
                time=datetime.now().strftime("%I:%M %p"),
                agent="Task Execution Engine",
                event=f"Task #{task.id} (\"{task.title}\") marked COMPLETED",
                severity="success"
            )
            db.add(log)

        await db.commit()
        await db.refresh(task)
        return TaskResponse.model_validate(task)

    async def create_task(self, db: AsyncSession, farm_id: str, data: TaskCreate) -> TaskResponse:
        task = FarmTask(
            id=f"TSK-{random.randint(10, 99)}",
            farm_id=farm_id,
            plan_id=data.planId,
            title=data.title,
            field=data.field,
            status="todo",
            priority=data.priority,
            due_time=data.dueTime,
            assigned_to=data.assignedTo,
            icon=data.icon,
            notes=data.notes or ""
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return TaskResponse.model_validate(task)

task_service = TaskService()
