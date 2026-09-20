from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# 1. User DTOs
class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: str = "FARMER"

# 2. Field Coordinate DTO
class CoordinateDTO(BaseModel):
    lat: float
    lng: float

# 3. Field DTO
class FieldDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    farm_id: str
    name: str
    area: str
    crop_name: str
    stage: str
    health_score: int
    soil_moisture: float
    status: str
    risk_category: str
    pest_risk: str
    soil_ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    boundary: List[Dict[str, float]]
    color: str
    drip_status: str
    recommendation: str

# 4. Farm DTO
class FarmDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    owner_id: str
    name: str
    farmer_name: str
    village: str
    taluka: str
    district: str
    state: str
    latitude: float
    longitude: float
    area: float
    soil_type: str
    irrigation_method: str

# 5. Crop DTO
class CropDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    farm_id: str
    field_id: Optional[str] = None
    crop_name: str
    variety: str
    sowing_date: str
    expected_harvest_date: str
    current_stage: str
    health_status: str
    area: float

# 6. Sensor Reading DTO & Pagination Filter
class SensorReadingDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    sensor_id: str
    field_id: Optional[str] = None
    timestamp: datetime
    soil_moisture: float
    soil_temperature: float
    soil_ph: float
    soil_ec: float
    nitrogen: float
    phosphorus: float
    potassium: float
    air_temperature: float
    air_humidity: float

class ReadingFilterDTO(BaseModel):
    sensor_id: Optional[str] = None
    field_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 50
    offset: int = 0

# 7. Risk DTO
class RiskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    farm_id: str
    field_id: Optional[str] = None
    category: str
    risk_type: str
    severity: str
    confidence: int
    evidence: List[str]
    explanation: str
    recommended_action: str
    status: str
    plan_generated: bool
    plan_id: Optional[str] = None

# 8. Action Plan DTO
class ActionPlanDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    farm_id: str
    field_id: Optional[str] = None
    title: str
    target_field: str
    action: str
    action_type: str
    scheduled_time: str
    duration: str
    estimated_cost: float
    water_volume: str
    constraints: Dict[str, Any]
    hardware_target: str
    assigned_to: str
    priority: str
    confidence: int
    status: str

# 9. Task DTO
class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    farm_id: str
    field_id: Optional[str] = None
    action_plan_id: Optional[str] = None
    title: str
    description: str
    assigned_to: str
    priority: str
    status: str
    due_time: str
    icon: str
    notes: str

# 10. Activity Log DTO
class ActivityLogDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: Optional[str] = None
    farm_id: Optional[str] = None
    field_id: Optional[str] = None
    agent: str
    event: str
    event_type: str
    time: str
    severity: str
    created_at: datetime
