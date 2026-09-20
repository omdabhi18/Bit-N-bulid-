from pydantic import BaseModel
from typing import List, Optional, Dict
from app.schemas.farm import FieldDetail
from app.schemas.advisory import AdvisoryResponse
from app.schemas.task import TaskResponse

class DashboardResponse(BaseModel):
    farmHealthScore: int
    soilMoisture: float
    soilMoistureStatus: str
    soilTemperature: float
    airTemperature: float
    airHumidity: float
    rainfallProb24h: int
    windSpeed: float
    overallRisk: str
    activeRisksCount: int
    primaryAdvisory: Optional[AdvisoryResponse] = None
    fields: List[FieldDetail]
    pendingTasks: List[TaskResponse]
    activeValve: Dict[str, bool]
