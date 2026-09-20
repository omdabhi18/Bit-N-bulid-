from pydantic import BaseModel
from typing import Optional, Dict

class PlanConstraints(BaseModel):
    costBudget: str
    weatherWindow: str
    waterAvailability: str
    safetyProtocols: str

class ActionPlanResponse(BaseModel):
    id: str
    title: str
    targetField: str
    actionType: str
    scheduledTime: str
    status: str
    priority: str
    estimatedCost: float
    waterVolume: str
    constraints: PlanConstraints
    hardwareTarget: str
    assignedTo: str

class ActionPlanCreate(BaseModel):
    title: str
    targetField: str
    actionType: str
    scheduledTime: str
    priority: str = "High"
    estimatedCost: float = 50.0
    waterVolume: str = "2,000 L"
    hardwareTarget: Optional[str] = None
    assignedTo: Optional[str] = None
