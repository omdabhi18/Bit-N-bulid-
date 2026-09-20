from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.action_plan_service import action_plan_service
from app.schemas.action_plan import ActionPlanResponse

router = APIRouter(prefix="/action-plans", tags=["Action Plans"])

@router.get("", response_model=List[ActionPlanResponse])
async def get_action_plans(db: AsyncSession = Depends(get_db)):
    return await action_plan_service.get_action_plans(db)

@router.post("/{plan_id}/approve")
async def approve_plan(plan_id: str, db: AsyncSession = Depends(get_db)):
    success = await action_plan_service.approve_plan(db, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Action Plan not found")
    return {"success": True, "message": f"Plan {plan_id} approved and dispatched to Task board"}
