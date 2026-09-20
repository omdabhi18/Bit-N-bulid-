from pydantic import BaseModel
from typing import List, Optional

class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    status: str
    confidence: int
    lastRun: str
    currentTask: str
    inputs: List[str]
    outputs: List[str]
    icon: str

class OrchestrateCycleRequest(BaseModel):
    farmId: Optional[str] = None
    forceRun: bool = False

class OrchestrateCycleResponse(BaseModel):
    success: bool
    cycleId: str
    executionTimeMs: int
    agentsRan: List[str]
    detectedRisksCount: int
    generatedPlansCount: int
    summary: str
