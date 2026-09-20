from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
import random
from app.models.action_plan import ActionPlan
from app.models.task import FarmTask
from app.models.audit import ActivityLog
from app.schemas.action_plan import ActionPlanResponse, ActionPlanCreate, PlanConstraints

class ActionPlanService:
    async def get_action_plans(self, db: AsyncSession, farm_id: str = "farm-greenvalley-01") -> List[ActionPlanResponse]:
        res = await db.execute(select(ActionPlan).filter(ActionPlan.farm_id == farm_id).order_by(ActionPlan.created_at.desc()))
        plans = res.scalars().all()
        return [
            ActionPlanResponse(
                id=p.id,
                title=p.title,
                targetField=p.target_field,
                actionType=p.action_type,
                scheduledTime=p.scheduled_time,
                status=p.status,
                priority=p.priority,
                estimatedCost=p.estimated_cost,
                waterVolume=p.water_volume,
                constraints=PlanConstraints(**(p.constraints or {
                    "costBudget": "₹150 Max",
                    "weatherWindow": "Safe",
                    "waterAvailability": "Adequate",
                    "safetyProtocols": "Standard"
                })),
                hardwareTarget=p.hardware_target,
                assignedTo=p.assigned_to
            ) for p in plans
        ]

    async def approve_plan(self, db: AsyncSession, plan_id: str) -> bool:
        res = await db.execute(select(ActionPlan).filter(ActionPlan.id == plan_id))
        plan = res.scalars().first()
        if not plan:
            return False

        plan.status = "Approved"

        # Auto-create task on Kanban board
        new_task = FarmTask(
            id=f"TSK-{random.randint(50, 99)}",
            farm_id=plan.farm_id,
            plan_id=plan.id,
            title=plan.action_type,
            field=plan.target_field.split("(")[0].strip(),
            status="todo",
            priority=plan.priority,
            due_time=plan.scheduled_time,
            assigned_to=plan.assigned_to,
            icon="Droplets" if "Irrigation" in plan.action_type else "Bug" if "Spray" in plan.action_type else "CheckCircle",
            notes=f"Auto-dispatched from approved plan {plan.id}"
        )
        db.add(new_task)

        # Log event
        log = ActivityLog(
            farm_id=plan.farm_id,
            time=datetime.now().strftime("%I:%M %p"),
            agent="Farmer Interaction",
            event=f"Farmer approved Action Plan #{plan.id} ({plan.title})",
            severity="success"
        )
        db.add(log)
        await db.commit()
        return True

action_plan_service = ActionPlanService()
