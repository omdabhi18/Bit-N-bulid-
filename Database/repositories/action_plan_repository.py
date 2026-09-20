import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.models.action_plan import ActionPlan
from Database.models.task import Task
from Database.models.activity_log import ActivityLog
from Database.repositories.base_repository import BaseRepository

class ActionPlanRepository(BaseRepository[ActionPlan]):
    def __init__(self, session: AsyncSession):
        super().__init__(ActionPlan, session)

    async def get_plans_for_farm(self, farm_id: str) -> List[ActionPlan]:
        res = await self.session.execute(
            select(ActionPlan)
            .filter(ActionPlan.farm_id == farm_id)
            .order_by(ActionPlan.created_at.desc())
        )
        return list(res.scalars().all())

    async def approve_and_dispatch_task(
        self,
        action_plan_id: Optional[str] = None,
        plan_id: Optional[str] = None,
        user_name: str = "Kishanbhai Patel",
        user_id: Optional[str] = None,
    ):
        """
        Executes atomic database transaction:
        1. Updates ActionPlan status to APPROVED / SCHEDULED
        2. Automatically creates and dispatches corresponding Kanban Task
        3. Appends ActivityLog entry
        Rolls back atomically if any step fails.
        """
        target_id = action_plan_id or plan_id
        if not target_id:
            raise ValueError("action_plan_id must be provided")
        plan = await self.get_by_id(target_id)
        if not plan:
            raise ValueError(f"Action plan '{target_id}' not found")

        # 1. Update plan status
        plan.status = "APPROVED"

        # 2. Create Task
        new_task = Task(
            id=f"TSK-{uuid.uuid4().hex[:6].upper()}",
            farm_id=plan.farm_id,
            field_id=plan.field_id,
            action_plan_id=plan.id,

            title=plan.action or plan.action_type,
            description=f"Auto-dispatched from approved plan #{plan.id}",
            assigned_to=plan.assigned_to or user_name,
            status="PENDING",
            priority=plan.priority or "High",
            due_at=plan.scheduled_time,
            due_time=plan.scheduled_time,
            icon="Droplets" if ("Irrigation" in (plan.action_type or "") or "Irrigation" in (plan.action or "")) else "Bug"
        )
        self.session.add(new_task)

        # 3. Create Activity Log
        log = ActivityLog(
            user_id=user_id,
            farm_id=plan.farm_id,
            field_id=plan.field_id,
            agent="Farmer Interaction",
            event=f"Farmer approved Action Plan #{plan.id} ({plan.title})",
            event_type="PLAN_APPROVAL",
            severity="success"
        )
        self.session.add(log)

        # Atomic commit
        await self.session.commit()
        await self.session.refresh(plan)
        await self.session.refresh(new_task)
        return (plan, new_task)

