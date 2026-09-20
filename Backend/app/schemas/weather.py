from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class WeatherCurrent(BaseModel):
    temp: float
    condition: str
    humidity: float
    wind: str
    rainfallProb: int
    uvIndex: int
    dewPoint: float
    et0: str
    advisory: str

class HourlyForecastItem(BaseModel):
    time: str
    temp: float
    rainProb: int
    humidity: float

class DailyForecastItem(BaseModel):
    day: str
    tempMax: float
    tempMin: float
    rainProb: int
    condition: str
    sprayRating: str

class WeatherForecastResponse(BaseModel):
    current: WeatherCurrent
    hourly: List[HourlyForecastItem]
    daily: List[DailyForecastItem]

class WeatherWindowResponse(BaseModel):
    shouldIrrigateNow: bool
    confidence: int
    recommendation: str
    recommendationGu: Optional[str] = None
    factors: dict
    bestWindow: str
    windSpeed: str
    rainProbability: int
    currentTemperature: float
