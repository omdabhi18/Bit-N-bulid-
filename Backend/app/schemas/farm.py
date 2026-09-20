from pydantic import BaseModel, Field as PField
from typing import List, Optional, Any

class Coordinate(BaseModel):
    lat: float
    lng: float

class CropItem(BaseModel):
    id: str
    name: str
    name_gujarati: Optional[str] = None
    category: Optional[str] = "Cash Crop"
    scientific_name: Optional[str] = None
    disease_ai_supported: bool = False
    is_active: bool = True
    variety: Optional[str] = "Standard Variety"
    stage: Optional[str] = "Vegetative"
    area: Optional[float] = 5.0
    field: Optional[str] = None
    sowingDate: Optional[str] = None

class CropCatalogResponse(BaseModel):
    success: bool = True
    crops: List[CropItem]


class FieldDetail(BaseModel):
    id: str
    name: str
    crop: str
    area: str
    stage: str
    healthScore: int
    soilMoisture: float
    status: str
    riskCategory: str
    pestRisk: str
    soilPH: float
    nitrogen: str
    phosphorus: str
    potassium: str
    sensorNode: str
    sensorStatus: str
    coordinates: List[Coordinate]
    color: str
    dripStatus: str
    recommendation: str

class FarmProfile(BaseModel):
    farmerName: str
    farmName: str
    village: str
    taluka: str
    district: str
    state: str
    totalAreaAcre: float
    soilType: str
    irrigationMethod: str
    coordinates: Coordinate
    crops: List[CropItem]

class FarmUpdate(BaseModel):
    farmerName: Optional[str] = None
    farmName: Optional[str] = None
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    totalAreaAcre: Optional[float] = None
    soilType: Optional[str] = None
    irrigationMethod: Optional[str] = None
