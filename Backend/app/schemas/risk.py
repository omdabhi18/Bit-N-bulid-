from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RiskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    category: str
    icon: str
    severity: str
    field: str
    probability: int
    indicators: List[str]
    recommendedAction: str
    planGenerated: bool
    planId: Optional[str] = None

class GeneratePlanFromRiskRequest(BaseModel):
    riskId: str
