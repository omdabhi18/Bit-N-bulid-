from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ExplainabilityFactor(BaseModel):
    name: str
    value: str
    impact: str
    threshold: str

class AdvisoryExplainability(BaseModel):
    factors: List[ExplainabilityFactor]
    whyText: str

class AdvisoryActionDetails(BaseModel):
    action: str
    volume: str
    duration: str
    zone: str
    costEstimate: str
    waterSource: str

class AdvisoryResponse(BaseModel):
    id: str
    title: str
    titleGu: Optional[str] = None
    titleHi: Optional[str] = None
    field: str
    priority: str
    confidenceScore: int
    status: str
    timestamp: str
    orchestratorSummary: str
    explainability: AdvisoryExplainability
    actionDetails: AdvisoryActionDetails

class AdvisoryActionRequest(BaseModel):
    reason: Optional[str] = None
