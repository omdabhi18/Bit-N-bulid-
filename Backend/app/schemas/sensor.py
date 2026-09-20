from pydantic import BaseModel
from typing import List, Optional

class TelemetryCurrent(BaseModel):
    farmHealthScore: int
    soilMoisture: float
    soilMoistureStatus: str
    soilTemperature: float
    soilPH: float
    soilEC: float
    nitrogenLevel: float
    phosphorusLevel: float
    potassiumLevel: float
    airTemperature: float
    airHumidity: float
    rainfallProb24h: int
    windSpeed: float
    solarRadiation: float
    dripValveA: str
    dripValveB: str
    dripValveC: str

class TimeSeriesPoint(BaseModel):
    time: str
    moisture: float
    temp: float
    humidity: float
    ec: float

class NPKRadarPoint(BaseModel):
    nutrient: str
    actual: float
    optimal: float
    fullMark: float = 100.0

class HardwareSensorResponse(BaseModel):
    id: str
    name: str
    field: str
    battery: int
    signal: str
    status: str
    lastSync: str
    type: str

class MonitoringResponse(BaseModel):
    telemetry: TelemetryCurrent
    timeSeries: List[TimeSeriesPoint]
    npkRadar: List[NPKRadarPoint]
    sensors: List[HardwareSensorResponse]

class ValveTriggerRequest(BaseModel):
    fieldId: str
    minutes: int = 35

class ValveTriggerResponse(BaseModel):
    success: bool
    fieldId: str
    minutes: int
    status: str
    message: str
