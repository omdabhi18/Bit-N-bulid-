from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    title: str
    field: str
    priority: str = "High"
    dueTime: str = "Today 18:00"
    assignedTo: str = "Kishanbhai Patel"
    icon: str = "CheckCircle"
    notes: Optional[str] = ""

class TaskCreate(TaskBase):
    planId: Optional[str] = None

class TaskStatusUpdate(BaseModel):
    status: str # todo | in-progress | completed

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    planId: Optional[str] = None
    status: str
