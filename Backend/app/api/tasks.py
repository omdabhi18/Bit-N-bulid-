from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.task_service import task_service
from app.schemas.task import TaskResponse, TaskCreate, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["Task Execution"])

@router.get("", response_model=List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await task_service.get_tasks(db)

@router.post("", response_model=TaskResponse)
async def create_task(data: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await task_service.create_task(db, "farm-greenvalley-01", data)

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: str, status_data: TaskStatusUpdate, db: AsyncSession = Depends(get_db)):
    updated = await task_service.update_status(db, task_id, status_data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
