from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.notification_service import notification_service
from app.schemas.notification import ActivityLogResponse

router = APIRouter(prefix="/notifications", tags=["Notifications & Audit Logs"])

@router.get("/activity-logs", response_model=List[ActivityLogResponse])
async def get_activity_logs(db: AsyncSession = Depends(get_db)):
    return await notification_service.get_activity_logs(db)
